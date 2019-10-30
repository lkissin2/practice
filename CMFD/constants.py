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
    boundaries = lines[1].split(' ')
    boundaries.pop(0)
    # print('boundaries = ' + str(boundaries))
    boundaries[-1] = boundaries[-1][:-1]
    # boundaries = [0] + [float(boundaries[n]) for n in range(len(boundaries))]
    boundaries = [float(boundaries[n]) for n in range(len(boundaries))]

    # Build a list for cross sections
    xs = []
    # xs = np.empty([nr, 2])
    for n in range(2, 2 + 2 * nr):
        if n % 2 == 0:
            next_xs = [[], []]
            next_xs[0] = lines[n].split(' ')
            next_xs[0].pop(0)
            next_xs[0][-1] = next_xs[0][-1][:-1]
            next_xs[1] = lines[n+1].split(' ')
            next_xs[1].pop(0)
            next_xs[1][-1] = next_xs[1][-1][:-1]
        # print(next_xs)
            xs.append([[float(next_xs[0][i]) for i in range(len(next_xs[0]))],
                       [float(next_xs[1][i]) for i in range(len(next_xs[1]))]])
            # xs.append([float(next_xs[1][i]) for i in range(len(next_xs[1]))])
    # print('xs')
    # print(xs)
    for i in range(len(xs)):
        for j in range(len(xs[i])):
            xs[i][j].append(xs[i][j][1] - xs[i][j][2])             # scattering
            xs[i][j].append(math.sqrt(xs[i][j][0] / xs[i][j][2]))  # diff lengt
            if i + 2 >= len(xs):                        # extrapolated distance
                xs[i][j].append(boundaries[-1] + 2 * xs[i][j][0])
            else:
                xs[i][j].append(0)
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
                # print('n = ' + str(n))
                # print('g = ' + str(group))
                if name == 'd':
                    # print(self.xs[n][group][0])
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
    #
    # # A long array with xs data:
    # xsa = np.empty([N, 2, 7])
    #
    # for n in np.arange(N):
    #     x = axis[n]
    #     # print(x)
    #     for i in np.arange(len(bounds)):
    #         # print(i)
    #         if x <= bounds[i]:
    #             xsa[n] = [xs[i], xs[i+1]]
    #             break



# g = geometry
# # print(g.N)
# # print(g.nr)
# # g = geometry
# # print(g.bounds)
# print(g.xs)
# for x in g.xs:
#     print(x)
# print(g.xsa[0])
# print(g.xsa[1])


#
# class material(geometry):
#     """inherits from geometry and makes an array of material properties"""
#     # super().__init__()

    # print(N)

    # def axis():
    #     """makes the x axis, in the future let's make it 2D"""
    #     return np.linspace(0, r, N)
    #
    # for x in axis():
    #     print(x)

# g = geometry()
# print(g.N)

#
# class fast(geometry):
#     """group 1 constants"""
#     # d1c = 1.2627               # fast diffusion coeff
#     # r1c = 0.02619             # removal fast xsn
#     # a1c = 0.01207             # absorption fast xsn
#     # f1c = 0.008476           # nu sigma f fast
#     # sc = r1c - a1c            # scattering cross-section
#     # l1c = (d1c / r1c) ** 0.5    # diffusion lengths
#     # # ########################## REFLECTOR PROPERTIES
#     # d1r = 1.13                 # diffusion
#     # r1r = 0.0494              # removal
#     # a1r = 0.0004              # absorption
#     # bt = r + 2 * d1r               # extrapolated distance
#     # l1r = (d1r / r1r) ** 0.5    # diffusion length
#     # sr = r1r - a1r            # scattering
#
#     def __init__(self):
#         """inherit from geometry and get xs from input"""
#         self.xs = extractor()['xs']
#         super().__init__(*args, **kwargs)
#
#
#
#     # def __init__(self, N):
#     #     self.S = [self.sc if x < a else self.sr for x in np.linspace(0, r, N)]
#     #     self.R = [self.r1c if x < a else self.r1r
#     #               for x in np.linspace(0, r, N)]
#     #     self.D = [self.d1c if x < a else self.d1r
#     #               for x in np.linspace(0, r, N)]
#     #     self.A = [self.a1c if x < a else self.a1r
#     #               for x in np.linspace(0, r, N)]
#     #     self.L = [self.l1c if x < a else self.l1r
#     #               for x in np.linspace(0, r, N)]
#     #     self.F = [self.f1c if x < a else 0 for x in np.linspace(0, r, N)]
#
#
# class thermal(object):
#     """thermal material properties"""
#     # # ########################## CORE PROPERTIES
#     d2c = 0.3543               # thermal diffusion coeff
#     r2c = 0.1210              # removal thermal xsn
#     a2c = 0.12100             # absorption thermal xsn
#     f2c = 0.18514            # nu sigma f thermal
#     l2c = math.sqrt(d2c / a2c)  #
#     # ######################### REFLECTOR PROPERTIES
#     d2r = 0.16                 #
#     a2r = 0.0197              #
#     bt = r + 2 * d2r               # extrapolated distance
#     l2r = math.sqrt(d2r / a2r)  #
#
#     def __init__(self, N):
#         self.D = [self.d2c if x < a else self.d2r
#                   for x in np.linspace(0, r, N)]
#         self.A = [self.a2c if x < a else self.a2r
#                   for x in np.linspace(0, r, N)]
#         self.L = [self.l2c if x < a else self.l2r
#                   for x in np.linspace(0, r, N)]
#         self.F = [self.f2c if x < a else 0 for x in np.linspace(0, r, N)]
