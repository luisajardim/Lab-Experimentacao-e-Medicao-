from __future__ import annotations

import pytest

from metrics import cfr_release


@pytest.mark.parametrize(
    ("tag", "expected"),
    [
        ("v1.2.3", (1, 2, 3)),
        ("1.8.1", (1, 8, 1)),
        ("rel/v5.6", (5, 6, 0)),
        ("v0.33.14-beta", (0, 33, 14)),
        ("release-2.3.3", (2, 3, 3)),
        ("nightly", None),
        ("", None),
        (None, None),
    ],
)
def test_semver(tag: str | None, expected: tuple[int, int, int] | None) -> None:
    assert cfr_release.semver(tag) == expected


@pytest.mark.parametrize(
    ("tag", "previous", "expected"),
    [
        ("v1.2.4", "v1.2.3", True),
        ("rel/v5.6.1", "rel/v5.6", True),
        ("v1.3.0", "v1.2.9", False),  # minor
        ("v2.0.0", "v1.9.9", False),  # major
        ("v1.2.3", "v1.2.3", False),  # mesma versão
        ("v1.2.2", "v1.2.3", False),  # patch menor (fora de ordem)
        ("v1.2.4", None, False),  # primeira release
        ("nightly", "v1.2.3", False),
    ],
)
def test_is_patch_only(tag: str, previous: str | None, expected: bool) -> None:
    assert cfr_release.is_patch_only(tag, previous) is expected
    assert cfr_release.v1(tag, previous) is expected


def test_keyword_pattern_substring_vs_whole_word() -> None:
    substring = cfr_release.keyword_pattern()
    word = cfr_release.keyword_pattern(whole_word=True)
    for message in ("Fix crash", "HOTFIX: login", "Revert \"feat\"", "fixes #12"):
        assert substring.search(message)
        assert word.search(message)
    assert substring.search("add prefix option")
    assert not word.search("add prefix option")


def test_keyword_ratio() -> None:
    pattern = cfr_release.keyword_pattern()
    assert cfr_release.keyword_ratio(["fix a", "feat b", "revert c", "docs"], pattern) == 0.5
    assert cfr_release.keyword_ratio([], pattern) == 0.0
    assert cfr_release.keyword_ratio(None, pattern) == 0.0


def test_v2_and_v3() -> None:
    assert cfr_release.v2("v1.2.4", "v1.2.3", 0.0)
    assert cfr_release.v2("v1.3.0", "v1.2.3", 0.1)
    assert not cfr_release.v2("v1.3.0", "v1.2.3", 0.0)

    assert cfr_release.v3_score("v1.2.4", "v1.2.3", 0.5) == pytest.approx(2.0)
    assert cfr_release.v3("v1.3.0", "v1.2.3", 0.5, cutoff=1.0)
    assert not cfr_release.v3("v1.3.0", "v1.2.3", 0.25, cutoff=1.0)
    assert cfr_release.v3("v1.2.4", "v1.2.3", 0.0, cutoff=1.0)


def test_evaluate() -> None:
    scores = cfr_release.evaluate(
        [True, True, False, False, True], [True, False, True, False, True]
    )
    assert (scores.tp, scores.fp, scores.fn, scores.tn) == (2, 1, 1, 1)
    assert scores.precision == pytest.approx(2 / 3)
    assert scores.recall == pytest.approx(2 / 3)
    assert scores.f1 == pytest.approx(2 / 3)

    empty = cfr_release.evaluate([False], [False])
    assert (empty.precision, empty.recall, empty.f1) == (0.0, 0.0, 0.0)

    with pytest.raises(ValueError):
        cfr_release.evaluate([True], [True, False])
