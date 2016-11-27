""""Loader class that coordinates loading of data samples and converting them to XY array"""

import os, fnmatch
import numpy as np
from preprocessor import DataPreprocessor
from data.paths import Paths
from data.features import Features


class Loader:
    def load_data(self):
        warming_file_names = fnmatch.filter(os.listdir(Paths.raw_data), '*A.wav')
        boiling_file_names = fnmatch.filter(os.listdir(Paths.raw_data), '*B.wav')

        pp = DataPreprocessor()

        warming_data = self.load_samples(warming_file_names)
        boiling_data = self.load_samples(boiling_file_names)

        data = []
        data.extend(warming_data)
        data.extend(boiling_data)

        target = np.zeros(len(warming_data) + len(boiling_data)) # set zero for feature of class 1 (warming water)
        for index in range(len(warming_data),len(warming_data) + len(boiling_data)):
            target[index] = 1 # set one for feature of class 2 (boiling water)

        X = np.array(data)
        Y = target
        return X, Y

    def load_samples(self, files):
        samples = []
        pp = DataPreprocessor()
        for file in files:
            samples.extend(pp.preprocess(file))
        return samples

if __name__ == '__main__':
    l = Loader();
    X, Y = l.load_data();   
    print "Loader selftest..."
    print "X: "
    print X
    print "Y: " + str(Y)  
    print "Done!"