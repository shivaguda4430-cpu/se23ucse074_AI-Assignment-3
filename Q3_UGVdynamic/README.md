# UGV Dynamic Pathfinding using A* (Replanning)

## Overview
This project simulates an Unmanned Ground Vehicle (UGV) navigating a dynamic battlefield environment using the A* search algorithm with replanning.

Unlike static pathfinding, the environment changes during execution:
- Obstacles can appear dynamically
- The UGV must detect blocked paths
- The system replans routes in real-time

This simulates real-world scenarios such as autonomous vehicles and military robots operating in uncertain environments.

---

## Objectives
- Implement A* search for optimal pathfinding
- Introduce dynamic obstacles during traversal
- Trigger replanning when paths become invalid
- Evaluate performance using real-time metrics
- Visualize the UGV movement and environment

---

## Algorithm Used

### A* Search with Replanning

Evaluation Function:
f(n) = g(n) + h(n)

Where:
- g(n) = cost from start to current node
- h(n) = heuristic estimate (Euclidean distance)

When the path becomes blocked:
- A* is re-executed from current position
- New path is generated dynamically

---

## Features
- Grid size: 70 × 70
- Obstacle density levels:
  - Low (15%)
  - Medium (30%)
  - High (50%)
- Dynamic obstacles introduced during traversal
- Replanning triggered automatically
- Supports 8-directional movement
- Visualization using matplotlib
- Performance tracking system

---

## Project Structure
UGV_Dynamic_Pathfinder
│
├── main.py
├── README.md
└── output_images/

---

## Requirements
- Python 3.x
- numpy
- matplotlib

Install dependencies:
pip install numpy matplotlib

---

## How to Run
1. Navigate to the project folder:
cd UGV_Dynamic_Pathfinder

2. Run the program:
python main.py

---

## Usage
1. Generate grid with obstacle density
2. Set start and goal positions
3. Run dynamic simulation
4. View visualization of path
5. Analyze performance metrics

---

## Measures of Effectiveness (MOE)

The system evaluates:

- Straight-line Distance (ideal path)
- Initial Planned Path Distance
- Actual Distance Travelled
- Extra Distance due to replanning
- Path Optimality (%)
- Number of Replans Triggered
- Dynamic Obstacles Generated
- Steps Taken
- Direction Changes
- Time Taken

---

## Example Behavior
- UGV starts moving toward goal
- New obstacles appear during traversal
- If path is blocked:
  - A* recalculates a new route
- UGV continues until goal is reached or blocked

---

## Applications
- Autonomous vehicles
- Military robotics (UGV navigation)
- Drone navigation systems
- Warehouse automation
- Game AI (dynamic environments)

---

## Conclusion
This project demonstrates how A* can be extended to handle dynamic environments through replanning. It reflects real-world AI systems where conditions change unpredictably and adaptive decision-making is required.

---

## Author
G.Shiva Reddy
B.Tech Computer Science
