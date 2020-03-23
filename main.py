# coding=utf-8
import math
import socket
import threading
import numpy as np
from copy import deepcopy

import csidraw
import csi_receive
from glovar import *    # 配置文件


matrix = np.zeros((step, NFFT), dtype=np.complex)   # 子载波数×步长
processed_matrix = np.zeros((step, NFFT), dtype=np.complex)   # 处理过后的幅值矩阵
magic_1 = 0
magic_2 = 0


class CSI:
    def __init__(self, bn_file):  # 读入底噪
        self.bn_file = bn_file
        file = open(self.bn_file, mode='r')
        self.background_noise = list(float(i.strip('\n')) for i in file.readlines())
        file.close()
        # print(self.background_noise)

    def update_bn(self, new_bn):  # 更新底噪
        file = open(self.bn_file, mode='w')
        for i in new_bn:
            self.background_noise = file.write(str(i) + '\n')
        file.close()

    def get_csi(self, lk):
        global matrix
        global magic_1

        PORT = 5500
        while True:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            s.bind(('255.255.255.255', PORT))
            
            local_matrix = np.zeros((NFFT, step), dtype=np.complex)
            for i in range(step):
                buffer, address = s.recvfrom(65535)
                # print('Server received from {}:{}'.format(address, buffer))
                data = csi_receive.parse(buffer)
                local_vector = csi_receive.read_csi(data, NFFT)
                local_matrix[i] = local_vector
            print(local_matrix)
            if magic_1 == 0:  # 状态为等待接收时传入数据
                lk.acquire()
                matrix = local_matrix  # 赋值给matrix
                magic_1 = 1  # 转入状态1，等待处理
                lk.release()

    def process(self, lk):
        global matrix
        global processed_matrix
        global magic_1
        global magic_2

        while True:
            if magic_1 == 1:  # 状态为待处理时进行处理
                lk.acquire()
                local_matrix = matrix
                magic_1 = 0  # 转入状态0，等待接收
                lk.release()
                processed_matrix = np.abs(local_matrix)

    def plot(self, lk):
        global processed_matrix
        global magic_2

        while True:
            local_matrix = processed_matrix
            for local_vector in local_matrix:
                csidraw.real_time_draw(self.background_noise, local_vector.tolist())

    def work(self):  # 多线程工作
        lock = threading.Lock()
        get_t = threading.Thread(target=self.get_csi, args=(lock,))
        process_t = threading.Thread(target=self.process, args=(lock,))
        # print(self.background_noise)
        plot_t = threading.Thread(target=self.plot, args=(lock,))
        get_t.start()
        process_t.start()
        plot_t.start()
        get_t.join()
        process_t.join()
        plot_t.join()


if __name__ == '__main__':
    csi = CSI('noise.txt')
    # csi.update_bn([100 for i in range(NFFT)])
    csi.work()
