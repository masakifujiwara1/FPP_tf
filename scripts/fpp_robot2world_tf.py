import numpy as np
import matplotlib.pyplot as plt
import math

def tf_x(x, y, end_x, end_y, theta):
    x_ = (x - end_x) * math.cos(theta) + (y - end_y) * math.sin(theta)
    return x_

def tf_y(x, y, end_x, end_y, theta):
    y_ = -(x - end_x) * math.sin(theta) + (y - end_y) * math.cos(theta)
    return y_

# ToDo computing relative pose with (tf_ped - tf_ped2robot)
def relative_pos():
    pass

# ロボットと見なす歩行者の軌跡（0 <= t <= 10）
ped2robot = np.array((
    [1, 2],
    [2, 3],
    [3, 4],
    [4, 5],
    [5, 6],
    [6, 7],
    [6.5, 7.5],
    [6.95, 5],
    [7.5, 4],
    [8, 6]
))

dx = ped2robot[-1, 0] - ped2robot[-2, 0]
dy = ped2robot[-1, 1] - ped2robot[-2, 1]

theta = math.atan2(dy, dx)
end_x = ped2robot[-1, 0]
end_y = ped2robot[-1, 1]

# 見なしロボットの座標変換
transformed_xy = []
for [x, y] in ped2robot:
    x_ = tf_x(x, y, end_x, end_y, theta)
    y_ = tf_y(x, y, end_x, end_y, theta)
    transformed_xy.append([x_, y_])
transformed_xy = np.array(transformed_xy)

# 他の歩行者の初期化，及び座標変換
ped1 = []
tf_ped1 = []
ped2 = []
tf_ped2 = []

for [x, y] in ped2robot:
    y1_ = y + np.random.standard_normal()
    y2_ = y + np.random.standard_normal() * 1.5
    ped1.append([x, y1_])
    ped2.append([x, y2_])
    tf_x1_ = tf_x(x, y1_, end_x, end_y, theta)
    tf_y1 = tf_y(x, y1_, end_x, end_y, theta)
    tf_x2_ = tf_x(x, y2_, end_x, end_y, theta)
    tf_y2 = tf_y(x, y2_, end_x, end_y, theta)
    tf_ped1.append([tf_x1_, tf_y1])
    tf_ped2.append([tf_x2_, tf_y2])

ped1 = np.array(ped1)
ped2 = np.array(ped2)
tf_ped1 = np.array(tf_ped1)
tf_ped2 = np.array(tf_ped2)

# pos_plot
plt.plot(ped2robot[:, 0], ped2robot[:, 1])
plt.plot(ped1[:, 0], ped1[:, 1])
plt.plot(ped2[:, 0], ped2[:, 1])

# tf_pos_plot
plt.plot(transformed_xy[:, 0], transformed_xy[:, 1])
plt.plot(tf_ped1[:, 0], tf_ped1[:, 1])
plt.plot(tf_ped2[:, 0], tf_ped2[:, 1])

# visualize
plt.show()

if __name__ == '__main__':
    pass