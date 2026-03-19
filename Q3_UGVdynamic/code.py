import heapq
import random
import time
import math
import numpy as np
import matplotlib.pyplot as plt

SIZE = 70

LEVEL_MAP = {
    "1": ("Low", 0.15),
    "2": ("Medium", 0.30),
    "3": ("High", 0.50)
}

SPAWN_RATE = 5
SPAWN_COUNT = 8


class DynamicUGV:

    def __init__(self):
        self.grid = None
        self.start = None
        self.goal = None
        self.result = None
        self.level = None

    # -------- GRID -------- #
    def create_world(self, density):
        self.grid = np.zeros((SIZE, SIZE))

        for i in range(SIZE):
            for j in range(SIZE):
                if random.random() < density:
                    self.grid[i][j] = 1

    def set_points(self):
        self.start = self.input_pos("Start")
        self.goal = self.input_pos("Goal")

        self.grid[self.start] = 0
        self.grid[self.goal] = 0

    def input_pos(self, label):
        while True:
            try:
                r, c = map(int, input(f"{label} (row col): ").split())
                if 0 <= r < SIZE and 0 <= c < SIZE:
                    return (r, c)
                print("Out of bounds")
            except:
                print("Invalid input")

    # -------- HEURISTIC -------- #
    def h(self, a, b):
        return math.hypot(a[0]-b[0], a[1]-b[1])

    def adj(self, node):
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

    # -------- A* -------- #
    def search(self, src, dst):
        pq = [(0, src)]
        parent = {src: None}
        cost = {src: 0}
        expanded = 0

        while pq:
            _, curr = heapq.heappop(pq)
            expanded += 1

            if curr == dst:
                return self.trace(parent, dst), expanded

            for nxt, w in self.adj(curr):
                new_cost = cost[curr] + w

                if nxt not in cost or new_cost < cost[nxt]:
                    cost[nxt] = new_cost
                    priority = new_cost + self.h(nxt, dst)
                    heapq.heappush(pq, (priority, nxt))
                    parent[nxt] = curr

        return None, expanded

    def trace(self, parent, node):
        path = []
        while node:
            path.append(node)
            node = parent[node]
        return path[::-1]

    # -------- DYNAMIC -------- #
    def inject_obstacles(self, safe):
        added = []
        tries = 0

        while len(added) < SPAWN_COUNT and tries < SPAWN_COUNT * 20:
            r = random.randint(0, SIZE-1)
            c = random.randint(0, SIZE-1)
            tries += 1

            if self.grid[r][c] == 0 and (r,c) not in safe:
                self.grid[r][c] = 2
                added.append((r,c))

        return added

    def blocked(self, path):
        for p in path:
            if self.grid[p] != 0:
                return True
        return False

    # -------- SIMULATION -------- #
    def simulate(self):
        t0 = time.time()

        init_path, _ = self.search(self.start, self.goal)
        if init_path is None:
            return None

        current = init_path[:]
        track = [self.start]
        pos = self.start

        replans = 0
        expansions = 0
        dynamic_obs = []
        steps = 0

        safe = {self.start, self.goal}

        while pos != self.goal:
            steps += 1

            if steps % SPAWN_RATE == 0:
                new_obs = self.inject_obstacles(safe)
                dynamic_obs.extend(new_obs)

                if self.blocked(current):
                    new_path, exp = self.search(pos, self.goal)
                    expansions += exp
                    replans += 1

                    if new_path is None:
                        return {
                            "success": False,
                            "track": track,
                            "replans": replans,
                            "time": time.time()-t0,
                            "dyn": dynamic_obs
                        }

                    current = new_path

            if len(current) > 1:
                nxt = current[1]

                if self.grid[nxt] != 0:
                    new_path, exp = self.search(pos, self.goal)
                    expansions += exp
                    replans += 1

                    if new_path is None:
                        return {
                            "success": False,
                            "track": track,
                            "replans": replans,
                            "time": time.time()-t0,
                            "dyn": dynamic_obs
                        }

                    current = new_path
                    nxt = current[1]

                pos = nxt
                track.append(pos)
                current.pop(0)

        return {
            "success": True,
            "track": track,
            "replans": replans,
            "exp": expansions,
            "time": time.time()-t0,
            "dyn": dynamic_obs,
            "init": init_path
        }

    # -------- METRICS -------- #
    def dist(self, path):
        return round(sum(self.h(path[i-1], path[i]) for i in range(1,len(path))), 3)

    def turns(self, path):
        t = 0
        for i in range(1, len(path)-1):
            if (path[i][0]-path[i-1][0], path[i][1]-path[i-1][1]) != \
               (path[i+1][0]-path[i][0], path[i+1][1]-path[i][1]):
                t += 1
        return t

    def report(self):
        if not self.result:
            print("Run simulation first")
            return

        r = self.result

        print("\n===== METRICS =====")
        print("Density:", self.level)
        print("Start:", self.start)
        print("Goal:", self.goal)
        print("Distance:", self.dist(r["track"]))
        print("Replans:", r["replans"])
        print("Dynamic Obstacles:", len(r["dyn"]))
        print("Turns:", self.turns(r["track"]))
        print("Time:", round(r["time"]*1000, 3), "ms")
        print("===================\n")

    # -------- VISUAL -------- #
    def show(self):
        if not self.result:
            return

        img = np.ones((SIZE, SIZE, 3))

        for i in range(SIZE):
            for j in range(SIZE):
                if self.grid[i][j] == 1:
                    img[i][j] = [0,0,0]
                elif self.grid[i][j] == 2:
                    img[i][j] = [1,0,0]

        for r,c in self.result["track"]:
            img[r][c] = [0,0.6,1]

        sr,sc = self.start
        gr,gc = self.goal

        img[sr][sc] = [0,1,0]
        img[gr][gc] = [1,0,0]

        plt.imshow(img)
        plt.title("Dynamic UGV Path")
        plt.show()

    # -------- MENU -------- #
    def run(self):
        while True:
            print("\n1. Generate Grid")
            print("2. Set Points")
            print("3. Run Simulation")
            print("4. Show Metrics")
            print("5. Exit")

            ch = input("Choice: ")

            if ch == "1":
                print("1 Low | 2 Medium | 3 High")
                d = input("Density: ")
                if d in LEVEL_MAP:
                    self.level, val = LEVEL_MAP[d]
                    self.create_world(val)
                    print("Grid ready")

            elif ch == "2":
                if self.grid is None:
                    print("Generate grid first")
                else:
                    self.set_points()

            elif ch == "3":
                if self.grid is None or self.start is None:
                    print("Setup first")
                    continue

                self.result = self.simulate()

                if self.result:
                    print("Simulation done")
                    self.show()
                else:
                    print("No path possible")

            elif ch == "4":
                self.report()

            elif ch == "5":
                break

            else:
                print("Invalid")


if __name__ == "__main__":
    sim = DynamicUGV()
    sim.run()
