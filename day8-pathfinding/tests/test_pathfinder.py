import pytest

from src.map_loader import load_map
from src.pathfinder import dijkstra

nodes, edges = load_map()


def test_shortest_path():
    path, distance = dijkstra(nodes, edges, 0, 15)

    assert path[0] == 0
    assert path[-1] == 15
    assert distance > 0


def test_same_start_end():
    path, distance = dijkstra(nodes, edges, 5, 5)

    assert path == [5]
    assert distance == 0


def test_invalid_start():
    with pytest.raises(ValueError):
        dijkstra(nodes, edges, 100, 1)


def test_invalid_end():
    with pytest.raises(ValueError):
        dijkstra(nodes, edges, 1, 100)


def test_invalid_both():
    with pytest.raises(ValueError):
        dijkstra(nodes, edges, 100, 200)