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

dirnames_p_a = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),p=1,obs=Pore(R=20,pf=*,turn=align),c=NoC')
dirnames_Dr_a = glob('/Users/ewj/Desktop/porous/ahoy_data/pf_scan/ahoy_2D,dt=0.01,seed=1,n=5000,align=(0,0),origin=(0,0),v=20,L=(300,300),Dr=1,obs=Pore(R=20,pf=*,turn=align),c=NoC')


def plot(dirname_sets_u, dirname_sets_D, cs, labels, ax):
    ejm_rcparams.prettify_axes(ax)

    for dirnames_u, dirnames_D, c, label in zip(dirname_sets_u,
                                                dirname_sets_D, cs, labels):
        pfs, uds, uds_err = utils.pf_uds_x(dirnames_u)
        i_sort = np.argsort(pfs)
        pfs, uds, uds_err = pfs[i_sort], uds[i_sort], uds_err[i_sort]
        pfs, Ds, Ds_err = utils.pf_Ds_scalar(dirnames_D)
        i_sort = np.argsort(pfs)
        pfs, Ds, Ds_err = pfs[i_sort], Ds[i_sort], Ds_err[i_sort]

        uds_norm = uds / u_x_0
        uds_norm_err = uds_err / u_x_0

        Ds_norm = Ds / D_0
        Ds_norm_err = Ds_err / D_0

        ls = Ds_norm / uds_norm
        ls_err = ls * np.sqrt(np.sum(np.square([Ds_norm_err / Ds_norm,
                                                uds_norm_err / uds_norm])))
        ax.errorbar(pfs, ls, yerr=ls_err, label=label, c=c)

    ax.set_xlim(0.0, 1.0)
    ax.set_ylim(0.5, 6.5)
    ax.set_xlabel(r'$\phi$', fontsize=35)
    ax.set_ylabel(r'$l_x$', fontsize=35)
    ax.tick_params(axis='both', labelsize=26, pad=10.0)

D_0 = 400.0
u_x_0 = 0.2
l_0 = D_0 / u_x_0

fig = plt.figure(figsize=(12, 24 * ejm_rcparams.golden_ratio))

ax = fig.add_subplot(211)
labels = ['Tumbling, two-sided', 'Diffusing, two-sided']
plot([dirnames_p_2side_S, dirnames_Dr_2side_S], [dirnames_p_a, dirnames_Dr_a],
     ejm_rcparams.set2[:2], labels, ax)
labels = ['Tumbling, one-sided', 'Diffusing, one-sided']
plot([dirnames_p_1side_S, dirnames_Dr_1side_S], [dirnames_p_a, dirnames_Dr_a],
     ejm_rcparams.set2[2:4], labels, ax)
ax.add_artist(AnchoredText('(a) Spatial', loc=2, prop=dict(size=26)))
ax.axhline(1.0, c=ejm_rcparams.almost_black, ls='dashed',
           label=r'$\mathrm{D} / u_x = \mathrm{D}_0 / u_{x,0}$')
ax.legend(loc='upper right', fontsize=26)

ax = fig.add_subplot(212)
labels = ['', '']
plot([dirnames_p_2side_T, dirnames_Dr_2side_T], [dirnames_p_a, dirnames_Dr_a],
     ejm_rcparams.set2[:2], labels, ax)
labels = ['', '']
plot([dirnames_p_1side_T, dirnames_Dr_1side_T], [dirnames_p_a, dirnames_Dr_a],
     ejm_rcparams.set2[2:4], labels, ax)
ax.add_artist(AnchoredText('(b) Temporal', loc=2, prop=dict(size=26)))
ax.axhline(1.0, c=ejm_rcparams.almost_black, ls='dashed')

if save_flag:
    plt.savefig('pf_scan_ls.pdf', bbox_inches='tight')
else:
    plt.show()
