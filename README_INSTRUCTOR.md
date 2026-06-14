# Instructor Reference Guide: Panini Logistics Workshop

## Overview

This folder contains a **complete reference implementation** of the Panini Logistics search algorithms workshop. It serves as:

1. **Correctness baseline** for verifying student submissions
2. **Performance benchmark** for evaluating efficiency
3. **Detailed analysis** of algorithm behavior on the Colombian road network
4. **Grading rubric** with quantitative acceptance criteria

---

## Files in This Reference

### Code Implementation
- **`algorithms/search.py`** - Complete, working implementations of:
  - `depthFirstSearch()` (DFS)
  - `breadthFirstSearch()` (BFS)
  - `uniformCostSearch()` (UCS)
  - `aStarSearch()` (A*)
  - `depthLimitedSearch()` (DLS)
  - `iterativeDeepeningSearch()` (IDS)

- **`algorithms/heuristics.py`** - Complete, working implementations of:
  - `straightLineHeuristic()` - Haversine geodesic for single-delivery
  - `multiDeliveryHeuristic()` - MST-based for multi-delivery TSP
  - `straightLineMultiDeliveryHeuristic()` - Faster geodesic-only variant

### Reference Documents
- **`BASELINE_ANALYSIS.md`** - Comprehensive analysis including:
  - Correctness verification (A* vs UCS)
  - Complexity analysis (time, space, completeness, optimality)
  - Heuristic admissibility proofs
  - Performance benchmarks
  - Recommended algorithm-problem pairings
  - Grading rubric with acceptance criteria

- **`BASELINE_RESULTS.json`** - Execution results from all test cases:
  - 11 test scenarios covering all 5 points
  - Metrics: cost, actions, nodes expanded, frontier size, execution time
  - All tests pass with 100% success rate

- **`BASELINE_TESTS.py`** - Automated test suite:
  - Runs all 11 baseline test cases
  - Parses output and generates JSON report
  - Provides summary statistics
  - Useful for validating student implementations

---

## Quick Start: Using This Reference

### 1. Verify Student Submissions

Run your grading against the baseline:

```bash
# Run baseline tests (should take ~3-5 minutes total)
python3 BASELINE_TESTS.py

# Compare student results to BASELINE_RESULTS.json
# Key checks:
# - Are costs identical? (tolerance: ±0.01 km)
# - Are node expansions similar? (tolerance: ±20%)
# - Do execution times scale reasonably?
```

### 2. Check Specific Algorithms

Test individual implementations:

```bash
# Point 1: DFS vs BFS
python3 main.py --problem stops --algorithm dfs --start n1037511 --goal n39739
python3 main.py --problem stops --algorithm bfs --start n1037511 --goal n39739

# Point 2: UCS (minimum distance)
python3 main.py --instance single_bogota_medellin

# Point 3: A* (should match UCS cost but expand fewer nodes)
python3 main.py --instance single_bogota_cartagena_astar
python3 main.py --problem single --algorithm ucs --start n1037511 --goal n1006018

# Point 4: IDS (iterative deepening)
python3 main.py --instance ids_local_depth

# Point 5: Multi-delivery (TSP-like)
python3 main.py --instance multi_andes_caribe
python3 main.py --instance multi_national_challenge
```

### 3. Common Student Errors to Check

| Error | How to Detect | Reference Metric |
|-------|--------------|------------------|
| Forgot `_remember_frontier()` | Frontier size always 0 | BFS should show ~550 |
| Missing visited set | Infinite loops or wrong costs | DFS should show 32,511 expansions |
| Wrong DLS depth counting | IDS finds wrong depth | IDS should find depth=3 for local test |
| Non-admissible heuristic | A* returns worse cost than UCS | Both should = 911.37 km |
| Heuristic not consistent | Inefficient exploration | A* should expand fewer than UCS |
| Multi-delivery bug | Visits same location twice | Route should be valid path |

---

## Baseline Metrics Reference

### Point 1: DFS & BFS (FewestStops)

**Test Case**: Bogotá (n1037511) → Medellín (n39739)

| Metric | DFS | BFS |
|--------|-----|-----|
| **Cost (steps)** | 5,744 ✗ | 110 ✓ |
| **Nodes Expanded** | 32,511 | 22,963 |
| **Frontier Peak** | 4,708 | 548 |
| **Time** | 0.83s | 0.09s |
| **Optimal?** | ✗ Non-optimal | ✓ Optimal |

**Expected behavior**: BFS finds shortest path; DFS explores deeply and finds suboptimal solution.

