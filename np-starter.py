"""
Initialize utility functions for numpy

Usage:

function yy-np() { python3 -i $YY_SCRIPTS/np-starter.py }

"""

import numpy as np

array = np.array
inv = np.linalg.inv

def arr(s):
    t = list(map(lambda x: eval(x), s.split()))
    size = int(len(t)**0.5)
    return array(t).reshape((size, size))
