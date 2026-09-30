---
layout: default
title: Homework 1
nav_order: 10
permalink: /hw_1/
---

# CSCI 3212 Homework 1: Advanced Search Trees and Self-Balancing Structures

**Due Date:** Thursday, October 8, 2026 @ 23:59  
**Topics Covered:** Full AVL cascading deletion, Order-Statistic Tree augmentation, Splay Trees, Amortized potential analysis, and empirical workload benchmarks.

> **Note:** Credit will not be given just for answers - show all your work: your reasoning, the steps you took, and how you reached your answer.

---

## Part I: Pen-and-paper exercises (submit as PDF)

### Problem 1: AVL Cascading Deletion Dynamics & Worst-Case Construction
*(Type: Argument / Proof & Construct an Example)*

In an AVL tree of height $h$, inserting a new key requires tracing a path from the root to a leaf, followed by backtracking to restore balance invariants. It is a well-known theorem that at most **one** single or double rotation suffices to restore the AVL property for the entire tree after an insertion. However, for **deletion**, rebalancing can cascade up the ancestor chain, requiring up to $\lfloor h/2 \rfloor = \Theta(\log n)$ rotations.

1. **Proof of Single/Double Rotation Sufficiency on Insertion:**  
   Let $z$ be the deepest unbalanced ancestor after an insertion. Prove that restoring balance at $z$ via a single (LL/RR) or double (LR/RL) rotation restores the height of the subtree rooted at $z$ to its exact pre-insertion height. Explain why this guarantees that no ancestor above $z$ has its balance factor altered, proving that at most one restructuring suffices.
2. **Mechanism of Cascading Deletion:**  
   Explain why restoring balance at an unbalanced node $z$ via rotation after a deletion may decrease the overall height of $z$'s restructured subtree by 1. Detail how this height reduction can propagate an imbalance to $z$'s parent, continuing potentially all the way to the root.
3. **Worst-Case Minimal AVL Tree Construction ($T_5$):**  
   Recall that a minimal Fibonacci-like AVL tree $T_h$ of height $h$ contains the minimum number of nodes for that height:
   $$N(0) = 0,\quad N(1) = 1,\quad N(2) = 2,\quad N(h) = 1 + N(h-1) + N(h-2)$$
   Every internal node in $T_h$ has $|\text{BF}| = 1$.  
   Construct and draw an explicit minimal AVL tree of height 5 ($N(5) = 12$ nodes). Label every node with its key, height, and balance factor. Identify a specific leaf node whose deletion triggers a rebalancing rotation at **every** level along its ancestor path up to the root.
4. **Step-by-Step Deletion Trace:**  
   Trace the rebalancing process after deleting your chosen leaf from $T_5$. For each step:
   - Identify the imbalanced node and its balance factor $\text{BF}$.
   - State whether a single or double rotation is applied (LL, RR, LR, or RL).
   - Draw or clearly describe the tree structure after the rotation.
   - Conclude with the final balanced tree and verify all node balance factors.

---

### Problem 2: The Data Structure Augmentation Theorem & The Non-Augmentability of Depth
*(Type: Argument / Proof)*

The Data Structure Augmentation Theorem (CLRS Theorem 14.1) establishes that if an additional field $f$ stored at node $x$ can be computed using only the information in $x$ and $x$'s immediate children ($x.\text{left}$ and $x.\text{right}$), then $f$ can be maintained during dynamic insertions, deletions, and rotations without asymptotically increasing the $O(\log n)$ running time of standard balanced BST operations.

1. **Order-Statistic Property Formulation:**  
   Show that the order-statistic property $x.\text{size}$ (the total number of nodes in the subtree rooted at $x$) satisfies the conditions of the augmentation theorem by writing its exact recursive equation in terms of $x.\text{left}$ and $x.\text{right}$.
2. **Subtree Size Maintenance During Rotation:**  
   Consider a left rotation `rotate_left(x)` where $y = x.\text{right}$. Using a diagram, write the explicit $O(1)$ update equations for $x.\text{size}$ and $y.\text{size}$ after the rotation in terms of the unchanged subtrees.
3. **Proof of the Non-Augmentability of Absolute Depth:**  
   Suppose a student proposes augmenting each node with its absolute depth from the root: $x.\text{depth}$, where $\text{root}.\text{depth} = 0$ and $u.\text{depth} = u.\text{parent}.\text{depth} + 1$.  
   Prove that augmenting a BST with explicit absolute depth **cannot** be maintained in $O(1)$ time per rotation. Specifically, construct a family of binary search trees where a single rotation at or near the root requires $\Omega(n)$ depth updates.
