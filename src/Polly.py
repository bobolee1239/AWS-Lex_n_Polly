#!/usr/bin/env python3

import boto3
import numpy as np 
import sounddevice as sd

client = boto3.client("polly")

response = client.synthesize_speech(
    LexiconNames = [], 
    OutputFormat = "pcm",
    SampleRate = "8000",
#    SpeechMarkTypes = ["ssml"],
    Text = "I'm fuck up, bro", 
    TextType = "text",
    VoiceId = "Brian",
    LanguageCode = "en-US",
)

content = np.fromstring(response["AudioStream"].read(), dtype="<i2")
# convert speech from 16 signed integer to float point number
MAX = 32768.0
speech = np.array([x / MAX for x in content])
sd.play(speech, 8000)

##f = open('speech.mp3', 'wb')
##f.write(response['AudioStream'].read())
##f.close()
