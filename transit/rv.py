'''
Two methods to determine some exoplanet properties using radial velocity measurements.
'''

import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

#   number of steps
n_fit = 10000

t    = np.array([3791.7441, 3793.6623, 3793.7635, 3794.7132, 3794.8735, 3853.5400, 3853.5753, 3854.4999, 3856.6192, 3858.6166,
                 3859.7276, 4143.7804, 4144.7438, 4144.7730, 4145.7741, 4148.6511, 4149.7774, 4150.7396, 4203.5920, 4204.5496,
                 4205.5464, 4207.6555, 4208.5372, 4209.6534])
u    = np.array([22.433, 22.297, 22.209, 22.325, 22.293, 22.161, 22.238, 22.374, 22.500, 22.430, 22.488, 22.191, 22.325, 22.256,
                 22.504, 22.330, 22.454, 22.452, 22.368, 22.259, 22.407, 22.229, 22.260, 22.457])
u_sd = np.array([0.056, 0.118, 0.067, 0.056, 0.058, 0.062, 0.057, 0.056, 0.060, 0.057, 0.070, 0.062, 0.061, 0.057, 0.082, 0.060,
                 0.064, 0.057, 0.046, 0.070, 0.070, 0.043, 0.050, 0.054])

#   Determine radial velocity amplitude through variance of radial velocity.
n         = u.shape[0]
u_sd_norm = np.sum(1 / u_sd**2)
w         = np.sum(u / u_sd**2) / u_sd_norm
w_var     = n / (n - 1) * np.sum(((u - w) / u_sd)**2) / u_sd_norm
w_sd      = np.sqrt(w_var)
w_var_var = n / (n - 2) * np.sum((((u - w)**2 - w_var) / u_sd)**2) / u_sd_norm
w_var_sd  = np.sqrt(w_var_var)

print('variance method')
print(f'drift\t{w:.1f} km/s')
print(f'amplitude sin(inclination)\t{w_sd:.3f}±{w_var_sd:.3f} km/s')
print()

#   Determine radial velocity properties through direct fitting to sinusoidal model.
P   = 3.97910            #   in days, pm 0.00001
P_s = 3600 * 24 * P      #   in seconds
inc = 85.7 * np.pi / 180 #   pm 0.3
def f(t, w, b, t_0):
    return w + 2 * np.pi * b / P_s * np.sin(2 * np.pi / P * (t - t_0)) * np.sin(inc)
fit, fit_cov = curve_fit(f, t, u, p0 = [22.35, 6750, 3])
fit_sd = np.sqrt(fit_cov.diagonal())

print('fit method')
print(f'drift\t{fit[0]:.1f}±{fit_sd[0]:.1f} km/s')
print(f'semi-major radius\t{fit[1]:.0f}±{fit_sd[1]:.0f} km')
print(f'amplitude sin(inclination)\t {2 * np.pi * fit[1] / P_s * np.sin(inc):.3f}±{2 * np.pi * fit_sd[1] / P_s * np.sin(inc):.3f} km/s')
print(f't_0\t{fit[2]:.2f}±{fit_sd[2]:.2f} days')

t_fit = np.linspace(np.min(t), np.max(t), n_fit)
u_fit = np.empty(n_fit)
for i in range(0, n_fit):
    u_fit[i] = f(t_fit[i], fit[0], fit[1], fit[2])

fig = plt.figure(figsize = (5, 8))
axs = [fig.add_subplot(411), fig.add_subplot(412), fig.add_subplot(413), fig.add_subplot(414)]
for ax in axs:
    ax.plot(t_fit, u_fit, color = 'red')
    ax.errorbar(t, u, yerr = u_sd, fmt = 'o', color = 'black')
    ax.set_xlabel('time [BJD]',             size = 10)
    ax.set_ylabel('radial velocity [km/s]', size = 10)
    ax.grid()
axs[0].set_xlim([3791, 3796])
axs[1].set_xlim([3851, 3862])
axs[2].set_xlim([4142, 4153])
axs[3].set_xlim([4201, 4211])
plt.tight_layout()
plt.show()
