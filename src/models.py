"""
Thin domain layer. Re-exports the recommendation engine so app/cli import
from src.models (matches srm-ballistics convention).
All real logic lives in data.py for this simple table-driven tool.
"""

from .data import (
    score_recommendation,
    get_current_season,
    REGIONS,
    SEASONS,
    COMMON_BIRDS,
    SEED_LABELS,
    get_bird_groups,
)

__all__ = [
    "score_recommendation",
    "get_current_season",
    "REGIONS",
    "SEASONS",
    "COMMON_BIRDS",
    "SEED_LABELS",
    "get_bird_groups",
]