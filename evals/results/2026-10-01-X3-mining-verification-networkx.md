# X3 harder-task band — NetworkX mining verification

Mined 2026-10-01 (EDT) by worker A2. Local git/pytest only; no model runs.

## Setup

- The A1 partial clone was absent: `~/workspace/x3-mining/a/` was empty on
  arrival. Fresh full clone of https://github.com/networkx/networkx made at
  `~/workspace/x3-mining/a/src-networkx`; `git fsck` clean (75,225 objects,
  single pack).
- Venv at `~/workspace/x3-mining/a/venv`: pytest 9.1.1, numpy 2.5.3,
  scipy 1.18.1. NetworkX imported from the worktree under test (no installed
  networkx in the venv).

## Method (per candidate)

1. `git worktree add` the parent commit (`fix^`) and the fix commit.
2. In the parent worktree only, overlay the fix commit's test files
   (`git show fix:<path>` for each file under `tests/` in the fix diff).
3. Run the grading nodes in the parent worktree → must FAIL.
4. Run the same nodes in the fix worktree → must PASS.
5. A candidate whose oracle does not discriminate is dropped, no exceptions.

---

## nx-t5-betweenness-k-scaling — ACCEPTED

- Parent: `4ec9e3abdc8330992f05a289482e16c38dbae01b`
- Fix: `a802a27f50623ba5669420bb2edeaafd30242323` — "BUG/MAINT: fix edge
  betweenness centrality scaling when `k<N` and merge all b.c. rescale helper
  functions (#8256)"
- Fix diff stat:
  ```
  networkx/algorithms/centrality/betweenness.py             | 42 ++++++-----------
  networkx/algorithms/centrality/betweenness_subset.py      | 52 +++++-----------------
  networkx/algorithms/centrality/tests/test_betweenness_centrality.py        | 20 +++++++++
  networkx/algorithms/centrality/tests/test_betweenness_centrality_subset.py | 14 +++++++
  4 files changed, 58 insertions(+), 70 deletions(-)
  ```
- Why harder than T1–T4: three separate rescale helpers across two modules
  encode four normalization variants (node/edge × full/subset); the edge
  variant never receives `k`, so the n/k sampling correction is structurally
  absent, not merely miscomputed. Fixing it requires deriving the unified
  scale from the (s, t)-pair counting argument; the obvious patch (multiply
  by n/k in the old helper) double-counts when `normalized=True`.
- Grading nodes:
  - `networkx/algorithms/centrality/tests/test_betweenness_centrality.py::TestEdgeBetweennessCentrality::test_edge_betweenness_k`
  - `networkx/algorithms/centrality/tests/test_betweenness_centrality_subset.py::test_equivalence_non_subset`
- Oracle at parent (FAIL, as required):
  ```
  >       assert eb == {(0, 1): 9 / 4, (1, 2): 9 / 4}
  E       assert {(0, 1): 1.5, (1, 2): 1.5} == {(0, 1): 2.25, (1, 2): 2.25}
  FAILED networkx/algorithms/centrality/tests/test_betweenness_centrality.py::TestEdgeBetweennessCentrality::test_edge_betweenness_k
  1 failed, 1 passed in 0.58s
  ```
  (test_equivalence_non_subset passes at parent too — the subset test uses a
  DiGraph, where the old scales coincide; it is kept as a regression guard.
  The discriminating node is test_edge_betweenness_k.)
- Oracle at fix (PASS):
  ```
  2 passed in 0.97s
  ```

## nx-t6-is-aperiodic-strong-connectivity — ACCEPTED

- Parent: `ffaa9ef8d51eceddee4ec47f887e476fc42b89bb`
- Fix: `86e143dd83f350f7d6684bc81750573dfc309ea7` — "A minimal fix for
  `is_aperiodic` (#8029)"
- Fix diff stat:
  ```
  networkx/algorithms/dag.py            | 82 ++++++++++++++++++++++++++++-------
  networkx/algorithms/tests/test_dag.py | 40 +++++++++--------
  2 files changed, 87 insertions(+), 35 deletions(-)
  ```
  (Most of the dag.py delta is docstring; the behavioral change is the
  strong-connectivity gate plus removal of the recursion over unvisited
  subgraphs.)
- Why harder than T1–T4: nothing crashes; the BFS-gcd routine runs fine on
  disconnected inputs and its recursion over unvisited subgraphs looks like
  due diligence. The fix requires the mathematical invariant — period is
  undefined without strong connectivity — so the correct move is to refuse
  (raise), not to repair the recursion. The tempting fix (keep recursing,
  combine gcds across components) is the wrong one.
- Grading nodes:
  - `networkx/algorithms/tests/test_dag.py::test_is_aperiodic_null_graph_raises`
  - `networkx/algorithms/tests/test_dag.py::test_is_aperiodic_disconnected_raises`
  - `networkx/algorithms/tests/test_dag.py::test_is_aperiodic_weakly_connected_raises`
  - `networkx/algorithms/tests/test_dag.py::test_is_aperiodic_single_node`
  - `networkx/algorithms/tests/test_dag.py::test_is_aperiodic_selfloop`
  - `networkx/algorithms/tests/test_dag.py::test_is_aperiodic_bipartite`
- Oracle at parent (FAIL, as required):
  ```
  E       Failed: DID NOT RAISE NetworkXError
  FAILED networkx/algorithms/tests/test_dag.py::test_is_aperiodic_disconnected_raises
  FAILED networkx/algorithms/tests/test_dag.py::test_is_aperiodic_weakly_connected_raises
  2 failed, 4 passed in 1.98s
  ```
- Oracle at fix (PASS):
  ```
  6 passed in 0.77s
  ```

## nx-t7-network-simplex-faux-inf — ACCEPTED

- Parent: `f87c3611d12510c495bd471e13f7c6978c4c5d02`
- Fix: `7768b9273e2f039bd91ded6cc020046a4b9ff6c2` — "Fix handling of
  faux_infinite values in network_simplex (#7796)"
- Fix diff stat:
  ```
  networkx/algorithms/flow/networksimplex.py         |  10 +-
  networkx/algorithms/flow/tests/test_networksimplex.py | 125 +++++++++++++++++++--
  2 files changed, 119 insertions(+), 16 deletions(-)
  ```
- Why harder than T1–T4: the symptom (spurious "negative cycle with infinite
  capacity") points at the unboundedness detector, but the cause is the
  sentinel magnitude: `faux_inf` must dominate every legitimate flow value,
  which scales with the *sum* of demands; the old code aggregated the largest
  *single* demand. Not a typo — the aggregation itself is wrong — and the
  failing instance is the all-small-values one, so magnitude intuition
  misleads. Locating it requires tracing how `faux_inf` is consumed by two
  independent checks in the simplex core.
- Grading nodes:
  - `networkx/algorithms/flow/tests/test_networksimplex.py::test_network_simplex_large_capacities` (8 parametrized cases)
  - `networkx/algorithms/flow/tests/test_networksimplex.py::test_network_simplex_unbounded_flow`
- Oracle at parent (FAIL, as required):
  ```
  E           networkx.exception.NetworkXUnbounded: negative cycle with infinite capacity found
  FAILED networkx/algorithms/flow/tests/test_networksimplex.py::test_network_simplex_large_capacities[False-False-False]
  1 failed, 8 passed in 0.97s
  ```
- Oracle at fix (PASS):
  ```
  9 passed in 0.99s
  ```

## nx-t8-diameter-usebounds-weighted — ACCEPTED

- Parent: `707d19536666517a1d9a6d4610a146e553010273`
- Fix: `c732e43461f2c638178e86272a32f92424b5ab92` — "Fixing nx.diameter
  inconsistent results with usebounds=True (#7954)"
- Fix diff stat:
  ```
  networkx/algorithms/distance_measures.py              |  6 ++---
  networkx/algorithms/tests/test_distance_measures.py   | 30 ++++++++++++++++++++++
  2 files changed, 33 insertions(+), 3 deletions(-)
  ```
- Why harder than T1–T4: `_extrema_bounding`'s pruning is only sound if the
  initial eccentricity upper bound dominates every true eccentricity; the
  node count N silently stops being a valid bound once edges carry weights
  (weighted eccentricities exceed N), so candidates are pruned before their
  true distances are known. The symptom — diameter disagreeing with itself —
  gives no location hint; the candidate set, the bound updates, and the
  eccentricity computation each look locally correct.
- Grading nodes:
  - `networkx/algorithms/tests/test_distance_measures.py::TestDistance::test_use_bounds_on_off_consistency` (500 parametrized cases: 10 seeds × 10 sizes × 5 densities, each checking diameter/radius/periphery/center, unweighted and at three weight scales)
- Oracle at parent (FAIL, as required — all 500 cases fail; representative
  assertion):
  ```
  E               AssertionError: assert 13 == 10
  E                +  where 13 = diameter(G, weight='w')
  E                +  and   10 = diameter(G, weight='w', usebounds=True)
  500 failed in 26.75s
  ```
- Oracle at fix (PASS):
  ```
  500 passed in 13.11s
  ```

---

## Verified spare (oracle discriminates; not packaged — 4 slots filled)

**optimize_edit_paths self-loops** — fix `9c17836f784a69bcec9af6d7b1203aa5505c0de5`,
parent `6b57b27787ce02b0798aabbed506ced64de840fb`. Diff: similarity.py 5 lines,
test_similarity.py 14 lines. The first-node edge-matching guard fires even
when no substitution is possible, so self-loops on the first node are
auto-deleted and `graph_edit_distance` undercounts.
Nodes: `TestSimilarity::test_one_node_one_loop_and_empty_graph`,
`TestSimilarity::test_one_node_two_loops_and_empty_graph`,
`TestSimilarity::test_two_directed_loops`.
Parent: `2 failed, 1 passed in 3.38s` (e.g. `assert 1.0 == 3`).
Fix: `3 passed in 2.92s`. Smallest fix of the five verified; held as spare.

## Rejected during mining

| Commit | Subject | Reason |
|---|---|---|
| `3284e6a870…` | Fix `min_weight_matching` (#8062) | Library change is docstring-only; behavior identical at parent → oracle cannot discriminate. |
| `4a0a6754a5…` | directed_edge_swap test rewrite (#6426) | Library change is one docstring line; oracle cannot discriminate. |
| `772c8dcf1f…` | Floyd–Warshall self positive loop (#8425) | One-line library fix (2-line diff incl. test) → dropped per one-line rule. |
| `fe5e667f68…` | scipy 1d sparse indexing (#7541) | No test changes in the commit → no oracle. |
| `41440a90c4…` | asadpour_atsp `if` condition (#7753) | Off-by-one guard plus a 2-node special case; edge-case, not materially harder. |
| `5872457bf3…` | minimum_spanning_arborescence regression (#7280) | Missing-attribute robustness (`d[attr]` → `d.get(attr, default)`); discoverable directly from the KeyError traceback. |
| `1515862e8e…` | FISTA nonstandard node labels (#8332) | Single-expression fix (heap keyed by position instead of node). |
| `5cfb44f7af…` | Raise on directed graphs in `find_cliques_recursive` (#8211) | Simple input guard. |
