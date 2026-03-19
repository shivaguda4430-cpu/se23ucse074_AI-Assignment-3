import heapq
import random
import time
import math
import matplotlib.pyplot as plt
import numpy as np

SIZE = 70

LEVELS = {
    "1": ("Low", 0.15),
    "2": ("Medium", 0.30),
    "3": ("High", 0.50)
}


class UGVSimulator:

    def __init__(self):
        self.grid = None
        self.start = None
        self.goal = None
        self.last = None
        self.label = None

    # ---------- GRID ----------
    def generate_map(self, density):
        self.grid = np.zeros((SIZE, SIZE))

        for i in range(SIZE):
            for j in range(SIZE):
                if random.random() < density:
                    self.grid[i][j] = 1

    def set_positions(self):
        self.start = self.get_input("Start")
        self.goal = self.get_input("Goal")

        self.grid[self.start] = 0
        self.grid[self.goal] = 0

    def get_input(self, name):
        while True:
            try:
                r, c = map(int, input(f"{name} (row col): ").split())
                if 0 <= r < SIZE and 0 <= c < SIZE:
                    return (r, c)
                else:
                    print("Out of bounds")
            except:
                print("Invalid input")

    # ---------- HEURISTIC ----------
    def h(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def neighbors(self, node):
        x, y = node
        moves = [(-1,0),(1,0),(0,-1),(0,1),
                 (-1,-1),(-1,1),(1,-1),(1,1)]

        result = []
        for dx, dy in moves:
            nx, ny = x+dx, y+dy
            if 0 <= nx < SIZE and 0 <= ny < SIZE:
                if self.grid[nx][ny] == 0:
                    cost = 1.414 if dx != 0 and dy != 0 else 1
                    result.append(((nx, ny), cost))
        return result

    # ---------- A* ----------
    def run_astar(self):
        pq = []
        heapq.heappush(pq, (0, self.start))

        parent = {self.start: None}
        cost = {self.start: 0}
        explored = 0

        start_time = time.time()

        while pq:
            _, current = heapq.heappop(pq)
            explored += 1

            if current == self.goal:
                return self.reconstruct(parent), explored, time.time() - start_time

            for nxt, move in self.neighbors(current):
                new_cost = cost[current] + move

                if nxt not in cost or new_cost < cost[nxt]:
                    cost[nxt] = new_cost
                    priority = new_cost + self.h(nxt, self.goal)
                    heapq.heappush(pq, (priority, nxt))
                    parent[nxt] = current

        return None, explored, time.time() - start_time

    def reconstruct(self, parent):
        node = self.goal
        path = []
        while node:
            path.append(node)
            node = parent[node]
        return path[::-1]

    # ---------- METRICS ----------
    def path_distance(self, path):
        dist = 0
        for i in range(1, len(path)):
            dist += self.h(path[i-1], path[i])
        return round(dist, 3)

    def turns(self, path):
        t = 0
        for i in range(1, len(path)-1):
            d1 = (path[i][0]-path[i-1][0], path[i][1]-path[i-1][1])
            d2 = (path[i+1][0]-path[i][0], path[i+1][1]-path[i][1])
            if d1 != d2:
                t += 1
        return t

    def show_stats(self):
        if not self.last:
            print("Run pathfinding first")
            return

        path, explored, t = self.last
        direct = self.h(self.start, self.goal)
        actual = self.path_distance(path)

        print("\n----- PERFORMANCE -----")
        print("Density:", self.label)
        print("Grid:", SIZE, "x", SIZE)
        print("Start:", self.start)
        print("Goal:", self.goal)
        print("Straight:", round(direct, 3))
        print("Path:", actual)
        print("Efficiency:", round((direct/actual)*100, 2), "%")
        print("Expanded:", explored)
        print("Nodes:", len(path))
        print("Turns:", self.turns(path))
        print("Time:", round(t*1000, 3), "ms")
        print("-----------------------\n")

    # ---------- VISUAL ----------
    def draw(self, path):
        img = np.ones((SIZE, SIZE, 3))

        for i in range(SIZE):
            for j in range(SIZE):
                if self.grid[i][j] == 1:
                    img[i][j] = [0,0,0]

        for r,c in path:
            img[r][c] = [0,0.5,1]

        sr,sc = self.start
        gr,gc = self.goal

        img[sr][sc] = [0,1,0]
        img[gr][gc] = [1,0,0]

        plt.imshow(img)
        plt.title(f"{self.label} Density Path")
        plt.show()

    # ---------- MENU ----------
    def menu(self):
        while True:
            print("\n1. Generate Grid")
            print("2. Set Start/Goal")
            print("3. Run A*")
            print("4. Show Stats")
            print("5. Exit")

            ch = input("Choice: ")

            if ch == "1":
                print("1 Low | 2 Medium | 3 High")
                d = input("Density: ")
                if d in LEVELS:
                    self.label, val = LEVELS[d]
                    self.generate_map(val)
                    print("Grid ready")
                else:
                    print("Invalid")

            elif ch == "2":
                if self.grid is None:
                    print("Generate grid first")
                else:
                    self.set_positions()

            elif ch == "3":
                if self.grid is None or self.start is None:
                    print("Setup first")
                    continue

                path, exp, t = self.run_astar()

                if path:
                    self.last = (path, exp, t)
                    self.draw(path)
                    print("Path found")
                else:
                    print("No path!")

            elif ch == "4":
                self.show_stats()

            elif ch == "5":
                break

            else:
                print("Invalid choice")


# -------- RUN -------- #
if __name__ == "__main__":
    sim = UGVSimulator()
    sim.menu()
