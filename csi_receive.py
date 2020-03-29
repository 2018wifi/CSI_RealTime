# coding=utf-8
import sys
import socket
import struct
import numpy as np
from glovar import *

PORT = 5500


def get_bn(count):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('255.255.255.255', PORT))

    bn_matrix = np.zeros((count, NFFT), dtype=np.complex)
    for i in range(count):
        buffer, _ = s.recvfrom(65535)
        # print('Server received from {}:{}'.format(address, buffer))
        data = parse(buffer)
        local_vector = read_csi(data)
        bn_matrix[i]=local_vector
    return bn_matrix

def get_csi_local(count, filename):
    matrix = get_bn(count)
    np.save(filename, matrix)

def parse(buffer):      # 解析二进制流
    nbyte = int(len(buffer))        # 字节数
    data = np.array(struct.unpack(nbyte * "B", buffer), dtype=np.uint8)

    return data

def read_header(data):  # 提取头信息
    header = {}

    header["magic_bytes"] = data[:4]
    header["source_mac"] = data[4:10]
    header["sequence_number"] = data[10:12]

    coreSpatialBytes = int.from_bytes(data[12:14], byteorder="little")
    header["core"] = [int(coreSpatialBytes & x != 0) for x in range(3)]
    header["spatial_stream"] = [int(coreSpatialBytes & x != 0) for x in range(3, 6)]

    header["channel_spec"] = data[14:16]
    header["chip"] = data[18:20]

    return header

def read_csi(data):     # 提取CSI信息，并转换成矩阵
    csi = np.zeros(NFFT, dtype=np.complex)
    sourceData = data[18:]
    sourceData.dtype = np.int16
    csi_data = sourceData.reshape(-1, 2).tolist()

    i = 0
    for x in csi_data:
        csi[i] = np.complex(x[0], x[1])
        i += 1

    return csi

if __name__ == '__main__':
    get_csi_local(int(sys.argv[1]), sys.argv[2])
