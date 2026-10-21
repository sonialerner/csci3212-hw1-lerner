import random
import time
from typing import Any, Callable, Dict, List, Tuple, Type

import matplotlib.pyplot as plt

from splay_tree import SplayTree


def generate_sequential_workload(n: int) -> Tuple[List[int], List[int]]:
    # Insert and search keys in ascending order from 1 through n.
    keys = list(range(1, n + 1))
    return keys.copy(), keys.copy()


def generate_uniform_workload(
    n: int, rng: random.Random
) -> Tuple[List[int], List[int]]:
    # Sample n distinct keys, then draw n searches uniformly from those keys.
    insert_keys = rng.sample(range(1, 10 * n + 1), n)
    search_keys = [rng.choice(insert_keys) for _ in range(n)]
    return insert_keys, search_keys


def generate_locality_workload(
    n: int, rng: random.Random
) -> Tuple[List[int], List[int]]:
    # Insert n distinct random keys and designate the largest 20% as the hot set.
    insert_keys = rng.sample(range(1, 10 * n + 1), n)
    sorted_keys = sorted(insert_keys)
    hot_count = max(1, (n + 4) // 5)
    hot_keys = sorted_keys[-hot_count:]
    cold_keys = sorted_keys[:-hot_count]

    # Create 2n searches: 80% from the hot set and 20% from the cold set.
    total_searches = 2 * n
    hot_search_count = round(0.8 * total_searches)
    cold_search_count = total_searches - hot_search_count

    search_keys = [
        rng.choice(hot_keys) for _ in range(hot_search_count)
    ]

    # Handle n=1, where there is no cold set, while still returning 2n searches.
    if cold_keys:
        search_keys.extend(
            rng.choice(cold_keys) for _ in range(cold_search_count)
        )
    else:
        search_keys.extend(
            rng.choice(hot_keys) for _ in range(cold_search_count)
        )

    rng.shuffle(search_keys)
    return insert_keys, search_keys


def run_workload(
    tree_class: Type[Any],
    insert_keys: List[int],
    search_keys: List[int],
) -> Dict[str, float]:
    # Time construction by inserting all keys, then time the search sequence.
    tree = tree_class()

    start = time.perf_counter()
    for key in insert_keys:
        tree.insert(key, key)
    insert_ms = (time.perf_counter() - start) * 1000.0

    start = time.perf_counter()
    for key in search_keys:
        tree.search(key)
    search_ms = (time.perf_counter() - start) * 1000.0

    return {
        "insert_ms": insert_ms,
        "search_ms": search_ms,
        "cumulative_ms": insert_ms + search_ms,
    }


class BinarySearchTreeNode:
    # Basic node used by the unbalanced BST comparison implementation.
    def __init__(self, key: int, value: Any = None):
        self.key = key
        self.value = value
        self.left: BinarySearchTreeNode | None = None
        self.right: BinarySearchTreeNode | None = None


class BinarySearchTree:
    # Iterative ordinary BST; iterative operations avoid recursion-depth failures.
    def __init__(self):
        self.root: BinarySearchTreeNode | None = None

    def insert(self, key: int, value: Any = None) -> None:
        # Insert a new key or update the value of an existing key.
        if self.root is None:
            self.root = BinarySearchTreeNode(key, value)
            return

        current = self.root
        while True:
            if key == current.key:
                current.value = value
                return
            if key < current.key:
                if current.left is None:
                    current.left = BinarySearchTreeNode(key, value)
                    return
                current = current.left
            else:
                if current.right is None:
                    current.right = BinarySearchTreeNode(key, value)
                    return
                current = current.right

    def search(self, key: int) -> Any:
        # Return the stored value or None when the key is absent.
        current = self.root
        while current is not None:
            if key == current.key:
                return current.value
            if key < current.key:
                current = current.left
            else:
                current = current.right
        return None


def print_summary(results: Dict[str, Dict[int, Dict[str, Dict[str, float]]]]) -> None:
    # Print one aligned row per workload, size, and tree implementation.
    print(
        f"{'Workload':<22} {'N':>6} {'Tree':<18} "
        f"{'Insert (ms)':>14} {'Search (ms)':>14} {'Cumulative (ms)':>18}"
    )
    print("-" * 96)

    for workload_name, sizes in results.items():
        for n, tree_results in sizes.items():
            for tree_name, metrics in tree_results.items():
                print(
                    f"{workload_name:<22} {n:>6} {tree_name:<18} "
                    f"{metrics['insert_ms']:>14.3f} "
                    f"{metrics['search_ms']:>14.3f} "
                    f"{metrics['cumulative_ms']:>18.3f}"
                )


def save_comparison_figure(
    results: Dict[str, Dict[int, Dict[str, Dict[str, float]]]],
    output_path: str = "workload_benchmark.png",
) -> None:
    # Plot cumulative runtime against N in one panel per workload.
    workload_names = list(results.keys())
    tree_names = ["Splay Tree", "Binary Search Tree"]

    fig, axes = plt.subplots(1, 3, figsize=(16, 4.8))

    for axis, workload_name in zip(axes, workload_names):
        sizes = sorted(results[workload_name].keys())

        for tree_name in tree_names:
            cumulative_times = [
                results[workload_name][n][tree_name]["cumulative_ms"]
                for n in sizes
            ]
            axis.plot(
                sizes,
                cumulative_times,
                marker="o",
                linewidth=2,
                label=tree_name,
            )

        axis.set_title(workload_name)
        axis.set_xlabel("Tree size N")
        axis.set_ylabel("Cumulative time (ms)")
        axis.grid(True, alpha=0.3)
        axis.legend()

    fig.suptitle("Splay Tree vs. Binary Search Tree Workload Benchmarks")
    fig.tight_layout()
    fig.savefig(output_path, dpi=200, bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    # Use one seeded generator so the benchmark is reproducible.
    rng = random.Random(42)
    sizes = [500, 1000, 2000, 4000]

    tree_classes = {
        "Splay Tree": SplayTree,
        "Binary Search Tree": BinarySearchTree,
    }

    workload_generators: List[
        Tuple[str, Callable[..., Tuple[List[int], List[int]]]]
    ] = [
        ("Sequential", generate_sequential_workload),
        ("Uniform Random", generate_uniform_workload),
        ("80/20 Locality", generate_locality_workload),
    ]

    results: Dict[str, Dict[int, Dict[str, Dict[str, float]]]] = {}

    for workload_name, generator in workload_generators:
        results[workload_name] = {}

        for n in sizes:
            if workload_name == "Sequential":
                insert_keys, search_keys = generator(n)
            else:
                insert_keys, search_keys = generator(n, rng)

            results[workload_name][n] = {}

            for tree_name, tree_class in tree_classes.items():
                results[workload_name][n][tree_name] = run_workload(
                    tree_class, insert_keys, search_keys
                )

    print_summary(results)
    save_comparison_figure(results)
    print("\nSaved comparison figure to workload_benchmark.png")


if __name__ == "__main__":
    main()
