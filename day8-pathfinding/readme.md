# AI Bootcamp Day 8 – AI Pathfinding Web Application

A Flask-based web application that computes and visualizes the shortest path between two locations using **Dijkstra's Algorithm**. The application loads a map from text files, calculates the optimal route, and generates a visual representation of the path.

---

## Features

- Load map data from text files (`Node_Info.txt` and `Graph_Path.txt`)
- Compute the shortest path using **Dijkstra's Algorithm**
- Visualize the map with **Matplotlib**
- Highlight the computed shortest path
- Simple password-based authentication for editor mode
- Unit tests using **Pytest**
- Docker support
- One-command PowerShell startup script (`run.ps1`)

---

## Project Structure

```text
day8-pathfinding/
│
├── app.py
├── run.ps1
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── README.md
│
├── data/
│   ├── Node_Info.txt
│   └── Graph_Path.txt
│
├── docs/
│   ├── ai_review_notes.md
│   ├── ci_result_summary.md
│   └── test_plan.md
│
├── src/
│   ├── __init__.py
│   ├── auth.py
│   ├── map_loader.py
│   ├── pathfinder.py
│   └── visualizer.py
│
├── static/
│   └── map.png
│
├── templates/
│   ├── index.html
│   └── login.html
│
└── tests/
    ├── test_auth.py
    └── test_pathfinder.py
```

---

## Prerequisites

Before running the project, ensure you have:

- Python 3.12 or later
- Git
- Docker Desktop (optional, for Docker support)

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd day8-pathfinding
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment.

### Windows

```powershell
.venv\Scripts\Activate.ps1
```

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Quick Start

A PowerShell helper script is included to simplify running the project.

Execute:

```powershell
.\run.ps1
```

The script will:

1. Install project dependencies (if required)
2. Run all unit tests
3. Build the Docker image
4. Launch the Flask web application

Once the application starts, open:

```text
http://localhost:60003
```

---

## Manual Execution

### Run the application

```bash
python app.py
```

### Run the unit tests

```bash
python -m pytest
```

Expected output:

```text
=====================
7 passed
=====================
```

### Build the Docker image

```bash
docker compose build
```

### Run the Docker container

```bash
docker compose up
```

---

## Technologies Used

- Python
- Flask
- Matplotlib
- Pytest
- HTML / CSS
- Docker

---

## Project Highlights

- Implements **Dijkstra's Algorithm** for shortest path computation.
- Visualizes graphs and routes using **Matplotlib**.
- Provides a simple web interface built with **Flask**.
- Includes automated unit tests with **Pytest**.
- Supports containerization using **Docker**.

---