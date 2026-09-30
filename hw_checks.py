"""Provided test checks for CSCI 3212 Homework 1.

No third-party packages required for checks.
Usage:
    python3 hw_checks.py [optional_directory_to_test] [--perf]
"""

import sys
import os
import random
import time
from typing import List, Tuple, Callable


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def run_checks(cases: List[Tuple[str, Callable[[], None]]]) -> int:
    """Run (name, zero-arg callable) pairs; return process exit status.

    NotImplementedError -> [TODO]; any other exception -> [FAIL].
    """
    failed = 0
    passed = 0

    for name, test in cases:
        try:
            test()
            passed += 1
            print(f"[PASS] {name}")
        except NotImplementedError as error:
            failed += 1
            print(f"[TODO] {name}: {error}")
        except Exception as error:
            failed += 1
            print(f"[FAIL] {name}: {type(error).__name__}: {error}")

    total = len(cases)
    print(f"\n{passed}/{total} checks passed")
    return 1 if failed else 0


# --- Dynamic Import Helpers with [TODO] Reporting ---

def import_ost_module():
    try:
        import ost_avl
    except ImportError as e:
        raise NotImplementedError(f"Create ost_avl.py: {e}")
    if not hasattr(ost_avl, "AVLOrderStatisticTree"):
        raise NotImplementedError("Create ost_avl.py with class AVLOrderStatisticTree")
    return ost_avl


def import_splay_module():
    try:
        import splay_tree
    except ImportError as e:
        raise NotImplementedError(f"Create splay_tree.py: {e}")
    if not hasattr(splay_tree, "SplayTree"):
        raise NotImplementedError("Create splay_tree.py with class SplayTree")
    return splay_tree


def import_benchmark_module():
    try:
        import benchmark
    except ImportError as e:
        raise NotImplementedError(f"Create benchmark.py: {e}")
    return benchmark


# --- Test Cases ---

def test_ost_basic_operations():
    ost = import_ost_module()
    tree = ost.AVLOrderStatisticTree()

    require(tree.size() == 0, "Initial tree size must be 0")
    require(tree.find(10) is None, "Search on empty tree must return None")

    # Insert unique keys
    for k in [20, 10, 30, 5, 15]:
        tree.insert(k, f"val-{k}")

    require(tree.size() == 5, "Size must match number of inserted unique keys")
    require(tree.find(20) == "val-20", "Find returned incorrect value")
    require(tree.find(15) == "val-15", "Find returned incorrect value")
    require(tree.find(99) is None, "Find returned non-None for absent key")

    # Value update on duplicate key
    tree.insert(20, "val-20-updated")
    require(tree.size() == 5, "Duplicate key insert must not increase size")
    require(tree.find(20) == "val-20-updated", "Duplicate key insert must update value")

    if hasattr(tree, "is_valid_avl"):
        require(tree.is_valid_avl(), "Tree violated AVL or size invariants after basic inserts")


def test_ost_sorted_insertion_balance():
    ost = import_ost_module()
    tree = ost.AVLOrderStatisticTree()

    # Sequential insertion must remain strictly balanced
    n = 63
    for k in range(1, n + 1):
        tree.insert(k, k * 10)

    require(tree.size() == n, "Size invariant violated during sequential inserts")
    if hasattr(tree, "is_valid_avl"):
        require(tree.is_valid_avl(), "Sequential inserts caused AVL balance violation")

    # Verify height is bounded by AVL logarithmic height: height <= 1.44 * log2(n + 2)
    if hasattr(tree, "root") and tree.root is not None:
        require(tree.root.height <= 8, "Tree height exceeded logarithmic AVL bound")


def test_ost_order_statistics():
    ost = import_ost_module()
    tree = ost.AVLOrderStatisticTree()
    rng = random.Random(3212)

    values = rng.sample(range(1, 1000), 100)
    sorted_values = sorted(values)

    for v in values:
        tree.insert(v, v)

    require(tree.size() == 100, "Size mismatch after insertions")

    # Check select(k) for all valid 1-indexed ranks
    for k in range(1, 101):
        expected_key = sorted_values[k - 1]
        got_key = tree.select(k)
        require(got_key == expected_key, f"select({k}) returned incorrect key")

    # Check select(k) out of bounds raises IndexError
    for bad_k in [0, -1, 101, 200]:
        raised = False
        try:
            tree.select(bad_k)
        except IndexError:
            raised = True
        require(raised, f"select({bad_k}) must raise IndexError for out-of-bounds rank")

    # Check rank(key) for all present keys
    for idx, key in enumerate(sorted_values, start=1):
        got_rank = tree.rank(key)
        require(got_rank == idx, f"rank({key}) returned incorrect 1-indexed position")

    # Check rank(key) for boundary and non-present keys
    require(tree.rank(0) == 0, "rank() for key smaller than all elements must return 0")
    require(tree.rank(1001) == 100, "rank() for key larger than all elements must return total size")


