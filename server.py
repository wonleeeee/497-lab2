import socket
import threading
import pickle

port_list = [65432, 65433, 65434] # server1, server2, server3
server_index = -1
while (server_index == -1):
    try:
        temp_index = input(int("choose server index [0, 1, 2]"))
        if (temp_index < 3 and temp_index > -1):
            server_index = temp_index
    except:
        print('Please enter valid integer')

HOST = '127.0.0.1'
PORT = port_list[server_index]
RDCN = "DC" + str(server_index)

socketList = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(HOST, PORT)
s.listen()

def socket_target(conn):
    try:
        while True:
            data = conn.recv(1024)
    
    except ConnectionResetError:
        print('connection lost')
        socketList.remove(conn)

while True:
    conn, addr = s.accept()
    socketList.append(conn)
    threading.Thread(target=socket_target, args=([conn])).start()