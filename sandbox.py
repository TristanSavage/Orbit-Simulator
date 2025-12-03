import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# x = np.linspace(0, 10, 400)

# fig, ax = plt.subplots()

# # Create artists (empty lines)
# (line1,) = ax.plot([], [], lw=2, label="sin")
# (line2,) = ax.plot([], [], lw=2, label="cos")

# ax.set_xlim(0, 10)
# ax.set_ylim(-1.5, 1.5)
# ax.legend()

# def update(frame):
#     tail = 0
#     if frame > 50:
#         tail = frame - 50

#     line1.set_data(x[tail:frame], np.sin(x[tail:frame]))
#     line2.set_data(x[tail:frame], np.cos(x[tail:frame]))

#     ax.set_title(f"Frame {frame}")
#     # return line1, line2

# ani = FuncAnimation(fig, update, frames=len(x), interval=10)

# plt.show()

# print(type(line1))

# d = {
#     '1' : 1,
#     '2' : 2,
#     '3' : 3,
#     '4' : 4,
#     }
# print(list(*d.values()))

z = np.linspace(0,6.3,10)
x = np.cos(z)
y = np.sin(z)
t = np.array([[0,1,2,3,4]])

print(z.size)
print(x.size)
print(y.size)
print(t.size)

# plt.plot(z,y)
# plt.plot(x,z)
# plt.plot(x + 2,y + 3)
# plt.plot(x*2,y*2)
# plt.plot(x*0.5,y*0.5)
# plt.show()

w = np.linspace(0,6.3,10)
print(w)
w += z
print(w)