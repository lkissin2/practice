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
            # if self.grid[i] > 0 and self.grid[i] < G.r:
            #     phi_1[i] = (source[i] + F.D[i] / self.dx ** 2 * (phi_prev[i+1]
            #                 + phi_prev[i-1])) / (2 * F.D[i] / self.dx ** 2 +
            #                                      F.R[i])
            x = self.grid[i]
            if x > 0 and x < P.r:
                phi_1[i] = (source[i] + P.getXS(P, x, 0, 'd') / self.dx ** 2
                            * (phi_prev[i+1] + phi_prev[i-1])) / (2 *
                               P.getXS(P, x, 0, 'd') / self.dx ** 2 + P.getXS(P, x, 0, 'r'))
            elif self.grid[i] == P.r:  # VACUUM
                phi_1[i] = P.getXS(P, x, 0, 'd') / (self.dx + 3) * (4 * phi_1[i-1] -
                                                     phi_1[i-2])
            else:  # SYMMETRY
                phi_1[i] = phi_1[i + 1]
        return phi_1

    def phi_2(self, N, phi_1, phi_prev):
        phi_2 = phi_prev.copy()
        for i in range(N):
            x = self.grid[i]
            # if self.grid[i] > 0 and self.grid[i] < G.r:
            #     phi_2[i] = (F.S[i] * phi_1[i] + T.D[i] / self.dx ** 2 *
            #                 (phi_prev[i+1] + phi_prev[i-1])) * \
            #                 (1 / (T.A[i] + 2 * T.D[i] / self.dx ** 2))
            if x > 0 and x < P.r:
                phi_2[i] = (P.getXS(P, x, 0, 's') * phi_1[i] + P.getXS(P, x, 1, 'd') / self.dx ** 2 *
                            (phi_prev[i+1] + phi_prev[i-1])) * \
                            (1 / (P.getXS(P, x, 1, 'a') + 2 * P.getXS(P, x, 1, 'd') / self.dx ** 2))

            elif x == P.r:
                # phi_2[i] = T.D[i] / (self.dx + 3) * (4 * phi_2[i-1] -
                #                                      phi_2[i-2])
                phi_2[i] = P.getXS(P, x, 1, 'd') / (self.dx + 3) * (4 * phi_2[i-1] -
                                                     phi_2[i-2])
            else:
                phi_2[i] = phi_2[i+1]
        return phi_2

    def source_update(self, N, phi_1, phi_2, k):
        S = []
        for i in range(N):
            x = self.grid[i]
            # S.append((F.F[i] * phi_1[i] + T.F[i] * phi_2[i]) / k)
            S.append((P.getXS(P, x, 0, 'f') * phi_1[i] + P.getXS(P, x, 1, 'f') * phi_2[i]) / k)
        return S

    def k_update(self, k_prev, source_prev, source_pres):
        nume = sum(source_pres)
        deno = sum(source_prev)
        return k_prev * nume / deno

    def convergence_checker(self, k, k_prev):
        if k - k_prev > 10 ** -3:
            return False
        else:
            return True


# flux = flux()
# phi_1_1 = flux.phi_1(N, flux.source_guess, flux.phi_1_guess)
# print(phi_1_1)
# phi_2_1 = flux.phi_2(N, phi_1_1, flux.phi_2_guess)
# print(phi_2_1)
# S_1 = flux.source_update(N, phi_1_1, phi_2_1, 1.3)
# print(S_1)
#
#
# plt.plot(flux.grid, phi_1_1, label='fast')
# plt.plot(flux.grid, phi_2_1, label='thermal')
# plt.plot(flux.grid, S_1, label='source')
# plt.legend()
# plt.show()
#
# phi_1_prev = flux.phi_1_guess
# phi_2_prev = flux.phi_2_guess
# source_prev = flux.source_guess
# k_prev = 1.2
# convergence = False
# outer_it_num = 0
# k_evo = []
#
# while outer_it_num < 10 ** 2: #  and convergence == False:
#     phi_1_pres = flux.phi_1(N, source_prev, phi_1_prev)
#     phi_2_pres = flux.phi_2(N, phi_1_pres, phi_2_prev)
#     source_pres = flux.source_update(N, phi_1_pres, phi_2_pres, k_prev)
#     k_pres = flux.k_update(k_prev, source_prev, source_pres)
#     print(k_pres)
#     k_evo.append(k_pres)
#     convergence = flux.convergence_checker(k_pres, k_prev)
#     phi_1_prev = phi_1_pres.copy()
#     phi_2_prev = phi_2_pres.copy()
#     source_prev = source_pres.copy()
#     k_prev = k_pres.copy()
#     # if outer_it_num % 10 ==
#     outer_it_num += 1
#
# print(k_evo)
