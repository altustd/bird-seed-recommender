"""
Bird seed affinity data and recommendation engine.

Curated from public sources (Cornell All About Birds, Kaytee, Audubon Guide to Birdseed,
Avian Report Eastern NA feeder study, state wildlife notes). Affinities are relative
preferences (0.0-1.0) for the seed type by that species at feeders. Not absolute
consumption rates.

All values are for "typical" healthy birds in the listed region during the listed
season. Regional and seasonal multipliers are applied on top.

No external calls; fully static for reliability and privacy.
"""

from __future__ import annotations
from datetime import datetime
from typing import Dict, List, Tuple
import pandas as pd

# Core seed types offered (keys used everywhere)
SEED_TYPES: List[str] = [
    "black_oil_sunflower",
    "nyjer",
    "safflower",
    "white_proso_millet",
    "peanuts",
    "suet",
    "sunflower_hearts",
    "cracked_corn",
    "milo",
]

SEED_LABELS: Dict[str, str] = {
    "black_oil_sunflower": "Black Oil Sunflower",
    "nyjer": "Nyjer (Thistle)",
    "safflower": "Safflower",
    "white_proso_millet": "White Proso Millet",
    "peanuts": "Peanuts (shelled)",
    "suet": "Suet Cakes / Dough",
    "sunflower_hearts": "Sunflower Hearts (no mess)",
    "cracked_corn": "Cracked Corn",
    "milo": "Milo / Sorghum",
}

SEED_TIPS: Dict[str, str] = {
    "black_oil_sunflower": "Best all-around; thin shell, high fat/energy. Tube, hopper, or platform.",
    "nyjer": "Goldfinches & small finches. Use sock or tube with tiny ports; keep fresh (small seed spoils).",
    "safflower": "Cardinals love it; bitter to many squirrels. Good in hopper or platform.",
    "white_proso_millet": "Ground feeders (doves, juncos, sparrows, towhees). Scatter or platform.",
    "peanuts": "Woodpeckers, nuthatches, jays, titmice. Mesh feeder or platform (shelled). High protein/fat.",
    "suet": "Woodpeckers, nuthatches, chickadees, titmice. Cage feeder. Especially valuable in winter.",
    "sunflower_hearts": "No-mess version of sunflower; attracts widest variety. More expensive but clean.",
    "cracked_corn": "Larger birds, doves, jays. Inexpensive but can attract starlings/grackles/pigeons.",
    "milo": "Western ground birds (quail, thrashers, some jays) like it; often filler in cheap mixes. Avoid in East.",
}

# ~18 common desirable backyard birds (focus on songbirds people want to attract)
# Display names chosen for multiselect; internal keys match AFFINITY.
COMMON_BIRDS: List[str] = [
    "Northern Cardinal",
    "American Goldfinch",
    "Black-capped Chickadee",
    "Tufted Titmouse",
    "White-breasted Nuthatch",
    "Downy Woodpecker",
    "Red-bellied Woodpecker",
    "Mourning Dove",
    "Blue Jay",
    "House Finch",
    "Pine Siskin",
    "Dark-eyed Junco",
    "White-throated Sparrow",
    "Song Sparrow",
    "Indigo Bunting",
    "Common Redpoll",
    "Carolina Wren",
    "Red-winged Blackbird",  # note: can be numerous/aggressive at seed
]

