import numpy as np
import math


def extractor(filename='input.txt'):
    """extract geometry and material parameters from input.txt"""

    # Open the file
    file = open(filename, 'rt')
    lines = file.readlines()

    # Determine the number of regions, given the number of lines in filename
    nr = int((len(lines) - 2) / 2)

    # Extract number of grid points and positions of boundaries
    N = int(lines[0].split(' ')[1][:-1])
    boundaries = lines[1].split(' ').pop(0)
    boundaries[-1] = boundaries[-1][:-1]
    boundaries = [float(boundaries[n]) for n in range(len(boundaries))]
    for n in range(len(boundaries)):
        if n > 0:
            if boundaries[n] < boundaries[n-1]:
                print('Error: boundary postions should be in ascending order' +
                      '(e.g. 75 90 100 not 75 15 10)')

    # Build a list for cross sections
    xs = []

    for n in range(2, 2 + 2 * nr):
        # Add data in pairs so that fast and thermal xsns are together
        if n % 2 == 0:
            next_xs = [[], []]
            next_xs[0] = lines[n].split(' ')
            next_xs[0].pop(0)
            next_xs[0][-1] = next_xs[0][-1][:-1]
            next_xs[1] = lines[n+1].split(' ')
            next_xs[1].pop(0)
            next_xs[1][-1] = next_xs[1][-1][:-1]
            xs.append([[float(next_xs[0][i]) for i in range(len(next_xs[0]))],
                       [float(next_xs[1][i]) for i in range(len(next_xs[1]))]])

    for i in range(len(xs)):
        for j in range(len(xs[i])):
            xs[i][j].append(xs[i][j][1] - xs[i][j][2])             # scattering
            xs[i][j].append(math.sqrt(xs[i][j][0] / xs[i][j][2]))  # diff lengt
            if len(xs[i][j]) != 6:
                print('error: material number' + str(i + j) +
                      'does not have 4 cross sections')
                      
    return {'N': N, 'nr': nr, 'bounds': boundaries, 'xs': xs}


class properties(object):
    """geometry properties of core
       includes positions of boundaries
       and a method that builds the x axis for the FD scheme
       in the future we can add cylindrical, spherical options
       and maybe multiple dimensions"""

    def __init__(self):
        """run extractor and set the geometry properties to relevant values"""
        print('hello')

    props = extractor()

    N = props['N']
    nr = props['nr']
    bounds = props['bounds']
    r = bounds[-1]
    xs = props['xs']

    axis = np.linspace(0, bounds[-1], N)

    def getXS(self, x, group, name):
        for n in range(len(self.bounds)):
            if x <= self.bounds[n]:
                if name == 'd':
                    return self.xs[n][group][0]
                elif name == 'r':
                    return self.xs[n][group][1]
                elif name == 'a':
                    return self.xs[n][group][2]
                elif name == 'f':
                    return self.xs[n][group][3]
                elif name == 's':
                    return self.xs[n][group][4]
                elif name == 'l':
                    return self.xs[n][group][5]
                elif name == 'b':
                    return self.xs[n][group][6]
                else:
                    print('error in name entry! Please use one of these' +
                          'names: drafslb')
                    return None
