from typing import List, Tuple, Callable

#
# data classes
#

class AVLNode:
    key: int
    value: int
    height: int
    size: int
    left: AVLNode | None
    right: AVLNode | None

    def __init__(self, key, value=None) -> None:
        self.key = key
        self.value = value # type: ignore
        self.left = None
        self.right = None
        self.height = 1
        self.size = 1

    def bf(self) -> int:
        # Balance factor: height(left) - height(right).
        return height_of(self.left) - height_of(self.right)


class AVLOrderStatisticTree:
    root: AVLNode | None

    def __init__(self) -> None:
        self.root = None

    def path_to(self, key) -> List[AVLNode]:
        # Nodes from the root down to the node holding key ([] if absent).
        path = []
        node = self.root
        while node is not None:
            path.append(node)
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return path
        return []

    #
    # replacements and rotations
    #

    def replace_at(self, path: List[AVLNode], new_sub: AVLNode) -> None:
        # Put new_sub where path[-1] was, then refresh ancestors' metadata.
        old = path[-1]
        if len(path) == 1:
            self.root = new_sub
        else:
            parent = path[-2]
            if parent.left is old:
                parent.left = new_sub
            else:
                parent.right = new_sub
        for anc in reversed(path[:-1]):
            update_node(anc)

    def rotate_right(self, key) -> bool:
        # Rotate the node holding key right. False if absent / no left child.
        path = self.path_to(key)
        if not path or path[-1].left is None:
            return False
        self.replace_at(path, rot_right_node(path[-1])) # type: ignore
        return True

    def rotate_left(self, key) -> bool:
        # Rotate the node holding key left. False if absent / no right child.
        path = self.path_to(key)
        if not path or path[-1].right is None:
            return False
        self.replace_at(path, rot_left_node(path[-1])) # type: ignore
        return True

    #
    # cases
    #

    def apply_case(self, key, case: Callable[[AVLNode], AVLNode | None]) -> bool:
        # Apply a node-level case fix at the node holding key, if it applies
        path = self.path_to(key)
        if not path:
            return False
        fixed = case(path[-1])
        if fixed is None:
            return False
        self.replace_at(path, fixed)
        return True

    def rr_case(self, key) -> bool:
        # Right-right imbalance at key: single left rotation.
        return self.apply_case(key, rr_node)

    def ll_case(self, key) -> bool:
        # Left-left imbalance at key: single right rotation.
        return self.apply_case(key, ll_node)

    def rl_case(self, key) -> bool:
        # Right-left imbalance at key: right-rotate child, then left-rotate.
        return self.apply_case(key, rl_node)

    def lr_case(self, key) -> bool:
        # Left-right imbalance at key: left-rotate child, then right-rotate.
        return self.apply_case(key, lr_node)

    def insert(self, key, value=None) -> None:
        # Insert (key, value); update the value if key already exists.
        self.root = insert_node(self.root, key, value)

    def delete(self, key) -> bool:
        # Delete key. Returns True if it was present, else False.
        self.root, found = delete_node(self.root, key)
        return found

    def find(self, key) -> int | None:
        # Return the value stored under key, or None if absent.
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        return None

    def select(self, k) -> int | None:
        # Return the k-th smallest key (1-indexed). IndexError if invalid
        if not isinstance(k, int) or k < 1 or k > size_of(self.root):
            raise IndexError("select index out of range")
        node = self.root
        while True:
            left_size = size_of(node.left) # type: ignore
            if k == left_size + 1:
                return node.key # type: ignore
            if k <= left_size:
                node = node.left # type: ignore
            else:
                k -= left_size + 1
                node = node.right # type: ignore

    def rank(self, key) -> int:
        # Return the number of keys <= key (key need not be in the tree).
        r = 0
        node = self.root
        while node is not None:
            if key < node.key:
                node = node.left
            else:
                r += size_of(node.left) + 1
                node = node.right
        return r

    def size(self) -> int:
        # Number of elements, O(1).
        return size_of(self.root)

    def is_valid_avl(self) -> bool:
        # Check BST order, stored heights/sizes, and |BF| <= 1 everywhere.
        return check_node(self.root, None, None) is not None


#
# helpers
#

def height_of(node) -> int:
    # Height of a subtree; 0 for None.
    return node.height if node else 0


