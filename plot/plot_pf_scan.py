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

dirnames_p_a = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=1,obs=Pore(R=20,pf=*,turn=align),c=NoC')
dirnames_Dr_a = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=1,obs=Pore(R=20,pf=*,turn=align),c=NoC')
dirnames_p_r = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=1,obs=Pore(R=20,pf=*,turn=reflect),c=NoC')
dirnames_Dr_r = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=1,obs=Pore(R=20,pf=*,turn=reflect),c=NoC')
dirnames_p_b = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=1,obs=Pore(R=20,pf=*,turn=bback),c=NoC')
dirnames_Dr_b = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=1,obs=Pore(R=20,pf=*,turn=bback),c=NoC')
dirnames_p_s = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=1,obs=Pore(R=20,pf=*,turn=stall),c=NoC')
dirnames_Dr_s = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=1,obs=Pore(R=20,pf=*,turn=stall),c=NoC')


def plot(dirname_sets, cs, labels, ax):
    ejm_rcparams.prettify_axes(ax)

    for dirnames, c, label in zip(dirname_sets, cs, labels):
        pfs, Ds, Ds_err = utils.pf_Ds_scalar(dirnames)
        i_sort = np.argsort(pfs)
        pfs, Ds, Ds_err = pfs[i_sort], Ds[i_sort], Ds_err[i_sort]
        ax.errorbar(pfs, Ds / Ds[0], yerr=Ds_err / Ds[0], label=label, c=c)

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 1.0)

    ax.set_xlabel(r'$\phi$', fontsize=35)
    ax.set_ylabel(r'$\mathrm{D} / \mathrm{D}_0$', fontsize=35)
    ax.tick_params(axis='both', labelsize=26, pad=10.0)

fig = plt.figure(figsize=(20, 24 * ejm_rcparams.golden_ratio))

ax = fig.add_subplot(221)
labels = ['Tumbling', 'Diffusing']
plot([dirnames_p_a, dirnames_Dr_a], ejm_rcparams.set2[:2], labels, ax)
ax.legend(loc='lower right', fontsize=26)
ax.add_artist(AnchoredText('(a) Align', loc=3, prop=dict(size=26)))
ax = fig.add_subplot(222)
labels = ['', '']
plot([dirnames_p_r, dirnames_Dr_r], ejm_rcparams.set2[:2], labels, ax)
ax.add_artist(AnchoredText('(b) Reflect', loc=3, prop=dict(size=26)))
ax = fig.add_subplot(223)
labels = ['', '']
plot([dirnames_p_b, dirnames_Dr_b], ejm_rcparams.set2[:2], labels, ax)
ax.add_artist(AnchoredText('(c) Reverse', loc=3, prop=dict(size=26)))
ax = fig.add_subplot(224)
labels = ['', '']
plot([dirnames_p_s, dirnames_Dr_s], ejm_rcparams.set2[:2], labels, ax)
ax.add_artist(AnchoredText('(d) Stall', loc=3, prop=dict(size=26)))

if save_flag:
    plt.savefig('pf_scan.pdf', bbox_inches='tight')
else:
    plt.show()
