""""Process raw data to samples"""
import os
import numpy as np
from interactive.audio.io import save_recording, load_recording
from interactive.audio.model import Recording


class DataPreprocessor:
    """Klasa odpowiedzialna za wczytywanie i downsampling danych"""
    def _print(self, message):
        if not self.silent:
            import time
            print(time.strftime('%X') + " " + str(message))

    def preprocess(self, fileName, silent = True):
        """ wczytuje plik z danymi i zwraca tablice która w wierszach ma kolejne próbki, a w kolumnach dane w próbce """
        recording = load_recording(os.path.join(self.rawData, fileName))
        rec_seconds = float(len(recording.sound_data))/recording.bitrate        
        frames_per_sample = int(float(recording.bitrate)  * self.seconds_per_sample)
        arrays_number= (len(recording.sound_data) / float(frames_per_sample));

        if not arrays_number.is_integer():
            arrays_number = arrays_number + 1
        arrays_number = int(arrays_number)    
    

        data = np.array(recording.sound_data)
        split = np.array_split(data, arrays_number)

        # remove last element
        if not len(split[0]) == len(split[-1]):
            split.pop()

        self._print('Recording length: ' + str(rec_seconds) + ' chunks: ' + str(len(split)))
    
        result = np.zeros([len(split), self.elements_per_sample])
        for split_index, split_element in enumerate(split):
            
            for elem_index, elem in enumerate(np.array_split(split_element, self.elements_per_sample)):
                result[split_index, elem_index] = elem[0]
 
        self._print('Got elements: ' + str(len(result)))
        
  
        return result
    
    silent = False
    seconds_per_sample = 2
    """number of seconds of recording that make one vector"""
    elements_per_sample = 100
    """length of vector"""
    rawData = os.path.join("..", "data", "raw")
    internimData = os.path.join("..", "data", "interim")

        
if __name__ == '__main__':
    processor = DataPreprocessor()
    processed = processor.preprocess('KoloRobotyki1A.wav')
    print str(len(processed))

    recording = load_recording(os.path.join(processor.rawData, 'KoloRobotyki1A.wav'))

    print "Testing..."
    if not recording.sound_data[0] == processed[0][0]:
        print "Fail!"
    if not recording.sound_data[877] == processed[0][1]:
        print "Fail!"
    print "Done!"