---

### Point 2: UCS (SingleDelivery - minimize km)

**Test Case**: Bogotá → Medellín

| Metric | Value |
|--------|-------|
| **Distance** | 405.31 km |
| **Actions** | 316 segments |
| **Nodes Expanded** | 23,173 |
| **Frontier Peak** | 198 |
| **Time** | 0.18s |
| **Optimal?** | ✓ Yes |

**Student Check**: Cost must be ≤ 405.31 km (exact match within 0.01 km). Should expand 20k-30k nodes.

---

### Point 3: A* vs UCS (straightLineHeuristic)

**Test Case**: Bogotá (n1037511) → Cartagena (n1006018)

| Metric | A\* | UCS | Improvement |
|--------|-----|-----|-------------|
| **Distance** | 911.37 km | 911.37 km | ✓ Same (optimal) |
| **Nodes Expanded** | 23,761 | 38,517 | 38.5% reduction |
| **Frontier Peak** | 277 | 209 | — |
| **Time** | 0.31s | 0.32s | Similar |

**Student Check**: 
- A* cost MUST equal UCS cost (same path)
- A* should expand ≤ UCS expansions (heuristic effectiveness)
- If A* > UCS expansions, heuristic may not be admissible

**Heuristic Validation**: 
- Straight-line heuristic uses Haversine distance
- Must return 0 at goal node
- Must be ≤ actual road distance (admissibility)

---

### Point 4: IDS (FewestStops - local delivery)

**Test Case**: Bogotá (n1037511) → Nearby node (n66995) with max_depth=6

| Metric | Value |
|--------|-------|
| **Cost (steps)** | 3 |
| **Nodes Expanded** | 9 |
| **Depth Found** | 3 |
| **Time** | <0.001s |
| **Optimal?** | ✓ Yes |

**Student Check**:
- `problem._ids_depth_found` must be set to 3
- Must find solution in depth ≤ 6
- Should expand very few nodes (solution is shallow)
- Time should be < 0.01s

---

### Point 5: Multi-Delivery (minimize km)

#### Scenario A: 4 Deliveries (Andes-Caribe Region)

| Metric | Value |
|--------|-------|
| **Distance** | 1,796.15 km |
| **Deliveries** | Medellín, Cali, Buenaventura, Popayán |
| **Nodes Expanded** | 77,134 |
| **Frontier Peak** | 427 |
| **Time** | 2.72s |

#### Scenario B: 6 Deliveries (National Challenge)

| Metric | Value |
|--------|-------|
| **Distance** | 2,868.96 km |
| **Nodes Expanded** | 612,769 |
| **Frontier Peak** | 2,295 |
| **Time** | 31.69s |

**Student Check**:
- Cost should be ≤ baseline (better heuristics → lower or equal cost)
- Time for 4 deliveries should be < 10s
- Time for 6 deliveries should be < 60s (state space explosion expected)
- Heuristic must be admissible: never overestimate cost to visit all remaining deliveries

**Common Issues**:
- ✗ MST heuristic not cached → timeout
- ✗ Heuristic overestimates → non-optimal solution
- ✗ Not handling `frozenset` correctly → wrong state representation

---

## Grading Rubric Template

### Rubric Score Mapping

| Points | Criteria |
|--------|----------|
| **20%** (Point 1) | DFS & BFS implementations correct and optimal for FewestStops |
| **15%** (Point 2) | UCS finds optimal minimum-distance routes |
| **20%** (Point 3) | A\* with straight-line heuristic matches UCS optimality |
| **15%** (Point 4) | IDS correctly implements iterative deepening with depth tracking |
| **20%** (Point 5) | Multi-delivery heuristic admissible, handles 6+ deliveries |
| **10%** (Point 6) | Analysis document: complexity, completeness, optimality claims with evidence |

### Per-Algorithm Deductions

```python
def check_student_submission(student_results, baseline):
    deductions = {}
    
    for algo, baseline_metrics in baseline.items():
        student = student_results[algo]
        
        # Cost check (±0.01 km tolerance)
        if abs(student['cost'] - baseline['cost']) > 0.01:
            deductions[algo] = 10  # Cost mismatch
        
        # Expansion check (±20% tolerance)
        exp_ratio = student['expanded'] / baseline['expanded']
        if exp_ratio > 1.2 or exp_ratio < 0.8:
            deductions[algo] = 5  # Inefficient exploration
        
        # Frontier tracking (critical)
        if 'frontier' not in student or student['frontier'] == 0:
            if algo in ['bfs', 'ucs', 'astar']:  # Should track frontier
                deductions[algo] = 10  # Missing frontier tracking
        
        # Optimality check (for algorithms that should be optimal)
        if algo in ['bfs', 'ucs', 'astar', 'ids']:
            if student['cost'] > baseline['cost'] * 1.01:
                deductions[algo] = 15  # Non-optimal solution
    
    total_score = 100 - sum(deductions.values())
    return max(0, min(100, total_score))
```

