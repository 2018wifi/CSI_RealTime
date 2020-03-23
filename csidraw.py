import random
import numpy as np
import matplotlib.pyplot as plt
from glovar import *
from mpl_toolkits.mplot3d import Axes3D

'''定义参数'''
ax = [i for i in range(-int(NFFT / 2), int(NFFT / 2))]  # 定义一个 x 轴的空列表


def real_time_draw(ay1, ay2):
    # print(ay2)
    for i in [0, 29, 30, 31, 32, 33, 34, 35]:
        ay1[i] = 0
        ay2[i] = 0
    # print(ay2)
    ay1 = np.hstack((ay1[0:32], ay1[32:64]))
    ay2 = np.hstack((ay2[0:32], ay2[32:64]))

    plt.clf()  # 清除之前画的图
    plt.ylabel('SNR')
    plt.xlabel('Subcarrier')
    plt.xlim(-int(NFFT / 2), int(NFFT / 2))
    plt.plot(ax, ay1, 'red')  # 初始状态的图
    plt.plot(ax, ay2, 'cyan')  # 当前状态
    ay3 = ay2 - ay1
    plt.plot(ax, ay3, 'b')  # 差值
    plt.pause(0.1)  # 暂停
    # plt.show()
    # plt.ioff()  # 关闭画图的窗口


def threeD_draw(Z_list):
    fig = plt.figure()
    ax = Axes3D(fig)
    X = np.arange(0, NFFT, 1)
    Y = np.arange(0, MAX, 1)
    X, Y = np.meshgrid(X, Y)
    Z = np.array(Z_list)
    # print(Z.shape)
    # help(ax.plot_surface)
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='coolwarm')
    plt.show()

# def pcr_main(ay1, ay2):
#     '''随机数，这里应该传'''
#     for i in range(NFFT):
#         ay1.append(random.randint(1000, 3000))
#     ''''''''''''''''''''''''''
#     plt.ion()  # 开启一个画图的窗口
#     for n in range(MAX):
#         '''随机数，这里应该传'''
#         for i in range(NFFT):
#             ay2.append(random.randint(1000, 8000))
#         ''''''''''''''''''''''''''
#         Z_list[n] = ay2
#         real_time_draw(ax, ay1, ay2)
#     draw()
