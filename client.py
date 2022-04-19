import socket
import pickle
import sys

port_list = [65432, 65433, 65434] # server1, server2, server3
server_index = -1
while (server_index == -1):
    try:
        temp_index = int(input("Choose server index from [0, 1, 2]: "))
        if (temp_index < 3 and temp_index > -1):
            server_index = temp_index
    except:
        print('Please enter valid integer')

# Connect to the server
cs = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
cs.connect(('127.0.0.1', port_list[server_index]))

username = input('Enter username: ')

cs.sendall(pickle.dumps([username]))

while True:

    # Receive command from user
    line = input('Choose command [w/r] or exit: ')

    # End the process
    if line == 'exit':
        cs.sendall(pickle.dumps(['end']))
        cs.close()
        sys.exit('Exit program')

    # Receive key and value from user, then send to the server
    elif line == "w":
        print ('write')
        keyInput = input('Enter key: ')
        valueInput = input('Enter value: ')
        smsg = ['write', keyInput, valueInput]
        cs.sendall(pickle.dumps(smsg))

    # Receive key from user, then request the value for the key
    elif line == "r":
        print('read')
        keyInput = input('Enter key: ')
        smsg = ['read', keyInput]
        cs.sendall(pickle.dumps(smsg))
        rmsg = pickle.loads(cs.recv(1024))
        print("Received ", rmsg)
        
    else:
        print('Enter valid command')