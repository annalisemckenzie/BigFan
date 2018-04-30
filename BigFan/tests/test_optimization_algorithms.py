# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 15:45:57 2018

@author: Annalise

Unit tests for optimization_algorithms.py
ME 599 Project - Spring 2018
"""

from .. import optimization_algorithms as op_al
import numpy as np
import pytest

# test constraint checker
def test_check_interference():
    xlocation = [[0.], [200.], [-100.]]
    ylocation = [[0.], [200.], [100.]]
    index = 2
    turb_sep = 100.
    exp_val = op_al.Check_Interference(xlocation, ylocation, index, turb_sep)
    assert exp_val == False
    turb_sep = 300.
    exp_val = op_al.Check_Interference(xlocation, ylocation, index, turb_sep)
    assert exp_val == True

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
    assert exp == ([[50., -50.000000000000007], [40., -40.000000000000007]],
                   [[70., -70.], [40., -39.999999999999993]])
    chromosome = [-1, 0, 2, 3, 4, 1, 2, 1]
    with pytest.raises(ValueError):
        exp = op_al.translate_chromosome(chromosome, binary_x, options_x,
                                         binary_y, options_y, mesh_size,
                                         directions)
if __name__ == '__main__':
    pass