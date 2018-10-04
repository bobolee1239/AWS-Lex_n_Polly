#!/usr/bin/env python3

import socket
import sys

# Create a TCP/IP socket 
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the port
server_address = ('localhost', 10000)

print("Starting up on {0[0]} port {0[1]}".format(server_address))

sock.bind(server_address)

# Listening for incoming connection
sock.listen(1)

while True:
    # Wait for a connection
    print("waiting for a connection ...")
    connection, client_address = sock.accept()

    try:
        print("Connection from", client_address)
        
        while True:
            data = connection.recv(16)
            print("receive ", data)

            if data:
                print("sending data back to the client ...")
                connection.sendall(data)
            else:
                print("no more data from", client_address)
                break

    finally:
        # Clean up the connection
        connection.close()


