from main import CSI
import csi_receive
import socket
import math

csi = CSI('test.txt')
PORT = 5500
local_matrix = []
for i in range(100):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(('255.255.255.255', PORT))
    local_matrix = []
    buffer, address = s.recvfrom(65535)
    print('Server received from {}:{}'.format(address, buffer))
    data = csi_receive.parse(buffer)
    # header = read_header(data)
    local_vector = csi_receive.read_csi(data)
    local_matrix.append(local_vector)
temp_bn = [[0 for i in range(len(local_vector))]for j in range(local_matrix)]
for i in range(len(local_matrix)):
    for j in range(len(local_vector)):
        temp_bn[i][j] = math.sqrt(local_matrix[i][j][0] ** 2 + local_matrix[i][j][1] ** 2)
new_bn = []
for i in range(len(local_vector)):
    sum_column = 0
    for j in range(len(local_matrix)):
        sum_column = sum_column + temp_bn[j][i]
    new_bn.append(sum_column/len(local_matrix))
csi.update_bn(new_bn)

