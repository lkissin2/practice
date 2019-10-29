import numpy as np
import math

# # geometric constants:
a = 75  # length of inner assembly, cm
b = 15  # length of reflector, cm
r = a+b  # total length


def extractor(filename):
    file = open(filename, 'rt')
    lines = file.readlines()
    ng = int(lines[0].split(' ')[1][0])
    nr = int(lines[1].split(' ')[1][0])
    boundaries = lines[2].split(' ')
    boundaries.pop(0)
    # print('boundaries = ' + str(boundaries))
    boundaries[-1] = boundaries[-1][:-1]
    boundaries = [0] + [float(boundaries[n]) for n in range(len(boundaries))]
    xs = []
    for n in range(3, 3+ng*nr):
        next_xs = lines[n].split(' ')
        next_xs.pop(0)
        next_xs[-1] = next_xs[-1][:-1]
        # print(next_xs)
        xs.append([float(next_xs[i]) for i in range(len(next_xs))])
        # print(xs)
    for i in range(len(xs)):
        xs[i].append(xs[i][1] - xs[i][2])               # scattering
        xs[i].append(math.sqrt(xs[i][0] / xs[i][2]))    # diffusion length
        if i % 2 == 1:                                  # extrapolated distance
            xs[i].append(sum(boundaries) + 2 * xs[i][0])
    return {'ng': ng, 'nr': nr, 'bounds': boundaries, 'xs': xs}


class geometry(object):
    """geometry properties of core
       includes positions of boundaries
       and a method that builds the x axis for the FD scheme
       in the future we can add cylindrical, spherical options
       and maybe multiple dimensions"""
    a = 75  # length of core, cm
    b = 15  # length of refl, cm
    boundaries = [a, b]
    r = sum(boundaries)  # total length

    def axis(self, N):
        return np.linspace(0, self.r, N)


class fast(object):
    """group 1 constants"""
    d1c = 1.2627               # fast diffusion coeff
    r1c = 0.02619             # removal fast xsn
    a1c = 0.01207             # absorption fast xsn
    f1c = 0.008476           # nu sigma f fast
    sc = r1c - a1c            # scattering cross-section
    l1c = (d1c / r1c) ** 0.5    # diffusion lengths
    # ########################## REFLECTOR PROPERTIES
    d1r = 1.13                 # diffusion
    r1r = 0.0494              # removal
    a1r = 0.0004              # absorption
    bt = r + 2 * d1r               # extrapolated distance
    l1r = (d1r / r1r) ** 0.5    # diffusion length
    sr = r1r - a1r            # scattering

    def __init__(self, N):
        self.S = [self.sc if x < a else self.sr for x in np.linspace(0, r, N)]
        self.R = [self.r1c if x < a else self.r1r
                  for x in np.linspace(0, r, N)]
        self.D = [self.d1c if x < a else self.d1r
                  for x in np.linspace(0, r, N)]
        self.A = [self.a1c if x < a else self.a1r
                  for x in np.linspace(0, r, N)]
        self.L = [self.l1c if x < a else self.l1r
                  for x in np.linspace(0, r, N)]
        self.F = [self.f1c if x < a else 0 for x in np.linspace(0, r, N)]


class thermal(object):
    """thermal material properties"""
    # # ########################## CORE PROPERTIES
    d2c = 0.3543               # thermal diffusion coeff
    r2c = 0.1210              # removal thermal xsn
    a2c = 0.12100             # absorption thermal xsn
    f2c = 0.18514            # nu sigma f thermal
    l2c = math.sqrt(d2c / a2c)  #
    # ######################### REFLECTOR PROPERTIES
    d2r = 0.16                 #
    a2r = 0.0197              #
    bt = r + 2 * d2r               # extrapolated distance
    l2r = math.sqrt(d2r / a2r)  #

    def __init__(self, N):
        self.D = [self.d2c if x < a else self.d2r
                  for x in np.linspace(0, r, N)]
        self.A = [self.a2c if x < a else self.a2r
                  for x in np.linspace(0, r, N)]
        self.L = [self.l2c if x < a else self.l2r
                  for x in np.linspace(0, r, N)]
        self.F = [self.f2c if x < a else 0 for x in np.linspace(0, r, N)]
