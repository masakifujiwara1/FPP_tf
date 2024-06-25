import numpy as np
import matplotlib.pyplot as plt
import math

# 軌跡（0 <= t <= 7）
trajectories = np.array((
    [
        [
            [[ 1.76405235,  0.40015721],
            [ 0.97873798,  2.2408932 ],
            [ 1.86755799, -0.97727788],
            [ 0.95008842, -0.15135721]],

            [[ 1.66083349,  0.81075571],
            [ 1.12278156,  3.69516671],
            [ 2.62859572, -0.85560286],
            [ 1.39395165,  0.18231712]],

            [[ 3.15491257,  0.60559745],
            [ 1.43584926,  2.84107097],
            [ 0.0756059 , -0.20198427],
            [ 2.25838785, -0.5598479 ]],

            [[ 5.42466719, -0.84876823],
            [ 1.48160777,  2.65388712],
            [ 1.60838511,  1.2673745 ],
            [ 2.41333527, -0.18168538]],

            [[ 4.53688144, -2.8295647 ],
            [ 1.13369562,  2.81023609],
            [ 2.83867579,  2.46975435],
            [ 2.02600846, -0.48398813]],

            [[ 3.48832848, -4.24958263],
            [-0.57257457,  4.76101148],
            [ 2.32902361,  2.03168005],
            [ 0.7732131 ,  0.29350222]],

            [[ 1.87443063, -4.46232291],
            [-1.46804113,  5.14791398],
            [ 1.81821848,  0.85104787],
            [ 0.74503087,  0.72183409]],

            [[ 1.94094785, -4.15985102],
            [-2.10236322,  4.78517281],
            [ 1.14575803,  0.4914947 ],
            [-0.06811541, -1.00444851]]
        ]
    ]
))

# シミュレーションのパラメータ
batch_size = 1
sequence_length = 8
num_pedestrians = 4
coordinates = 2

ped1_trajectory = trajectories[0, :, 0, :]
end_x, end_y = ped1_trajectory[-1]

dx = ped1_trajectory[-1, 0] - ped1_trajectory[-2, 0]
dy = ped1_trajectory[-1, 1] - ped1_trajectory[-2, 1]
theta = math.atan2(dy, dx)

# 座標変換を行う関数
def transform_coordinates(x, y, end_x, end_y, theta):
    x_ = (x - end_x) * math.cos(theta) + (y - end_y) * math.sin(theta)
    y_ = -(x - end_x) * math.sin(theta) + (y - end_y) * math.cos(theta)
    return x_, y_

# 変換後の軌道データを格納する配列
transformed_trajectories = np.zeros_like(trajectories)

# 各歩行者の軌道データを変換
for i in range(num_pedestrians):
    for t in range(sequence_length):
        x, y = trajectories[0, t, i]
        x_, y_ = transform_coordinates(x, y, end_x, end_y, theta)
        transformed_trajectories[0, t, i] = [x_, y_]

# 1人目の歩行者に対するその他の歩行者の相対位置を計算する関数（変換後）
def calculate_transformed_relative_positions(transformed_trajectories):
    transformed_relative_positions = np.zeros_like(transformed_trajectories)
    ped1_transformed_positions = transformed_trajectories[0, :, 0, :]
    
    for i in range(1, num_pedestrians):
        for t in range(sequence_length):
            transformed_relative_positions[0, t, i] = transformed_trajectories[0, t, i] - ped1_transformed_positions[t]
    
    return transformed_relative_positions

# 変換後の相対位置を計算
transformed_relative_positions = calculate_transformed_relative_positions(transformed_trajectories)

plt.figure(figsize=(10, 10))

colors = ['red', 'blue', 'green', 'orange']
for i in range(1, num_pedestrians):
    pedestrian_transformed_relative_trajectory = transformed_relative_positions[0, :, i, :]
    plt.plot(pedestrian_transformed_relative_trajectory[:, 0], pedestrian_transformed_relative_trajectory[:, 1], marker='o', color=colors[i], label=f'Pedestrian {i+1} relative to Pedestrian 1')
    plt.plot(pedestrian_transformed_relative_trajectory[0, 0], pedestrian_transformed_relative_trajectory[0, 1], marker='*', color=colors[i], markersize=12)  # 初めのフレームのマーカーを強調

plt.title('Pedestrian Trajectories in World Coordinates')
plt.xlabel('X Coordinate')
plt.ylabel('Y Coordinate')
plt.legend()
plt.grid(True)
plt.show()

if __name__ == '__main__':
    pass