# Affinity matrix: bird -> {seed: 0.0-1.0 preference}
# Values synthesized/cross-checked from the cited guides (rounded for simplicity).
# Higher = stronger preference at feeders.
AFFINITY: Dict[str, Dict[str, float]] = {
    "Northern Cardinal": {
        "black_oil_sunflower": 0.95,
        "nyjer": 0.10,
        "safflower": 0.98,
        "white_proso_millet": 0.65,
        "peanuts": 0.55,
        "suet": 0.30,
        "sunflower_hearts": 0.90,
        "cracked_corn": 0.45,
        "milo": 0.25,
    },
    "American Goldfinch": {
        "black_oil_sunflower": 0.70,
        "nyjer": 1.00,
        "safflower": 0.15,
        "white_proso_millet": 0.35,
        "peanuts": 0.20,
        "suet": 0.10,
        "sunflower_hearts": 0.85,
        "cracked_corn": 0.10,
        "milo": 0.05,
    },
    "Black-capped Chickadee": {
        "black_oil_sunflower": 0.90,
        "nyjer": 0.55,
        "safflower": 0.40,
        "white_proso_millet": 0.25,
        "peanuts": 0.80,
        "suet": 0.85,
        "sunflower_hearts": 0.95,
        "cracked_corn": 0.30,
        "milo": 0.10,
    },
    "Tufted Titmouse": {
        "black_oil_sunflower": 0.88,
        "nyjer": 0.40,
        "safflower": 0.45,
        "white_proso_millet": 0.30,
        "peanuts": 0.85,
        "suet": 0.80,
        "sunflower_hearts": 0.92,
        "cracked_corn": 0.35,
        "milo": 0.15,
    },
    "White-breasted Nuthatch": {
        "black_oil_sunflower": 0.75,
        "nyjer": 0.15,
        "safflower": 0.35,
        "white_proso_millet": 0.20,
        "peanuts": 0.95,
        "suet": 0.92,
        "sunflower_hearts": 0.80,
        "cracked_corn": 0.25,
        "milo": 0.10,
    },
    "Downy Woodpecker": {
        "black_oil_sunflower": 0.60,
        "nyjer": 0.10,
        "safflower": 0.25,
        "white_proso_millet": 0.15,
        "peanuts": 0.70,
        "suet": 1.00,
        "sunflower_hearts": 0.65,
        "cracked_corn": 0.20,
        "milo": 0.05,
    },
    "Red-bellied Woodpecker": {
        "black_oil_sunflower": 0.70,
        "nyjer": 0.05,
        "safflower": 0.30,
        "white_proso_millet": 0.20,
        "peanuts": 0.85,
        "suet": 0.95,
        "sunflower_hearts": 0.75,
        "cracked_corn": 0.35,
        "milo": 0.15,
    },
    "Mourning Dove": {
        "black_oil_sunflower": 0.55,
        "nyjer": 0.05,
        "safflower": 0.40,
        "white_proso_millet": 0.90,
        "peanuts": 0.25,
        "suet": 0.05,
        "sunflower_hearts": 0.50,
        "cracked_corn": 0.85,
        "milo": 0.70,
    },
    "Blue Jay": {
        "black_oil_sunflower": 0.80,
        "nyjer": 0.05,
        "safflower": 0.35,
        "white_proso_millet": 0.30,
        "peanuts": 0.95,
        "suet": 0.50,
        "sunflower_hearts": 0.70,
        "cracked_corn": 0.75,
        "milo": 0.40,
    },
    "House Finch": {
        "black_oil_sunflower": 0.85,
        "nyjer": 0.75,
        "safflower": 0.25,
        "white_proso_millet": 0.45,
        "peanuts": 0.35,
        "suet": 0.20,
        "sunflower_hearts": 0.80,
        "cracked_corn": 0.25,
        "milo": 0.15,
    },
    "Pine Siskin": {
        "black_oil_sunflower": 0.65,
        "nyjer": 0.98,
        "safflower": 0.15,
        "white_proso_millet": 0.40,
        "peanuts": 0.25,
        "suet": 0.15,
        "sunflower_hearts": 0.70,
        "cracked_corn": 0.15,
        "milo": 0.10,
    },
    "Dark-eyed Junco": {
        "black_oil_sunflower": 0.50,
        "nyjer": 0.20,
        "safflower": 0.35,
        "white_proso_millet": 0.95,
        "peanuts": 0.30,
        "suet": 0.10,
        "sunflower_hearts": 0.55,
        "cracked_corn": 0.60,
        "milo": 0.50,
    },
    "White-throated Sparrow": {
        "black_oil_sunflower": 0.55,
        "nyjer": 0.15,
        "safflower": 0.40,
        "white_proso_millet": 0.90,
        "peanuts": 0.35,
        "suet": 0.15,
        "sunflower_hearts": 0.50,
        "cracked_corn": 0.55,
        "milo": 0.45,
    },
    "Song Sparrow": {
        "black_oil_sunflower": 0.45,
        "nyjer": 0.10,
        "safflower": 0.30,
        "white_proso_millet": 0.85,
        "peanuts": 0.25,
        "suet": 0.10,
        "sunflower_hearts": 0.45,
        "cracked_corn": 0.50,
        "milo": 0.40,
    },
    "Indigo Bunting": {
        "black_oil_sunflower": 0.60,
        "nyjer": 0.90,
        "safflower": 0.20,
        "white_proso_millet": 0.35,
        "peanuts": 0.25,
        "suet": 0.10,
        "sunflower_hearts": 0.65,
        "cracked_corn": 0.15,
        "milo": 0.10,
    },
    "Common Redpoll": {
        "black_oil_sunflower": 0.65,
        "nyjer": 0.95,
        "safflower": 0.15,
        "white_proso_millet": 0.30,
        "peanuts": 0.20,
        "suet": 0.25,
        "sunflower_hearts": 0.70,
        "cracked_corn": 0.15,
        "milo": 0.10,
    },
    "Carolina Wren": {
        "black_oil_sunflower": 0.70,
        "nyjer": 0.15,
        "safflower": 0.25,
        "white_proso_millet": 0.20,
        "peanuts": 0.60,
        "suet": 0.90,
        "sunflower_hearts": 0.65,
        "cracked_corn": 0.25,
        "milo": 0.10,
    },
    "Red-winged Blackbird": {
        "black_oil_sunflower": 0.50,
        "nyjer": 0.05,
        "safflower": 0.20,
        "white_proso_millet": 0.70,
        "peanuts": 0.40,
        "suet": 0.15,
        "sunflower_hearts": 0.45,
        "cracked_corn": 0.80,
        "milo": 0.60,
    },
}

