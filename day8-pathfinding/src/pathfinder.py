"""
pathfinder.py

Implements Dijkstra's shortest path algorithm.
"""

import heapq
from pathlib import Path
from src.map_loader import load_map

def build_graph(nodes, edges):
    """
    Convert edge list into an adjacency list.

    graph[node] = [(neighbor, distance), ...]
    """

    graph = {node_id: [] for node_id in nodes}

    for edge in edges:
        a = edge["from"]
        b = edge["to"]
        d = edge["distance"]

        # Undirected graph
        graph[a].append((b, d))
        graph[b].append((a, d))

    return graph


def dijkstra(nodes, edges, start, end):
    """
    Returns:
        path (list[int])
        total_distance (float)
    """

    # ------------------------
    # Validate input
    # ------------------------

    if start not in nodes:
        raise ValueError(f"Invalid start node: {start}")

    if end not in nodes:
        raise ValueError(f"Invalid end node: {end}")

    if start == end:
        return [start], 0

    graph = build_graph(nodes, edges)

    # ------------------------
    # Initialisation
    # ------------------------

    distances = {
        node: float("inf")
        for node in graph
    }

    previous = {
        node: None
        for node in graph
    }

    distances[start] = 0

    priority_queue = [(0, start)]

    # ------------------------
    # Dijkstra
    # ------------------------

    while priority_queue:

        current_distance, current_node = heapq.heappop(priority_queue)

        # Skip outdated entries
        if current_distance > distances[current_node]:
            continue

        # Destination reached
        if current_node == end:
            break

        for neighbor, weight in graph[current_node]:

            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:

                distances[neighbor] = new_distance
                previous[neighbor] = current_node

                heapq.heappush(
                    priority_queue,
                    (new_distance, neighbor)
                )

    # ------------------------
    # No path found
    # ------------------------

    if distances[end] == float("inf"):
        raise ValueError("No path exists.")

    # ------------------------
    # Reconstruct path
    # ------------------------

    path = []

    current = end

    while current is not None:
        path.append(current)
        current = previous[current]

    path.reverse()

    return path, distances[end]


# -------------------------------------------------
# Test
# -------------------------------------------------

if __name__ == "__main__":

    BASE_DIR = Path(__file__).resolve().parent.parent

    NODE_FILE = BASE_DIR / "data" / "Node_Info.txt"
    EDGE_FILE = BASE_DIR / "data" / "Graph_Path.txt"

    nodes, edges = load_map(NODE_FILE, EDGE_FILE)
    path, distance = dijkstra(
        nodes,
        edges,
        0,
        15
    )

    print("Shortest Path:")
    print(path)

    print("Total Distance:")
    print(distance)