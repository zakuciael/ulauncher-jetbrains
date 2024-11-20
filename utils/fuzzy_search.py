# The following source code was obtained from https://github.com/Ulauncher/Ulauncher under GPLv3 license.
# The original file can be found at:
# https://raw.githubusercontent.com/Ulauncher/Ulauncher/7a667ff629b4e838e29619b26738a8683ded7421/ulauncher/utils/fuzzy_search.py

from __future__ import annotations

import logging
import unicodedata
from difflib import Match, SequenceMatcher
from functools import lru_cache

logger = logging.getLogger()


def _get_matching_blocks_native(query: str, text: str) -> list[Match]:
    return SequenceMatcher(None, query, text).get_matching_blocks()


# Using Levenshtein is ~10x faster, but some older distro releases might not package Levenshtein
# with these methods. So we fall back on difflib.SequenceMatcher (native Python library) to be sure.
try:
    from Levenshtein import editops, matching_blocks  # type: ignore[import-not-found, unused-ignore]

    def _get_matching_blocks(query: str, text: str) -> list[tuple[int, int, int]]:
        return matching_blocks(editops(query, text), query, text)  # type: ignore[no-any-return, unused-ignore]

except ImportError:
    logger.info(
        "Using fuzzy-matching with Native Python SequenceMatcher module. "
        "optional dependency 'python-Levenshtein' is recommended for better performance"
    )
    _get_matching_blocks = _get_matching_blocks_native  # type: ignore[assignment]


# convert strings to easily typable ones without accents, so ex "motorhead" matches "motörhead"
def _normalize(string: str) -> str:
    return unicodedata.normalize("NFD", string.casefold()).encode("ascii", "ignore").decode("utf-8")


@lru_cache(maxsize=1000)
def get_matching_blocks(query: str, text: str) -> tuple[list[tuple[int, str]], int]:
    """
    Uses our _get_matching_blocks wrapper method to find the blocks using "Longest Common Substrings",
    :returns: list of tuples, containing the index and matching block, number of characters that matched
    """
    blocks = _get_matching_blocks(_normalize(query), _normalize(text))[:-1]
    output = []
    total_len = 0
    for _, text_index, length in blocks:
        output.append((text_index, text[text_index : text_index + length]))
        total_len += length
    return output, total_len


def get_score(query: str, text: str) -> float:
    """
    Uses get_matching_blocks() to figure out how much of the query that matches the text,
    and tries to weight this to slightly favor shorter results and largely favor word matches
    :returns: number between 0 and 100
    """

    if not query or not text:
        return 0.0

    query_len = len(query)
    text_len = len(text)
    max_len = max(query_len, text_len)
    blocks, matching_chars = get_matching_blocks(query, text)

    # Ratio of the query that matches the text
    base_similarity = matching_chars / query_len

    # Lower the score if the match is in the middle of a word.
    for index, _ in blocks:
        is_word_boundary = index == 0 or text[index - 1] == " "
        if not is_word_boundary:
            base_similarity -= 0.5 / query_len

    # Rank matches lower for each extra character, to slightly favor shorter ones.
    return 100 * base_similarity * query_len / (query_len + (max_len - query_len) * 0.001)

