# AI Bootcamp Day 8 – Pathfinding Web Application

## Overview

This project is a Flask-based web application that calculates and visualizes the shortest path between two locations using **Dijkstra's Algorithm**.

The application loads node and edge information from text files, computes the shortest path, and displays the result on a generated map.

---

## Features

- Load map data from `Node_Info.txt`
- Load graph data from `Graph_Path.txt`
- Compute the shortest path using Dijkstra's Algorithm
- Visualize the graph using Matplotlib
- Highlight the shortest path
- Simple password authentication for editor mode
- Unit tests using pytest

---

## Project Structure

```
day8-pathfinding/
│
├── app.py
├── requirements.txt
├── README.md
├── docker-compose.yml
│
├── data/
│   ├── Node_Info.txt
│   └── Graph_Path.txt
│
├── src/
│   ├── __init__.py
│   ├── auth.py
│   ├── map_loader.py
│   ├── pathfinder.py
│   └── visualizer.py
│
├── templates/
│   ├── index.html
│   └── login.html
│
├── static/
│   └── map.png
│
├── tests/
│   ├── test_auth.py
│   └── test_pathfinder.py
│
└── docs/
```

---

## Installation

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Running the Application

Start the Flask application:

```bash
python app.py
```

Open your browser and visit:

```
http://localhost:60003
```

---

## Running Tests

Run all unit tests:

```bash
python -m pytest
```

Expected output:

```
7 passed
```

---

## Technologies Used

- Python
- Flask
- Matplotlib
- Pytest
- HTML
- CSS

---

## Author

AI Bootcamp Day 8 Project