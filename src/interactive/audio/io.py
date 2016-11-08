from struct import pack, unpack
from array import array
from model import Recording

import wave

def save_recording(path, recording):
    """Records from the microphone and outputs the resulting data to 'path'"""
    packed_data = pack('<' + ('h'*len(recording.sound_data)), *recording.sound_data)
    wf = wave.open(path, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(recording.sample_width)
    wf.setframerate(recording.bitrate)
    wf.writeframes(packed_data)
    wf.close()

def load_recording(path):
    """Loads sample_width, bitrate, sound_data from given filename"""
    wf = wave.open(path, 'rb')
    sample_width = wf.getsampwidth()
    bitrate = wf.getframerate()
    packed_data = wf.readframes(wf.getnframes())
    sound_data = unpack('<' + ('h'*wf.getnframes()), packed_data)
    return Recording(sample_width, bitrate, array('h', sound_data))