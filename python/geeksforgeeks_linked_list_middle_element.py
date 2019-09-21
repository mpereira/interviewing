#!/usr/bin/env python3

# https://practice.geeksforgeeks.org/problems/finding-middle-element-in-a-linked-list/1


class node:
    def __init__(self, val):
        self.data = val
        self.next = None


class Linked_List:
    def __init__(self):
        self.head = None

    def insert(self, val):
        if self.head is None:
            self.head = node(val)
        else:
            new_node = node(val)
            temp = self.head
            while temp.next:
                temp = temp.next
            temp.next = new_node


def createList(arr, n):
    lis = Linked_List()
    for i in range(n):
        lis.insert(arr[i])
    return lis.head


def findMid(head):
    if not head:
        return

    length = 0
    p = head

    while p:
        p = p.next
        length += 1

    p = head
    j = 0

    middle = length // 2

    while j < middle:
        p = p.next
        j += 1

    return p


if __name__ == "__main__":
    t = int(input())
    for i in range(t):
        n = int(input())
        arr = list(map(int, input().strip().split()))
        head = createList(arr, n)
        print(findMid(head).data)
