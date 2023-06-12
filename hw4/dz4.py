import vosk
import sys
import os
import wave
import json
import re
from pprint import pprint
import numpy as np



infile = 'output_file.wav'

model = vosk.Model("vosk-model-small-ru-0.22")
spk_model = vosk.SpkModel('vosk-model-spk-0.4')

def cosine_dist(x, y):
    nx = np.array(x)
    ny = np.array(y)
    return 1 - np.dot(nx, ny) / np.linalg.norm(nx) / np.linalg.norm(ny)



wf = wave.open(infile, "rb")
rcgn_fr = wf.getframerate() * wf.getnchannels()
rec = vosk.KaldiRecognizer(model, rcgn_fr, spk_model)
rec.SetSpkModel(spk_model)
wf.rewind()
result = ''
last_n = False
# read_block_size = 4000
read_block_size = wf.getnframes()

while True:
    data = wf.readframes(read_block_size)
    if len(data) == 0:
        break

    if rec.AcceptWaveform(data):
        res = json.loads(rec.Result())

        if res['text'] != '':
            result += f" {res['text']}"
            if read_block_size < 200000:
                print(res['text'] + " \n")

            last_n = False
        elif not last_n:
            result += '\n'
            last_n = True


# res = json.loads(rec.Result())
# print(res)
# result += f" {res['text']}"
# pprint(result)
