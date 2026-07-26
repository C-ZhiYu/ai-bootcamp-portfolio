"""
map_loader.py

Loads:
- Node_Info.txt
- Graph_Path.txt

Ignores:
- blank lines
- comment lines beginning with '#'
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

def load_nodes(filename):
    nodes = {}

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            node_id = int(parts[0])
            x = float(parts[1])
            y = float(parts[2])
            type_id = int(parts[3])
            name = parts[4]

            nodes[node_id] = {
                "id": node_id,
                "x": x,
                "y": y,
                "type": type_id,
                "name": name,
            }

    return nodes


def load_edges(filename):
    edges = []

    with open(filename, "r") as file:
        for line in file:
            line = line.strip()

            if not line or line.startswith("#"):
                continue

            parts = line.split()

            edge = {
                "id": int(parts[0]),
                "from": int(parts[1]),
                "to": int(parts[2]),
                "distance": float(parts[3]),
            }

            edges.append(edge)

    return edges


def load_map(node_file=None, edge_file=None):
    if node_file is None:
        node_file = DATA_DIR / "Node_Info.txt"

    if edge_file is None:
        edge_file = DATA_DIR / "Graph_Path.txt"

    nodes = load_nodes(node_file)
    edges = load_edges(edge_file)

    return nodes, edges


if __name__ == "__main__":

    node_path = DATA_DIR / "Node_Info.txt"
    edge_path = DATA_DIR / "Graph_Path.txt"

    nodes, edges = load_map(node_path, edge_path)

    print(f"Loaded {len(nodes)} nodes")
    print(f"Loaded {len(edges)} edges")

    print(nodes[0])
    print(edges[0])