# Regional multipliers (applied to base affinity before normalization)
# Values >1.0 boost, <1.0 penalize. "National" = 1.0 everywhere.
REGION_MULT: Dict[str, Dict[str, float]] = {
    "Northeast": {"milo": 0.25, "safflower": 1.10, "cracked_corn": 0.85},
    "Mid-Atlantic": {"milo": 0.35, "safflower": 1.08},
    "Southeast": {"milo": 0.50, "cracked_corn": 1.05, "safflower": 1.05},
    "Midwest": {"milo": 0.60},
    "Great Plains": {"milo": 1.10, "cracked_corn": 1.10},
    "Mountain West": {"milo": 1.25, "cracked_corn": 1.05, "peanuts": 0.95},
    "Pacific": {"milo": 0.70, "cracked_corn": 0.90},
    "Southwest": {"milo": 1.40, "cracked_corn": 1.15, "safflower": 0.95},
    "National": {},  # neutral
}

# Seasonal multipliers (winter = high fat/energy; summer = still seeds but less emphasis on suet)
SEASON_MULT: Dict[str, Dict[str, float]] = {
    "Winter": {"suet": 1.45, "peanuts": 1.25, "black_oil_sunflower": 1.10, "sunflower_hearts": 1.08},
    "Spring": {"suet": 1.10, "nyjer": 1.05},
    "Summer": {"suet": 0.70, "cracked_corn": 0.85, "milo": 0.80},  # insects abundant, but still want seed
    "Fall": {"suet": 1.15, "peanuts": 1.10},
}

REGIONS: List[str] = list(REGION_MULT.keys())
SEASONS: List[str] = ["Winter", "Spring", "Summer", "Fall"]


def get_current_season() -> str:
    """Return one of SEASONS based on current month (Northern Hemisphere)."""
    month = datetime.now().month
    if month in (12, 1, 2):
        return "Winter"
    if month in (3, 4, 5):
        return "Spring"
    if month in (6, 7, 8):
        return "Summer"
    return "Fall"


def get_region_multiplier(region: str, seed: str) -> float:
    return REGION_MULT.get(region, {}).get(seed, 1.0)


def get_season_multiplier(season: str, seed: str) -> float:
    return SEASON_MULT.get(season, {}).get(seed, 1.0)


