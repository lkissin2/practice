import numpy as np
import math
import random
import matplotlib.pyplot as plt

print('hello')


class Points(object):
    """We will make many random points in the first quadrant and see if they lie
       within a quarter unit circle centered on the origin"""
    radius = 1  #  Distance of every point from origin will be compared to this
    digits = 100 #  How many digits in the position float
    def __init__(self):
        self.y = random.randint(0, Points.digits) / Points.digits
        self.x = random.randint(0, Points.digits) / Points.digits
        if self.x ** 2 + self.y ** 2 <= 1:  # not sure if it should be < or <=
            self.incircle = 1  # 1 indicates in circle
        else:
            self.incircle = 0
    def inner_loop(N_trials):
        """Computes pi for an integer N_trials number of points"""
        tot = 0
        n = 0
        while n < N_trials:
            point = Points()
            tot += point.incircle
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




tot_axis = []
err_axis = []
num_outer_loops = 250
num_axis = np.linspace(1, 501)

for num in num_axis:
    pair = Points.outer_loop(num, num_outer_loops)
    tot_axis.append(pair[0])
    err_axis.append(pair[1])

plt.plot(num_axis, err_axis)
plt.xlabel('Number of Sampled Points')
plt.ylabel('Average Percent Error')
plt.title('Error vs Number of Points Sampled with {} outer loops'.
           format(num_outer_loops))
plt.show()

def InverseRSquared(r):
    return r ** -0.5

r_axis = [err_axis[0] * InverseRSquared(r) for r in num_axis]
plt.plot(num_axis, err_axis, label = 'experimental')
plt.plot(num_axis, r_axis, label = '1/r^2')
plt.xlabel('Number of Sampled Points')
plt.ylabel('Average Percent Error')
plt.title('Error vs Number of Points Sampled with {} outer loops'.
           format(num_outer_loops))
plt.legend()
plt.show()
