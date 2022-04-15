import random
import socket

# HOST = '127.0.0.1'
# PORT = random.randint(49152, 65431)

port_list = [65432, 65433, 65434] # server1, server2, server3
server_index = -1
while (server_index == -1):
    try:
        temp_index = input(int("Choose server index from [0, 1, 2]"))
        if (temp_index < 3 and temp_index > -1):
            server_index = temp_index
    except:
        print('Please enter valid integer')

cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(('127.0.0.1', port_list[server_index]))

username = input('Enter username: ')