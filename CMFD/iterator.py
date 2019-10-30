import numpy as np
import matplotlib.pyplot as plt
from solver import flux

N = 100  # number of gridpoints

flux = flux()

phi_1_prev = flux.phi_1_guess
phi_2_prev = flux.phi_2_guess
source_prev = flux.source_guess
k_prev = 1.2
convergence = False
outer_it_num = 0
k_evo = []
source_evo = []

while outer_it_num <= 5 * 10 ** 3:  # and convergence == False:
    print(outer_it_num)
    if outer_it_num > 300 and outer_it_num < 400:
        print(phi_1_pres)
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
    if outer_it_num % 1000 == 0:
        source_evo.append(source_pres)
    outer_it_num += 1


def normalizer(list):
    maximum = max(np.array(list).flatten())
    for item in range(len(list)):
        for subitem in range(len(list[item])):
            list[item][subitem] /= maximum
    return list


# source_evo = normalizer(source_evo)
# label_num = 0
# for item in source_evo:
#     plt.plot(flux.grid, item, label = str(label_num) + 'iterations')
#     label_num += 1000

# plt.xlabel('Position')
# plt.ylabel('Source Neutron Density')
# plt.title('Normalized Source Neutron Distribution at Different Iterations')
# plt.legend()
# plt.show()
#
# plt.plot(np.arange(0, 5 * 10 ** 3 + 1), k_evo)
# plt.xlabel('Iteration Number')
# plt.ylabel('k')
# plt.title('k vs Iteration Number')
# plt.show()


def normalizer2(list1, list2):
    maximum = max(max(list1), max(list2))
    for item in range(len(list1)):
        list1[item] /= maximum
        list2[item] /= maximum
    return [list1, list2]


phi_plot = normalizer2(phi_1_pres, phi_2_pres)
plt.plot(flux.grid, phi_plot[0], label='fast')
plt.plot(flux.grid, phi_plot[1], label='thermal')
plt.xlabel('Position')
plt.ylabel('Normalized Flux')
plt.title('Normalized and Converged Flux Distributions')
plt.legend()
plt.show()

print(k_pres)
