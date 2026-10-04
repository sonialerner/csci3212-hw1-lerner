from typing import List, Tuple, Callable, Any

#
# data classes
#

class SplayNode:
    key: int
    value: int

class SplayTree:
    root: SplayNode | None

    def zig(self, key) -> bool:
        return False

    def zig_zig(self, key) -> bool:
        return False

    def zig_zag(self, key) -> bool:
        return False

    def splay(self, key) -> bool:
        return False

    def insert(self, key, value=None) -> None:
        pass

    def search(self, key) -> int | None:
        pass

    def delete(self, key) -> bool:
        return False

    def to_inorder_keys(self) -> List[Any]:
        return [None]

    def root_key(self) -> int | None:
        pass

    def size(self) -> int:
        return 0