def test_ost_cascading_deletion():
    ost = import_ost_module()
    tree = ost.AVLOrderStatisticTree()

    # Construct a tree where leaf deletion triggers cascading rebalancing
    # Insert specific keys
    keys = [50, 25, 75, 15, 35, 65, 85, 10, 20, 30, 40, 60, 70, 80, 90, 5]
    for k in keys:
        tree.insert(k, k)

    require(tree.size() == len(keys), "Tree size incorrect after build")
    if hasattr(tree, "is_valid_avl"):
        require(tree.is_valid_avl(), "Initial tree before deletion violated AVL invariant")

    # Delete leaf node that forces multi-level balance propagation
    deleted = tree.delete(5)
    require(deleted is True, "Delete returned False for present key")
    require(tree.find(5) is None, "Deleted key still found in tree")
    require(tree.size() == len(keys) - 1, "Size not decremented after deletion")
    if hasattr(tree, "is_valid_avl"):
        require(tree.is_valid_avl(), "Tree balance or size violated after leaf deletion")

    # Delete 2-child root node
    deleted_root = tree.delete(50)
    require(deleted_root is True, "Delete returned False for root key")
    require(tree.find(50) is None, "Deleted root still found in tree")
    if hasattr(tree, "is_valid_avl"):
        require(tree.is_valid_avl(), "Tree balance or size violated after 2-child root deletion")

    # Delete remaining keys in arbitrary order
    remaining_keys = [25, 75, 15, 35, 65, 85, 10, 20, 30, 40, 60, 70, 80, 90]
    for k in remaining_keys:
        tree.delete(k)
        if hasattr(tree, "is_valid_avl"):
            require(tree.is_valid_avl(), f"Tree balance violated after deleting key {k}")

    require(tree.size() == 0, "Tree size must be 0 after all keys deleted")


def test_splay_insert_and_root():
    splay = import_splay_module()
    tree = splay.SplayTree()

    require(tree.size() == 0, "Initial splay tree size must be 0")
    require(tree.root_key() is None, "Initial splay root_key must be None")

    # Every inserted key must become root immediately
    for k in [10, 20, 5, 15, 30]:
        tree.insert(k, f"val-{k}")
        require(tree.root_key() == k, "Newly inserted key must be splayed to root")

    require(tree.size() == 5, "Splay tree size mismatch after inserts")
    inorder = tree.to_inorder_keys()
    require(inorder == [5, 10, 15, 20, 30], "In-order traversal order corrupted after splaying")


def test_splay_search_and_splay():
    splay = import_splay_module()
    tree = splay.SplayTree()

    keys = [10, 20, 30, 40, 50]
    for k in keys:
        tree.insert(k, k * 2)

    # Search for an existing key; it must become root
    val = tree.search(20)
    require(val == 40, "Search returned incorrect value")
    require(tree.root_key() == 20, "Accessed key must be splayed to root on search")

    # Search for non-existent key; the last accessed node must become root
    val_missing = tree.search(25)
    require(val_missing is None, "Search for non-existent key must return None")
    # 25 would fall between 20 and 30, so either 20 or 30 must be splayed to root
    require(tree.root_key() in [20, 30], "Last visited node must be splayed to root on miss")


def test_splay_rotations_mechanics():
    splay = import_splay_module()

    # Zig-Zig Test: Left-Left chain
    tree_ll = splay.SplayTree()
    # Insert 30, 20, 10
    tree_ll.insert(30)
    tree_ll.insert(20)
    tree_ll.insert(10)
    # Search for 30 (deepest node)
    tree_ll.search(30)
    require(tree_ll.root_key() == 30, "Zig-Zig failed to bring accessed target to root")
    require(tree_ll.to_inorder_keys() == [10, 20, 30], "BST order lost during Zig-Zig")

    # Zig-Zag Test: Left-Right
    tree_lr = splay.SplayTree()
    tree_lr.insert(30)
    tree_lr.insert(10)
    tree_lr.insert(20)
    tree_lr.search(10)
    require(tree_lr.root_key() == 10, "Zig-Zag failed to bring accessed target to root")
    require(tree_lr.to_inorder_keys() == [10, 20, 30], "BST order lost during Zig-Zag")


