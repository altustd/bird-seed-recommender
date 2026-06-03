#!/usr/bin/env python
"""
CLI entry point for Backyard Seed Advisor.

Examples:
  python cli.py --region Southeast --season Winter --birds "Northern Cardinal,American Goldfinch"
  python cli.py --help
  python cli.py --region National --season Summer --birds "Dark-eyed Junco" --out-mix recipe.txt --out-csv scores.csv
"""

import argparse
import sys
from pathlib import Path

from src.models import score_recommendation, REGIONS, SEASONS, COMMON_BIRDS
from src.export import save_recipe_txt, save_scores_csv, save_excel


def parse_birds(arg: str) -> list[str]:
    if not arg:
        return []
    return [b.strip() for b in arg.split(",") if b.strip()]


def main() -> int:
    p = argparse.ArgumentParser(
        description="Backyard Seed Advisor — recommend seed from location + season + sightings (CLI)"
    )
    p.add_argument(
        "--region",
        choices=REGIONS,
        default="National",
        help="Your region (affects regional multipliers, e.g. milo value in Southwest vs Northeast)",
    )
    p.add_argument(
        "--season",
        choices=SEASONS,
        default="Winter",
        help="Current season (affects suet/peanut/fat emphasis)",
    )
    p.add_argument(
        "--birds",
        type=str,
        default="",
        help="Comma-separated list of common names you've seen, e.g. 'Northern Cardinal,American Goldfinch,Dark-eyed Junco'",
    )
    p.add_argument(
        "--out-mix",
        type=Path,
        default=None,
        help="Write recipe text to this path (e.g. recipe.txt)",
    )
    p.add_argument(
        "--out-csv",
        type=Path,
        default=None,
        help="Write per-seed scores CSV to this path",
    )
    p.add_argument(
        "--out-xlsx",
        type=Path,
        default=None,
        help="Write formatted Excel report (Recipe + Scores sheets)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="Print full recommendation dict as JSON (for scripting)",
    )
    args = p.parse_args()

    birds = parse_birds(args.birds)
    unknown = [b for b in birds if b not in COMMON_BIRDS]
    if unknown:
        print(f"Warning: unknown bird name(s) will be ignored: {unknown}", file=sys.stderr)

    rec = score_recommendation(args.region, args.season, birds)

    if args.json:
        import json

        print(json.dumps(rec, indent=2, default=str))
        return 0

    # Human readable
    print(f"Region: {rec['region']} | Season: {rec['season']}")
    print(f"Birds: {', '.join(rec['selected_birds']) or '(none — generic mix)'}")
    print()
    print("Top seeds:")
    for i, s in enumerate(rec["top_seeds"], 1):
        print(f"  {i}. {s}")
    print()
    print("Suggested mix (% by weight):")
    for label, pct in rec["recipe"][:6]:
        print(f"  {pct:5.0f}%  {label}")
    if len(rec["recipe"]) > 6:
        print("  ... (truncated)")

    if rec["notes"]:
        print()
        print("Notes:")
        for n in rec["notes"]:
            print(f"  - {n}")

    # Exports if requested
    if args.out_mix:
        p = save_recipe_txt(rec, args.out_mix)
        print(f"\nWrote recipe: {p}")

    if args.out_csv:
        p = save_scores_csv(rec, args.out_csv)
        print(f"Wrote scores CSV: {p}")

    if args.out_xlsx:
        p = save_excel(rec, args.out_xlsx)
        print(f"Wrote Excel report: {p}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())