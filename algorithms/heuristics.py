"""Heuristics for graph-search delivery problems."""

from __future__ import annotations

import math
from typing import Any

from algorithms import utils
from graph.road_graph import haversine_km


def nullHeuristic(_state: Any, _problem: Any = None) -> float:
    """A trivial admissible heuristic."""

    return 0.0


def straightLineHeuristic(state: str, problem: Any) -> float:
    """Geodesic distance from the current node to the destination.

    Tips:
    - Use `problem.graph.coordinates` and `haversine_km`.
    - Return 0 when the problem optimizes number of stops, not kilometers.
    """

    if problem.cost_mode == "stops":
        return 0.0

    current_coords = problem.graph.coordinates(state)
    goal_coords = problem.graph.coordinates(problem.goal)
    return haversine_km(current_coords, goal_coords)


def multiDeliveryHeuristic(state: tuple[str, frozenset[str]], problem: Any) -> float:
    """Admissible MST heuristic for the multi-delivery TSP-like problem.

    The estimate is:
      shortest-path distance from current node to the nearest remaining delivery
      + MST cost over the remaining deliveries using shortest-path distances.

    This is a lower bound on any route that visits all pending deliveries.

    Tips:
    - Split the state into current node and pending deliveries.
    - Cache pairwise road distances in `problem.heuristicInfo` to avoid recomputing.
    - Reuse `_mst_cost` with a distance function defined over delivery node IDs.
    """

    current, remaining = state

    if len(remaining) == 0:
        return 0.0

    cache_key = ("multi_distances", frozenset([current] | remaining))
    if cache_key not in problem.heuristicInfo:
        problem.heuristicInfo[cache_key] = {}

    distances_cache = problem.heuristicInfo[cache_key]

    def shortest_distance(a, b):
        if a == b:
            return 0.0
        pair = tuple(sorted([a, b]))
        if pair not in distances_cache:
            _, cost, _ = problem.graph.shortest_path(a, b)
            distances_cache[pair] = cost
        return distances_cache[pair]

    remaining_list = list(remaining)
    min_to_nearest = min(shortest_distance(current, delivery) for delivery in remaining_list)
    mst_cost = _mst_cost(remaining_list, shortest_distance)

    return min_to_nearest + mst_cost


def straightLineMultiDeliveryHeuristic(
    state: tuple[str, frozenset[str]], problem: Any
) -> float:
    """Lighter admissible MST heuristic using geodesic distances only.

    Tips:
    - Same structure as `multiDeliveryHeuristic`, but use geodesic distances only.
    - This trades some informativeness for much faster heuristic evaluation.
    """

    current, remaining = state

    if len(remaining) == 0:
        return 0.0

    remaining_list = list(remaining)
    current_coords = problem.graph.coordinates(current)

    def geodesic_distance(a, b):
        if a == b:
            return 0.0
        a_coords = problem.graph.coordinates(a)
        b_coords = problem.graph.coordinates(b)
        return haversine_km(a_coords, b_coords)

    min_to_nearest = min(geodesic_distance(current, delivery) for delivery in remaining_list)
    mst_cost = _mst_cost(remaining_list, geodesic_distance)

    return min_to_nearest + mst_cost


def _mst_cost(nodes: list[str], distance_fn) -> float:
    if len(nodes) <= 1:
        return 0.0
    in_tree = {nodes[0]}
    total = 0.0
    while len(in_tree) < len(nodes):
        best_cost = math.inf
        best_node = None
        for source in in_tree:
            for target in nodes:
                if target in in_tree:
                    continue
                cost = distance_fn(source, target)
                if cost < best_cost:
                    best_cost = cost
                    best_node = target
        if best_node is None:
            return math.inf
        in_tree.add(best_node)
        total += best_cost
    return total
