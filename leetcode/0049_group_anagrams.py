#!/usr/bin/env python3

from typing import List
from collections import defaultdict

ALPHABET_SIZE = 26


def alpha_to_int(c) -> int:
    return ord(c) - 97


def zero_list(size) -> List[int]:
    return [0] * size


def alpha_key(memo, s: str) -> List[str]:
    if s in memo:
        return memo[s]

    l = zero_list(ALPHABET_SIZE)
    for c in s:
        l[alpha_to_int(c)] += 1

    t = tuple(l)
    memo[s] = t

    return t


def group_anagrams(ss: List[str]) -> List[List[str]]:
    alpha_key_memo = {}

    ss_idxs_by_alpha_key = defaultdict(list)
    alpha_keys_by_s = {}

    for idx, s in enumerate(ss):
        key = alpha_key(alpha_key_memo, s)
        ss_idxs_by_alpha_key[key].append(idx)
        alpha_keys_by_s[s] = key

    anagrams = []
    anagrams_idx = -1

    for cs, s_idxs in ss_idxs_by_alpha_key.items():
        for s_idx in s_idxs:
            s = ss[s_idx]
            if (
                anagrams
                and len(anagrams) > 0
                and alpha_keys_by_s[anagrams[anagrams_idx][0]]
                == alpha_keys_by_s[s]
            ):
                anagrams[anagrams_idx].append(s)
            else:
                anagrams_idx += 1
                anagrams.append([])
                anagrams[anagrams_idx].append(s)

    return anagrams


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        return group_anagrams(strs)