4. **Logarithmic Alternative:**  
   Explain how to answer depth queries in $O(\log n)$ worst-case time in an AVL tree without storing explicit absolute depth fields at nodes.

---

### Problem 3: Splay Tree Zig-Zig vs. Naive Double Rotation
*(Type: Code Analysis & Construct an Example)*

In a Splay Tree, when a node $x$ is a left child of $p$, and $p$ is a left child of $g$ (the "Zig-Zig" configuration), Sleator and Tarjan's algorithm rotates $p$ around $g$ **first**, and then rotates $x$ around $p$.  
A student suggests simplifying this: *"Why have a separate Zig-Zig rule? Let's just always rotate $x$ around its current parent repeatedly until $x$ reaches the root (i.e. rotate $x$ around $p$, then rotate $x$ around $g$)!"*

1. **Trace on a Linear Degenerate Chain:**  
   Consider an initial tree consisting of a linear chain of $n$ keys: $1, 2, 3, \dots, n$ where each node $i$ is the left child of $i+1$, and $n$ is the root. Key $1$ is accessed.  
   - Describe the resulting tree structure and state its height when key 1 is splayed using true **Sleator-Tarjan Zig-Zig** rotations.
   - Describe the resulting tree structure and state its height when key 1 is moved to the root using **naive repeated single rotations**.
2. **Asymptotic Degeneration Proof:**  
   Suppose the sequence of accesses `access(1)`, `access(2)`, ..., `access(n)` is executed on the initial linear chain.  
   Prove that using naive repeated single rotations requires $\Theta(n^2)$ total work, resulting in an amortized cost of $\Theta(n)$ per operation.
3. **Geometric Halving Intuition:**  
   Explain geometrically why rotating the parent before the child in the Zig-Zig step approximately halves the depth of nearly all nodes along the access path, whereas naive single rotation preserves linear chains.

---

### Problem 4: Amortized Potential Analysis of Splay Trees (The Zig-Zag Case)
*(Type: Recurrence & Amortized Analysis)*

