from __future__ import print_function, division
from os.path import basename
from glob import glob
import numpy as np
from scipy.optimize import curve_fit
from ahoy.utils import utils

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

D_0 = 400.0
u_x_0 = 0.2
l_0 = D_0 / u_x_0

dirname_sets = [
    (dirnames_p_1side_T, dirnames_p_a),
    (dirnames_Dr_1side_T, dirnames_Dr_a),
    (dirnames_p_2side_T, dirnames_p_a),
    (dirnames_Dr_2side_T, dirnames_Dr_a),
    (dirnames_p_1side_S, dirnames_p_a),
    (dirnames_Dr_1side_S, dirnames_Dr_a),
    (dirnames_p_2side_S, dirnames_p_a),
    (dirnames_Dr_2side_S, dirnames_Dr_a),
]


def f(x, m):
    return 1.0 + m * x


for dirnames_u, dirnames_D in dirname_sets:
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

    # pfs, ls, ls_err = pfs[:-3], ls[:-3], ls_err[:-3]
    popt, pcov = curve_fit(f, pfs, ls, sigma=ls_err)
    # print('{}: {:g} pm {:.1g}'.format(basename(dirnames_u[0]),
    #                                   popt[0], np.sqrt(pcov[0, 0])))
    print('{}: {} pm {:.1g}'.format(basename(dirnames_u[0]),
                                      ls, ls_err[-1]))
