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

dirnames_1D_p = glob('/Users/ewj/Desktop/porous/ahoy_data/Dr_scan_uniform/ahoy_1D,dt=0.01,seed=1,n=5000,align=(0),origin=(1),v=20,p=*,obs=NoObs,c=NoC')
dirnames_2D_p = glob('/Users/ewj/Desktop/porous/ahoy_data/Dr_scan_uniform/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(1,1),v=20,p=*,obs=NoObs,c=NoC')
dirnames_2D_Dr = glob('/Users/ewj/Desktop/porous/ahoy_data/Dr_scan_uniform/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(1,1),v=20,Dr=*,obs=NoObs,c=NoC')

noise_0s, Ds, Ds_err = utils.noise_0_tot_Ds_scalar(dirnames_1D_p)
i_sort = np.argsort(noise_0s)
noise_0s, Ds, Ds_err = noise_0s[i_sort], Ds[i_sort], Ds_err[i_sort]
ax.errorbar(noise_0s, Ds, yerr=Ds_err, label='1D, Tumbling')

noise_0s, Ds, Ds_err = utils.noise_0_tot_Ds_scalar(dirnames_2D_p)
i_sort = np.argsort(noise_0s)
noise_0s, Ds, Ds_err = noise_0s[i_sort], Ds[i_sort], Ds_err[i_sort]
ax.errorbar(noise_0s, Ds, yerr=Ds_err, label='2D, Tumbling')

noise_0s, Ds, Ds_err = utils.noise_0_tot_Ds_scalar(dirnames_2D_Dr)
i_sort = np.argsort(noise_0s)
noise_0s, Ds, Ds_err = noise_0s[i_sort], Ds[i_sort], Ds_err[i_sort]
ax.errorbar(noise_0s, Ds, yerr=Ds_err, label='2D, Diffusing')

noise_0_ths = np.logspace(-3, 2, 1000)
v_0 = 20.0
Ds_th = v_0 ** 2 / (1.0 * noise_0_ths)
ax.plot(noise_0_ths, Ds_th, ls='dashed',
        label=r'$\mathrm{D} = v^2 / (\alpha_0, \mathrm{D}_{r,0})$')

ax.set_xscale('log')
ax.set_yscale('log')
ax.set_xlim(1e-2, 1e1)
ax.set_ylim(3e1, 0.5e5)
ax.legend(loc='upper right', fontsize=26)
ax.set_xlabel(r'$(\alpha_0, \mathrm{D}_{r,0}) / \si{\per\s}$', fontsize=35)
ax.set_ylabel(r'$\mathrm{D} / (\si{\um^2\per\s})$', fontsize=35)
ax.tick_params(axis='both', labelsize=26, pad=10.0)

if save_flag:
    plt.savefig('Dr_scan_uniform.pdf', bbox_inches='tight')
else:
    plt.show()