def score_recommendation(
    region: str,
    season: str,
    selected_birds: List[str],
) -> Dict:
    """
    Core engine. Returns rich dict with:
      - per_seed: {seed: {"score": float 0-100, "label": str, "why": str, "mult": float}}
      - recipe: list of (seed, pct) sorted desc, suitable for a mix
      - top_seeds: list of labels
      - bird_coverage: {bird: {"best_seed": , "score": , "covered": bool}}
      - notes: list of str (warnings, tips)
    """
    if not selected_birds:
        selected_birds = []
        # Provide a sensible national default mix so UI/CLI always have something to show
        default_recipe = [
            ("black_oil_sunflower", 50),
            ("white_proso_millet", 25),
            ("sunflower_hearts", 15),
            ("safflower", 10),
        ]
        # We'll short-circuit later for recipe
        _use_default = True
    else:
        _use_default = False

    # 1. Base scores per seed (sum affinity over selected birds)
    raw: Dict[str, float] = {s: 0.0 for s in SEED_TYPES}
    bird_contrib: Dict[str, Dict[str, float]] = {b: {} for b in selected_birds}

    for bird in selected_birds:
        if bird not in AFFINITY:
            continue
        for seed, aff in AFFINITY[bird].items():
            contrib = aff
            raw[seed] += contrib
            bird_contrib[bird][seed] = contrib

    # 2. Apply region + season multipliers
    adjusted: Dict[str, float] = {}
    mults: Dict[str, float] = {}
    for seed in SEED_TYPES:
        m = get_region_multiplier(region, seed) * get_season_multiplier(season, seed)
        mults[seed] = m
        adjusted[seed] = raw[seed] * m

    # 3. Normalize to 0-100
    max_raw = max(adjusted.values()) if any(adjusted.values()) else 1.0
    scores: Dict[str, float] = {
        s: round((v / max_raw) * 100, 1) if max_raw > 0 else 50.0
        for s, v in adjusted.items()
    }

    # 4. Build per-seed rich info + simple "why" (top 1-2 birds that drove it)
    per_seed = {}
    for seed in SEED_TYPES:
        # Find birds that contributed most to this seed
        contribs = []
        for bird in selected_birds:
            if bird in bird_contrib and seed in bird_contrib[bird]:
                contribs.append((bird, bird_contrib[bird][seed]))
        contribs.sort(key=lambda x: x[1], reverse=True)
        top_birds = [c[0] for c in contribs[:2]]
        why = ""
        if top_birds:
            why = f"Strong for your {', '.join(top_birds)}"
        else:
            why = "Broadly attractive; good default"

        per_seed[seed] = {
            "score": scores[seed],
            "label": SEED_LABELS[seed],
            "why": why,
            "mult": round(mults[seed], 2),
            "tip": SEED_TIPS[seed],
        }

    # 5. Recipe % (normalize the adjusted scores, drop very low)
    if _use_default:
        recipe = [(SEED_LABELS[s], float(p)) for s, p in default_recipe]
    else:
        total = sum(adjusted.values()) or 1.0
        recipe_pairs: List[Tuple[str, float]] = []
        for seed in SEED_TYPES:
            pct = round((adjusted[seed] / total) * 100, 0)
            if pct >= 5:  # ignore tiny %
                recipe_pairs.append((seed, pct))
        recipe_pairs.sort(key=lambda x: x[1], reverse=True)
        # renormalize to 100 if we dropped some
        sum_pct = sum(p for _, p in recipe_pairs) or 100.0
        recipe = [(SEED_LABELS[s], round(p * 100 / sum_pct, 0)) for s, p in recipe_pairs]

    # 6. Bird coverage
    coverage = {}
    for bird in selected_birds:
        if bird not in AFFINITY:
            coverage[bird] = {"best_seed": "—", "score": 0.0, "covered": False}
            continue
        # best seed for this bird under current mults
        best_seed = max(
            AFFINITY[bird].keys(),
            key=lambda s: AFFINITY[bird][s] * mults.get(s, 1.0),
        )
        best_score = round(
            AFFINITY[bird][best_seed] * mults.get(best_seed, 1.0) * 100, 1
        )
        # Is it reasonably covered by our top 3 seeds?
        top3_seeds = sorted(scores, key=scores.get, reverse=True)[:3]
        covered = best_seed in top3_seeds or scores[best_seed] >= 60
        coverage[bird] = {
            "best_seed": SEED_LABELS[best_seed],
            "score": best_score,
            "covered": covered,
        }

    # 7. Notes / warnings
    notes: List[str] = []
    if region in ("Northeast", "Mid-Atlantic") and scores.get("milo", 0) > 20:
        notes.append("Milo is often ignored or wasted in your region — consider dropping it from mixes.")
    if "Red-winged Blackbird" in selected_birds and scores.get("cracked_corn", 0) > 60:
        notes.append("Cracked corn + millet will also draw lots of blackbirds/starlings. Use safflower or hearts in a tube if you want to favor songbirds.")
    if season == "Winter":
        notes.append("Suet and high-fat seeds (sunflower/peanuts) are critical in cold weather.")
    if not selected_birds:
        notes.append("No birds selected — showing a balanced national mix. Add your sightings for personalized results.")

    top_seeds = [SEED_LABELS[s] for s in sorted(scores, key=scores.get, reverse=True)[:3]]

    return {
        "region": region,
        "season": season,
        "selected_birds": selected_birds,
        "per_seed": per_seed,
        "recipe": recipe,
        "top_seeds": top_seeds,
        "bird_coverage": coverage,
        "notes": notes,
        "scores_raw": scores,  # for plots / export
    }


def get_bird_groups() -> Dict[str, List[str]]:
    """Return grouped birds for nicer multiselect in UI."""
    return {
        "Cardinals & Grosbeaks": ["Northern Cardinal"],
        "Finches & Siskins": ["American Goldfinch", "House Finch", "Pine Siskin", "Common Redpoll", "Indigo Bunting"],
        "Chickadees, Titmice, Nuthatches & Wrens": ["Black-capped Chickadee", "Tufted Titmouse", "White-breasted Nuthatch", "Carolina Wren"],
        "Woodpeckers": ["Downy Woodpecker", "Red-bellied Woodpecker"],
        "Doves & Ground Feeders": ["Mourning Dove", "Dark-eyed Junco", "White-throated Sparrow", "Song Sparrow"],
        "Jays & Larger": ["Blue Jay"],
        "Other / Icterids": ["Red-winged Blackbird"],
    }


if __name__ == "__main__":
    # Quick self-test
    rec = score_recommendation("National", "Summer", ["American Goldfinch"])
    print("Top 3:", rec["top_seeds"])
    print("Recipe:", rec["recipe"][:4])
    print("Notes:", rec["notes"])
    assert rec["per_seed"]["nyjer"]["score"] > 85  # goldfinch loves it
    print("Data module OK")