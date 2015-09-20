from __future__ import print_function, division
from itertools import product
import numpy as np
from agaro import run_utils
from ahoy.model import Model


default_model_kwargs = {
    'seed': 1,
    'dim': 2,
    'dt': 0.01,
    'n': 5000,
    'v_0': 20.0,
    'dt_mem': 0.1,
    't_mem': 5.0,
    'pore_R': 20.0,
    'pore_turner': 'align',
    'L': np.array([300.0, 300.0]),
    'Dr_0': 1.0,
    'p_0': 1.0,
}

# Better to do this with named tuples
combo_to_chi = {
    ('Dr_0', False, False): 0.38747846573137146,
    ('Dr_0', False, True): 0.91610356364005729,
    ('Dr_0', True, False): 0.55171912452935623,
    ('Dr_0', True, True): 0.95031324074045198,
    ('p_0', False, False): 0.38527303561393739,
    ('p_0', False, True): 0.85519056757936063,
    ('p_0', True, False): 0.54788034865582758,
    ('p_0', True, True): 0.88731933438050015
}


def run_spatial():
    extra_model_kwargs = {
        'spatial_flag': True,
        'periodic_flag': True,
        'pore_flag': True,
        'pore_pf': 0.0707,

        'tumble_flag': True,
        'tumble_chemo_flag': True,
        'temporal_chemo_flag': True,
        'onesided_flag': True,
        'chi': 0.5,
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    model = Model(**model_kwargs)

    t_output_every = 50.0
    t_upto = 100.0
    output_dir = None
    force_resume = None

    run_utils.run_model(t_output_every, output_dir, m=model,
                        force_resume=force_resume, t_upto=t_upto)


def run_Dr_scan_uniform():
    extra_model_kwargs = {
        'spatial_flag': True,
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    t_output_every = 50.0
    t_upto = 1000.0
    noise_0s = np.logspace(-3, 2, 22)
    force_resume = True
    parallel = True

    model_kwarg_sets = []

    dims = [1, 2]
    noise_vars = ['Dr_0', 'p_0']
    for noise_var, dim, noise_0 in product(noise_vars, dims, noise_0s):
        model_kwargs_cur = model_kwargs.copy()
        if noise_var == 'Dr_0':
            if dim == 1:
                continue
            model_kwargs_cur['rotation_flag'] = True
            model_kwargs_cur['tumble_flag'] = False
            model_kwargs_cur['Dr_0'] = noise_0
        else:
            model_kwargs_cur['rotation_flag'] = False
            model_kwargs_cur['tumble_flag'] = True
            model_kwargs_cur['p_0'] = noise_0
        model_kwargs_cur['dim'] = dim
        model_kwarg_sets.append(model_kwargs_cur)
    run_utils.run_kwarg_scan(Model, model_kwarg_sets,
                             t_output_every, t_upto,
                             force_resume=force_resume, parallel=parallel)


def run_chi_scan():
    extra_model_kwargs = {
        'spatial_flag': True,
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    t_output_every = 50.0
    t_upto = 300.0
    chis = np.linspace(0.0, 0.99, 22)
    force_resume = True
    parallel = True

    model_kwarg_sets = []

    dims = [1, 2]
    noise_vars = ['Dr_0', 'p_0']
    onesided_flags = [True, False]
    temporal_chemo_flags = [True, False]
    combos = product(noise_vars, dims, onesided_flags, temporal_chemo_flags,
                     chis)
    for noise_var, dim, onesided_flag, temporal_chemo_flag, chi in combos:
        model_kwargs_cur = model_kwargs.copy()
        if noise_var == 'Dr_0':
            if dim == 1:
                continue
            model_kwargs_cur['rotation_flag'] = True
            model_kwargs_cur['rotation_chemo_flag'] = True
            model_kwargs_cur['tumble_flag'] = False
            model_kwargs_cur['tumble_chemo_flag'] = False
        else:
            model_kwargs_cur['rotation_flag'] = False
            model_kwargs_cur['rotation_chemo_flag'] = False
            model_kwargs_cur['tumble_flag'] = True
            model_kwargs_cur['tumble_chemo_flag'] = True
        model_kwargs_cur['dim'] = dim
        model_kwargs_cur['onesided_flag'] = onesided_flag
        model_kwargs_cur['temporal_chemo_flag'] = temporal_chemo_flag
        model_kwargs_cur['chi'] = chi
        model_kwarg_sets.append(model_kwargs_cur)

    run_utils.run_kwarg_scan(Model, model_kwarg_sets,
                             t_output_every, t_upto,
                             force_resume=force_resume, parallel=parallel)


def run_pf_scan():
    extra_model_kwargs = {
        'spatial_flag': True,
        'periodic_flag': True,
        'pore_flag': True,
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    t_output_every = 50.0
    t_upto = 1000.0
    pore_pfs = np.linspace(0.0, 0.8, 22)
    force_resume = True
    parallel = True

    model_kwarg_sets = []

    pore_turners = ['stall', 'bounce_back', 'reflect', 'align']
    noise_vars = ['Dr_0', 'p_0']
    for noise_var, pore_turner, pore_pf in product(noise_vars, pore_turners,
                                                   pore_pfs):
        model_kwargs_cur = model_kwargs.copy()
        if noise_var == 'Dr_0':
            model_kwargs_cur['rotation_flag'] = True
            model_kwargs_cur['tumble_flag'] = False
        else:
            model_kwargs_cur['rotation_flag'] = False
            model_kwargs_cur['tumble_flag'] = True
        model_kwargs_cur['pore_turner'] = pore_turner
        model_kwargs_cur['pore_pf'] = pore_pf
        model_kwarg_sets.append(model_kwargs_cur)

    run_utils.run_kwarg_scan(Model, model_kwarg_sets,
                             t_output_every, t_upto,
                             force_resume=force_resume, parallel=parallel)


def run_Dr_scan_porous():
    extra_model_kwargs = {
        'spatial_flag': True,
        'periodic_flag': True,
        'pore_flag': True,
        'pore_pf': 0.5,
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    t_output_every = 50.0
    t_upto = 1000.0
    noise_0s = np.logspace(-3, 2, 22)
    force_resume = True
    parallel = True

    model_kwarg_sets = []

    pore_turners = ['stall', 'bounce_back', 'reflect', 'align']
    noise_vars = ['Dr_0', 'p_0']
    for noise_var, pore_turner, noise_0 in product(noise_vars, pore_turners,
                                                   noise_0s):
        model_kwargs_cur = model_kwargs.copy()
        if noise_var == 'Dr_0':
            model_kwargs_cur['rotation_flag'] = True
            model_kwargs_cur['tumble_flag'] = False
            model_kwargs_cur['Dr_0'] = noise_0
        else:
            model_kwargs_cur['rotation_flag'] = False
            model_kwargs_cur['tumble_flag'] = True
            model_kwargs_cur['p_0'] = noise_0
        model_kwargs_cur['pore_turner'] = pore_turner
        model_kwarg_sets.append(model_kwargs_cur)
    run_utils.run_kwarg_scan(Model, model_kwarg_sets,
                             t_output_every, t_upto,
                             force_resume=force_resume, parallel=parallel)


def run_pf_scan_drift():
    extra_model_kwargs = {
        'spatial_flag': True,
        'periodic_flag': True,
        'pore_flag': True,
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    t_output_every = 50.0
    t_upto = 1000.0
    pore_pfs = np.linspace(0.0, 0.8, 22)
    force_resume = True
    parallel = True

    model_kwarg_sets = []

    noise_vars = ['Dr_0', 'p_0']
    onesided_flags = [True, False]
    temporal_chemo_flags = [True, False]
    combos = product(noise_vars, onesided_flags, temporal_chemo_flags,
                     pore_pfs)
    for noise_var, onesided_flag, temporal_chemo_flag, pore_pf in combos:
        model_kwargs_cur = model_kwargs.copy()

        if noise_var == 'Dr_0':
            model_kwargs_cur['rotation_flag'] = True
            model_kwargs_cur['rotation_chemo_flag'] = True
            model_kwargs_cur['tumble_flag'] = False
            model_kwargs_cur['tumble_chemo_flag'] = False
        else:
            model_kwargs_cur['rotation_flag'] = False
            model_kwargs_cur['rotation_chemo_flag'] = False
            model_kwargs_cur['tumble_flag'] = True
            model_kwargs_cur['tumble_chemo_flag'] = True
        model_kwargs_cur['onesided_flag'] = onesided_flag
        model_kwargs_cur['temporal_chemo_flag'] = temporal_chemo_flag
        key = noise_var, onesided_flag, temporal_chemo_flag
        model_kwargs_cur['chi'] = combo_to_chi[key]
        model_kwargs_cur['pore_pf'] = pore_pf
        model_kwarg_sets.append(model_kwargs_cur)

    run_utils.run_kwarg_scan(Model, model_kwarg_sets,
                             t_output_every, t_upto,
                             force_resume=force_resume, parallel=parallel)


def run_field():
    rho_0 = 0.002
    c_delta_0 = 0.1
    c_delta = c_delta_0 / rho_0

    extra_model_kwargs = {
        'rho_0': rho_0,

        'spatial_flag': True,
        'periodic_flag': True,
        'pore_flag': True,

        'origin_flags': np.array([True, False]),

        'L': np.array([1000.0, 300.0]),

        'pore_pf': 0.1,

        'c_field_flag': True,
        'c_dx': 50.0,
        'c_D': 10.0,
        'c_delta': c_delta,
        'c_0': 1.0,

        'tumble_flag': True,
        'tumble_chemo_flag': True,

        'chi': 100.0,
        'temporal_chemo_flag': False,
    }
    model_kwargs = dict(default_model_kwargs, **extra_model_kwargs)

    model = Model(**model_kwargs)

    t_output_every = 1.0
    t_upto = 50.0
    output_dir = None
    force_resume = None

    run_utils.run_model(t_output_every, output_dir, m=model,
                        force_resume=force_resume, t_upto=t_upto)
