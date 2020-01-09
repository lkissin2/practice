import numpy as np
import math
import random
import matplotlib.pyplot as plt


def dart():
    """throws a dart and returns true if it lands inside the circle,
       otherwise returns false else"""
    y = random.random()
    x = random.random()
    return x * x + y * y < 1


def inner_loop(N_trials):
    """Computes pi for an integer N_trials number of points"""
    N_trials = int(N_trials)
    tot = 0

    for _ in range(N_trials):
        if dart():
            tot += 1

    # tot = sum(_ for in range(N_trials) if dart())

    tot /= N_trials
    tot *= 4
    return (tot, 100 * abs(tot - math.pi) / math.pi)


def outer_loop(N_trials, N_trials_out):
    N_trials = int(N_trials)
    N_trials_out = int(N_trials_out)
    """Takes an average of averages from inner_loop"""
    estimate, error = (0, 0)

    for _ in range(N_trials_out):
        estimate_increment, error_increment = inner_loop(N_trials)
        estimate += estimate_increment
        error += error_increment

    estimate /= N_trials_out
    error /= N_trials_out

    return (estimate, error)



# ############################################################################
# ####################             PLOTTING               ####################
# ############################################################################

def InverseRSquared(r):
    return r ** -0.5

N = 501
# InverseRSquared = (math.sqrt(r) for r in range(N))

#  Plot % error vs num inner loops
tot_axis = []
err_axis = []
num_outer_loops = 250
num_axis = np.linspace(1, N)

for num in num_axis:
    pair = outer_loop(num, num_outer_loops)
    tot_axis.append(pair[0])
    err_axis.append(pair[1])

plt.plot(num_axis, err_axis)
plt.xlabel('Number of Sampled Points')
plt.ylabel('Average Percent Error')
plt.title('Error vs Number of Points Sampled with {} outer loops'.
          format(num_outer_loops))
plt.savefig('err_v_num_in')
plt.show()

# #  Plot % error vs num inner loops with 1 /r^2
#
r_axis = [err_axis[0] * InverseRSquared(r) for r in num_axis]
plt.plot(num_axis, err_axis, label='experimental')
plt.plot(num_axis, r_axis, label='1/n^2')
plt.xlabel('Number of Sampled Points')
plt.ylabel('Average Percent Error')
plt.title('Error vs Number of Points Sampled with {} outer loops'.
          format(num_outer_loops))
plt.legend()
plt.savefig('err_v_num_in-with_1_on_r2')
plt.show()
#
# Plot % error vs num outer loops
#
# tot_axis_in = []
# err_axis_in = []
# num_inner_loops = 250
# num_axis = np.linspace(1, 5001)
#
# for num in num_axis:
    # pair = outer_loop(num_inner_loops, num)
    # tot_axis_in.append(pair[0])
    # err_axis_in.append(pair[1])
#
# plt.plot(num_axis, err_axis_in)
# plt.xlabel('Number of Outer Loops')
# plt.ylabel('Average Percent Error')
# plt.title('Error vs Number of Points Sampled with {} inner loops'.
          # format(num_inner_loops))
# plt.savefig('err_v_num_in')
# plt.show()
#
# Plot % error vs num inner loops with 1 /r^2
# r_axis_in = [err_axis_in[0] * InverseRSquared(r) for r in num_axis]
# plt.plot(num_axis, err_axis_in, label='experimental')
# plt.plot(num_axis, r_axis_in, label='1/n^2')
# plt.xlabel('Number of Sampled Points')
# plt.ylabel('Average Percent Error')
# plt.title('Error vs Number of Points Sampled with {} outer loops'.
          # format(num_inner_loops))
# plt.legend()
# plt.savefig('err_v_num_in-with_1_on_r2')
# plt.show()