In the Sleator-Tarjan amortized analysis of Splay Trees, for any node $x$ in tree $T$, let $s(x)$ denote the number of nodes in the subtree rooted at $x$, and define the rank of $x$ as:
$$r(x) = \log_2 s(x)$$
The potential function $\Phi(T)$ is the sum of ranks of all nodes:
$$\Phi(T) = \sum_{x \in T} r(x)$$
The amortized cost of a splay step is $\hat{c} = c + \Delta \Phi = c + \Phi(T') - \Phi(T)$, where $c$ is the number of rotations performed and $T'$ is the tree after the step.

1. **Rank Potential Difference:**  
   In a **Zig-Zag** step, $x$ is a right child of $p$, and $p$ is a left child of $g$. The actual cost is $c = 2$ rotations. Identify which nodes change their rank, and express $\Delta \Phi$ in terms of initial ranks $r(x), r(p), r(g)$ and post-rotation ranks $r'(x), r'(p), r'(g)$.
2. **Simplification:**  
   Observe that after the two rotations, $x$ occupies the position formerly occupied by $g$. Justify why $r'(x) = r(g)$, and show that:
   $$\hat{c} = 2 + r'(p) + r'(g) - r(x) - r(p)$$
3. **Initial Rank Inequality:**  
   Show that $r(x) \le r(p)$ and use this to establish:
   $$\hat{c} \le 2 + r'(p) + r'(g) - 2r(x)$$
4. **Log Sum Inequality:**  
   Show that the subtrees of $p$ and $g$ after the Zig-Zag step are disjoint subtrees of $x$'s new tree, so $s'(p) + s'(g) \le s'(x)$. Using the concavity of the logarithm, prove that:
   $$\log_2 s'(p) + \log_2 s'(g) \le 2 \log_2 s'(x) - 2$$
   Conclude that $2 + r'(p) + r'(g) \le 2r'(x)$.
5. **Access Lemma Conclusion:**  
   Combine the results of parts (3) and (4) to prove that the amortized cost of a Zig-Zag step satisfies:
   $$\hat{c}_{\text{Zig-Zag}} \le 2(r'(x) - r(x)) \le 3(r'(x) - r(x))$$

---

### Problem 5: Multiway Trees (B-Trees) vs. Balanced Binary Trees in Disk I/O
*(Type: Asymptotic Order & Concrete System Analysis)*

Database storage engines organize disk-backed indexes using multiway trees (B-Trees) rather than binary search trees to optimize block transfer efficiency across the memory hierarchy.  
Assume the following system specifications:
- Disk page / block size: $B = 4096\text{ bytes}$
- Key size: $32\text{ bytes}$
- Child pointer size: $8\text{ bytes}$
- Record pointer size: $8\text{ bytes}$
- Total indexed records: $N = 10,000,000\ (10^7)$

1. **Optimal B-Tree Order $M$:**  
   An internal node of a B-tree of order $M$ contains at most $M - 1$ keys, $M - 1$ record pointers, and $M$ child pointers. Compute the maximum order $M$ such that an internal node fits within a single $4096$-byte page.
2. **Worst-Case B-Tree Height:**  
   In the worst case (minimally filled nodes), the root has at least 2 children, and every other internal node has at least $\lceil M/2 \rceil$ children. Calculate the maximum possible height $h_{\text{B-Tree}}$ of this B-tree storing $N = 10^7$ records.
3. **AVL Tree Height Comparison:**  
   Calculate the minimum height $h_{\min}$ and maximum height $h_{\max}$ of an AVL tree containing $10^7$ nodes.
4. **Disk I/O and Latency Analysis:**  
   Assuming the root node of each structure is cached in RAM but all other node visits require fetching a block from disk:
   - Calculate the maximum number of disk I/O operations required for a search in the minimally filled B-tree versus the AVL tree.
   - On an enterprise hard drive with an average seek time of $10\text{ ms}$, compute the maximum time needed for a lookup in both structures. Explain why multiway trees are indispensable for external memory storage.

---

### Problem 6: Pseudocode Design: Order-Statistic Range Sum Query
*(Type: Pseudocode Design & Recurrence)*

Consider an Order-Statistic Tree where each node $x$ stores:
- $x.\text{key}$: a real number
- $x.\text{val}$: associated satellite data
- $x.\text{size}$: number of nodes in the subtree rooted at $x$
- $x.\text{sum}$: the sum of all keys in the subtree rooted at $x$

Design an algorithm `range_sum(T, low, high)` that computes the sum of all keys in tree $T$ falling within the closed interval $[low, high]$:
$$\sum_{x \in T,\, low \le x.\text{key} \le high} x.\text{key}$$
The algorithm must operate in **$O(\log n)$ worst-case time**, completely independent of the number of keys located inside the range $[low, high]$.

1. **Pseudocode:**  
   Provide pseudocode using the standard course header format. You may write modular helper procedures (e.g. `prefix_sum(node, k)`).
   ```text
   Method: range_sum (T, low, high)
   Input: An augmented BST root T where each node x has fields x.key, x.left, x.right, x.sum, and interval [low, high] with low <= high

     (... fill in pseudocode here ...)

   Output: The exact sum of all keys in T satisfying low <= key <= high
   ```
2. **Correctness Proof:**  
   Argue why your algorithm correctly aggregates all keys within the interval without omitting or double-counting any elements.
3. **Runtime Recurrence:**  
   Formulate the running time recurrence $T(h)$ in terms of tree height $h$, and prove that the running time is $O(\log n)$ on an AVL tree.

---

## Part II: Programming

In this part, you will implement two self-balancing data structures from scratch and conduct an empirical benchmark comparing their performance under distinct workload distributions.

### Part II (a): Order-Statistic AVL Tree (`ost_avl.py`)

Implement an augmented AVL Tree that maintains subtree sizes and performs full cascading rebalancing on both insertion and deletion.

#### Required File and Signatures

| File | Function or Class | Returns / Signature |
|---|---|---|
| `ost_avl.py` | `AVLNode(key, value=None)` | Node with `key`, `value`, `left`, `right`, `height`, `size` |
| `ost_avl.py` | `AVLOrderStatisticTree()` | Empty AVL tree initialized with `root = None` |
| `ost_avl.py` | `insert(key, value=None)` | `None`: Inserts pair; updates value if key exists; maintains AVL invariants |
| `ost_avl.py` | `delete(key)` | `bool`: Deletes key; returns `True` if found and deleted, `False` otherwise |
| `ost_avl.py` | `find(key)` | `Any`: Returns value for `key`, or `None` if absent |
| `ost_avl.py` | `select(k)` | `Any`: 1-indexed $k$-th smallest key ($1 \le k \le \text{size}$); raises `IndexError` if invalid |
| `ost_avl.py` | `rank(key)` | `int`: 1-indexed count of keys $\le key$ in $O(\log n)$ time |
| `ost_avl.py` | `size()` | `int`: Total number of elements in tree in $O(1)$ time |
| `ost_avl.py` | `is_valid_avl()` | `bool`: Validates BST order, AVL height balance ($|\text{BF}| \le 1$), and size invariants |

#### Behavior Specification & Invariants
- **Heights and Sizes:** An empty subtree (`None`) has height 0 and size 0. A leaf node has height 1 and size 1. For any node $u$:
  $$u.\text{height} = 1 + \max(\text{height}(u.\text{left}), \text{height}(u.\text{right}))$$
  $$u.\text{size} = 1 + \text{size}(u.\text{left}) + \text{size}(u.\text{right})$$
- **Balance Factor:** $\text{BF}(u) = \text{height}(u.\text{left}) - \text{height}(u.\text{right})$. An AVL tree requires $|\text{BF}(u)| \le 1$ for all nodes.
- **Cascading Deletion:** When a node with 2 children is deleted, replace its contents with its in-order successor (the minimum node of the right subtree). As deletion recurses back to the root, every ancestor must recalculate its size, height, and balance factor, performing rotations wherever $|\text{BF}| > 1$.
- **Select & Rank:** `select(k)` and `rank(key)` must use the augmented subtree sizes to run in $O(\log n)$ time without performing linear in-order walks.

#### Worked Example
```python
tree = AVLOrderStatisticTree()
for x in [20, 10, 30, 5, 15]:
    tree.insert(x, x * 10)

assert tree.size() == 5
assert tree.select(1) == 5    # Smallest key
assert tree.select(3) == 15   # 3rd smallest key
assert tree.rank(15) == 3     # Exactly rank 3
assert tree.rank(12) == 2     # Keys <= 12 are {5, 10}

deleted = tree.delete(10)
assert deleted is True
assert tree.size() == 4
assert tree.is_valid_avl() is True
```

#### Your Own Tests
Under `if __name__ == "__main__":` in `ost_avl.py`, include minimum tests verifying:
- Single and double rotation triggers (LL, RR, LR, RL).
- `select(k)` and `rank(key)` boundary conditions ($k = 1$, $k = n$, out-of-bounds `IndexError`).
- Cascading rebalance deletion on multi-level trees.

---

### Part II (b): Self-Adjusting Splay Tree (`splay_tree.py`)

Implement a bottom-up Splay Tree using parent pointers, implementing Sleator-Tarjan Zig, Zig-Zig, and Zig-Zag restructuring.

#### Required File and Signatures

| File | Function or Class | Returns / Signature |
|---|---|---|
| `splay_tree.py` | `SplayNode(key, value=None)` | Node with `key`, `value`, `left`, `right`, `parent` |
| `splay_tree.py` | `SplayTree()` | Empty Splay Tree initialized with `root = None` |
| `splay_tree.py` | `insert(key, value=None)` | `None`: Inserts pair and splays node to root |
| `splay_tree.py` | `search(key)` | `Any`: Returns value or `None`; splays accessed node to root |
| `splay_tree.py` | `delete(key)` | `bool`: Deletes key via splay-split-join; returns `True` if found, `False` otherwise |
| `splay_tree.py` | `to_inorder_keys()` | `List[Any]`: Returns in-order list of keys |
| `splay_tree.py` | `root_key()` | `Any`: Returns key at root, or `None` if empty |
| `splay_tree.py` | `size()` | `int`: Total number of elements in tree |

#### Behavior Specification & Splaying Rules
- **Bottom-Up Splay:** When splaying node $x$ to the root:
  - **Zig:** If $x.\text{parent}$ is the root, rotate $x$ around its parent.
  - **Zig-Zig:** If $x$ and $p = x.\text{parent}$ are both left children (or both right children) of $g = p.\text{parent}$, **rotate $p$ around $g$ first**, then rotate $x$ around $p$.
  - **Zig-Zag:** If $x$ is a right child and $p$ is a left child (or vice versa), rotate $x$ around $p$, then rotate $x$ around $g$.
- **Search Splay:** If `key` is present, splay that node to the root. If `key` is not present, splay the **last non-None node visited** during the search to the root.
- **Delete via Split-Join:** Splay `key` to the root. If `root.key != key`, the key does not exist; return `False`. If present:
  1. Detach `root.left` and `root.right`.
  2. If `root.left` is `None`, `root.right` becomes the new root.
  3. If `root.right` is `None`, `root.left` becomes the new root.
  4. If both subtrees exist, find the maximum element in `root.left` and splay it to the root of the left subtree (its right child will be `None`). Attach `root.right` as the right child of this new root.

#### Worked Example
```python
tree = SplayTree()
tree.insert(10)
tree.insert(20)
assert tree.root_key() == 20   # Newly inserted key becomes root

tree.search(10)
assert tree.root_key() == 10   # Accessed key splayed to root

deleted = tree.delete(10)
assert deleted is True
assert tree.root_key() == 20   # Leftover elements rejoined
assert tree.to_inorder_keys() == [20]
```

#### Your Own Tests
Under `if __name__ == "__main__":` in `splay_tree.py`, include tests verifying:
- Zig, Zig-Zig, and Zig-Zag root placements.
- Splay on search hit and search miss.
- Splay deletion and tree re-assembly.

---

### Part II (c): Empirical Workload Benchmarks (`benchmark.py`)

Evaluate the empirical performance trade-offs between `AVLOrderStatisticTree` and `SplayTree` across three distinct access distributions.

#### Required File and Signatures

| File | Function or Class | Returns / Signature |
|---|---|---|
| `benchmark.py` | `generate_sequential_workload(n)` | `Tuple[List[int], List[int]]`: Returns `(insert_keys, search_keys)` for $1..N$ |
| `benchmark.py` | `generate_uniform_workload(n, rng)` | `Tuple[List[int], List[int]]`: Returns $N$ distinct random keys and $N$ uniform searches |
| `benchmark.py` | `generate_locality_workload(n, rng)` | `Tuple[List[int], List[int]]`: Returns $N$ random keys and $2N$ searches with 80/20 locality |
| `benchmark.py` | `run_workload(tree_class, insert_keys, search_keys)` | `Dict[str, float]`: Measures insert, search, and cumulative runtime in milliseconds |

#### Workload Descriptions
1. **Workload 1 (Sequential):** Insert keys $1, 2, \dots, N$ in sorted order, then search keys $1, 2, \dots, N$ in sorted order.
2. **Workload 2 (Uniform Random):** Insert $N$ distinct random keys, then perform $N$ searches for keys chosen uniformly at random from the inserted set.
3. **Workload 3 (80/20 Locality):** Insert $N$ distinct random keys. Then perform $2N$ searches where 80% of searches target the top 20% of keys (hot set) and 20% target the remaining 80% of keys (cold set).

#### Experiment Deliverable
1. Evaluate across tree sizes $N \in [500, 1000, 2000, 4000]$.
2. Use `time.perf_counter()` to record millisecond timings.
3. Print an aligned summary table reporting insertion time, search time, and cumulative time for both trees.
4. Generate and save a 3-panel comparison figure to `workload_benchmark.png` plotting cumulative time (ms) versus tree size $N$. The script should complete execution in under 30 seconds.

---

## Provided Test Harness

A self-contained test checker is provided in `hw_checks.py`. Run:

```bash
python3 hw_checks.py
```

To run checks against a specific directory or print a performance comparison table:
```bash
python3 hw_checks.py . --perf
```

> `hw_checks.py` helps with testing, not debugging - it tells you a check failed, not why. Use your own unit tests in each file to diagnose and fix bugs.

---

## Submission

Submit a single `.zip` file containing:
1. `theory_answers.pdf`: Your written solutions, proofs, hand traces, and pseudocode for Part I.
2. `ost_avl.py`: Your complete Order-Statistic AVL Tree implementation.
3. `splay_tree.py`: Your complete Splay Tree implementation.
4. `benchmark.py`: Your benchmark generation and plotting script.
5. `workload_benchmark.png`: Your generated 3-panel benchmark plot.

Code will be evaluated on correctness, adherence to specified interfaces, invariant maintenance, and documentation. All files must run cleanly under Python 3.8+ with zero third-party dependencies beyond standard `matplotlib`.
