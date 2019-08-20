# From Dean Ballard, one small step for man, one giant problem for The Riddler:
# Sometime in the near future people from Earth will land on Mars. Someone will
# step out of the landing pod and become the first human to leave his or her
# footprints on another planet.
# Imagine two astronauts sitting in the pod, both of whom would love to take
# that first step. But they would also like to decide which of them gets the
# honor in a fair manner, so they flip a coin. Despite the change in gravity,
# this method is fair as long as the coin is fair. If there were four astronauts
# in the landing pod, then they could flip a fair coin twice, assigning the
# four possible outcomes — heads-heads, heads-tails, tails-heads and tails-
# tails — to each of the four astronauts. This would also be fair as long as
# the coins were fair. But what if there were three astronauts in the landing
# pod? Then our fair coin
# doesn’t work so well. We could, for example, assign three of the four
# possible outcomes — say heads-heads, heads-tails and tails-heads — to each of
# the astronauts. Then, if the outcome were tails-tails, they could simply
# start over again with two more flips. This would give an ever-increasing
# probability that a fair decision would eventually be made, but that could
# take a long time, and the required number of flips would be unknown. And
# there’s a planet to walk on!
# Another approach, however, is to use an “unfair coin” — one in which the
# probabilities of heads and tails are not equal. Is it possible to make a
# fair choice among three astronauts with a fixed number of flips of an unfair
# coin?
# You are able to set the coin’s probability of heads to any number you like
# between 0 and 1. You may flip the coin as many times as you like, as long as
# that is some known, fixed number. And, you may assign any combination of
# possible outcomes to each of the three astronauts.
# Extra credit: What if there were five astronauts?

# First, given a probability of heasds, how many flips until no individual tree
# has a probability exceeding 0.33?

import math
import numpy as np
import matplotlib.pyplot as plt
from tabulate import tabulate as tabu

p_axis = np.linspace(0.11, 0.89, 79)
n_axis = []

def getP13(pHeads):
    """how many flips until no individual tree has more than 1/3 probability?
    given pHeads, the probability of heads between 0 and 1"""
    pMax = max(pHeads, 1 - pHeads)
    nFlips = math.log(1 /3) / math.log(pMax)
    nFlips = math.ceil(nFlips)
    return nFlips

# table = []

for i in p_axis:
    p13i = getP13(i)
    n_axis.append(p13i)
#     row = [i, p13i]
#     table.append(row)

# print(p_axis)
# print(n_axis)

plt.plot(p_axis, n_axis)
plt.xlabel('probability of heads')
plt.ylabel('number of flips til no single tree has more than 1/3 probability')
plt.show()

# print(tabu(table))


def getProbList(pHeads, nFlips):
    """returns a list of probabilities for different trees for a float pHeads
    and an int nFlips"""
    pTails = 1 - pHeads
    pList = [pHeads, pTails]
    for i in range(nFlips + 1):
        pList.append(pList[i] * pHeads)
        pList.append(pList[i] * pTails)
    # j = 0
    # i = nFlips
    # pList = []
    # while i >= 0:
    #     if i == 0 or j == 0:
    #         pList.append(pHeads ** i * (1 - pHeads) ** j)
    #     else:
    #         pList.append(pHeads ** i * (1 - pHeads) ** j)
    #         pList.append(pHeads ** i * (1 - pHeads) ** j)
    #     j += 1
    #     i -= 1
    return pList


p = 0.75
n = 3
print(getProbList(p, n), sum(getProbList(p, n)))


# for i in p_axis:
#     p13i = getP13(i)
#     n_axis.append(p13i)
#     row = [i, p13i]
#     table.append(row)