---

## Testing Your Grading Script

```bash
#!/bin/bash
# Example automated grading script

echo "Validating student submission..."

# Run student code
python3 main.py --instance single_bogota_medellin > student_output.txt

# Check if baseline metrics are met
if grep -q "Cost:.*405.3" student_output.txt; then
    echo "✓ UCS cost correct"
else
    echo "✗ UCS cost incorrect"
fi

if grep -q "Expanded:.*2[0-9][0-9][0-9][0-9]" student_output.txt; then
    echo "✓ Expansion count reasonable"
else
    echo "✗ Expansion count out of range"
fi

# Test all cases
python3 BASELINE_TESTS.py > grading_report.txt
```

---

## FAQ for Instructors

### Q: Student's A\* cost differs from UCS. What's wrong?

**A:** Check three things:
1. Heuristic admissibility: h(n) must be ≤ actual distance
2. Heuristic implementation: ensure `problem.goal` is accessible
3. Priority queue ordering: f(n) = g(n) + h(n), not just h(n)

### Q: Student's DFS/BFS give same cost. What happened?

**A:** Likely mistake: using visited set for BFS but not respecting depth for DFS. DFS should allow revisits to nodes on different paths (or use path-based visited tracking).

### Q: Multi-delivery takes too long. Normal?

**A:** Yes, 6-delivery case takes 31s in reference. If > 120s, check:
1. Heuristic caching (should cache distances)
2. MST computation efficiency
3. Infinite loops in state expansion

### Q: How strict should cost tolerance be?

**A:** 
- For costs ≤ 100 km: ±0.1 km tolerance
- For costs > 100 km: ±0.01% tolerance
- Floating point errors are expected

### Q: What if student's solution is better (lower cost) than baseline?

**A:** 
- If cost < baseline by > 1%: likely error in baseline or new better solution found
- Run UCS to verify baseline is optimal
- Review student's heuristic for inadmissibility (might overestimate)

---

## Integration with Your LMS

### Automated Feedback Template

```
ALGORITHM ASSESSMENT REPORT
===========================

Point 1 (DFS/BFS): [PASS/FAIL]
  DFS cost: {actual} steps (optimal cost: 5744)
  BFS cost: {actual} steps (optimal cost: 110)
  Status: {'✓' if within tolerance else '✗'}

Point 2 (UCS): [PASS/FAIL]
  Cost: {actual} km (expected: 405.31)
  Nodes: {actual} (expected: 23173 ±20%)
  Status: {'✓' if within tolerance else '✗'}

Point 3 (A*): [PASS/FAIL]
  Cost: {actual} km (expected: 911.37)
  vs UCS: {'✓ Same cost (optimal)' if matches else '✗ Different cost'}
  Heuristic effectiveness: {expansion_reduction}% reduction vs UCS
  Status: {'✓' if optimal else '✗'}

Point 4 (IDS): [PASS/FAIL]
  Depth found: {actual} (expected: 3)
  Time: {actual}s (should be < 0.01s)
  Status: {'✓' if correct else '✗'}

Point 5 (Multi): [PASS/FAIL]
  4-delivery cost: {actual} km (expected: 1796.15)
  6-delivery time: {actual}s (should be < 60s)
  Heuristic admissible: {'✓' if cost reasonable else '✗'}
  Status: {'✓' if passes else '✗'}

TOTAL POINTS: {score}/100
```

---

## Contact & Troubleshooting

If student code fails baseline validation:

1. **Verify graph loads**: Check `graph.py` is unmodified
2. **Check Python version**: Requires Python 3.9+
3. **Verify dependencies**: `pip install -r requirements.txt`
4. **Test minimal case**: Run `main.py --help` to ensure setup works

For questions on this reference implementation, consult:
- `BASELINE_ANALYSIS.md` - Detailed complexity analysis
- `BASELINE_RESULTS.json` - Raw metrics
- `main.py` - Integration and metric reporting

---

**Last Updated**: 2026-06-14  
**Status**: Complete & Tested ✓  
**All 11 Tests**: PASS ✓
