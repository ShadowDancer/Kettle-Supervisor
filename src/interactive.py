import sys
sys.path.append("..")

from interactive.audio.recorder import AudioRecorder

from interactive.audio.io import save_recording, load_recording
import time
import os
def print_m(message):
    print(time.strftime('%X') + " " + str(message));

if __name__ == '__main__':
    print_m("Hi!")
    recording = AudioRecorder().record()
    print_m("Recording length: " + str(float(len(recording.sound_data))/recording.bitrate));
    file_name = raw_input("Type name of the recording: ")
    if not file_name.lower().endswith(".wav"):
        file_name += ".wav";    

    directory = os.path.join("data", "raw")
    path = os.path.join("..", "data", "raw", file_name)
    if not os.path.exists(directory):
        os.makedirs(directory)

    print_m("Saving to " + path)
    save_recording(path, recording)
    print_m("Good night")


