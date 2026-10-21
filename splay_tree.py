
from typing import List, Any

#
# data classes
#

class SplayNode:
    def __init__(self, key: int, value: Any = None):
        self.key = key
        self.value = value
        self.left: SplayNode | None = None
        self.right: SplayNode | None = None
        self.parent: SplayNode | None = None

class SplayTree:
    def __init__(self):
        self.root: SplayNode | None = None
        self.tree_size = 0

    #
    # searches and rotations
    #

    
    def find_node(self, key: int) -> tuple[SplayNode | None, SplayNode | None]:
        # Find a node by key and return it along with the last visited node
        current = self.root
        last = None

        while current is not None:
            last = current

            if key == current.key:
                return current, last
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        return None, last


    def rotate(self, node: SplayNode) -> None:
        # Rotate a node around its parent
        parent = node.parent

        if parent is None:
            return

        grandparent = parent.parent

        # Right rotation when node is the child
        if node is parent.left:
            parent.left = node.right

            if node.right is not None:
                node.right.parent = parent

            node.right = parent

        # Left rotation when node is right child
        else:
            parent.right = node.left

            if node.left is not None:
                node.left.parent = parent

            node.left = parent

        parent.parent = node
        node.parent = grandparent

        # Connect rotated subtree to its former grandparent
        if grandparent is None:
            self.root = node
        elif grandparent.left is parent:
            grandparent.left = node
        else:
            grandparent.right = node


    #
    # splay functions
    #

    def splay_node(self, node: SplayNode) -> None:
    # Splay a node to the root
        while node.parent is not None:
            parent = node.parent
            grandparent = parent.parent

            # Zig: the node's parent is the root
            if grandparent is None:
                self.rotate(node)

            # Zig-Zig: node and parent both left or both right children
            elif ((node is parent.left) ==
                  (parent is grandparent.left)):
                self.rotate(parent)
                self.rotate(node)

            # Zig-Zag: node and parent on opposite sides
            else:
                self.rotate(node)
                self.rotate(node)

        self.root = node

    def splay(self, key: int) -> bool:
    # Splay last visited node or requested key to root
        node, last = self.find_node(key)

        if node is None:
            if last is not None:
                self.splay_node(last)
            return False

        self.splay_node(node)
        return True

    #
    # other helpers
    #

    def insert(self, key: int, value: Any = None) -> None:
    # Insert kv pair and splay to root
        if self.root is None:
            self.root = SplayNode(key, value)
            self.tree_size = 1
            return

        current = self.root
        parent = None

        while current is not None:
            parent = current

            if key == current.key:
                current.value = value
                self.splay_node(current)
                return
            elif key < current.key:
                current = current.left
            else:
                current = current.right

        new_node = SplayNode(key, value)
        new_node.parent = parent

        if key < parent.key: # type: ignore
            parent.left = new_node # type: ignore
        else:
            parent.right = new_node # type: ignore

        self.tree_size += 1
        self.splay_node(new_node)

    def search(self, key: int) -> Any:
    # Return value for a key and splay the accessed node
        node, last = self.find_node(key)

        if node is not None:
            self.splay_node(node)
            return node.value

        # Splay last visited node when the key is absent
        if last is not None:
            self.splay_node(last)

        return None

    def delete(self, key: int) -> bool:
    # Delete a key using splay-split-join
        if not self.splay(key):
            return False

        old_root = self.root
        left_subtree = old_root.left # type: ignore
        right_subtree = old_root.right # type: ignore

        # Detach both subtrees from the deleted root
        if left_subtree is not None:
            left_subtree.parent = None

        if right_subtree is not None:
            right_subtree.parent = None
 
        old_root.left = None # type: ignore
        old_root.right = None # type: ignore
        old_root.parent = None # type: ignore

        # If no left subtree, promote right subtree
        if left_subtree is None:
            self.root = right_subtree

        # If no right subtree, promote left subtree
        elif right_subtree is None:
            self.root = left_subtree

        # Otherwise, join subtrees using maximum of left
        else:
            self.root = left_subtree
            maximum = left_subtree

            while maximum.right is not None:
                maximum = maximum.right

            # Splay maximum to root of the left subtree
            self.splay_node(maximum)

            # Attach right subtree to the new root
            self.root.right = right_subtree
            right_subtree.parent = self.root

        self.tree_size -= 1
        return True

    def to_inorder_keys(self) -> List[Any]:
    # Return keys in ascending order
        keys = []

        def traverse(node: SplayNode | None) -> None:
            if node is None:
                return

            traverse(node.left)
            keys.append(node.key)
            traverse(node.right)

        traverse(self.root)
        return keys

    def root_key(self) -> int | None:
    # Return root key, or None if tree is empty
        if self.root is None:
            return None

        return self.root.key

    # Return number of distinct keys in the tree
    def size(self) -> int:
        return self.tree_size
