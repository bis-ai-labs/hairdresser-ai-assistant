from pathlib import Path

import pytest

from course_library import COURSE_MATERIALS_DIR, search_course_materials


def test_search_returns_matching_pricing_lesson() -> None:
    results = search_course_materials(
        "What costs should I consider when pricing a service?"
    )

    assert results
    assert results[0].source == "pricing-basics.md"
    assert results[0].title == "Pricing a Hair Service: A Simple Starting Point"
    assert "Direct materials" in results[0].content


def test_search_can_return_relevant_passages_from_multiple_lessons() -> None:
    results = search_course_materials("cancellation capacity")

    sources = {result.source for result in results}
    assert "booking-policy.md" in sources
    assert "monthly-review.md" in sources


def test_search_returns_no_results_for_unrelated_question() -> None:
    assert search_course_materials("spacecraft nebula telescope") == []


def test_search_returns_no_results_for_empty_or_stop_word_only_question() -> None:
    assert search_course_materials("") == []
    assert search_course_materials("what should I do") == []


def test_search_returns_no_results_for_missing_or_empty_directory(
    tmp_path: Path,
) -> None:
    missing_directory = tmp_path / "missing"
    empty_directory = tmp_path / "empty"
    empty_directory.mkdir()

    assert search_course_materials("pricing", missing_directory) == []
    assert search_course_materials("pricing", empty_directory) == []


def test_search_respects_max_results() -> None:
    results = search_course_materials(
        "appointment", COURSE_MATERIALS_DIR, max_results=2
    )

    assert len(results) == 2
    assert len({result.source for result in results}) == 2


def test_search_rejects_non_positive_max_results() -> None:
    with pytest.raises(ValueError, match="max_results must be at least 1"):
        search_course_materials("pricing", max_results=0)
