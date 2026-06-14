"""Reference baseline tests for Panini Logistics workshop.

This script executes all algorithm implementations against predefined test cases
and records the results for use as a grading baseline and performance reference.

Instructor use: Run this to verify algorithm correctness and obtain baseline metrics.
"""

import subprocess
import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any


def run_test(
    problem: str = "",
    algorithm: str = "",
    start: str = "n1037511",
    goal: str = "n39739",
    deliveries: str = "",
    heuristic: str = "",
    max_depth: int = None,
    instance: str = "",
) -> Dict[str, Any]:
    """Execute a single test case and parse the output."""

    cmd = [
        "python3",
        "main.py",
        "--problem", problem,
        "--algorithm", algorithm,
        "--start", start,
        "--goal", goal,
    ]

    if instance:
        cmd = ["python3", "main.py", "--instance", instance]
    else:
        if deliveries:
            cmd.extend(["--deliveries", deliveries])
        if heuristic:
            cmd.extend(["--heuristic", heuristic])
        if max_depth is not None:
            cmd.extend(["--max-depth", str(max_depth)])

    try:
        result = subprocess.run(
            cmd,
            cwd=Path(__file__).parent,
            capture_output=True,
            text=True,
            timeout=120,
        )

        if result.returncode != 0:
            return {
                "status": "error",
                "error": result.stderr,
                "stdout": result.stdout,
            }

        output = result.stdout
        data = {
            "problem": problem,
            "algorithm": algorithm,
            "instance": instance,
        }

        for line in output.split("\n"):
            if line.startswith("Cost:"):
                data["cost"] = float(line.split()[1])
            elif line.startswith("Actions:"):
                data["actions"] = int(line.split()[1])
            elif line.startswith("Expanded:"):
                data["expanded"] = int(line.split()[1])
            elif line.startswith("Frontier:"):
                data["frontier"] = int(line.split()[1])
            elif line.startswith("Time:"):
                data["time"] = float(line.split()[1])
            elif line.startswith("IDS depth:"):
                data["ids_depth"] = int(line.split()[2])

        data["status"] = "success"
        return data

    except subprocess.TimeoutExpired:
        return {"status": "timeout", "problem": problem, "algorithm": algorithm}
    except Exception as e:
        return {
            "status": "error",
            "problem": problem,
            "algorithm": algorithm,
            "error": str(e),
        }


def main():
    """Run all baseline tests."""

    print("=" * 80)
    print("PANINI LOGISTICS - BASELINE TEST SUITE")
    print("=" * 80)
    print()

    tests = [
        # Point 1: DFS and BFS (FewestStops)
        {
            "name": "Point 1a: DFS on FewestStops",
            "problem": "stops",
            "algorithm": "dfs",
            "start": "n1037511",
            "goal": "n39739",
        },
        {
            "name": "Point 1b: BFS on FewestStops",
            "problem": "stops",
            "algorithm": "bfs",
            "start": "n1037511",
            "goal": "n39739",
        },
        {
            "name": "Point 1c: DFS vs BFS comparison (alt pair)",
            "problem": "stops",
            "algorithm": "bfs",
            "start": "n1037511",
            "goal": "n15395",
        },
        # Point 2: UCS (SingleDelivery)
        {
            "name": "Point 2a: UCS on SingleDelivery (Bogotá-Medellín)",
            "instance": "single_bogota_medellin",
        },
        {
            "name": "Point 2b: UCS on SingleDelivery (alternate)",
            "problem": "single",
            "algorithm": "ucs",
            "start": "n1037511",
            "goal": "n15395",
        },
        # Point 3: A* with Straight-line heuristic
        {
            "name": "Point 3a: A* vs UCS (same destination)",
            "instance": "single_bogota_cartagena_astar",
        },
        {
            "name": "Point 3b: A* (UCS comparison baseline)",
            "problem": "single",
            "algorithm": "ucs",
            "start": "n1037511",
            "goal": "n1006018",
        },
        # Point 4: Iterative Deepening
        {
            "name": "Point 4a: IDS on FewestStops",
            "instance": "ids_local_depth",
        },
        {
            "name": "Point 4b: BFS comparison for IDS",
            "instance": "stops_bogota_cali_bfs",
        },
        # Point 5: Multi-delivery
        {
            "name": "Point 5a: Multi-delivery (4 destinations)",
            "instance": "multi_andes_caribe",
        },
        {
            "name": "Point 5b: Multi-delivery (6 destinations)",
            "instance": "multi_national_challenge",
        },
    ]

    results = []
    for i, test in enumerate(tests, 1):
        print(f"[{i}/{len(tests)}] {test['name']}...")
        result = run_test(**{k: v for k, v in test.items() if k != "name"})

        if result["status"] == "success":
            print(
                f"  ✓ Cost: {result.get('cost', 'N/A')}, "
                f"Nodes: {result.get('expanded', 'N/A')}, "
                f"Time: {result.get('time', 'N/A')}s"
            )
        else:
            print(f"  ✗ {result['status']}")

        results.append({"test": test["name"], **result})
        print()

    # Save results to JSON
    output_file = Path(__file__).parent / "BASELINE_RESULTS.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print("=" * 80)
    print(f"Results saved to {output_file}")
    print("=" * 80)

    # Summary statistics
    successful = [r for r in results if r["status"] == "success"]
    print(f"\nSuccessful tests: {len(successful)}/{len(results)}")

    if successful:
        avg_time = sum(r.get("time", 0) for r in successful) / len(successful)
        avg_expanded = sum(r.get("expanded", 0) for r in successful) / len(successful)
        print(f"Average execution time: {avg_time:.4f}s")
        print(f"Average nodes expanded: {avg_expanded:.0f}")


if __name__ == "__main__":
    main()
