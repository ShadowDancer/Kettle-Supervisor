
from array import array

MAX_VOLUME = 16384

def normalize_volume(data):
        "Average the volume of raw file"
        factor = float(MAX_VOLUME)/max(abs(i) for i in data)
        r = array('h')
        for i in data:
            r.append(int(i*factor))
        return r