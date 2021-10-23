'''
Graphing some basic exoplanet transfer model I made to fit to data.
'''

import numpy as np
import matplotlib.pyplot as plt

n = 1000 #   steps
r = .2   #   ratio of planetary radius to star radius
c = 10   #   ratio of orbit radius to star radius
f = .2   #   fraction of maximum inclination
i = np.pi / 2 - f * (np.pi / 2 - np.arccos(1 / c)) #   inclination
F_0 = 1  #   flux at center
B = .3   #   linear flux component
P = 1    #   perioddd

x = np.linspace(-1 -2 * r, 1 + 2 * r, n)
I_plot = np.empty(n)

#   Model based on a small circle eclipsing a larger one. Accounts for edges and stuff too, and linear limb darkening.
#   (relative space dependence)
def I_x(x, F_0, B, r, c, i):
    A = 1 - B
    if x < 0:
        return I_x(-x, F_0, B, r, c, i);
    elif x >= np.sqrt(1 - c**2 * np.cos(i)**2) + r:
        return np.pi * F_0 * (A + 2/3 * B)
    elif x <= np.sqrt(1 - c**2 * np.cos(i)**2) - r:
        return np.pi * F_0 * ((1 - r**2) * A + (2/3 - r**2 * np.sqrt(1 - x**2 - c**2 * np.cos(i)**2)) * B)
    elif x >= np.sqrt(1 - c**2 * np.cos(i)**2):
        return np.pi * F_0 * (A + 2/3 * B) - F_0 * A * (r**2 * np.arccos((x - np.sqrt(1 - c**2 * np.cos(i)**2)) / r)\
               -(x - np.sqrt(1 - c**2 * np.cos(i)**2))\
               * np.sqrt(2 * r * (np.sqrt(1 - c**2 * np.cos(i)**2) + r - x) - (np.sqrt(1 - c**2 * np.cos(i)**2) + r - x)**2))
    else:
        return np.pi * F_0 * (A + 2/3 * B) - F_0 * (A + B * np.sqrt(1 - x**2 - c**2 * np.cos(i)**2))\
               * (r**2 * np.arccos((x - np.sqrt(1 - c**2 * np.cos(i)**2)) / r) - (x - np.sqrt(1 - c**2 * np.cos(i)**2))\
                  * np.sqrt(2 * r * (np.sqrt(1 - c**2 * np.cos(i)**2) + r - x) - (np.sqrt(1 - c**2 * np.cos(i)**2) + r - x)**2))

#   For fitting to time dependent data.
#   (absolute time dependence)
def I(t, F_0, B, r, c, i, t_0):
    x = 2 * np.pi * c * np.sin(i) * (t - t_0) / P
    return I_x(x, F_0, B, r, c, i)

for j in range(n):
    I_plot[j] = I_x(x[j], F_0, B, r, c, i)

fig = plt.figure(figsize = (6, 4))
ax  = fig.add_subplot(111)
ax.plot(x, I_plot, color = 'black')
ax.set_xlim(x[0], x[-1])
ax.set_xlabel('x',        size = 12)
ax.set_ylabel('F [a.u.]', size = 12)
plt.show()
