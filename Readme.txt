# 497-lab2

There are two files for this lab: client.py and server.py.

Both client and server knows every server's IP address and port number.

To begin the server, enter server id from 0 to 2.

After turning on all three servers, client have to choose which server to connect and enter username.

Then, user can enter three type of command: w, r, and end.

  1. w: write command that requires key and value
  2. r: read command that requires key 
  3. end: end command that ends the client process

And servers can also receive three types of request: write, read, and replicated-write
  1. write
     - Creates empty dependency list for the client
     - Adds key value pair to the dictionary named keyValueDict
     - Create socket connection with other two server, if connection hasn't been created
     - Send replicated write request to other two server
         - Sleep mechanism: before sending replicated write, sleep for (sending_server_index + local_server_index)*(local_server_index + 1) 
         - ex) if server 1 sending request to server 2: Sleep for (1+2)*(1+1) = 6 seconds
         - ex) if server 2 sending request to server 1: Sleep for (2+1)*(2+1) = 9 seconds
     - Update local dependency list
  2. read
     - Check if the requested key is in keyValueDict
         - Send value back to client if the key exists
         - Else, send error message
  3. replicated-write
     - Compare the time from replicated write request with local time
         - If received time is bigger than local time, delay the request
         - Else, operate replicated write