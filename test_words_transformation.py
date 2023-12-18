from unittest.mock import patch
import pytest

from words_transformation import WordsTransformation


@patch("words_transformation.INSERT_COST", 1)
@patch("words_transformation.DELETE_COST", 1)
@patch("words_transformation.REPLACE_COST", 1)
@pytest.mark.parametrize("word1, word2, distance", [
    ("", "", 0),
    ("qwerty", "qwerty", 0),
    ("q", "", 1),
    ("qwerty", "werty", 1),
    ("werty", "Qwerty", 1),
    ("qwerty", "Qwerty", 1),
    ("qwerty", "", 6),
    ("qwerty", "RTY", 6),
    ("qwerty", "et", 4),
])
def test_get_minimal_distance(word1: str, word2: str, distance: int) -> None:
    assert WordsTransformation(word1, word2).get_minimal_distance() == distance
    assert WordsTransformation(word2, word1).get_minimal_distance() == distance


@patch("words_transformation.INSERT_COST", 1)
@patch("words_transformation.DELETE_COST", 2)
@patch("words_transformation.REPLACE_COST", 3)
@pytest.mark.parametrize("word1, word2, distance", [
    ("A", "A", 0),
    ("asd", "asd", 0),
    ("", "A", 1),
    ("aaa", "aaaA", 1),
    ("A", "", 2),
    ("Aaaa", "aaa", 2),
    ("A", "B", 3),
    ("AaaaA", "BaaaB", 6),
])
def test_get_minimal_distance_cost_is_not_equal(word1: str, word2: str, distance: int) -> None:
    assert WordsTransformation(word1, word2).get_minimal_distance() == distance


@patch("words_transformation.INSERT_COST", 1)
@patch("words_transformation.DELETE_COST", 1)
@patch("words_transformation.REPLACE_COST", 100)
@pytest.mark.parametrize("word1, word2, distance", [
    ("A", "A", 0),
    ("asd", "asd", 0),
    ("", "A", 1),
    ("aaa", "aaaA", 1),
    ("A", "", 1),
    ("Aaaa", "aaa", 1),
    ("A", "B", 2),  # add and remove instead replace operation
    ("AaaaA", "BaaaB", 4),  # add and remove instead replace operation
])
def test_get_minimal_distance_replace_is_too_expensive(word1: str, word2: str, distance: int) -> None:
    assert WordsTransformation(word1, word2).get_minimal_distance() == distance


@patch("words_transformation.INSERT_COST", 1)
@patch("words_transformation.DELETE_COST", 1)
@patch("words_transformation.REPLACE_COST", 1)
@pytest.mark.parametrize("word1, word2, res", [
    ("", "", [""]),
    ("qwerty", "qwerty", ["qwerty"]),
    ("q", "", ["q", ""]),
    ("qwerty", "werty", ["qwerty", "werty"]),
    ("werty", "Qwerty", ["werty", "Qwerty"]),
    ("qwerty", "Qwerty", ["qwerty", "Qwerty"]),
    ("qwerty", "", ["qwerty", "qwert", "qwer", "qwe", "qw", "q", ""]),
    ("qwerty", "RTY", ["qwerty", "qwertY", "qwerTY", "qweRTY", "qwRTY", "qRTY", "RTY"]),
    ("qwerty", "etz", ["qwerty", "qwertz", "qwetz", "qetz", "etz"]),
])
def test_get_get_transformation(word1: str, word2: str, res: list[str]) -> None:
    assert list(
        WordsTransformation(word1, word2).get_transformation()
    ) == res


@pytest.mark.parametrize("arr, index, new_item, res", [
    ([], 0, "A", ["A"]),
    ([], -1, "A", ["A"]),
    (["A", "B", "C"], -1, "A", ["A", "B", "A", "C"]),
    (["A", "B", "C"], 2, "A", ["A", "B", "A", "C"]),
    (["A", "B", "C"], 3, "A", ["A", "B", "C", "A"]),
    (["A", "B", "C"], 4, "A", ["A", "B", "C", "A"]),
    (["A", "B", "C"], 55, "A", ["A", "B", "C", "A"]),
])
def test__insert_into_array(arr: list[str], index: int, new_item: str, res: list[str]):
    assert WordsTransformation._insert_into_array(arr, index, new_item) == res
