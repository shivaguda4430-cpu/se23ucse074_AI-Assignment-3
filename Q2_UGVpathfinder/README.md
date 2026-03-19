# UGV Pathfinding using A* Algorithm

## Overview
This project simulates an Unmanned Ground Vehicle (UGV) navigating a battlefield environment using the A* search algorithm.

The environment is represented as a grid where:
- Each cell is either free or blocked (obstacle)
- The UGV must move from a start position to a goal position
- Obstacles are randomly generated based on density levels

The system finds the shortest path while avoiding obstacles and evaluates performance using various metrics.

---

## Objectives
- Implement A* Search Algorithm for pathfinding
- Simulate a grid-based environment with obstacles
- Support diagonal and straight movements
- Visualize the path taken by the UGV
- Evaluate performance using Measures of Effectiveness (MOE)

---

## Algorithm Used

### A* Search Algorithm

Evaluation Function:
f(n) = g(n) + h(n)

Where:
- g(n) = cost from start to current node
- h(n) = heuristic (estimated distance to goal)

Heuristic used:
- Euclidean Distance

---

## Features
- Grid size: 70 × 70
- Obstacle density levels:
  - Low (15%)
  - Medium (30%)
  - High (50%)
- Supports 8-directional movement (including diagonals)
- Path visualization using matplotlib
- Performance metrics calculation
- Interactive menu-driven system

---

## Project Structure

```bash

Q2_UGVpathfinder/
├── README.md
├── code.py
└── requirements.txt

```
---

## Requirements
- Python 3.x
- numpy
- matplotlib

Install dependencies:
pip install numpy matplotlib

---

## How to Run
1. Navigate to project folder:
cd UGV_Pathfinder

2. Run the program:
python main.py

---

## Usage
1. Generate grid with obstacle density
2. Set start and goal positions
3. Run A* algorithm
4. View path visualization
5. Check performance metrics

---

## Measures of Effectiveness (MOE)

The system evaluates performance using:

- Path Length: Total distance of path
- Straight-line Distance: Ideal shortest distance
- Path Optimality: (Straight-line / Actual Path) × 100
- Nodes Expanded: Number of explored nodes
- Path Nodes: Total nodes in path
- Direction Changes: Number of turns
- Time Taken: Execution time in milliseconds

---

## Example Output
- Path displayed on grid
- Start point marked in green
- Goal point marked in red
- Obstacles shown in black
- Path shown in blue

---

## Applications
- Robotics navigation
- Autonomous vehicles
- Military UGV systems
- Game AI pathfinding
- Drone navigation systems

---

## Conclusion
This project demonstrates how the A* algorithm can efficiently find optimal paths in complex environments using heuristic guidance. It is widely used in real-world navigation and AI systems.

---

## Author

G.Shiva Reddy  
B.Tech Computer Science
