"""
visualizer.py

Draws the map and highlights the shortest path.
"""

import matplotlib.pyplot as plt


# Colour for each TypeID
TYPE_COLORS = {
    0: "green",      # School
    1: "orange",     # Shop
    2: "blue",       # Mall
    3: "gray",       # HDB
    4: "limegreen",  # Park
}


def draw_map(nodes, edges, path=None, output_file="static/map.png"):
    """
    Draw the entire map.

    Parameters
    ----------
    nodes : dict
    edges : list
    path : list[int]
        Shortest path to highlight
    output_file : str
    """

    plt.figure(figsize=(10, 8))

    # -------------------------------------------------
    # Draw all edges
    # -------------------------------------------------

    for edge in edges:

        node_a = nodes[edge["from"]]
        node_b = nodes[edge["to"]]

        plt.plot(
            [node_a["x"], node_b["x"]],
            [node_a["y"], node_b["y"]],
            color="lightgray",
            linewidth=1,
            zorder=1,
        )

    # -------------------------------------------------
    # Highlight shortest path
    # -------------------------------------------------

    if path and len(path) > 1:

        for i in range(len(path) - 1):

            a = nodes[path[i]]
            b = nodes[path[i + 1]]

            plt.plot(
                [a["x"], b["x"]],
                [a["y"], b["y"]],
                color="red",
                linewidth=3,
                zorder=2,
            )

    # -------------------------------------------------
    # Draw nodes
    # -------------------------------------------------

    for node in nodes.values():

        color = TYPE_COLORS.get(node["type"], "black")

        plt.scatter(
            node["x"],
            node["y"],
            color=color,
            s=120,
            edgecolors="black",
            zorder=3,
        )

        plt.text(
            node["x"] + 1,
            node["y"] + 1,
            f'{node["id"]}',
            fontsize=9,
        )

    plt.title("Pathfinding Map")

    plt.xlabel("X")

    plt.ylabel("Y")

    plt.grid(True)

    plt.axis("equal")

    plt.tight_layout()

    plt.savefig(output_file)

    plt.close()

# -------------------------------------------------
# Test
# -------------------------------------------------

if __name__ == "__main__":

    from src.map_loader import load_map
    from src.pathfinder import dijkstra

    nodes, edges = load_map()

    path, distance = dijkstra(
        nodes,
        edges,
        0,
        15,
    )

    print("Shortest Path:", path)
    print("Distance:", distance)

    draw_map(
        nodes,
        edges,
        path,
        "test_map.png",
    )

    print("Map saved as test_map.png")