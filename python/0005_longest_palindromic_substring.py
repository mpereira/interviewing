from pprint import pprint


class Solution:
    def longestPalindrome(self, s: str) -> str:
        return longest_palindrome(s)


def longest_common_substring_offsets(s1, s2):
    m = [0] * len(s1)
    biggest = None

    for i in range(0, len(s1)):
        m[i] = [0] * len(s2)
        for j in range(0, len(s2)):
            if s1[i] == s2[j]:
                if i == 0 or j == 0:
                    m[i][j] = 1
                else:
                    m[i][j] = m[i - 1][j - 1] + 1

                if not biggest or m[biggest[0]][biggest[1]] < m[i][j]:
                    biggest = (i, j)

    if not biggest:
        return

    m_offsets = []
    k, l = biggest

    while k >= 0 and l >= 0 and m[k][l] != 0:
        m_offsets.append((k, l))
        k -= 1
        l -= 1

    first = m_offsets[0]
    last = m_offsets[len(m_offsets) - 1]
    s1_start, s1_end = last[0], first[0]
    s2_start, s2_end = last[1], first[1]

    return (s1_start, s1_end), (s2_start, s2_end)


def reverse_offsets(length, offsets):
    start, end = offsets
    print("reverse", offsets, length - end - 1, length - start - 1)
    return length - end - 1, length - start - 1


def longest_palindrome(s):
    if not s:
        return s

    length = len(s)

    r = "".join(reversed(s))
    current_longest_palindrome = s[0]
    offsets = longest_common_substring_offsets(s, r)
    print(offsets)

    if not offsets:
        return current_longest_palindrome

    s_offsets, r_offsets = offsets
    s_start, s_end = s_offsets
    r_start, r_end = r_offsets

    if s_offsets == reverse_offsets(length, r_offsets):
        palindrome = s[s_start : s_end + 1]
        print("palindrome", palindrome)
        if len(palindrome) >= len(current_longest_palindrome):
            print("palindrome longer", palindrome)
            current_longest_palindrome = palindrome

    return current_longest_palindrome


# print(longest_palindrome("aa"))
# print(longest_palindrome("acbcacbc"))
# print(longest_palindrome("xacbgbcaxafg"))
# print(longest_palindrome("aabb"))
# print(longest_palindrome("aacbb"))
# pprint(longest_palindrome("cbdcac"))
# pprint(longest_palindrome("cbdcac"))
# pprint(cached_is_palindrome({}, "adada"))
# pprint(longest_palindrome("dasaadaads"))
pprint(longest_palindrome("aacdefcaa"))
