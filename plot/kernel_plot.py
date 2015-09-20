from __future__ import print_function, division
import numpy as np
import matplotlib.pyplot as plt
from ciabatta import ejm_rcparams
from ahoy.dc_dx_measurers import get_K

save_flag = True

use_latex = save_flag
use_pgf = True

ejm_rcparams.set_pretty_plots(use_latex, use_pgf)

fig = plt.figure(figsize=(12, 12 * ejm_rcparams.golden_ratio))
ax = fig.add_subplot(111)
ejm_rcparams.prettify_axes(ax)


t_mem = 10.0
t_rot_0 = 1.0
dt = t_mem / 5000.0

K = get_K(t_mem, dt, t_rot_0)
ts = np.linspace(0.0, t_mem, K.shape[0])

ax.plot(ts, K)
ax.axhline(0.0, c=ejm_rcparams.almost_black, ls='dashed')

ax.set_xlabel(r'$t / \tau$', fontsize=35)
ax.set_ylabel(r'$K$', fontsize=35)
ax.tick_params(axis='both', labelsize=26, pad=10.0)
# ax.set_xlim(0.0, 8.0)
ax.set_ylim(None, 1.01)

if save_flag:
    plt.savefig('kernel.pdf', bbox_inches='tight')
else:
    plt.show()
