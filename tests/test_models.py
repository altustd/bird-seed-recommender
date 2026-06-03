"""
Basic tests for the recommendation engine and data.
Run with: pixi run test
"""

import pytest
from src.models import score_recommendation, REGIONS, SEASONS, COMMON_BIRDS


def test_basic_recommendation_has_expected_keys():
    rec = score_recommendation("Northeast", "Winter", ["Northern Cardinal", "American Goldfinch"])
    assert "per_seed" in rec
    assert "recipe" in rec
    assert "top_seeds" in rec
    assert "bird_coverage" in rec
    assert "scores_raw" in rec
    assert len(rec["top_seeds"]) >= 1


def test_goldfinch_loves_nyjer():
    rec = score_recommendation("National", "Summer", ["American Goldfinch"])
    nyjer_score = rec["per_seed"]["nyjer"]["score"]
    sunflower_score = rec["per_seed"]["black_oil_sunflower"]["score"]
    assert nyjer_score > 85
    assert nyjer_score > sunflower_score + 5  # strong preference


def test_region_changes_milo_value():
    rec_east = score_recommendation("Northeast", "Winter", ["Mourning Dove"])
    rec_sw = score_recommendation("Southwest", "Winter", ["Mourning Dove"])
    assert rec_sw["per_seed"]["milo"]["score"] > rec_east["per_seed"]["milo"]["score"]


def test_season_boosts_suet_in_winter():
    rec_w = score_recommendation("Midwest", "Winter", ["Downy Woodpecker"])
    rec_s = score_recommendation("Midwest", "Summer", ["Downy Woodpecker"])
    # suet gets a large seasonal multiplier in winter; the final normed score for a suet specialist
    # will be 100 either way, so check the returned "mult" factor instead
    assert rec_w["per_seed"]["suet"]["mult"] > rec_s["per_seed"]["suet"]["mult"]
    assert rec_w["per_seed"]["suet"]["mult"] >= 1.4


def test_no_birds_still_returns_something():
    rec = score_recommendation("National", "Fall", [])
    assert len(rec["recipe"]) >= 2
    # generic path now always emits a default recipe (notes may mention it)
    assert sum(p for _, p in rec["recipe"]) >= 95


def test_unknown_bird_ignored_gracefully():
    rec = score_recommendation("Pacific", "Spring", ["Northern Cardinal", "Purple People Eater"])
    assert "Northern Cardinal" in rec["bird_coverage"]
    assert "Purple People Eater" in rec["bird_coverage"]
    assert rec["bird_coverage"]["Purple People Eater"]["score"] == 0.0
    assert rec["bird_coverage"]["Purple People Eater"]["covered"] is False


def test_recipe_sums_near_100():
    rec = score_recommendation("Southeast", "Winter", ["Northern Cardinal", "Mourning Dove", "Blue Jay"])
    total = sum(pct for _, pct in rec["recipe"])
    assert 98 <= total <= 102  # rounding tolerance


def test_all_regions_and_seasons_work():
    for r in REGIONS:
        for s in SEASONS:
            rec = score_recommendation(r, s, ["Black-capped Chickadee"])
            assert max(rec["scores_raw"].values()) >= 50.0


def test_common_birds_list_is_nonempty_and_known():
    assert len(COMMON_BIRDS) >= 10
    rec = score_recommendation("National", "Winter", COMMON_BIRDS[:5])
    assert len(rec["bird_coverage"]) == 5