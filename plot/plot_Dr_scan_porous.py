from __future__ import print_function, division
from glob import glob
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid.anchored_artists import AnchoredText
from ciabatta import ejm_rcparams
from ahoy.utils import utils

save_flag = True

use_latex = save_flag
use_pgf = True

ejm_rcparams.set_pretty_plots(use_latex, use_pgf)

dirnames_p_a = glob('/Users/ewj/Desktop/porous/ahoy_data/Dr_scan_porous/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=*,obs=Pore(R=20,pf=0.5,turn=align),c=NoC')
dirnames_Dr_a = glob('/Users/ewj/Desktop/porous/ahoy_data/Dr_scan_porous/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=*,obs=Pore(R=20,pf=0.5,turn=align),c=NoC')
dirnames_p_r = glob('/Users/ewj/Desktop/porous/ahoy_data/Dr_scan_porous/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=*,obs=Pore(R=20,pf=0.5,turn=reflect),c=NoC')
dirnames_Dr_r = glob('/Users/ewj/Desktop/porous/ahoy_data/Dr_scan_porous/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=*,obs=Pore(R=20,pf=0.5,turn=reflect),c=NoC')
dirnames_p_b = glob('/Users/ewj/Desktop/porous/ahoy_data/Dr_scan_porous/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=*,obs=Pore(R=20,pf=0.5,turn=bback),c=NoC')
dirnames_Dr_b = glob('/Users/ewj/Desktop/porous/ahoy_data/Dr_scan_porous/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=*,obs=Pore(R=20,pf=0.5,turn=bback),c=NoC')
dirnames_p_s = glob('/Users/ewj/Desktop/porous/ahoy_data/Dr_scan_porous/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=*,obs=Pore(R=20,pf=0.5,turn=stall),c=NoC')
dirnames_Dr_s = glob('/Users/ewj/Desktop/porous/ahoy_data/Dr_scan_porous/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=*,obs=Pore(R=20,pf=0.5,turn=stall),c=NoC')


def plot(dirname_sets, cs, labels, ax):
    ejm_rcparams.prettify_axes(ax)

    for dirnames, c, label in zip(dirname_sets, cs, labels):
        noise_0_tots, Ds, Ds_err = utils.noise_0_tot_Ds_scalar(dirnames)
        i_sort = np.argsort(noise_0_tots)
        noise_0_tots, Ds, Ds_err = (noise_0_tots[i_sort],
                                    Ds[i_sort], Ds_err[i_sort])
        ax.errorbar(noise_0_tots, Ds, yerr=Ds_err, label=label, c=c)

    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlim(1e-2, 1e1)
    ax.set_ylim(1.0, 1e5)

    ax.set_xlabel(r'$(\alpha_0, \mathrm{D}_{r,0}) / \si{\per\s}$', fontsize=35)
    ax.set_ylabel(r'$\mathrm{D} / (\si{\um^2\per\s})$', fontsize=35)
    ax.tick_params(axis='both', labelsize=26, pad=10.0)

fig = plt.figure(figsize=(24, 26 * ejm_rcparams.golden_ratio))

noise_0s = np.logspace(-3, 2, 1000)
v_0 = 20.0
Ds_th = v_0 ** 2 / (1.0 * noise_0s)

ax = fig.add_subplot(221)
plot([dirnames_p_a, dirnames_Dr_a], ejm_rcparams.set2[:2],
     ['Tumbling', 'Diffusing'], ax)
ax.plot(noise_0s, Ds_th, c=ejm_rcparams.set2[2], ls='dashed',
        label=r'$\mathrm{D} = v^2 / (\alpha_0, \mathrm{D}_{r,0})$')
ax.legend(loc='lower left', fontsize=26)
ax.add_artist(AnchoredText('(a) Align', loc=1, prop=dict(size=26)))
ax = fig.add_subplot(222)
plot([dirnames_p_r, dirnames_Dr_r], ejm_rcparams.set2[:2],
     ['Tumbling', 'Diffusing'], ax)
ax.plot(noise_0s, Ds_th, c=ejm_rcparams.set2[2], ls='dashed')
ax.add_artist(AnchoredText('(b) Reflect', loc=1, prop=dict(size=26)))
ax = fig.add_subplot(223)
plot([dirnames_p_b, dirnames_Dr_b], ejm_rcparams.set2[:2],
     ['Tumbling', 'Diffusing'], ax)
ax.plot(noise_0s, Ds_th, c=ejm_rcparams.set2[2], ls='dashed')
ax.add_artist(AnchoredText('(c) Reverse', loc=1, prop=dict(size=26)))
ax = fig.add_subplot(224)
plot([dirnames_p_s, dirnames_Dr_s], ejm_rcparams.set2[:2],
     ['Tumbling', 'Diffusing'], ax)
ax.plot(noise_0s, Ds_th, c=ejm_rcparams.set2[2], ls='dashed')
ax.add_artist(AnchoredText('(d) Stall', loc=1, prop=dict(size=26)))


if save_flag:
    plt.savefig('Dr_scan_porous.pdf', bbox_inches='tight')
else:
    plt.show()
