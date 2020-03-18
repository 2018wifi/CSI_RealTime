import threading
import math
import csidraw
import random
import csi_receive
import socket

step = 1  # 步长
matrix = [[[0, 0] for i in range(64)] for i in range(step)]  # 从邹老板那里读到的复数矩阵
processed_data = [[0 for i in range(64)] for i in range(step)]  # 处理过后交给彭老板的幅值矩阵
magic_1 = 0
magic_2 = 0
NFFT = 64

def zlw(lk):
    global matrix
    global magic_1
    PORT = 5500

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('255.255.255.255', PORT))
    while True:
        local_matrix = []
        for i in range(step):
            buffer, address = s.recvfrom(65535)
            print('Server received from {}:{}'.format(address, buffer))
            data = csi_receive.parse(buffer)
            # header = read_header(data)
            local_vector = csi_receive.read_csi(data)
            local_matrix.append(local_vector)
        # print(csi)
        # ------这里用邹老板的脚本得到一个local_matrix------ #
        csi_receive.receive_csi(local_matrix)
        if magic_1 == 0:  # 中转站没货的时候才能往里边存东西
            lk.acquire()
            matrix = local_matrix  # 把matrix锁住后赶紧赋值，然后解锁
            lk.release()
            magic_1 = 1  # 中转站此时又有货了


def pcr(lk, bn):
    global processed_data
    global magic_2
    while True:
        if magic_2 == 1:  # 中转站有货才能画图
            lk.acquire()
            local_data = processed_data  # 把processed_data锁住后赶紧拷贝，然后解锁
            lk.release()
            for i in local_data:
                csidraw.real_time_draw(bn, [random.randint(1000, 3000) for j in range(64)])
            # csidraw.threeD_draw(local_data)
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

    def processing(self, lk):
        global matrix
        global processed_data
        global magic_1
        global magic_2
        while True:
            if magic_1 == 1:  # 邹老板中转站有货的时候把货取出来
                # print(matrix)
                lk.acquire()
                local_matrix = matrix
                lk.release()
                magic_1 = 0  # 告诉邹老板货已经拿走了
                local_data = [[0 for i in range(NFFT)] for i in range(step)]
                for i in range(step):
                    for j in range(NFFT):
                        local_data[i][j] = math.sqrt(local_matrix[i][j][0] ** 2 + local_matrix[i][j][1] ** 2)
                if magic_2 == 0:  # 彭老板中转站没货时补货
                    lk.acquire()
                    processed_data = local_data  # 为彭老板中转站放入加工好的货物
                    lk.release()
                    magic_2 = 1  # 告诉彭老板货物已经放好了

    def work(self):  # 多线程工作
        lock = threading.Lock()
        get_t = threading.Thread(target=zlw, args=(lock,))
        process_t = threading.Thread(target=self.processing, args=(lock,))
        print(self.background_noise)
        plot_t = threading.Thread(target=pcr, args=(lock, self.background_noise))
        get_t.start()
        process_t.start()
        plot_t.start()
        get_t.join()
        process_t.join()
        plot_t.join()


if __name__ == '__main__':
    csi = CSI('test.txt')
    # print(matrix)
    # csi.update_bn([100 for i in range(NFFT)])
    csi.work()
