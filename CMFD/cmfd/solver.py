import numpy as np
import math as math
import matplotlib.pyplot as plt
import os
import sys
from constants import properties as P

# N = 100  # number of gridpoints


class flux(object):
    """holds all the functions needed to build the flux list"""
    grid = np.linspace(0, P.r, P.N)
    dx = grid[1] - grid[0]
    source_guess = [1 if x < P.bounds[0] else 0 for x in grid]
    phi_1_guess = [1 / P.getXS(P, x, 0, 'd') for x in grid]
    phi_2_guess = [1 / P.getXS(P, x, 1, 'd') for x in grid]

    def phi_1(self, N, source, phi_prev):
        # guess = self.guess
        phi_1 = phi_prev.copy()
        for i in range(N):  # CENTRAL FINITE DIFFERENCE DIFFUSION
            x = self.grid[i]
            if x > 0 and x < P.r:
                phi_1[i] = (source[i] + P.getXS(P, x, 0, 'd') / self.dx ** 2
                            * (phi_prev[i+1] + phi_prev[i-1])) / \
                            (2 * P.getXS(P, x, 0, 'd') / self.dx ** 2 +
                             P.getXS(P, x, 0, 'r'))
            elif self.grid[i] == P.r:  # VACUUM
                phi_1[i] = P.getXS(P, x, 0, 'd') / \
                           (self.dx + 3) * (4 * phi_1[i-1] - phi_1[i-2])
            else:  # SYMMETRY
                phi_1[i] = phi_1[i + 1]
        return phi_1

    def phi_2(self, N, phi_1, phi_prev):
        phi_2 = phi_prev.copy()
        for i in range(N):
            x = self.grid[i]
            if x > 0 and x < P.r:
                phi_2[i] = (P.getXS(P, x, 0, 's') * phi_1[i] +
                            P.getXS(P, x, 1, 'd') / self.dx ** 2 *
                            (phi_prev[i+1] + phi_prev[i-1])) * \
                           (1 / (P.getXS(P, x, 1, 'a') +
                                 2 * P.getXS(P, x, 1, 'd') / self.dx ** 2))

            elif x == P.r:
                phi_2[i] = P.getXS(P, x, 1, 'd') / (self.dx + 3) * \
                           (4 * phi_2[i-1] - phi_2[i-2])
            else:
                phi_2[i] = phi_2[i+1]
        return phi_2

    def source_update(self, N, phi_1, phi_2, k):
        S = []
        for i in range(N):
            x = self.grid[i]
            S.append((P.getXS(P, x, 0, 'f') * phi_1[i] +
                      P.getXS(P, x, 1, 'f') * phi_2[i]) / k)
        return S

    def k_update(self, k_prev, source_prev, source_pres):
        nume = sum(source_pres)
        deno = sum(source_prev)
        return k_prev * nume / deno

    def convergence_checker(self, k, k_prev):
        if abs(k - k_prev) > 10 ** -3:
            return False
        else:
            return True
