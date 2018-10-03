#!/usr/bin/env python3

## ---------- VA Prototype ----------

import boto3
import numpy as np 
import sounddevice as sd
import pyaudio

## ---------- Helper Function ----------
def record(seconds):
    """
    Recording specific seconds and return byte string in following format:
        - little endian 
        - 2 byte signed int
        - sampling rate 8k 
        - mono 
    """
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 8000
    
    p = pyaudio.PyAudio()
    stream = p.open(format = FORMAT, 
                    channels = CHANNELS, 
                    rate = RATE, 
                    input = True, 
                    frames_per_buffer = CHUNK)
    print("\trecording ...")
    frames = []
    for i in range(0, int(RATE / CHUNK * seconds)):
        data = stream.read(CHUNK)
        frames.append(data)
    print("\tDone recording!")

    stream.stop_stream()
    stream.close()
    p.terminate()
    
    return b''.join(frames)
    

client = boto3.client('lex-runtime', region_name="us-west-2")
polly = boto3.client("polly")

print("Conversation Begin ...\n")
isFailed = False
while True:
    print("> How many second to record? ", end="")
    seconds = input()

    lpcm = record(int(seconds))

    response = client.post_content(
        botName = "musicBot", 
        botAlias = "songRequestor",
        userId = "brian", 
        sessionAttributes = {
        
        }, 
        requestAttributes = {
        }, 
        contentType = "audio/lpcm; sample-rate=8000; sample-size-bits=16; channel-count=1; is-big-endian=false", 
        accept = 'audio/pcm', 
        inputStream = lpcm
    )
    if response["dialogState"] == 'ReadyForFulfillment': break
    elif response["dialogState"] == "Failed": isFailed = True
    
##    # Play Music
##    pollySaid = polly.synthesize_speech(
##                   LexiconNames = [], 
##                   OutputFormat = "pcm",
##                   SampleRate = "8000", 
##                   Text = response["message"], 
##                   TextType = "text", 
##                   VoiceId = "Amy",
##                   LanguageCode = "en-US"
##                )
##    content = np.fromstring(pollySaid["AudioStream"].read(), dtype="<i2")
##    # convert speech from 16 signed integer to float point number
##    MAX = 32768.0
##    speech = np.array([x / MAX for x in content])
##    sd.play(speech, 8000)

    content = np.fromstring(response["audioStream"].read(), dtype="<i2")
    sd.play(content, 16000)

    # Print Message
    print(response["message"])
    
    if isFailed: break
if not isFailed:
    print("\n///// Request Information ///// ")
    for keys in response["slots"].keys():
        print("  * " + keys + ": " + response["slots"][keys])
    print("\n\nConversation END!")
