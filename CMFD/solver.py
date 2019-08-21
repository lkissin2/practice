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

    def phi_1(self, N, source, phi_prev):
        # guess = self.guess
        phi_1 = phi_prev.copy()
        for i in range(N):  # CENTRAL FINITE DIFFERENCE DIFFUSION
            if self.grid[i] > 0 and self.grid[i] < G.r:
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
            if self.grid[i] > 0 and self.grid[i] < G.r:
                phi_2[i] = (F.S[i] * phi_1[i] + T.D[i] / self.dx ** 2 *
                            (phi_prev[i+1] + phi_prev[i-1])) * \
                            (1 / (T.A[i] + 2 * T.D[i] / self.dx ** 2))
            elif self.grid[i] == G.r:
                phi_2[i] = T.D[i] / (self.dx + 3) * (4 * phi_2[i-1] -
                                                     phi_2[i-2])
            else:
                phi_2[i] = phi_2[i+1]
        return phi_2

    def source_update(self, N, phi_1, phi_2, k):
        S = []
        for i in range(N):
            S.append((F.F[i] * phi_1[i] + T.F[i] * phi_2[i]) / k)
        return S

    def k_update(self, k_prev, source_prev, source_pres):
        return k = k_prev * source_pres / source_prev

    def convergence_checker(self, k, k_prev):
        if k - k_prev > 10 ** -3:
            return False
        else:
            return True


flux = flux()
phi_1_1 = flux.phi_1(N, flux.source_guess, flux.phi_1_guess)
print(phi_1_1)
phi_2_1 = flux.phi_2(N, phi_1_1, flux.phi_2_guess)
print(phi_2_1)
S_1 = flux.source_update(N, phi_1_1, phi_2_1, 1.3)
print(S_1)


plt.plot(flux.grid, phi_1_1, label='fast')
plt.plot(flux.grid, phi_2_1, label='thermal')
plt.plot(flux.grid, S_1, label='source')
plt.legend()
plt.show()
