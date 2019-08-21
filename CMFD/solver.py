import numpy as np
import math as math
import matplotlib.pyplot as plt
import os
import sys
from constants import fast
from constants import thermal
from constants import geometry

N = 100  # number of gridpoints

G = geometry()
F = fast(N)
T = thermal(N)


class flux(object):
    """holds all the functions needed to build the flux list"""
    grid = np.linspace(0, G.r, N)
    guess = [1 for x in grid]
    # def __init__(self):
    #     """creates a guess distribution"""
    #     return guess
    def phi_1(self, N):
        guess = self.guess
        print(guess)

flux = flux()
flux.phi_1(N)
