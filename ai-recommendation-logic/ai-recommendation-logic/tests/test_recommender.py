from catalog import CATALOG
from recommender import jaccard_similarity, recommend


def test_jaccard_similarity_exact_match():
    assert jaccard_similarity(["python", "ai"], ["python", "ai"]) == 1.0


def test_jaccard_similarity_partial_match():
    assert jaccard_similarity(["python", "ai"], ["python", "web"]) == 1 / 3


def test_jaccard_similarity_empty_sets():
    assert jaccard_similarity([], []) == 0.0


def test_recommendation_ranks_matching_item_first():
    results = recommend(["python"], CATALOG, limit=5)
    assert results[0]["title"] == "Python for Beginners"
    assert results[0]["match_percent"] > 0


def test_recommendation_filters_category():
    results = recommend(["ai"], CATALOG, category="Music")
    assert all(item["category"] == "Music" for item in results)


def test_no_interests_returns_popular_items():
    results = recommend([], CATALOG, limit=3)
    assert len(results) == 3
    assert results[0]["popularity"] >= results[-1]["popularity"]


def test_limit_is_bounded():
    assert len(recommend([], CATALOG, limit=100)) == 12
    assert len(recommend([], CATALOG, limit=0)) == 1
