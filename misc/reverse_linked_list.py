class Node:
    def __init__(self, value):
        self.value = value
        self.next = None

    def add_next(self, node):
        self.next = node


def print_linked_list(node: Node) -> None:
    print(node.value)
    if node.next:
        print_linked_list(node.next)


def reverse_linked_list(node: Node) -> None:
    if not node:
        return

    p = node
    nodes = [node]

    while p.next:
        nodes.append(p.next)
        p = p.next

    i = len(nodes) - 1
    _reversed = nodes[i]

    while i >= 0:
        n = nodes[i]
        if i == 0:
            n.next = None
            break
        n.next = nodes[i - 1]
        i -= 1

    return _reversed
