# AI-Assisted Code Improvement - Proposed Prompts

This document outlines the prompts that would be used to improve the initial reference implementation following the course's AI use policy.

## Prompt 1: Search Algorithms Documentation & Optimization

**Purpose**: Add comprehensive docstrings, optimize data structure usage, and ensure consistency

**Proposed Prompt**:
```
I have implemented 6 search algorithms (DFS, BFS, UCS, A*, DLS, IDS) in algorithms/search.py 
for a logistics pathfinding problem on a 41,718-node Colombian road network. 

Analyze these functions:
1. Are they using the best data structures? (I'm using Stack, Queue, PriorityQueue)
2. Do they handle edge cases (unreachable goals, empty graphs)?
3. Are docstrings comprehensive with parameter types, return types, and usage examples?
4. Can you identify any algorithmic inefficiencies?
5. Are frontier tracking calls (_remember_frontier) placed correctly for metrics?

Please provide:
- A refactored version with detailed NumPy/Google-style docstrings
- Any optimization suggestions (e.g., better visited set handling)
- Clear examples of how each algorithm differs on a logistics problem
- Ensure consistency in code style across all 6 functions

Keep the core logic identical - focus on documentation, edge case handling, and code clarity.
```

---

## Prompt 2: Heuristic Functions - Admissibility Proof & Optimization

**Purpose**: Document heuristic properties mathematically, add type hints, and optimize MST caching

**Proposed Prompt**:
```
I implemented 3 heuristic functions for informed search:
1. straightLineHeuristic() - Haversine distance for single-delivery
2. multiDeliveryHeuristic() - MST-based lower bound for TSP
3. straightLineMultiDeliveryHeuristic() - Faster variant using only geodesic distances

For each heuristic, please:
1. Add docstrings that prove admissibility (h(n) ≤ actual cost)
2. Explain why each is consistent (satisfies triangle inequality)
3. Document the computational complexity
4. Add type hints for all parameters and returns
5. Review the MST caching strategy in multiDeliveryHeuristic - is it optimal?
6. Add concrete examples of heuristic values for sample nodes

Provide a refactored version that:
- Documents mathematical properties clearly for students to learn from
- Uses proper type hints (including frozenset, tuple types)
- Explains the trade-off between straightLineMultiDeliveryHeuristic and multiDeliveryHeuristic
- Shows how caching improves performance on repeated subproblems

Keep the algorithm logic unchanged - focus on clarity and mathematical rigor.
```

---

## Prompt 3: Test Suite Documentation & Error Handling

**Purpose**: Add comprehensive documentation to testing framework and improve robustness

**Proposed Prompt**:
```
I have a test suite (BASELINE_TESTS.py) that runs 11 test cases across 5 assignment points.

Please review and improve:
1. Add detailed docstrings explaining each test case's purpose
2. Document what "success" looks like (cost tolerance, expansion count bounds)
3. Add type hints throughout
4. Improve error handling (currently has basic try/except)
5. Add validation of results (e.g., check if cost >= 0, actions form valid path)
6. Document the metrics being tracked (expanded nodes, frontier size, time)

Provide a refactored version that:
- Has comprehensive docstrings for every function
- Explains each test case in the context of the course learning objectives
- Validates results beyond just success/failure
- Shows students how to think about testing search algorithms
- Includes clear comments on performance expectations

Keep test cases identical - improve documentation and robustness.
```

---

## Prompt 4: Code Organization & Comments

**Purpose**: Add educational comments explaining algorithmic choices

**Proposed Prompt**:
```
I implemented search algorithms for a university AI course. Students will read this code to 
understand how search works in practice.

For each algorithm, add comments that explain:
1. Why we use this particular data structure for the frontier
2. Why we mark nodes as visited (prevents cycles/redundant work)
3. How the algorithm explores the state space
4. The difference between this algorithm and others
5. When this algorithm is better/worse than alternatives

Add comments that help students understand:
- The relationship between g(n), h(n), and f(n) in A*
- Why BFS finds optimal solutions for unit-cost problems
- Why DFS uses less memory than BFS
- How IDS combines DFS and BFS benefits

Focus on educational clarity - these comments should help students debug and learn, 
not just explain what the code does.
```

---

## Prompt 5: Integration with Course Materials

**Purpose**: Link implementation to complexity analysis and theoretical guarantees

**Proposed Prompt**:
```
This code is part of a university AI course that includes:
- Complexity analysis in BASELINE_ANALYSIS.md
- Expected algorithm behavior on a 41,718-node graph
- Metrics like "expands ~23,000 nodes for UCS on long routes"

Please add docstrings and comments that:
1. Reference the expected complexity (O(b^d) for BFS, etc.)
2. Explain how this implementation achieves completeness/optimality guarantees
3. Link to the test results (e.g., "BFS should find 110-step solution")
4. Document frontier tracking for metrics collection
5. Explain edge cases with examples

This helps students connect theory to practice by seeing:
- How theoretical bounds match empirical results
- Why metrics matter for algorithm evaluation
- How to validate that their implementation is correct

Include references like: "See BASELINE_ANALYSIS.md §3 for complexity proof"
```

---

## Implementation Strategy

These prompts would be applied in this order:

1. **Search Algorithms** → Add docstrings, type hints, edge case handling
2. **Heuristics** → Add mathematical documentation, type hints, complexity notes
3. **Test Suite** → Improve robustness, validation, documentation
4. **Code Organization** → Add educational comments throughout
5. **Integration** → Link to course materials and analysis

## Documentation Format

For each improved function/file:

```python
"""
ORIGINAL VERSION (before AI improvement):
[Original implementation here as comments]

PROMPTS USED:
1. [Prompt 1 text here]
2. [Prompt 2 text here]

IMPROVEMENTS APPLIED:
- Added comprehensive docstrings
- [List other improvements]

FINAL VERSION:
[Refactored code here]
"""
```

## Learning Value

By documenting this process, students will learn:
1. **How to use AI responsibly** - AI for improvement, not generation
2. **Good documentation practices** - What makes code understandable
3. **Algorithmic thinking** - Why certain design choices matter
4. **Professional development** - How to iterate and improve code
5. **Peer learning** - Seeing before/after and understanding the changes

---

**Next**: Apply these prompts to create improved versions with full documentation.
