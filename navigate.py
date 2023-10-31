"""
GUI grid of 20 by 8 cells where each is a button that can be clicked to change its color.
User can select starting and ending cells, and then click a button to find the shortest path between them.
"""
import tkinter as tk
from queue import Queue

def on_cell_click(x, y):
    if grid[x][y]["bg"] == "white":
        grid[x][y].config(bg="blue")
    else:
        grid[x][y].config(bg="white")

# ask for start and end
def ask_for_position():
    global selected_x, selected_y
    selected_x, selected_y = 0, 0
    while True:
        try:
            selected_x = int(input("Enter x coordinate: "))
            selected_y = int(input("Enter y coordinate: "))
            break
        except ValueError:
            print("Invalid input. Try again.")

def set_start():
    global start
    ask_for_position()
    start = (selected_x, selected_y)
    grid[selected_x][selected_y].config(bg="green")

def set_end():
    global end
    ask_for_position()
    end = (selected_x, selected_y)
    grid[selected_x][selected_y].config(bg="red")

import heapq

def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def find_path():
    global start, end
    if start is None or end is None:
        print("Start or end not set")
        return

    open_set = [(0, start)]
    came_from = {}
    g_score = {(x, y): float("inf") for x in range(20) for y in range(8)}
    g_score[start] = 0

    while open_set:
        current = heapq.heappop(open_set)[1]
        if current == end:
            # Reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()

            # Change the color of the path cells to yellow
            for cell in path:
                grid[cell[0]][cell[1]].config(bg="yellow")
            return

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if 0 <= neighbor[0] < 20 and 0 <= neighbor[1] < 8:
                if grid[neighbor[0]][neighbor[1]]["bg"] == "blue":
                    continue

                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor))


root = tk.Tk()

# gotta clear tha paths

grid = []
start = None
end = None
selected_x, selected_y = 0, 0

for x in range(20):
    row = []
    for y in range(8):
        button = tk.Button(root, text=f"{x},{y}", bg="white", command=lambda x=x, y=y: on_cell_click(x, y))
        button.grid(row=x, column=y, sticky="nsew")
        row.append(button)
    grid.append(row)

tk.Button(root, text="Set Start", command=set_start).grid(row=20, column=0)
tk.Button(root, text="Set End", command=set_end).grid(row=20, column=1)
tk.Button(root, text="Find Path", command=find_path).grid(row=20, column=2)

root.mainloop()
