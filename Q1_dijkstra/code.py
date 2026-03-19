import heapq
import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()

CACHE = "distance_store.json"
API_KEY = os.getenv("GOOGLE_API_KEY")

# Initial cities
BASE_CITIES = [
    "Delhi","Mumbai","Chennai","Kolkata","Bengaluru",
    "Hyderabad","Ahmedabad","Pune","Jaipur","Lucknow",
    "Bhopal","Nagpur","Patna","Bhubaneswar","Chandigarh"
]


# ---------------- GRAPH HANDLING ---------------- #

def get_api_distances(city_list):
    endpoint = "https://maps.googleapis.com/maps/api/distancematrix/json"
    graph = {city: {} for city in city_list}

    for origin in city_list:
        params = {
            "origins": origin,
            "destinations": "|".join(city_list),
            "key": API_KEY
        }

        try:
            response = requests.get(endpoint, params=params).json()
        except:
            print("API request failed")
            return None

        if response.get("status") != "OK":
            print("API Error:", response.get("error_message", "Unknown"))
            return None

        for idx, dest in enumerate(city_list):
            if origin == dest:
                continue

            try:
                element = response["rows"][0]["elements"][idx]
                if element["status"] == "OK":
                    distance = element["distance"]["value"] // 1000
                else:
                    distance = float('inf')
            except:
                distance = float('inf')

            graph[origin][dest] = distance

    return graph


def save_graph(graph, cities):
    with open(CACHE, "w") as f:
        json.dump({"cities": cities, "graph": graph}, f, indent=2)


def load_graph():
    if not os.path.exists(CACHE):
        return None, None

    try:
        with open(CACHE, "r") as f:
            data = json.load(f)
        return data["graph"], data["cities"]
    except:
        return None, None


# ---------------- DIJKSTRA ---------------- #

def shortest_path(graph, source):
    pq = [(0, source)]
    dist = {node: float('inf') for node in graph}
    parent = {node: None for node in graph}

    dist[source] = 0

    while pq:
        current_cost, current = heapq.heappop(pq)

        for neighbor in graph[current]:
            new_cost = current_cost + graph[current][neighbor]

            if new_cost < dist[neighbor]:
                dist[neighbor] = new_cost
                parent[neighbor] = current
                heapq.heappush(pq, (new_cost, neighbor))

    return dist, parent


def build_path(parent, end):
    route = []
    while end:
        route.append(end)
        end = parent[end]
    return route[::-1]


# ---------------- UTIL ---------------- #

def normalize(name):
    return name.strip().title()


def display_cities(cities):
    print("\nCities in system:")
    for c in cities:
        print("-", c)


# ---------------- MAIN ---------------- #

graph, cities = load_graph()

if graph is None:
    print("Building initial graph...")
    graph = get_api_distances(BASE_CITIES)

    if graph:
        cities = BASE_CITIES[:]
        save_graph(graph, cities)
        print("Graph initialized.\n")
    else:
        print("Failed to build graph.")
        cities = BASE_CITIES[:]


while True:
    print("\n=== MENU ===")
    print("1. Add new cities")
    print("2. Rebuild full graph")
    print("3. Compute shortest path")
    print("4. Show cities")
    print("5. Exit")

    choice = input("Select option: ")

    # ---- ADD CITY ----
    if choice == "1":
        if not API_KEY:
            print("API key required (.env file)")
            continue

        new_input = input("Enter cities (comma separated): ")
        new_list = [normalize(c) for c in new_input.split(",")]

        new_cities = [c for c in new_list if c not in cities]

        if not new_cities:
            print("No new cities added.")
            continue

        updated = cities + new_cities
        print("Updating graph...")

        new_graph = get_api_distances(updated)

        if new_graph:
            graph = new_graph
            cities = updated
            save_graph(graph, cities)
            print("Graph updated.")
        else:
            print("Update failed.")

    # ---- REBUILD ----
    elif choice == "2":
        if not API_KEY:
            print("API key required.")
            continue

        print("Rebuilding entire graph...")
        new_graph = get_api_distances(cities)

        if new_graph:
            graph = new_graph
            save_graph(graph, cities)
            print("Graph refreshed.")
        else:
            print("Failed to rebuild.")

    # ---- SHORTEST PATH ----
    elif choice == "3":
        display_cities(cities)

        src = normalize(input("Source: "))
        dst = normalize(input("Destination: "))

        if src not in graph or dst not in graph:
            print("Invalid cities.")
            continue

        if src == dst:
            print("Distance = 0 km")
            continue

        distances, parents = shortest_path(graph, src)

        print("\nDistance:", distances[dst], "km")
        print("Route:", " -> ".join(build_path(parents, dst)))

    # ---- SHOW ----
    elif choice == "4":
        display_cities(cities)

    elif choice == "5":
        print("Exiting...")
        break

    else:
        print("Invalid option.")
