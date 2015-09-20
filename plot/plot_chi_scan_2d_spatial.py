from __future__ import print_function, division
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from ciabatta import ejm_rcparams
from ahoy.utils import utils

save_flag = True

use_latex = save_flag
use_pgf = True

ejm_rcparams.set_pretty_plots(use_latex, use_pgf)

fig = plt.figure(figsize=(12, 12 * ejm_rcparams.golden_ratio))
ax = fig.add_subplot(111)
ejm_rcparams.prettify_axes(ax)

dirnames_2D_p_1side_S = glob('/Users/ewj/Desktop/porous/ahoy_data/chi_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(1,1),v=20,p=1,chi=*,side=1,type=S,obs=NoObs,c=NoC')
dirnames_2D_p_2side_S = glob('/Users/ewj/Desktop/porous/ahoy_data/chi_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(1,1),v=20,p=1,chi=*,side=2,type=S,obs=NoObs,c=NoC')
dirnames_2D_Dr_1side_S = glob('/Users/ewj/Desktop/porous/ahoy_data/chi_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(1,1),v=20,Dr=1,chi=*,side=1,type=S,obs=NoObs,c=NoC')
dirnames_2D_Dr_2side_S = glob('/Users/ewj/Desktop/porous/ahoy_data/chi_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(1,1),v=20,Dr=1,chi=*,side=2,type=S,obs=NoObs,c=NoC')

chis, uds, uds_err = utils.chi_uds_x(dirnames_2D_p_2side_S)
i_sort = np.argsort(chis)
chis, uds, uds_err = chis[i_sort], uds[i_sort], uds_err[i_sort]
ax.errorbar(chis, uds, yerr=uds_err,
            label='Two-sided tumbling', c=ejm_rcparams.set2[0])

chis, uds, uds_err = utils.chi_uds_x(dirnames_2D_p_1side_S)
i_sort = np.argsort(chis)
chis, uds, uds_err = chis[i_sort], uds[i_sort], uds_err[i_sort]
ax.errorbar(chis, uds, yerr=uds_err,
            label='One-sided tumbling', c=ejm_rcparams.set2[1])

chis, uds, uds_err = utils.chi_uds_x(dirnames_2D_Dr_2side_S)
i_sort = np.argsort(chis)
chis, uds, uds_err = chis[i_sort], uds[i_sort], uds_err[i_sort]
ax.errorbar(chis, uds, yerr=uds_err,
            label='Two-sided diffusion', c=ejm_rcparams.set2[2])

chis, uds, uds_err = utils.chi_uds_x(dirnames_2D_Dr_1side_S)
i_sort = np.argsort(chis)
chis, uds, uds_err = chis[i_sort], uds[i_sort], uds_err[i_sort]
ax.errorbar(chis, uds, yerr=uds_err,
            label='One-sided diffusion', c=ejm_rcparams.set2[3])

chis_th = np.linspace(0.001, 0.99, 100)

ax.plot(chis_th, (1.0 - np.sqrt(1.0 - chis_th ** 2)) / chis_th,
        label=r'$u_x = (1 - \sqrt{1 - \chi^2}) / \chi$',
        ls='dashed', c=ejm_rcparams.set2[0])

ax.plot(chis_th, 0.25 * chis_th,
        label=r'$u_x = 0.25 \chi$',
        ls='dashed', c=ejm_rcparams.set2[1])

ax.set_xlim(0.0, 1.0)
ax.set_ylim(0.0, 1.0)

ax.legend(loc='upper left', fontsize=26)
ax.set_xlabel(r'$\chi$', fontsize=35)
ax.set_ylabel(r'$u_x$', fontsize=35)
ax.tick_params(axis='both', labelsize=26, pad=10.0)

if save_flag:
    plt.savefig('chi_scan_2d_spatial.pdf', bbox_inches='tight')
else:
    plt.show()
