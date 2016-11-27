""""Process raw data to samples"""
import os
import numpy as np
from data.paths import Paths
from interactive.audio.io import save_recording, load_recording
from interactive.audio.model import Recording


class DataPreprocessor:
    """Loads and downsamples data of given feature"""
    def _print(self, message):
        if self.silent:
            import time
            print(time.strftime('%X') + " " + str(message))

    def preprocess(self, fileName, silent = True):
        """ loads data files and restyrns array where each row is sample, and each columnt is point in sample """
        recording = load_recording(os.path.join(Paths.raw_data, fileName))
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
    
        result = []
        for split_index, split_element in enumerate(split):
            sample = np.zeros([self.elements_per_sample])
            for elem_index, elem in enumerate(np.array_split(split_element, self.elements_per_sample)):
                sample[elem_index] = elem[0]
            result.append(sample)
 
        self._print('Got elements: ' + str(len(result)))
        
  
        return result
    
    silent = False
    seconds_per_sample = 2
    """number of seconds of recording that make one vector"""
    elements_per_sample = 100
    """length of vector"""
        
if __name__ == '__main__':
    processor = DataPreprocessor()
    processed = processor.preprocess('KoloRobotyki1A.wav', False)
    print str(len(processed))

    recording = load_recording(os.path.join(Paths.raw_data, 'KoloRobotyki1A.wav'))

    print "Testing..."
    if not recording.sound_data[0] == processed[0][0]:
        print "Fail!"
    if not recording.sound_data[877] == processed[0][1]:
        print "Fail!"
    print "Done!"