# coding=utf-8
import socket
import struct
import numpy as np


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
    # csi = np.zeros((64,), dtype=np.complex)
    sourceData = data[18:]
    sourceData.dtype = np.int16
    csi_data = sourceData.reshape(-1, 2).tolist()

    # i = 0
    # for x in csi_data:
    #     csi[i] = np.complex(x[0], x[1])
    #     i += 1

    return csi_data

