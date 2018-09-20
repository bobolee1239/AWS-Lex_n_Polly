#!/usr/bin/env python3

import boto3
import numpy as np 
import sounddevice as sd

client = boto3.client('lex-runtime', region_name="us-west-2")
polly = boto3.client("polly")

print("Conversation Begin ...\n")
isFailed = False
while True:
    print("> ", end="")
    request = input("> ")
    response = client.post_text(
        botName = "musicBot", 
        botAlias = "songRequestor",
        userId = "brian", 
        sessionAttributes = {
        
        }, 
        requestAttributes = {
        }, 
        inputText = request
    )
    if response["dialogState"] == 'ReadyForFulfillment': break
    elif response["dialogState"] == "Failed": isFailed = True
    
    # Play Music
    pollySaid = polly.synthesize_speech(
                   LexiconNames = [], 
                   OutputFormat = "pcm",
                   SampleRate = "8000", 
                   Text = response["message"], 
                   TextType = "text", 
                   VoiceId = "Amy",
                   LanguageCode = "en-US"
                )
    content = np.fromstring(pollySaid["AudioStream"].read(), dtype="<i2")
    # convert speech from 16 signed integer to float point number
    MAX = 32768.0
    speech = np.array([x / MAX for x in content])
    sd.play(speech, 8000)

    # Print Message
    print(response["message"])
    
    if isFailed: break
if not isFailed:
    print("\n///// Request Information ///// ")
    for keys in response["slots"].keys():
        print("  * " + keys + ": " + response["slots"][keys])
    print("\n\nConversation END!")
