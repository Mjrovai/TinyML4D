#  Microphone Test
#  The data captured by the microphone will be displayed on Serial Monitor
#
#  mic_test.py - By: marcelo_rovai - Tue Aug 22 2023


import audio
from ulab import numpy as np

CHANNELS = 1

raw_buf = None
audio.init(channels=CHANNELS, frequency=16000, gain_db=24, highpass=0.9883)

def audio_callback(buf):
    # NOTE: do Not call any function that allocates memory.
    global raw_buf
    if (raw_buf == None):
        raw_buf = buf

# Start audio streaming
audio.start_streaming(audio_callback)


while (True):
    if (raw_buf != None):
        pcm_buf = np.frombuffer(raw_buf, dtype=np.int16)
        raw_buf = None
        print(max(pcm_buf))

# Stop streaming
audio.stop_streaming()