def size_of(node) -> int:
    # Size of a subtree; 0 for None.
    return node.size if node else 0


def update_node(node) -> None:
    # Recompute height and size of node from its children.
    node.height = 1 + max(height_of(node.left), height_of(node.right))
    node.size = 1 + size_of(node.left) + size_of(node.right)


def rot_right_node(y):
    # Right rotation about y; returns the new subtree root.
    x = y.left
    y.left = x.right
    x.right = y
    update_node(y)
    update_node(x)
    return x


def rot_left_node(x):
    # Left rotation about x; returns the new subtree root.
    y = x.right
    x.right = y.left
    y.left = x
    update_node(x)
    update_node(y)
    return y


def ll_node(node):
    # If node is left-left heavy, fix it and return the new root, else None.
    if node.bf() > 1 and node.left.bf() >= 0:
        return rot_right_node(node)
    return None


def lr_node(node):
    # If node is left-right heavy, fix it and return the new root, else None.
    if node.bf() > 1 and node.left.bf() < 0:
        node.left = rot_left_node(node.left)
        return rot_right_node(node)
    return None


def rr_node(node):
    # If node is right-right heavy, fix it and return the new root, else None.
    if node.bf() < -1 and node.right.bf() <= 0:
        return rot_left_node(node)
    return None


def rl_node(node):
    # If node is right-left heavy, fix it and return the new root, else None.
    if node.bf() < -1 and node.right.bf() > 0:
        node.right = rot_right_node(node.right)
        return rot_left_node(node)
    return None


def rebalance_node(node):
    # Update node, then apply whichever case (if any) restores |BF| <= 1.
    update_node(node)
    for fix in (ll_node, lr_node, rr_node, rl_node):
        fixed = fix(node)
        if fixed is not None:
            return fixed
    return node


def insert_node(node, key, value):
    # Recursive insert; returns the new subtree root.
    if node is None:
        return AVLNode(key, value)
    if key < node.key:
        node.left = insert_node(node.left, key, value)
    elif key > node.key:
        node.right = insert_node(node.right, key, value)
    else:
        node.value = value
        return node
    return rebalance_node(node)


def delete_min_node(node):
    # Remove the minimum node of a subtree; returns the new subtree root.
    if node.left is None:
        return node.right
    node.left = delete_min_node(node.left)
    return rebalance_node(node)


def delete_node(node, key) -> Tuple[AVLNode | None, bool]:
    # Recursive delete; returns (new subtree root, whether key was found).
    if node is None:
        return None, False
    if key < node.key:
        node.left, found = delete_node(node.left, key)
    elif key > node.key:
        node.right, found = delete_node(node.right, key)
    else:
        found = True
        if node.left is None:
            return node.right, True
        if node.right is None:
            return node.left, True
        # Two children: copy in-order successor, then delete it from right.
        succ = node.right
        while succ.left is not None:
            succ = succ.left
        node.key, node.value = succ.key, succ.value
        node.right = delete_min_node(node.right)
    return rebalance_node(node), found


def check_node(node, lo, hi):
    # Return (height, size) if the subtree is valid AVL/BST, else None.
    if node is None:
        return (0, 0)
    if lo is not None and not (node.key > lo):
        return None
    if hi is not None and not (node.key < hi):
        return None
    left = check_node(node.left, lo, node.key)
    if left is None:
        return None
    right = check_node(node.right, node.key, hi)
    if right is None:
        return None
    if abs(left[0] - right[0]) > 1:
        return None
    h = 1 + max(left[0], right[0])
    s = 1 + left[1] + right[1]
    if node.height != h or node.size != s:
        return None
    return (h, s)


if __name__ == "__main__":
    def build(keys):
        t = AVLOrderStatisticTree()
        for x in keys:
            t.insert(x, x * 10)
        return t

    def shape(node):
        # Nested-tuple view of a subtree, for exact shape assertions.
        if node is None:
            return None
        return (node.key, shape(node.left), shape(node.right))

    def manual(spec):
        # Build an UNbalanced tree from nested tuples (key, left, right).
        if spec is None:
            return None
        n = AVLNode(spec[0], spec[0] * 10)
        n.left, n.right = manual(spec[1]), manual(spec[2])
        update_node(n)
        return n

    def with_root(spec):
        t = AVLOrderStatisticTree()
        t.root = manual(spec)
        return t