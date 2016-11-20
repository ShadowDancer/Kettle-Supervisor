from sys import byteorder
from array import array

import pyaudio
from model import Recording
from normalization import normalize_volume

class AudioRecorder:
    """Rocords audio data; returns recorded data as wave objects"""

    threshold = 75
    """
    sound threshold treated as silence, 
    recording start and end with should that is trimmed afterwards
    """   

    chunk_size = 1024
    """Size of chunk processed at once"""
    format = pyaudio.paInt16
    
    bitrate = 44100
    """Bits per second"""
    
    silent = False
    """Hide all messages and user interaction"""

    def record(self):
        """
        Record sound from mic and 
        return the data as an array of signed shorts.

        Normalizes the audio, trims silence from the 
        start and end

        Returns sample_size, bitrate, sound_array
        """
        recorder = pyaudio.PyAudio()
        stream = recorder.open(format=self.format, channels=1, rate=self.bitrate,
            input=True, output=True,
            frames_per_buffer=self.chunk_size)

        sound_started = False


        self._print("Start. Waiting for silence...")
        silent_chunks = 0
        while 1:    # wait for silence at beginning
            sound_data = self._read_chunk(stream)
            
            if(self._is_silent(sound_data)):
                silent_chunks += 1 
                if(silent_chunks >= 5):
                    break

        self._print("Ready...")
        while 1:    # wait for sound
            sound_data = self._read_chunk(stream)
            
            if not self._is_silent(sound_data):
                break
        
        self._print("Recording...")
        result = array('h')
        silent_chunks = 0
        chunks_per_second = self.bitrate / self.chunk_size;
        while 1:
            sound_data = self._read_chunk(stream)
            result.extend(sound_data)

            if self._is_silent(sound_data):
                silent_chunks += 1
            else:
                silent_chunks = 0

            if silent_chunks > chunks_per_second * 5:
                break
        self._print("Done!")
        sample_width = recorder.get_sample_size(self.format)
        stream.stop_stream()
        stream.close()
        recorder.terminate()
        self._print("Terimming")

       #result = normalize_volume(result)
        result = self._trim(result)
        self._print("Done")
        return Recording(sample_width, self.bitrate, result)

    def _print(self, message):
        if not self.silent:
            import time
            print(time.strftime('%X') + " " + str(message))

    def _read_chunk(self, stream):
        sound_data = array('h', stream.read(self.chunk_size))
        if byteorder == 'big':
            sound_data.byteswap()
        return sound_data;

    def _is_silent(self, data):
        "Returns 'True' if below the 'silent' threshold"
        return max(data) < self.threshold

    def _trim(self, data):
        "Remove the silence at the start and end"
        def _trim_left(data):
            while abs(data[0])>self.threshold:
                data.pop(0)
            return data
        data = _trim_left(data)
        data.reverse()
        data = _trim_left(data)
        data.reverse()
        return data
