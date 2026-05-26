import numpy as np
import matplotlib.pyplot as plt

def neighbor_sum(grid, row, col):
    rows, cols = grid.shape
    total = 0

    for i in range(max(0, row-1), min(rows, row+2)):
        for j in range(max(0, col-1), min(cols, col+2)):
            if i == row and j == col:
                continue
            total += grid[i][j]

    return total

life_probability = 0.3
grid=64
life = (np.random.rand(grid,grid) < life_probability).astype(int)
plt.ion()
fig, ax = plt.subplots()
img = ax.imshow(life, cmap='binary')

for gen in range(1000):
    new_life = life.copy()
    for i in range(grid):
        for j in range(grid):
            neighbors = neighbor_sum(life, i, j)
            if life[i][j] == 1:
                if neighbors < 2 or neighbors > 3:
                    new_life[i][j] = 0
            else:
                if neighbors == 3:
                    new_life[i][j] = 1

    life = new_life

    img.set_data(life)
    plt.pause(0.01)

plt.ioff()
plt.show()