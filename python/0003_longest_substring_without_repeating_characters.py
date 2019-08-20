def _longest_substring_without_repeating_characters(
    memo, current_longest, current, offset, s
):
    if offset == len(s):
        return current_longest

    current_char = s[offset]

    if current_char in memo:
        previous_current_char_idx = memo[current_char]
        current_char_idx = current.index(current_char)
        new_current = s[previous_current_char_idx + 1 : offset + 1]
        for i in range(0, current_char_idx + 1):
            del memo[current[i]]
    else:
        new_current = current + current_char

        if len(new_current) >= len(current_longest):
            current_longest = new_current

    memo[current_char] = offset

    return _longest_substring_without_repeating_characters(
        memo, current_longest, new_current, offset + 1, s
    )


def longest_substring_without_repeating_characters(s):
    if len(s) == 0:
        return ""

    c = s[0]
    memo = {}
    memo[c] = 0
    return _longest_substring_without_repeating_characters(memo, c, c, 1, s)


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        return len(longest_substring_without_repeating_characters(s))
