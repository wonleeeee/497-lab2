import socket
import threading
import pickle
import time

port_list = [65432, 65433, 65434] # server1, server2, server3
server_index = -1
while (server_index == -1):
    try:
        temp_index = int(input("Choose server index [0, 1, 2]: "))
        if (temp_index < 3 and temp_index > -1):
            server_index = temp_index
    except TypeError:
        print('Please enter valid integer')

HOST = '127.0.0.1'
PORT = port_list[server_index]
RDCN = "DC" + str(server_index)

s1 = sersock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2 = sersock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s3 = sersock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

connectionCheck = 0

serverSocketList = [s1, s2, s3]
clientSocketList = []

# dependency list for each client
dependencyDict = {}     # {clientname->string: dependencyList->list [<key, (clock, Sid)>]}
keyValueDict = {}       # {key: value}

local_clock = 0
delayed_write = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen()

def client_connection(conn):
    info = pickle.loads(conn.recv(1024))
    username = info[0]

    # Create empty dependancy list for each client when connected
    print("user '" + username + "' connected")
    dependencyDict[username] = []

    try:
        while True:
            # Receives list that includes command and data from client
            data = pickle.loads(conn.recv(1024))
            global local_clock
            global connectionCheck
            print('Received', data[0])

            # When receive write command
            if data[0] == 'write':
                key = data[1]
                value = data[2]

                # Update local_clock and key-value dictionary
                keyValueDict[key] = value
                local_clock += 1
                print("w - add key-value:", key + ": " + value + " and new local time == " + str(local_clock))

                # Send replicated write and current dependency list to other data centers
                for i in range(3):
                    if i != server_index:
                        # Create new socket for other data centers
                        if (connectionCheck < 2):
                            serverSocketList[i].connect((HOST, port_list[i]))
                            serverSocketList[i].sendall(pickle.dumps(['Data Center-' + str(server_index)]))
                            connectionCheck += 1

                        # Sleep different amount of time for each server connection
                        print("w - Sleep for " + str((i+server_index)*(server_index+1)) + " then send to DC"+str(i))
                        time.sleep((i+server_index)*(server_index+1))

                        # Send msg
                        smsg = ["replicated-write", key, value, username, dependencyDict[username]]
                        serverSocketList[i].sendall(pickle.dumps(smsg))
                        
                # Update local dependency list
                dependencyDict[username] = [(key, (local_clock, server_index))]

            # When receive read command
            elif data[0] == 'read':
                key = data[1]

                # When valid key received
                if (key in keyValueDict):
                    # Send response with value 
                    conn.sendall(pickle.dumps(keyValueDict[key]))

                    # Update dependency list
                    dependencyDict[username] = [(key, (local_clock, server_index))]
                    print("r - Read key-value: " + key + ": " + keyValueDict[key] + " and update depList")

                # Return message when client requests for invalid key
                else:
                    conn.sendall(pickle.dumps("No such key in server"))
            
            # When receive replicated write command from other data center
            elif data[0] == "replicated-write":
                key = data[1]
                value = data[2]
                username = data[3]
                depList = data[4]

                # Dependency check
                # When empty dependency list
                if depList == []:
                    local_clock += 1
                    dependencyDict[username] = depList
                    keyValueDict[key] = value
                    print("rw - add key-value:", key + ": " + value + " and new local time == " + str(local_clock))

                # When dependency list exists, compare local time
                elif depList[0][1][0] == local_clock:
                    local_clock += 1
                    dependencyDict[username] = depList
                    keyValueDict[key] = value

                    print("rw - add key-value:", key + ": " + value + " and new local time == " + str(local_clock))

                    # If there is delayed write, compare updated local time
                    if delayed_write != []:
                        if delayed_write[0][4][0][1][0] == local_clock:
                            data = delayed_write[0]
                            local_clock += 1
                            dependencyDict[data[3]] = data[4]
                            keyValueDict[data[1]] = data[2]
                            delayed_write.remove(data)
                            print("rw - add delayed key-value:", data[1] + ": " + data[2] + " and new local time == " + str(local_clock))

                # When dependency check fails, delay the write command
                else:
                    delayed_write.append(data)
                    requiredTime = data[4][0][1][0]
                    print("rw - Delay write: data == " + str(data) + ", required time ==", str(requiredTime))

    except ConnectionResetError:
        print('connection lost')
        clientSocketList.remove(conn)

while True:
    conn, addr = s.accept()
    clientSocketList.append(conn)
    threading.Thread(target=client_connection, args=([conn])).start()
