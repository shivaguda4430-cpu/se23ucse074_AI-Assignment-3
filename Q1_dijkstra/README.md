# AI Search Assignment – Dijkstra with Real-Time API

## Overview
This project implements Dijkstra’s Algorithm (Uniform Cost Search) to compute the shortest path between cities in India using real-world road distances.

The system integrates the Google Distance Matrix API to fetch actual road distances and uses caching to store results locally, reducing repeated API calls.

## Objectives
- Implement Dijkstra’s Algorithm using a priority queue
- Use real-time API data instead of hardcoded values
- Store graph data locally using caching
- Allow dynamic addition of cities
- Compute shortest paths between any two cities

## Algorithm Used
Dijkstra’s Algorithm (Uniform Cost Search)

Evaluation Function:
f(n) = g(n)

Where:
g(n) = cost from start node to current node

## Features
- Real-time distance fetching using Google API
- Local caching (graph stored in JSON file)
- Add new cities dynamically
- Rebuild graph on demand
- Shortest path calculation with route display
- Error handling for API failures

## Project Structure

```bash
Q1_dijkstra/
├── .env.example
├── .gitignore
├── README.md
└── code.py
```
## Requirements
- Python 3.x
- requests library
- python-dotenv

Install dependencies:
pip install requests python-dotenv

## Setup Instructions
1. Clone the repository:
git clone https://github.com/yourusername/AI_Search_Assignment.git

2. Navigate into the folder:
cd AI_Search_Assignment

3. Create a .env file:
GOOGLE_API_KEY=your_api_key_here

4. Run the program:
python main.py

## Usage
1. Add cities (requires API)
2. Refresh graph
3. Find shortest path
4. View available cities
5. Exit program

## Example
Source: Hyderabad  
Destination: Delhi  

Output:
Shortest Distance: 1580 km  
Path: Hyderabad -> Nagpur -> Delhi

## Measures of Effectiveness
- Completeness: Always finds a path if one exists
- Optimality: Guarantees shortest path
- Time Complexity: O((V + E) log V)
- Space Complexity: O(V)

## Applications
- GPS Navigation Systems
- Route Optimization
- Logistics and Transportation
- Network Routing
- Intelligent Agents

## Conclusion
This project demonstrates how classical AI search algorithms can be enhanced using real-world data. By integrating APIs and caching, the system becomes both practical and efficient.

## Author

G.Shiva Reddy  
B.Tech Computer Science
