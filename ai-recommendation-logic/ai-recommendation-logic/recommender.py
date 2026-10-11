"""Transparent content-based recommendation logic."""
from __future__ import annotations

from typing import Iterable, Any


def jaccard_similarity(user_interests: Iterable[str], item_tags: Iterable[str]) -> float:
    """Return Jaccard similarity between two collections of tags, from 0 to 1."""
    interests = {str(value).strip().lower() for value in user_interests if str(value).strip()}
    tags = {str(value).strip().lower() for value in item_tags if str(value).strip()}
    union = interests | tags
    if not union:
        return 0.0
    return len(interests & tags) / len(union)


def recommend(
    user_interests: Iterable[str],
    catalog: list[dict[str, Any]],
    limit: int = 6,
    category: str = "All",
) -> list[dict[str, Any]]:
    """Rank catalog items by preference similarity, adding explanation metadata."""
    selected = {str(value).strip().lower() for value in user_interests if str(value).strip()}
    if not isinstance(limit, int):
        limit = 6
    limit = max(1, min(limit, 12))

    items = []
    for item in catalog:
        if category and category != "All" and item.get("category") != category:
            continue
        result = dict(item)
        tags = {str(tag).strip().lower() for tag in item.get("tags", [])}
        matched = sorted(selected & tags)
        result["score"] = jaccard_similarity(selected, tags) if selected else 0.0
        result["match_percent"] = round(result["score"] * 100)
        result["matched_tags"] = matched
        items.append(result)

    if selected:
        items.sort(key=lambda item: (-item["score"], -item.get("popularity", 0), item.get("title", "")))
    else:
        # No preferences: provide popular starter suggestions without claiming personalization.
        items.sort(key=lambda item: (-item.get("popularity", 0), item.get("title", "")))
    return items[:limit]
