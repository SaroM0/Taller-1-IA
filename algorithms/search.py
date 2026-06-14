"""Generic search algorithms for the Panini logistics workshop."""

from __future__ import annotations

from typing import Any

from algorithms import utils
from algorithms.heuristics import nullHeuristic
from algorithms.problems import SearchProblem, State


def _remember_frontier(problem: SearchProblem, frontier: Any) -> None:
    """Record the largest frontier size reached during a search.

    Call this helper after each push/pop cycle in DFS, BFS, UCS and A*.
    It updates `problem._max_frontier_size`, which `main.py` prints in the
    execution summary for your experimental analysis.

    You do not need to count expanded nodes here: `getSuccessors` in
    `algorithms/problems.py` already increments `problem._expanded`.
    """

    if hasattr(frontier, "_items"):
        size = len(frontier._items)
    elif hasattr(frontier, "heap"):
        size = len(frontier.heap)
    else:
        size = 0
    current = getattr(problem, "_max_frontier_size", 0)
    problem._max_frontier_size = max(current, size)


def depthFirstSearch(problem: SearchProblem) -> list[str]:
    """Search the deepest nodes in the search tree first.

    Tips:
    - Return the action list accumulated along the path, not the node sequence.
    - Call `_remember_frontier` whenever the frontier changes.
    - Expanded nodes are counted automatically inside `getSuccessors`.
    """

    frontier = utils.Stack()
    start = problem.getStartState()
    frontier.push((start, []))
    visited = {start}
    _remember_frontier(problem, frontier)

    while not frontier.isEmpty():
        state, actions = frontier.pop()
        _remember_frontier(problem, frontier)

        if problem.isGoalState(state):
            return actions

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor)
                frontier.push((successor, actions + [action]))
                _remember_frontier(problem, frontier)

    return []


def breadthFirstSearch(problem: SearchProblem) -> list[str]:
    """Search the shallowest nodes in the search tree first.

    Tips:
    - Mark a state as visited when you enqueue it, not when you dequeue it.
    - Test for the goal immediately after dequeuing a state.
    """

    frontier = utils.Queue()
    start = problem.getStartState()
    frontier.push((start, []))
    visited = {start}
    _remember_frontier(problem, frontier)

    while not frontier.isEmpty():
        state, actions = frontier.pop()
        _remember_frontier(problem, frontier)

        if problem.isGoalState(state):
            return actions

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in visited:
                visited.add(successor)
                frontier.push((successor, actions + [action]))
                _remember_frontier(problem, frontier)

    return []


def uniformCostSearch(problem: SearchProblem) -> list[str]:
    """Search the node with the lowest path cost first.

    Tips:
    - Use path cost `g(n)` as the priority queue key.
    - Ignore stale frontier entries whose stored `g` is worse than the best known.
    """

    frontier = utils.PriorityQueue()
    start = problem.getStartState()
    frontier.push((start, [], 0.0), 0.0)
    best_cost = {start: 0.0}
    _remember_frontier(problem, frontier)

    while not frontier.isEmpty():
        state, actions, cost = frontier.pop()
        _remember_frontier(problem, frontier)

        if cost > best_cost.get(state, float('inf')):
            continue

        if problem.isGoalState(state):
            return actions

        for successor, action, step_cost in problem.getSuccessors(state):
            new_cost = cost + step_cost
            if new_cost < best_cost.get(successor, float('inf')):
                best_cost[successor] = new_cost
                frontier.push((successor, actions + [action], new_cost), new_cost)
                _remember_frontier(problem, frontier)

    return []


def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic) -> list[str]:
    """Search the node with the lowest `g(n) + h(n)` first.

    Tips:
    - Push `g(n) + h(n)` to the frontier, but compare re-expansions against `g(n)`.
    - The UCS pattern still applies once a state is popped from the queue.
    """

    frontier = utils.PriorityQueue()
    start = problem.getStartState()
    h_start = heuristic(start, problem)
    frontier.push((start, [], 0.0), h_start)
    best_cost = {start: 0.0}
    _remember_frontier(problem, frontier)

    while not frontier.isEmpty():
        state, actions, g_cost = frontier.pop()
        _remember_frontier(problem, frontier)

        if g_cost > best_cost.get(state, float('inf')):
            continue

        if problem.isGoalState(state):
            return actions

        for successor, action, step_cost in problem.getSuccessors(state):
            new_g = g_cost + step_cost
            if new_g < best_cost.get(successor, float('inf')):
                best_cost[successor] = new_g
                h_successor = heuristic(successor, problem)
                f_value = new_g + h_successor
                frontier.push((successor, actions + [action], new_g), f_value)
                _remember_frontier(problem, frontier)

    return []


def depthLimitedSearch(problem: SearchProblem, limit: int) -> list[str] | None:
    """Return a solution with at most `limit` actions, or None if none is found.

    Tips:
    - Depth counts actions taken from the start, not recursive calls made.
    - Keep a set of nodes on the current path to avoid revisiting them in one branch.
    """

    def _dls_helper(state, actions, path, depth_remaining):
        if problem.isGoalState(state):
            return actions

        if depth_remaining == 0:
            return None

        for successor, action, _ in problem.getSuccessors(state):
            if successor not in path:
                path.add(successor)
                result = _dls_helper(successor, actions + [action], path, depth_remaining - 1)
                if result is not None:
                    return result
                path.remove(successor)

        return None

    start = problem.getStartState()
    result = _dls_helper(start, [], {start}, limit)
    return result


def iterativeDeepeningSearch(
    problem: SearchProblem, max_depth: int | None = None
) -> list[str]:
    """Run depth-limited DFS with increasing depth limits.

    Tips:
    - Increase the limit one step at a time and delegate each attempt to DLS.
    - Save the successful depth in `problem._ids_depth_found` before returning.
    """

    limit = 0
    max_limit = max_depth if max_depth is not None else 1000

    while limit <= max_limit:
        result = depthLimitedSearch(problem, limit)
        if result is not None:
            problem._ids_depth_found = limit
            return result
        limit += 1

    return []


# Abbreviations used by the CLI and the statement.
dfs = depthFirstSearch
bfs = breadthFirstSearch
ucs = uniformCostSearch
astar = aStarSearch
ids = iterativeDeepeningSearch
