from typing import List, Tuple, Callable

#
# data classes
#

class AVLNode:
    key: int
    value: int
    height: int

    def bf(self) -> int:
        return 0

class AVLOrderStatisticTree:
    root: AVLNode | None

    def rotate_right(self, key) -> bool:
        return False

    def rotate_left(self, key) -> bool:
        return False

    def rr_case(self, key) -> bool:
        return False

    def ll_case(self, key) -> bool:
        return False

    def rl_case(self, key) -> bool:
        return False

    def lr_case(self, key) -> bool:
        return False

    def insert(self, key, value=None) -> None:
        pass

    def delete(self, key) -> bool:
        return False 

    def find(self, key) -> int | None:
        pass

    def select(self, k) -> int | None:
        pass

    def rank(self, key) -> int:
        return 0

    def size(self) -> int:
        return 0

    def is_valid_avl(self) -> bool:
        return False

if __name__ == "__main__":
    # tests here
    pass