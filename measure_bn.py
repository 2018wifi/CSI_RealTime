import csi_receive
import numpy as np
from main import CSI
from glovar import *

csi = CSI('noise.txt')
bn_matrix = ((abs(csi_receive.get_bn(bn_step))).sum(axis=1)) / bn_step        # 获取矩阵后对每个复数求模，再对列叠加，最后除以样本数

csi.update_bn(bn_matrix)
