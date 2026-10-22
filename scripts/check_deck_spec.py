#!/usr/bin/env python3
"""Validate a deck-spec JSON's structure and references, not its factual truth.

Python 3.9+, standard library only. No network or filesystem writes.
Exit 0: checks passed; exit 1: invalid spec; exit 2: unreadable input/JSON.
"""
import argparse
import json
import math
from pathlib import Path


def validate(spec):
    errors = []
    warnings = []

    def fail(message):
        errors.append(message)

    def require_text(obj, fields, path):
        for field in fields:
            if not isinstance(obj.get(field), str) or not obj[field].strip():
                fail(f"{path}.{field}: expected nonempty text")

    def rows(obj, field, path, nonempty=False):
        value = obj.get(field)
        if not isinstance(value, list):
            fail(f"{path}.{field}: expected list")
            return []
        if nonempty and not value:
            fail(f"{path}.{field}: expected at least one item")
        return value

    def index(items, path):
        result = {}
        for i, item in enumerate(items):
            p = f"{path}[{i}]"
            if not isinstance(item, dict):
                fail(f"{p}: expected object")
                continue
            ident = item.get("id")
            if not isinstance(ident, str) or not ident.strip():
                fail(f"{p}.id: expected nonempty text")
            elif ident in result:
                fail(f"{p}.id: duplicate {ident}")
            else:
                result[ident] = item
        return result

    def refs(obj, field, known, path, required=False):
        values = rows(obj, field, path, required)
        for ident in values:
            if not isinstance(ident, str) or ident not in known:
                fail(f"{path}.{field}: unknown reference {ident!r}")

    if not isinstance(spec, dict):
        return ["root: expected object"], warnings
    if spec.get("schema_version") != "1.0":
        fail('root.schema_version: expected "1.0"')
    if not isinstance(spec.get("synthetic"), bool):
        fail("root.synthetic: expected boolean")
    require_text(spec, ["decision", "audience", "as_of"], "root")
    sources = index(rows(spec, "sources", "root"), "sources")
    claims = index(rows(spec, "claims", "root", True), "claims")
    slides = index(rows(spec, "slides", "root", True), "slides")

    for ident, source in sources.items():
        p = f"sources.{ident}"
        require_text(source, ["title", "publisher", "locator", "published_on",
                              "period", "scope", "limitations"], p)
        if source.get("provenance") not in ("public", "user_provided", "synthetic"):
            fail(f"{p}.provenance: expected public, user_provided or synthetic")
        if source.get("provenance") == "synthetic" and spec.get("synthetic") is not True:
            fail(f"{p}: synthetic source requires root.synthetic=true")
        for field in ["published_on", "period", "scope"]:
            if source.get(field) == "unknown":
                warnings.append(f"{p}.{field}: explicitly unknown")

    for ident, claim in claims.items():
        p = f"claims.{ident}"
        require_text(claim, ["text"], p)
        kind = claim.get("kind")
        if kind not in ("fact", "party_claim", "inference", "assumption", "recommendation"):
            fail(f"{p}.kind: unsupported claim kind")
        refs(claim, "source_ids", sources, p, kind in ("fact", "party_claim", "inference"))
        if kind in ("inference", "assumption", "recommendation"):
            require_text(claim, ["reasoning"], p)

    for ident, slide in slides.items():
        p = f"slides.{ident}"
        require_text(slide, ["title", "question", "implication", "visual"], p)
        refs(slide, "claim_ids", claims, p, True)
        for i, chart in enumerate(rows(slide, "charts", p)):
            cp = f"{p}.charts[{i}]"
            if not isinstance(chart, dict):
                fail(f"{cp}: expected object")
                continue
            require_text(chart, ["type", "unit", "period", "scope", "basis"], cp)
            refs(chart, "source_ids", sources, cp, True)
            if chart.get("basis") not in ("observed", "scenario", "mixed"):
                fail(f"{cp}.basis: expected observed, scenario or mixed")
            labels = rows(chart, "labels", cp, True)
            if any(not isinstance(x, str) or not x.strip() for x in labels):
                fail(f"{cp}.labels: expected nonempty strings")
            for j, series in enumerate(rows(chart, "series", cp, True)):
                sp = f"{cp}.series[{j}]"
                if not isinstance(series, dict):
                    fail(f"{sp}: expected object")
                    continue
                require_text(series, ["name"], sp)
                values = rows(series, "values", sp, True)
                if len(values) != len(labels):
                    fail(f"{sp}.values: count differs from labels")
                for value in values:
                    if isinstance(value, bool) or not isinstance(value, (int, float)) or (isinstance(value, float) and not math.isfinite(value)):
                        fail(f"{sp}.values: expected finite numbers; found {value!r}")
    if spec.get("synthetic") is True:
        warnings.append("Synthetic example: do not present as real-world evidence")
    return errors, warnings


def reject_constant(value):
    raise ValueError(f"non-standard JSON number: {value}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()
    try:
        spec = json.loads(args.spec.read_text(encoding="utf-8"), parse_constant=reject_constant)
    except (OSError, ValueError) as exc:
        print(f"INPUT ERROR: {exc}")
        return 2
    errors, warnings = validate(spec)
    for warning in warnings:
        print(f"WARNING: {warning}")
    for error in errors:
        print(f"ERROR: {error}")
    print(f"{'FAIL' if errors else 'PASS'}: {len(errors)} errors, {len(warnings)} warnings")
    print("Scope: structure and references only; not facts, calculations, causality, rendering or PPTX validity.")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