def test_splay_deletion():
    splay = import_splay_module()
    tree = splay.SplayTree()

    keys = [10, 5, 15, 2, 7, 12, 17]
    for k in keys:
        tree.insert(k, k)

    # Delete non-existent key
    deleted = tree.delete(99)
    require(deleted is False, "Delete must return False for missing key")
    require(tree.size() == 7, "Size modified on failed delete")

    # Delete root
    current_root = tree.root_key()
    deleted_root = tree.delete(current_root)
    require(deleted_root is True, "Delete must return True for present root")
    require(tree.size() == 6, "Size not decremented on successful delete")
    require(current_root not in tree.to_inorder_keys(), "Deleted key still present in tree")

    # Delete all remaining keys
    remaining = tree.to_inorder_keys()
    for k in remaining:
        tree.delete(k)

    require(tree.size() == 0, "Tree size must be 0 after deleting all keys")
    require(tree.root_key() is None, "Root must be None after deleting all keys")


def test_benchmark_structure():
    bench = import_benchmark_module()
    require(hasattr(bench, "generate_sequential_workload"), "benchmark.py missing generate_sequential_workload")
    require(hasattr(bench, "generate_uniform_workload"), "benchmark.py missing generate_uniform_workload")
    require(hasattr(bench, "generate_locality_workload"), "benchmark.py missing generate_locality_workload")
    require(hasattr(bench, "run_workload"), "benchmark.py missing run_workload")


def run_perf_benchmark():
    """Optional performance comparison table."""
    ost = import_ost_module()
    splay = import_splay_module()

    print("\n--- Running Quick Performance Check (N=2000) ---")
    sizes = [500, 1000, 2000]
    print(f"{'N':>6} | {'AVL Ins (ms)':>12} | {'AVL Srch (ms)':>13} | {'Splay Ins (ms)':>14} | {'Splay Srch (ms)':>15}")
    print("-" * 70)

    for n in sizes:
        rng = random.Random(3212 + n)
        keys = rng.sample(range(1, 10 * n + 1), n)
        queries = [rng.choice(keys) for _ in range(n)]

        # AVL
        t_avl = ost.AVLOrderStatisticTree()
        t0 = time.perf_counter()
        for k in keys:
            t_avl.insert(k, k)
        t_avl_ins = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        for q in queries:
            t_avl.find(q)
        t_avl_srch = (time.perf_counter() - t0) * 1000

        # Splay
        t_sp = splay.SplayTree()
        t0 = time.perf_counter()
        for k in keys:
            t_sp.insert(k, k)
        t_sp_ins = (time.perf_counter() - t0) * 1000

        t0 = time.perf_counter()
        for q in queries:
            t_sp.search(q)
        t_sp_srch = (time.perf_counter() - t0) * 1000

        print(f"{n:>6} | {t_avl_ins:>12.2f} | {t_avl_srch:>13.2f} | {t_sp_ins:>14.2f} | {t_sp_srch:>15.2f}")


def main():
    # Parse directory argument
    target_dir = os.path.dirname(os.path.abspath(__file__))
    perf_mode = False

    args = sys.argv[1:]
    if "--perf" in args:
        perf_mode = True
        args.remove("--perf")

    if args:
        target_dir = os.path.abspath(args[0])

    sys.path.insert(0, target_dir)

    cases = [
        ("AVLOrderStatisticTree: Basic insertion, search, update", test_ost_basic_operations),
        ("AVLOrderStatisticTree: Sorted insertion logarithmic balance", test_ost_sorted_insertion_balance),
        ("AVLOrderStatisticTree: Order-statistic select & rank queries", test_ost_order_statistics),
        ("AVLOrderStatisticTree: Multi-level cascading deletion", test_ost_cascading_deletion),
        ("SplayTree: Insertion and root splaying invariant", test_splay_insert_and_root),
        ("SplayTree: Search and access-path splaying", test_splay_search_and_splay),
        ("SplayTree: Zig-Zig and Zig-Zag mechanics", test_splay_rotations_mechanics),
        ("SplayTree: Delete via splay-split-join", test_splay_deletion),
        ("Workload Benchmark: Required generator and runner functions", test_benchmark_structure),
    ]

    print(f"Running Homework 1 checks against: {target_dir}\n")
    status = run_checks(cases)

    if perf_mode and status == 0:
        run_perf_benchmark()

    sys.exit(status)


if __name__ == "__main__":
    main()
