#!/usr/bin/env python3 

## ---------- Receive Binary Audio from Matlab ----------
## 
## FORMAT: 
##      * signed int 16
##      * TCP / IP
## ------------------------------------------------------

import socket
import numpy as np 
import sounddevice as sd
import boto3

server_address = ('localhost', 10000)
chunk_size = 512    # Byte
fs = 8*1e3          # Hz, sampling rate
toPlay = True       # for the sake of Debug

client = boto3.client('lex-runtime', region_name='us-west-2')

## Helper Function:
def decode(binaryString):
    """
    Decode binary string and return float list
    """
    return np.fromstring(binaryString, dtype="<i2")
    

# create a tcp/ip socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

print("  * starting up on {0[0]} port {0[1]}".format(server_address))
sock.bind(server_address)

# Listen for incoming connection 
sock.listen(5)
while True:
    # Wait for connection 
    print('  * waiting for connection ...')
    connection, client_address = sock.accept()

    sigs = []
    bsigs = b''
    receives = []
    try: 
        print('\tconncetion from', client_address)
        # Receive Data in chunck
        while True:
            data = connection.recv(chunk_size)
            if data:
                receives.append(data)
            else:
                print('\tno more data from', client_address)
                break
        # if toTest
        if toPlay:
            for d in receives:
                sigs.extend(decode(d))
            sigs = np.array(sigs)
            print('\tplaying back ...')
            sd.play(sigs, fs)
        
        for d in receives:
            bsigs = bsigs + d

        # push to aws
        response = client.post_content(
            botName = 'musicBot', 
            botAlias = 'songRequestor', 
            userId = 'colin', 
            sessionAttributes = {
            
            },
            requestAttributes = {
            
            },
            contentType = "audio/lpcm; sample-rate=8000; sample-size-bits=16; channel-count=1; is-big-endian=false", 
            accept = 'audio/pcm', 
            inputStream = bsigs
        )

        reply = np.fromstring(response["audioStream"].read(), dtype="<i2")
        
        if 'message' in response.keys():
            print('\tLex says "', response['message'], '"')
            sd.play(reply, 16000)

        if response["dialogState"] == 'ReadyForFulfillment':
            print("\b//////// Request Information //////////")
            for keys in response['slots'].keys():
                print("  * " + keys + ": ", response['slots'][keys])
            print("\n\n CONVERSATION END!! ")
            

    finally:
        # clean up the connection
        connection.close()


