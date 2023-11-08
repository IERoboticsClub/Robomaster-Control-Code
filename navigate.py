"""
GUI grid of 20 by 8 cells where each is a button that can be clicked to change its color.
User can select starting and ending cells, and then click a button to find the shortest path between them.
"""
import tkinter as tk
from queue import Queue

HEIGHT = 33
WIDTH = 5

def on_cell_click(x, y):
    if grid[x][y]["bg"] == "white":
        grid[x][y].config(bg="blue")
    else:
        grid[x][y].config(bg="white")

# ask for start and end
def ask_for_position():
    global selected_x, selected_y
    xy = input("Enter x,y: ")
    selected_x, selected_y = xy.split(",")
    selected_x = int(selected_x)
    selected_y = int(selected_y)



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
    g_score = {(x, y): float("inf") for x in range(HEIGHT) for y in range(WIDTH)}
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
            if 0 <= neighbor[0] < HEIGHT and 0 <= neighbor[1] < WIDTH:
                if grid[neighbor[0]][neighbor[1]]["bg"] == "blue":
                    continue

                tentative_g_score = g_score[current] + 1
                if tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, end)
                    heapq.heappush(open_set, (f_score, neighbor))

def clear_path():
    global start, end
    start = None
    end = None
    for x in range(HEIGHT):
        for y in range(WIDTH):
            if grid[x][y]["bg"] == "yellow":
                grid[x][y].config(bg="white")


def export_grid():
    with open("grid.txt", "w") as f:
        for x in range(HEIGHT):
            for y in range(WIDTH):
                if grid[x][y]["bg"] == "white":
                    f.write("0")
                else:
                    f.write("1")
            f.write("\n")

def import_grid():
    global start, end
    with open("grid.txt", "r") as f:
        for x in range(HEIGHT):
            line = f.readline()
            for y in range(WIDTH):
                if line[y] == "0":
                    grid[x][y].config(bg="white")
                else:
                    grid[x][y].config(bg="blue")
    start = None
    end = None

root = tk.Tk()

# gotta clear tha paths

grid = []
start = None
end = None
selected_x, selected_y = 0, 0


for x in range(HEIGHT):
    row = []
    for y in range(WIDTH):
        button = tk.Button(root, text=f"{x},{y}", bg="white", command=lambda x=x, y=y: on_cell_click(x, y))
        button.grid(row=x, column=y, sticky="nsew")
        row.append(button)
    grid.append(row)

# make scrollable grid
for x in range(HEIGHT):
    root.grid_rowconfigure(x, weight=1)
for y in range(WIDTH):
    root.grid_columnconfigure(y, weight=1)


tk.Button(root, text="Set Start", command=set_start).grid(row=HEIGHT, column=0)
tk.Button(root, text="Set End", command=set_end).grid(row=HEIGHT, column=1)
tk.Button(root, text="Find Path", command=find_path).grid(row=HEIGHT, column=2)
tk.Button(root, text="Clear Path", command=clear_path).grid(row=HEIGHT, column=3)
tk.Button(root, text="Export Grid", command=export_grid).grid(row=HEIGHT, column=4)
tk.Button(root, text="Import Grid", command=import_grid).grid(row=HEIGHT, column=5)

# exit
tk.Button(root, text="Exit", command=root.destroy).grid(row=HEIGHT, column=6)


root.mainloop()
