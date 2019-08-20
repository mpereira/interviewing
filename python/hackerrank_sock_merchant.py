#!/bin/python3

import math
import os
import random
import re
import sys

def sockMerchant(n, ar):
    m = {}
    for x in ar:
        if x in m:
            m[x] += 1
        else:
            m[x] = 1

    pairs = 0

    for color, count in m.items():
        rest = count % 2
        if rest == 0:
            pairs += count
        else:
            pairs += count - 1

    return pairs // 2


if __name__ == '__main__':
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    n = int(input())

    ar = list(map(int, input().rstrip().split()))

    result = sockMerchant(n, ar)

    fptr.write(str(result) + '\n')

    fptr.close()
