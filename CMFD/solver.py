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
    dx = grid[1] - grid[0]
    source_guess = [1 if x < G.a else 0 for x in grid]
    phi_1_guess = [1 / d for d in F.D]
    phi_2_guess = [1 / d for d in T.D]
    # def __init__(self):
    #     """creates a guess distribution"""
    #     return guess
    def phi_1(self, N, source, phi_prev):
        # guess = self.guess
        phi_1 = phi_prev.copy()
        for i in range(N):  # CENTRAL FINITE DIFFERENCE DIFFUSION
            if self.grid[i] > 0 and self.grid [i] < G.r:
                phi_1[i] = (source[i] + F.D[i] / self.dx ** 2 * (phi_prev[i+1]
                            + phi_prev[i-1])) / (2 * F.D[i] / self.dx ** 2 +
                                                 F.R[i])
            elif self.grid[i] == G.r:  # VACUUM
                phi_1[i] = F.D[i] / (self.dx + 3) * (4 * phi_1[i-1] -
                                                    phi_1[i-2])
            else:  # SYMMETRY
                phi_1[i] = phi_1[i + 1]
        return phi_1


    def phi_2(self, N, phi_1, phi_prev):
        phi_2 = phi_prev.copy()
        for i in range(N):
            if self.grid[i] > 0 and self.grid [i] < G.r:
                phi_2[i] = (F.S[i] * phi_1[i] + T.D[i] / self.dx ** 2 *
                (phi_prev[i + 1] + phi_prev[i - 1])) * \
                (1 / (T.A[i] + 2 * T.D[i] / self.dx ** 2))
            elif self.grid[i] == G.r:
                phi_2[i] = T.D[i] / (self.dx + 3) * (4 * phi_2[i-1] -
                                                    phi_2[i-2])
            else:
                phi_2[i] = phi_2[i+1]
        return phi_2




flux = flux()
phi_1_1 = flux.phi_1(N, flux.source_guess, flux.phi_1_guess)
print(phi_1_1)
phi_2_1 = flux.phi_2(N, phi_1_1, flux.phi_2_guess)
print(phi_2_1)


plt.plot(flux.grid, phi_1_1, label = 'fast')
plt.plot(flux.grid, phi_2_1, label = 'thermal')
plt.legend()
plt.show()
