class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def _add_numbers(previous_carry, l1, l2):
    current_sum = previous_carry

    if l1 and l2:
        current_sum += l1.val + l2.val
    elif l1 and not l2:
        current_sum += l1.val
    elif not l1 and l2:
        current_sum += l2.val
    elif previous_carry == 0:
        return None

    carry = current_sum // 10
    remainder = current_sum % 10
    l = ListNode(remainder)
    l.next = _add_numbers(carry, l1 and l1.next, l2 and l2.next)

    return l


def add_numbers(l1, l2):
    return _add_numbers(0, l1, l2)


class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        return add_numbers(l1, l2)
