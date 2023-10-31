import math
import matplotlib.pyplot as plt
# Corrected function to plot the path based on the instructions
def plot_path(instructions):
    x, y = 0, 0  # Initial position
    angle = 0  # Initial angle (facing along the positive x-axis)
    x_vals = [x]
    y_vals = [y]

    for instr in instructions:
        cmd, val = instr.split()[0], float(instr.split()[1])

        if cmd == 'x':
            # Compute the new position
            dx = val * math.cos(math.radians(angle))
            dy = val * math.sin(math.radians(angle))
            x += dx
            y += dy
            x_vals.append(x)
            y_vals.append(y)
        elif cmd == 'z':
            angle += val  # Update the angle by adding the turn value

    plt.figure(figsize=(8, 8))
    plt.plot(x_vals, y_vals, marker='o')
    plt.title('Path of the Object')
    plt.xlabel('X Position (m)')
    plt.ylabel('Y Position (m)')
    plt.grid(True)
    plt.show()

# Sample instructions
fp = 'star'
with open(fp, 'r') as f:
    instructions = f.read().splitlines()
plot_path(instructions)
