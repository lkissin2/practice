import numpy as np
import math as math
import matplotlib.pyplot as plt
import os
import sys
from constants import fast
from constants import thermal
from constants import geometry
from solver import flux

N = 100  # number of gridpoints

G = geometry()
F = fast(N)
T = thermal(N)
flux = flux()

phi_1_1 = flux.phi_1(N, flux.source_guess, flux.phi_1_guess)
print(phi_1_1)

phi_1_prev = flux.phi_1_guess
phi_2_prev = flux.phi_2_guess
source_prev = flux.source_guess
k_prev = 1.2
convergence = False
outer_it_num = 0
k_evo = []

while outer_it_num < 5 * 10 ** 3: # and convergence == False:
    phi_1_pres = flux.phi_1(N, source_prev, phi_1_prev)
    phi_2_pres = flux.phi_2(N, phi_1_pres, phi_2_prev)
    source_pres = flux.source_update(N, phi_1_pres, phi_2_pres, k_prev)
    k_pres = flux.k_update(k_prev, source_prev, source_pres)
    # print(k_pres)
    k_evo.append(k_pres)
    convergence = flux.convergence_checker(k_pres, k_prev)
    phi_1_prev = phi_1_pres.copy()
    phi_2_prev = phi_2_pres.copy()
    source_prev = source_pres.copy()
    k_prev = k_pres.copy()
    # if outer_it_num % 10 ==
    outer_it_num += 1

print(k_evo)
plt.plot(np.arange(0, 5 * 10 ** 3), k_evo)
plt.show()
