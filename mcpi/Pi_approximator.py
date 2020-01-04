import numpy as np
import math
import random
import matplotlib.pyplot as plt


class Points(object):
    """We will make many random points in the first quadrant and see if they lie
       within a quarter unit circle centered on the origin"""

    def __init__(self):
        """set self.x and self.y to a random number [0, 1.0)
           set self.incircle to true
           check if the point (x, y) is inside the unit quarter-circle
           set self.incircle to false if (x, y) is outsid the UQC"""
        self.y = random.random()
        self.x = random.random()
        self.incircle = True
        if self.x ** 2 + self.y ** 2 >= 1:  # not sure if it should be > or >=
            self.incircle = False

    def inner_loop(N_trials):
        """Computes pi for an integer N_trials number of points"""
        tot = 0
        n = 0

        while n < N_trials:
            point = Points()
            if point.incircle:
                tot += 1
            n += 1

        tot /= N_trials
        tot *= 4
        return (tot, 100 * abs(tot - math.pi) / math.pi)

    def outer_loop(N_trials, N_trials_out):
        """Takes an average of averages from inner_loop"""
        tot = [0.0, 0.0]
        n = 0

        while n < N_trials_out:
            tot[0] += Points.inner_loop(N_trials)[0]
            tot[1] += Points.inner_loop(N_trials)[1]
            n += 1

        tot[0] /= N_trials_out
        tot[1] /= N_trials_out
        return tot


# ############################################################################
# ####################             PLOTTING               ####################
# ############################################################################


#  Plot % error vs num inner loops
# tot_axis = []
# err_axis = []
# num_outer_loops = 250
# num_axis = np.linspace(1, 501)
#
# for num in num_axis:
#     pair = Points.outer_loop(num, num_outer_loops)
#     tot_axis.append(pair[0])
#     err_axis.append(pair[1])
#
# plt.plot(num_axis, err_axis)
# plt.xlabel('Number of Sampled Points')
# plt.ylabel('Average Percent Error')
# plt.title('Error vs Number of Points Sampled with {} outer loops'.
#           format(num_outer_loops))
# plt.savefig('err_v_num_in')
# plt.show()
#
# #  Plot % error vs num inner loops with 1 /r^2
#
#
def InverseRSquared(r):
    return r ** -0.5
#
#
# r_axis = [err_axis[0] * InverseRSquared(r) for r in num_axis]
# plt.plot(num_axis, err_axis, label='experimental')
# plt.plot(num_axis, r_axis, label='1/n^2')
# plt.xlabel('Number of Sampled Points')
# plt.ylabel('Average Percent Error')
# plt.title('Error vs Number of Points Sampled with {} outer loops'.
#           format(num_outer_loops))
# plt.legend()
# plt.savefig('err_v_num_in-with_1_on_r2')
# plt.show()

#  Plot % error vs num outer loops

tot_axis_in = []
err_axis_in = []
num_inner_loops = 250
num_axis = np.linspace(1, 5001)

for num in num_axis:
    pair = Points.outer_loop(num_inner_loops, num)
    tot_axis_in.append(pair[0])
    err_axis_in.append(pair[1])

plt.plot(num_axis, err_axis_in)
plt.xlabel('Number of Outer Loops')
plt.ylabel('Average Percent Error')
plt.title('Error vs Number of Points Sampled with {} inner loops'.
          format(num_inner_loops))
plt.savefig('err_v_num_in')
plt.show()

#  Plot % error vs num inner loops with 1 /r^2
r_axis_in = [err_axis_in[0] * InverseRSquared(r) for r in num_axis]
plt.plot(num_axis, err_axis_in, label='experimental')
plt.plot(num_axis, r_axis_in, label='1/n^2')
plt.xlabel('Number of Sampled Points')
plt.ylabel('Average Percent Error')
plt.title('Error vs Number of Points Sampled with {} outer loops'.
          format(num_inner_loops))
plt.legend()
plt.savefig('err_v_num_in-with_1_on_r2')
plt.show()
