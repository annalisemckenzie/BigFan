# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 15:45:57 2018

@author: Annalise

Unit tests for optimization_algorithms.py
ME 599 Project - Spring 2018
"""

from .. import optimization_algorithms as op_al
from .. import objectives as obj
from .. import wake_models as wm
from .. import cost_models as cm
import numpy as np
import pytest


# test constraint checker
def test_check_interference():
    xlocation = [[0.], [200.], [-100.]]
    ylocation = [[0.], [200.], [100.]]
    index = 2
    turb_sep = 100.
    exp_val = op_al.Check_Interference(xlocation, ylocation, index, turb_sep)
    assert not exp_val
    turb_sep = 300.
    exp_val = op_al.Check_Interference(xlocation, ylocation, index, turb_sep)
    assert exp_val


# test x translation
def test_translate_x():
    xlocation = [[0.0, 0.0],
                 [200.0, 73.205080756887767],
                 [300.0, 9.8076211353316296]]
    ylocation = [[0.0, 0.0],
                 [200.0, 273.20508075688775],
                 [500.0, 583.0127018922193]]
    newx = [[0.0, 0.0],
            [200.0, 73.205080756887767],
            [700.0, 356.21778264910711]]
    newy = [[0.0, 0.0],
            [200.0, 273.20508075688775],
            [500.0, 783.0127018922193]]
    index = 2
    turb_sep = 200.
    step_size = 400.
    farm_x = 2000.
    turb_sep = 200.
    directions = [0., 30. / 180. * np.pi]
    exp = op_al.translate_x(xlocation, ylocation, step_size, index, farm_x,
                            turb_sep, directions)
    assert exp == (False, newx, newy)
    xlocation = [[0.0, 0.0],
                 [200.0, 73.205080756887767],
                 [175.0, 1.5544456622768053]]
    ylocation = [[0.0, 0.0],
                 [200.0, 273.20508075688775],
                 [300.0, 347.3076211353316]]
    step_size = -100.
    exp = op_al.translate_x(xlocation, ylocation, step_size, index, farm_x,
                            turb_sep, directions)
    assert exp == (True, xlocation, ylocation)
    index = 0
    exp = op_al.translate_x(xlocation, ylocation, step_size, index, farm_x,
                            turb_sep, directions)
    assert exp == (True, xlocation, ylocation)


def test_translate_y():
    xlocation = [[0.0, 0.0],
                 [200.0, 73.205080756887767],
                 [300.0, 9.8076211353316296]]
    ylocation = [[0.0, 0.0],
                 [200.0, 273.20508075688775],
                 [500.0, 583.0127018922193]]
    newx = [[0.0, 0.0],
            [200.0, 73.205080756887767],
            [300.0, -90.192378864668342]]
    newy = [[0.0, 0.0],
            [200.0, 273.20508075688775],
            [700.0, 756.21778264910711]]
    index = 2
    turb_sep = 200.
    step_size = 200.
    farm_x = 2000.
    turb_sep = 200.
    directions = [0., 30. / 180. * np.pi]
    exp = op_al.translate_y(xlocation, ylocation, step_size, index, farm_x,
                            turb_sep, directions)
    assert exp == (False, newx, newy)
    xlocation = [[0.0, 0.0],
                 [200.0, 73.205080756887767],
                 [175.0, 1.5544456622768053]]
    ylocation = [[0.0, 0.0],
                 [200.0, 273.20508075688775],
                 [300.0, 347.3076211353316]]
    step_size = -100.
    exp = op_al.translate_y(xlocation, ylocation, step_size, index, farm_x,
                            turb_sep, directions)
    assert exp == (True, xlocation, ylocation)
    index = 0
    exp = op_al.translate_y(xlocation, ylocation, step_size, index, farm_x,
                            turb_sep, directions)
    assert exp == (True, xlocation, ylocation)


def test_Rand_Vector():
    initial_num = 12
    exp = op_al.Rand_Vector(initial_num)
    assert len(set(exp)) == 12
    assert len(exp) == 12
    initial_num = 11.5
    with pytest.raises(ValueError):
        exp = op_al.Rand_Vector(initial_num)
    initial_num = 0
    with pytest.raises(ValueError):
        exp = op_al.Rand_Vector(initial_num)


def test_translate_chromosome():
    chromosome = [1, 0, 1, 1, 1, 1, 0, 0, 1, 0, 0, 1]
    binary_x = 3
    binary_y = 3
    options_x = 8
    options_y = 8
    mesh_size = 10.
    directions = [0., np.pi]
    exp = op_al.translate_chromosome(chromosome, binary_x, options_x,
                                     binary_y, options_y, mesh_size,
                                     directions)
    assert np.allclose(exp,
                       ([[50., -50], [40., -40]],
                        [[70., -70.], [40., -40.]]),
                       atol=1e-3, rtol=1e-3)
    chromosome = [-1, 0, 2, 3, 4, 1, 2, 1]
    with pytest.raises(ValueError):
        exp = op_al.translate_chromosome(chromosome, binary_x, options_x,
                                         binary_y, options_y, mesh_size,
                                         directions)


def test_disc_EPS():
    xlocation = [0., 200., 400., 0., 200., 400., 0., 200.]
    ylocation = [0., 0., 0., 200., 200., 200., 400., 400.]
    directions = [i * 10. / 180 * np.pi for i in range(36)]
    ct = 0
    for i, j in zip(xlocation, ylocation):
        new_x = [i]
        new_y = [j]
        for k in range(1, len(directions)):
            new_x.append((i * np.cos(directions[k]))
                         - (j * np.sin(directions[k])))
            new_y.append((i * np.sin(directions[k]))
                         + (j * np.cos(directions[k])))
        xlocation[ct] = new_x
        ylocation[ct] = new_y
        ct += 1
    init_step = 8.
    minstep = 1.
    z0 = 0.0005
    U0 = [7., 10.]
    Zref = 80.
    alphah = 0.11
    ro = 1.225
    yrs = 20.
    WCOE = 0.1
    num_pops = 5
    max_pop_tries = 100
    aif = 0.314
    farm_x = 400.
    farm_y = 400.
    turb_sep = 200.
    Eval_Objective = obj.COP
    Compute_Wake = wm.PARK_3D
    Compute_Cost = cm.offshore_cost
    probwui = [[0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889]]
    rr = [40.] * 8
    hh = [80.] * 8
    cut_in = 3.5
    rated = 12.
    cut_out = 25.
    Cp = 0.5
    availability = 0.95
    nwp = False
    extra = False
    depth = 200.
    distance_to_shore = 32.
    a = 17.19
    mesh_width = 200.
    Ct = 8. / 9.
    rad2 = 200.
    mlDenom = 2.
    numx = 100
    numy = 100
    Lx = 100.
    Ly = 100.
    output = op_al.EPS_disc(xlocation, ylocation, init_step, minstep, z0, U0,
                            Zref, alphah, ro, yrs, WCOE, num_pops,
                            max_pop_tries, aif, farm_x, farm_y, turb_sep,
                            Eval_Objective, Compute_Wake, Compute_Cost,
                            probwui, rr, hh, cut_in, rated, cut_out, Cp,
                            availability, Ct, rad2, numx, numy, Lx, Ly,
                            mlDenom, nwp, extra, depth, distance_to_shore,
                            a, directions, mesh_width)
    sorted_x = sorted([i[0] for i in output[0]])
    sorted_y = sorted([i[0] for i in output[1]])
    assert np.allclose(sorted_x, [0., 0., 0., 200., 200., 400., 400., 400.],
                       atol=1e-2)
    assert np.allclose(sorted_y, [0., 0., 0., 200., 200., 400., 400., 400.],
                       atol=1e-2, rtol=0.01)
    xlocation = [0., 200., 400., 600., 800.,
                 0., 200., 400., 600., 800.,
                 0., 200., 400., 600., 800., 0.]
    ylocation = [0., 0., 0., 0., 0.,
                 200., 200., 200., 200., 200.,
                 400., 400., 400., 400., 400., 600.]
    rr = [40.] * 16
    hh = [80.] * 16
    ct = 0
    for i, j in zip(xlocation, ylocation):
        new_x = [i]
        new_y = [j]
        for k in range(1, len(directions)):
            new_x.append((i * np.cos(directions[k]))
                         - (j * np.sin(directions[k])))
            new_y.append((i * np.sin(directions[k]))
                         + (j * np.cos(directions[k])))
        xlocation[ct] = new_x
        ylocation[ct] = new_y
        ct += 1
    farm_x = 800.
    farm_y = 800.
    output = op_al.EPS_disc(xlocation, ylocation, init_step, minstep, z0, U0,
                            Zref, alphah, ro, yrs, WCOE, num_pops,
                            max_pop_tries, aif, farm_x, farm_y, turb_sep,
                            Eval_Objective, Compute_Wake, Compute_Cost,
                            probwui, rr, hh, cut_in, rated, cut_out, Cp,
                            availability, Ct, rad2, numx, numy, Lx, Ly,
                            mlDenom, nwp, extra, depth, distance_to_shore,
                            a, directions, mesh_width)
    sorted_x = sorted([i[0] for i in output[0]])
    sorted_y = sorted([i[0] for i in output[1]])
    assert np.allclose(sorted_x, [0., 0., 0., 0., 0.,
                                  200., 200.,
                                  400., 400.,
                                  600., 600.,
                                  800., 800., 800., 800., 800.],
                       atol=1e-2, rtol=0.01)
    assert np.allclose(sorted_y, [0., 0., 0., 0., 0.,
                                  200., 200.,
                                  400., 400.,
                                  600., 600.,
                                  800., 800., 800., 800., 800.],
                       atol=1e-2, rtol=0.01)


def test_GA():
    xlocation = [0., 200., 400., 0., 200., 400., 0., 200.]
    ylocation = [0., 0., 0., 200., 200., 200., 400., 400.]
    directions = [i * 10. / 180 * np.pi for i in range(36)]
    ct = 0
    for i, j in zip(xlocation, ylocation):
        new_x = [i]
        new_y = [j]
        for k in range(1, len(directions)):
            new_x.append((i * np.cos(directions[k]))
                         - (j * np.sin(directions[k])))
            new_y.append((i * np.sin(directions[k]))
                         + (j * np.cos(directions[k])))
        xlocation[ct] = new_x
        ylocation[ct] = new_y
        ct += 1
    z0 = 0.0005
    U0 = [7., 10.]
    Zref = 80.
    alphah = 0.11
    ro = 1.225
    yrs = 20.
    WCOE = 0.1
    aif = 0.314
    farm_x = 400.
    farm_y = 400.
    turb_sep = 200.
    Eval_Objective = obj.COP
    Compute_Wake = wm.PARK_3D
    Compute_Cost = cm.offshore_cost
    probwui = [[0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889],
               [0.013888889, 0.013888889], [0.013888889, 0.013888889]]
    rr = [40.] * 8
    hh = [80.] * 8
    cut_in = 3.5
    rated = 12.
    cut_out = 25.
    Cp = 0.5
    availability = 0.95
    nwp = False
    extra = False
    depth = 200.
    distance_to_shore = 32.
    a = 17.19
    mesh_size = 200.
    farm_x = 400.
    farm_y = 400.
    elite = 0.1
    mateable_range = 0.8
    mutation_rate = 0.05
    population_size = 20
    generations_to_converge = 20
    initial_num = 8
    Ct = 8. / 9.
    rad2 = 200.
    mlDenom = 2.
    numx = 100
    numy = 100
    Lx = 100.
    Ly = 100.
    output = op_al.GA(mesh_size, elite, mateable_range, mutation_rate,
                      z0, U0, Zref, alphah, ro, yrs, WCOE, initial_num,
                      population_size, generations_to_converge, aif, farm_x, 
                      farm_y, turb_sep, Eval_Objective, Compute_Wake,
                      Compute_Cost, probwui, rr, hh, cut_in, rated, cut_out,
                      Cp, availability, Ct, rad2, numx, numy, Lx, Ly, mlDenom,
                      nwp, extra, depth, distance_to_shore, a, directions)
    sorted_x = sorted([i[0] for i in output[0]])
    sorted_y = sorted([i[0] for i in output[1]])
    assert np.allclose(sorted_x, [0., 0., 0.,
                                  200., 200.,
                                  400., 400., 400.],
                       atol=1e-2, rtol=0.01)
    assert np.allclose(sorted_y, [0., 0., 0.,
                                  200., 200.,
                                  400., 400., 400.],
                       atol=1e-2, rtol=0.01)


if __name__ == '__main__':
    pass
