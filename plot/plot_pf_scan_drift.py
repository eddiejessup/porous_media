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

dirnames_p_1side_T = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan_drift/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=1,chi=*,side=1,type=T,dtMem=0.1,tMem=5,obs=Pore(R=20,pf=*,turn=align),c=NoC')
dirnames_Dr_1side_T = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan_drift/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=1,chi=*,side=1,type=T,dtMem=0.1,tMem=5,obs=Pore(R=20,pf=*,turn=align),c=NoC')
dirnames_p_2side_T = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan_drift/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=1,chi=*,side=2,type=T,dtMem=0.1,tMem=5,obs=Pore(R=20,pf=*,turn=align),c=NoC')
dirnames_Dr_2side_T = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan_drift/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=1,chi=*,side=2,type=T,dtMem=0.1,tMem=5,obs=Pore(R=20,pf=*,turn=align),c=NoC')
dirnames_p_1side_S = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan_drift/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=1,chi=*,side=1,type=S,obs=Pore(R=20,pf=*,turn=align),c=NoC')
dirnames_Dr_1side_S = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan_drift/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=1,chi=*,side=1,type=S,obs=Pore(R=20,pf=*,turn=align),c=NoC')
dirnames_p_2side_S = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan_drift/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=1,chi=*,side=2,type=S,obs=Pore(R=20,pf=*,turn=align),c=NoC')
dirnames_Dr_2side_S = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan_drift/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=1,chi=*,side=2,type=S,obs=Pore(R=20,pf=*,turn=align),c=NoC')


def plot(dirname_sets, cs, labels, ax):
    ejm_rcparams.prettify_axes(ax)

    for dirnames, c, label in zip(dirname_sets, cs, labels):
        pfs, uds, uds_err = utils.pf_uds_x(dirnames)
        i_sort = np.argsort(pfs)
        pfs, uds, uds_err = pfs[i_sort], uds[i_sort], uds_err[i_sort]
        ax.errorbar(pfs, uds, yerr=uds_err, label=label, c=c)

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.0, 0.21)

    ax.set_xlabel(r'$\phi$', fontsize=35)
    ax.set_ylabel(r'$u_x$', fontsize=35)
    ax.tick_params(axis='both', labelsize=26, pad=10.0)

fig = plt.figure(figsize=(12, 24 * ejm_rcparams.golden_ratio))

ax = fig.add_subplot(211)
labels = ['Tumbling, two-sided', 'Diffusing, two-sided']
plot([dirnames_p_2side_S, dirnames_Dr_2side_S],
     ejm_rcparams.set2[:2], labels, ax)
labels = ['Tumbling, one-sided', 'Diffusing, one-sided']
plot([dirnames_p_1side_S, dirnames_Dr_1side_S],
     ejm_rcparams.set2[2:4], labels, ax)
ax.add_artist(AnchoredText('(a) Spatial',
              loc=1, prop=dict(size=26)))
ax.legend(loc='lower left', fontsize=26)

ax = fig.add_subplot(212)
labels = ['', '']
plot([dirnames_p_2side_T, dirnames_Dr_2side_T],
     ejm_rcparams.set2[:2], labels, ax)
labels = ['', '']
plot([dirnames_p_1side_T, dirnames_Dr_1side_T],
     ejm_rcparams.set2[2:4], labels, ax)
ax.add_artist(AnchoredText('(b) Temporal',
              loc=1, prop=dict(size=26)))

if save_flag:
    plt.savefig('pf_scan_drift.pdf', bbox_inches='tight')
else:
    plt.show()
