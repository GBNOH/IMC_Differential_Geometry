import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Create data
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
X, Y = np.meshgrid(x, y)
Z = np.sin(np.sqrt(X**2 + Y**2))

# Create figure
fig = plt.figure(figsize=(7, 6))
ax = fig.add_subplot(111, projection='3d')

# Draw surface
ax.plot_surface(X, Y, Z, cmap='viridis', edgecolor='none')

ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")

# Rotation function
def update(frame):
    ax.view_init(elev=250, azim=frame)
    return []

# Animate
ani = FuncAnimation(
    fig,
    update,
    frames=np.arange(0, 360, 2),
    interval=50,
    blit=False
)

plt.show()