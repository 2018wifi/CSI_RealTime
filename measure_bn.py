from main import CSI
import csi_receive
import socket
import math

csi = CSI('test.txt')
PORT = 5500
local_matrix = []
for i in range(100):

temp_bn = [[0 for i in range(len(local_vector))]for j in range(len(local_matrix))]
for i in range(len(local_matrix)):
    for j in range(len(local_vector)):
        temp_bn[i][j] = math.sqrt(local_matrix[i][j][0] ** 2 + local_matrix[i][j][1] ** 2)
new_bn = []
for i in range(len(local_vector)):
    sum_column = 0
    for j in range(len(local_matrix)):
        sum_column = sum_column + temp_bn[j][i]
    new_bn.append(sum_column/len(local_matrix))
print(new_bn)
csi.update_bn(new_bn)
