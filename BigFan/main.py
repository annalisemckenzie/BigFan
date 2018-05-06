# -*- coding: utf-8 -*-
"""
Created on Tue Apr 24 11:18:56 2018

@author: Annalise

ME 599 Project
Spring 2018
Main File - accepts input values and sets up analysis
"""

import csv
import os
import objectives as obj
import cost_models as cm
import wake_models as wm
import optimization_algorithms as oa
import warnings
import random
import matplotlib.pyplot as plt
from time import time


# Take variables from input spreadsheet
def read_inputs():
    """Import user settings for analysis

    Args:

    Returns:
        input variables
        input values
    """
    # point to location of inputs
    dir_path = os.path.dirname(os.path.realpath(__file__))
    dir_path = os.path.join(dir_path, 'inputs.csv')
    all_inputs = []
    all_variables = []
    possible_strings = ['on', 'off', 'eps', 'disceps', 'ga', 'pso', 'hardcode']
    list_values = ['XLocations', 'YLocations', 'rr', 'hh', 'directions',
                   'U0', 'probwui']
    with open(dir_path) as infile:
        info = csv.reader(infile, delimiter=',', quotechar='|')
        next(infile)  # skip first line
        for row in info:
            variable = row[1]
            while '' in row:
                row.remove('')
            if variable in list_values and len(row) > 2:
                if variable in ['XLocations', 'YLocations']:
                    value = [[float(i)] for i in row[2:]]
                else:
                    value = [float(i) for i in row[2:]]
            else:
                try:
                    value = float(row[2])
                except ValueError:
                    # if the value is a string, deal with it appropriately
                    if row[2].lower() == 'false':
                        value = False
                    elif row[2].lower() == 'true':
                        value = True
                    elif row[2].lower() in possible_strings:
                        value = row[2].lower()
                    elif row[2].lower() == 'cost':
                        value = obj.cost
                    elif row[2].lower() == 'profit':
                        value = obj.profit
                    elif row[2].lower() == 'cop':
                        value = obj.COP
                    elif row[2].lower() == 'lcoe':
                        value = obj.LCOE
                    elif row[2].lower() == 'aep':
                        value = obj.AEP
                    elif row[2].lower() == 'park_2d':
                        value = wm.PARK_2D
                    elif row[2].lower() == 'park_3d':
                        value = wm.PARK_3D
                    elif row[2].lower() == 'offshore_cost':
                        value = cm.offshore_cost
                    elif row[2].lower() == 'onshore_cost':
                        value = cm.onshore_cost
                except IndexError:
                    if row[1] != 'shore':
                        value = 'ErrorUseDefault'
                    else:
                        value = 'off'
            all_variables.append(variable)
            all_inputs.append(value)
    type_index = all_variables.index('analysis_type')
    if all_inputs[type_index] == 'ErrorUseDefault':
        raise ValueError('no analysis type specified')
    try:
        num_directions = len(all_inputs[all_variables.index('directions')])
        num_ws = len(all_inputs[all_variables.index('U0')])
        probwui = all_inputs[all_variables.index('probwui')]
        new_prob_format = []
        for i in range(num_directions):
            dummy_var = []
            for j in range(num_ws):
                dummy_var.append(probwui[i*num_ws + j])
            new_prob_format.append(dummy_var)
        all_inputs[all_variables.index('probwui')] = new_prob_format
    except ValueError:
        raise ValueError('no probabilities given for wind speeds')
    return all_variables, all_inputs


def identify_defaults_needed(variables, inputs):
    """Identify which user values need defaults

    Args:
        variables: list of input variable names
        inputs: list of input variable values in same order as names
    Returns:
        indices of variables needing default values
    """
    shore = inputs[variables.index('shore')]
    while 'ErrorUseDefault' in inputs:
        index = inputs.index('ErrorUseDefault')
        inputs[index] = get_defaults(variables[index], shore)
        if variables[index] == 'rr' or variables[index] == 'hh':
            initial_num = inputs[variables['initial_num']]
            inputs[index] = [inputs[index] for ii in range(initial_num)]
    return variables, inputs


def identify_erroneous_inputs(variables, inputs):
    """Identify user values that don't make sense

    Args:
        variables: list of input variable names
        inputs: list of input variable values in same order as names
    Returns:
        none
    """
    string_values = ['shore', 'condition']
    list_values = ['XLocations', 'YLocations', 'rr', 'hh', 'directions',
                   'U0', 'probwui']
    float_values = ['aif', 'site_x', 'site_y', 'cut_in', 'rated', 'ro', 'a',
                    'cut_out', 'Cp', 'availability', 'depth', 'yrs',
                    'WCOE', 'distance_to_shore', 'turb_sep', 'z0', 'num_pops',
                    'max_pop_tries', 'init_step', 'minstep', 'mesh_size',
                    'elite', 'mateable_range', 'mutation_rate',
                    'population_size', 'genreations_to_converge',
                    'self_weight', 'gloabla_weight', 'swarm_size',
                    'initial_num', 'constraint_scale', 'mlDenom']
    bool_values = ['RandomStart', 'nwp', 'optimize']
    function_values = ['Eval_Objective', 'Compute_Wake', 'Compute_Cost']
    for var, inp in zip(variables, inputs):
        check_default = (inp != 'ErrorUseDefault')
        if var in string_values and type(inp) != str and check_default:
            raise ValueError('type(' + str(inp) + ') should be a string'
                             + ' or empty value')
        elif var in list_values and type(inp) != list and check_default:
            raise ValueError('type(' + str(inp) + ') should be a list'
                             + ' or empty value')
        elif var in float_values and type(inp) != float and check_default:
            raise ValueError('type(' + str(inp) + ') should be a float'
                             + ' or empty value')
        elif var in bool_values and type(inp) != bool and check_default:
            raise ValueError('type(' + str(inp) + ') should be a boolean'
                             + ' or empty value')
        elif var in function_values and not callable(inp) and check_default:
            raise ValueError('type(' + str(inp) + ') should be a function'
                             + ' or empty value')


def starting_locations(variables, inputs):
    initial_num = inputs[variables.index('initial_num')]
    xloc = inputs[variables.index('XLocations')]
    yloc = inputs[variables.index('YLocations')]
    RandStart = inputs[variables.index('RandomStart')]
    site_x = inputs[variables.index('site_x')]
    site_y = inputs[variables.index('site_y')]
    turb_sep = inputs[variables.index('turb_sep')]
    directions = inputs[variables.index('directions')]
    if site_x == 'ErrorUseDefault':
        site_x = get_defaults('site_x')
    if site_y == 'ErrorUseDefault':
        site_y = get_defaults('site_y')
    if turb_sep == 'ErrorUseDefault':
        turb_sep = get_defaults('turb_sep')
    if directions == 'ErrorUseDefault':
        directions = get_defaults('directions')
    disc = (inputs[variables.index('analysis_type')] == 'disceps',
            inputs[variables.index('mesh_size')])
    if type(RandStart) == bool:
        if RandStart:
            if initial_num != 'ErrorUseDefault':
                initial_num = inputs[variables.index('initial_num')]
                return random_layout(int(initial_num), site_x, site_y,
                                     turb_sep, directions, disc)
            else:
                warnings.warn('No initial number of turbines specified, '
                              + 'assuming default value and random '
                              + 'initial layout')
                return random_layout(int(initial_num), site_x, site_y,
                                     turb_sep, directions, disc)
        elif xloc == 'ErrorUseDefault' or yloc == 'ErrorUseDefault':
            raise ValueError('You must specify starting turbine locations'
                             + ' if you set the RandomStart variable to'
                             + ' False')
        else:
            return xloc, yloc
    if xloc == 'ErrorUseDefault' or yloc == 'ErrorUseDefault':
        warnings.warn('Insufficient starting information, '
                      + ' assuming random start with default number '
                      + 'of turbines')
        return random_layout(int(initial_num), site_x, site_y, turb_sep,
                             directions, disc)


def random_layout(initial_num, site_x, site_y, turb_sep,
                  directions, disc):
    xloc = [[0.] for i in range(initial_num)]
    yloc = [[0.] for i in range(initial_num)]
    if disc[0]:
        if site_x % disc[1] == 0 and site_y % disc[1] == 0:
            x_opt = int(site_x / disc[1] + 1)
            y_opt = int(site_y / disc[1] + 1)
        else:
            x_opt = int(site_x / disc[1])
            y_opt = int(site_y / disc[1])
    for n in range(0, initial_num):
        reset = 0
        checkx = 0
        while checkx == 0 and reset < 50000:
            if disc[0]:
                xloc[n] = [random.randint(0, x_opt) * disc[1]]
                yloc[n] = [random.randint(0, y_opt) * disc[1]]
            else:
                xloc[n] = [random.uniform(0, site_x)]
                yloc[n] = [random.uniform(0, site_y)]
            interference = oa.Check_Interference(xloc, yloc, n, turb_sep)
            if not interference:
                checkx = 1
                # If there is no interference and the turbine can be placed
            else:
                reset += 1
        if reset == 50000:
            raise ValueError('To many turbines for the space')
    return xloc, yloc


def get_defaults(variable, shore):
    """Get default values

    Args:
        variable: single input variable name for default selection
    Returns:
        default value
    """
    default_variables = ['rr', 'hh', 'aif', 'site_x', 'site_y', 'cut_in',
                         'rated', 'cut_out', 'Cp', 'availability', 'depth',
                         'yrs', 'WCOE', 'distance_to_shore', 'turb_sep',
                         'directions', 'U0', 'probwui', 'Zref',
                         'ro', 'nwp', 'a', 'optimize',
                         'Eval_Objective', 'Compute_Wake',
                         'num_pops', 'max_pop_tries', 'init_step', 'minstep',
                         'mesh_size', 'elite', 'mateable_range',
                         'mutation_rate', 'population_size',
                         'genreations_to_converge', 'self_weight',
                         'gloabla_weight', 'swarm_size', 'initial_num',
                         'constraint_scale', 'mlDenom']
    default_values = [40., 80., 0.314, 2000., 2000., 3., 12., 25., 0.5, 0.95,
                      200., 20., 0.1, 32., 200., [0.], [10.], [[1.]],
                      80., 1.225, False, 27., False, obj.LCOE, wm.PARK_3D, 5,
                      1000, 400., 3., 5., 0.2, 0.8, 0.05, 100., 100., 0.01,
                      0.01, 100, 10, 0.4, 2.]
    if variable in default_variables:
        return default_values[default_variables.index(variable)]
    elif variable == 'XLocations' or variable == 'YLocations':
        return 'NoDefault'
    else:
        if shore == 'on':
            if variable == 'z0':
                return 0.05
            elif variable == 'alphah':
                return 0.15567
            elif variable == 'Compute_Cost':
                return cm.onshore_cost
        elif shore == 'off':
            if variable == 'z0':
                return 0.0005
            elif variable == 'alphah':
                return 0.11
            elif variable == 'Compute_Cost':
                return cm.offshore_cost


def set_up_EPS(variables, values):
    """Set-up and run EPS

    Args:
        variable: ordered names of input values
        values: input values set by user
    Returns:
        optimized (xlocation, ylocation, power, nomove, tot_evals)
    """
    xlocations, ylocations = starting_locations(variables, values)
    start_time = time()
    output = oa.EPS(xlocations, ylocations,
                    values[variables.index('init_step')],
                    values[variables.index('minstep')],
                    values[variables.index('z0')],
                    values[variables.index('U0')],
                    values[variables.index('Zref')],
                    values[variables.index('alphah')],
                    values[variables.index('ro')],
                    values[variables.index('yrs')],
                    values[variables.index('WCOE')],
                    int(values[variables.index('num_pops')]),
                    int(values[variables.index('max_pop_tries')]),
                    values[variables.index('aif')],
                    values[variables.index('site_x')],
                    values[variables.index('site_y')],
                    values[variables.index('turb_sep')],
                    values[variables.index('Eval_Objective')],
                    values[variables.index('Compute_Wake')],
                    values[variables.index('Compute_Cost')],
                    values[variables.index('probwui')],
                    values[variables.index('rr')],
                    values[variables.index('hh')],
                    values[variables.index('cut_in')],
                    values[variables.index('rated')],
                    values[variables.index('cut_out')],
                    values[variables.index('Cp')],
                    values[variables.index('availability')],
                    values[variables.index('nwp')],
                    False,
                    values[variables.index('depth')],
                    values[variables.index('distance_to_shore')],
                    values[variables.index('a')],
                    values[variables.index('directions')])
    total_time = ((time() - start_time) / 60.)
    output = [i for i in output] + [total_time]
    return output


def set_up_discEPS(variables, values):
    """Set-up and run discretized EPS

    Args:
        variable: ordered names of input values
        values: input values set by user
    Returns:
        optimized (xlocation, ylocation, power, nomove, tot_evals)
    """
    xlocations, ylocations = starting_locations(variables, values)
    start_time = time()
    output = oa.EPS_disc(xlocations, ylocations,
                         values[variables.index('init_step')],
                         values[variables.index('minstep')],
                         values[variables.index('z0')],
                         values[variables.index('U0')],
                         values[variables.index('Zref')],
                         values[variables.index('alphah')],
                         values[variables.index('ro')],
                         values[variables.index('yrs')],
                         values[variables.index('WCOE')],
                         int(values[variables.index('num_pops')]),
                         int(values[variables.index('max_pop_tries')]),
                         values[variables.index('aif')],
                         values[variables.index('site_x')],
                         values[variables.index('site_y')],
                         values[variables.index('turb_sep')],
                         values[variables.index('Eval_Objective')],
                         values[variables.index('Compute_Wake')],
                         values[variables.index('Compute_Cost')],
                         values[variables.index('probwui')],
                         values[variables.index('rr')],
                         values[variables.index('hh')],
                         values[variables.index('cut_in')],
                         values[variables.index('rated')],
                         values[variables.index('cut_out')],
                         values[variables.index('Cp')],
                         values[variables.index('availability')],
                         values[variables.index('nwp')],
                         False,
                         values[variables.index('depth')],
                         values[variables.index('distance_to_shore')],
                         values[variables.index('a')],
                         values[variables.index('directions')],
                         values[variables.index('mesh_size')])
    total_time = ((time() - start_time) / 60.)
    output = [i for i in output] + [total_time]
    return output


def set_up_GA(variables, values):
    """Set-up and run GA

    Args:
        variable: ordered names of input values
        values: input values set by user
    Returns:
        optimized (xlocation, ylocation, power, nomove, tot_evals)
    """
    start_time = ()
    output = oa.GA(values[variables.index('mesh_size')],
                   values[variables.index('elite')],
                   values[variables.index('mateable_range')],
                   values[variables.index('mutation_rate')],
                   values[variables.index('z0')],
                   values[variables.index('U0')],
                   values[variables.index('Zref')],
                   values[variables.index('alphah')],
                   values[variables.index('ro')],
                   values[variables.index('yrs')],
                   values[variables.index('WCOE')],
                   values[variables.index('population_size')],
                   values[variables.index('generations_to_converge')],
                   values[variables.index('aif')],
                   values[variables.index('site_x')],
                   values[variables.index('site_y')],
                   values[variables.index('turb_sep')],
                   values[variables.index('Eval_Objective')],
                   values[variables.index('Compute_Wake')],
                   values[variables.index('Compute_Cost')],
                   values[variables.index('probwui')],
                   values[variables.index('rr')],
                   values[variables.index('hh')],
                   values[variables.index('cut_in')],
                   values[variables.index('rated')],
                   values[variables.index('cut_out')],
                   values[variables.index('Cp')],
                   values[variables.index('availability')],
                   values[variables.index('nwp')],
                   False,
                   values[variables.index('depth')],
                   values[variables.index('distance_to_shore')],
                   values[variables.index('a')],
                   values[variables.index('directions')])
    total_time = ((time() - start_time) / 60.)
    output = [i for i in output] + [total_time]
    return output


def set_up_PSO(variables, values):
    """Set-up and run PSO

    Args:
        variable: ordered names of input values
        values: input values set by user
    Returns:
        optimized (xlocation, ylocation, power, nomove, tot_evals)
    """
    start_time = time()
    output = oa.PSO(values[variables.index('self_weight')],
                    values[variables.index('global_weight')],
                    values[variables.index('swarm_size')],
                    values[variables.index('initial_num')],
                    values[variables.index('site_x')],
                    values[variables.index('site_y')],
                    values[variables.index('turb_sep')],
                    values[variables.index('generations_to_converge')],
                    values[variables.index('Eval_Objective')],
                    values[variables.index('constraint_scale')],
                    values[variables.index('z0')],
                    values[variables.index('U0')],
                    values[variables.index('Zref')],
                    values[variables.index('alphah')],
                    values[variables.index('ro')],
                    values[variables.index('aif')],
                    values[variables.index('yrs')],
                    values[variables.index('WCOE')],
                    values[variables.index('population_size')],
                    values[variables.index('generations_to_converge')],
                    values[variables.index('Compute_Wake')],
                    values[variables.index('Compute_Cost')],
                    values[variables.index('probwui')],
                    values[variables.index('rr')],
                    values[variables.index('hh')],
                    values[variables.index('cut_in')],
                    values[variables.index('rated')],
                    values[variables.index('cut_out')],
                    values[variables.index('Cp')],
                    values[variables.index('availability')],
                    values[variables.index('nwp')],
                    False,
                    values[variables.index('depth')],
                    values[variables.index('distance_to_shore')],
                    values[variables.index('a')],
                    values[variables.index('directions')])
    total_time = ((time() - start_time) / 60.)
    output = [i for i in output] + [total_time]
    return output


def set_up_hardcode(variables, values, xvals=0, yvals=0, hh=0,
                    rr=0, no_optimization=True):
    """Set-up and run hardcode analysis, or final analysis for windspeeds

    Args:
        variable: ordered names of input values
        values: input values set by user
    Returns:
        objective requiested, power generated by each turbine,
        windspeeds at each turbine, cumulative layout cost
    """
    if no_optimization:
        objective = values[variables.index('Eval_Objective')]
        no_x = values[variables.index('XLocations')] == 'NoDefault'
        no_y = values[variables.index('YLocations')] == 'NoDefault'
        length_x = len(values[variables.index('XLocations')])
        length_y = len(values[variables.index('YLocations')])
        if no_x or no_y or (length_x != length_y):
            raise ValueError('No input x- and y- locations specified '
                             + 'for hard coded analysis')
        xvals = values[variables.index('XLocations')]
        yvals = values[variables.index('YLocations')]
        rr = values[variables.index('rr')]
        hh = values[variables.index('hh')]
    output = objective(values[variables.index('Compute_Wake')],
                       values[variables.index('Compute_Cost')],
                       xvals, yvals, rr, hh,
                       values[variables.index('z0')],
                       values[variables.index('U0')],
                       values[variables.index('probwui')],
                       values[variables.index('Zref')],
                       values[variables.index('alphah')],
                       values[variables.index('ro')],
                       values[variables.index('aif')],
                       values[variables.index('site_y')],
                       values[variables.index('cut_in')],
                       values[variables.index('rated')],
                       values[variables.index('cut_out')],
                       values[variables.index('Cp')],
                       values[variables.index('availability')],
                       values[variables.index('nwp')],
                       True,
                       values[variables.index('depth')],
                       values[variables.index('yrs')],
                       values[variables.index('WCOE')],
                       values[variables.index('distance_to_shore')],
                       values[variables.index('a')])
    output = [i for i in output]
    return output


def plot_turbines(xlocs, ylocs, hh, rr):
    """Plot turbine layout

    Args:
        xlocs: turbine x-locaations (list)
        ylocs: turbine y-locaations (list)
        hh: turbine hub heights (list)
        rr: turbine rotor radii (list)
    Returns:
        objective requiested
        power generated by each turbine
        windspeeds at each turbine
        cumulative layout cost
    """
    redcx = []
    redcy = []
    yellowcx = []
    yellowcy = []
    greencx = []
    greency = []
    bluecx = []
    bluecy = []
    redtrx = []
    redtry = []
    yellowtrx = []
    yellowtry = []
    greentrx = []
    greentry = []
    bluetrx = []
    bluetry = []
    redrhx = []
    redrhy = []
    yellowrhx = []
    yellowrhy = []
    greenrhx = []
    greenrhy = []
    bluerhx = []
    bluerhy = []
    redsqx = []
    redsqy = []
    yellowsqx = []
    yellowsqy = []
    greensqx = []
    greensqy = []
    bluesqx = []
    bluesqy = []
    noplotx = []
    noploty = []

    for i in range(len(xlocs)):
        if hh[i] <= 60 and rr[i] <= 30:
            redcx.append(xlocs[i][0])
            redcy.append(ylocs[i][0])

        elif hh[i] <= 60 and rr[i] <= 40:
            yellowcx.append(xlocs[i][0])
            yellowcy.append(ylocs[i][0])

        elif hh[i] <= 60 and rr[i] <= 60:
            greencx.append(xlocs[i][0])
            greency.append(ylocs[i][0])

        elif hh[i] <= 60 and rr[i] > 60:
            bluecx.append(xlocs[i][0])
            bluecy.append(ylocs[i][0])

        elif hh[i] <= 80 and rr[i] <= 30:
            redtrx.append(xlocs[i][0])
            redtry.append(ylocs[i][0])

        elif hh[i] <= 80 and rr[i] <= 40:
            yellowtrx.append(xlocs[i][0])
            yellowtry.append(ylocs[i][0])

        elif hh[i] <= 80 and rr[i] <= 60:
            greentrx.append(xlocs[i][0])
            greentry.append(ylocs[i][0])

        elif hh[i] <= 80 and rr[i] > 60:
            bluetrx.append(xlocs[i][0])
            bluetry.append(ylocs[i][0])

        elif hh[i] <= 120 and rr[i] <= 30:
            redrhx.append(xlocs[i][0])
            redrhy.append(ylocs[i][0])

        elif hh[i] <= 120 and rr[i] <= 40:
            yellowrhx.append(xlocs[i][0])
            yellowrhy.append(ylocs[i][0])

        elif hh[i] <= 120 and rr[i] <= 60:
            greenrhx.append(xlocs[i][0])
            greenrhy.append(ylocs[i][0])

        elif hh[i] <= 120 and rr[i] > 60:
            bluerhx.append(xlocs[i][0])
            bluerhy.append(ylocs[i][0])

        elif hh[i] > 120 and rr[i] <= 30:
            redsqx.append(xlocs[i][0])
            redsqy.append(ylocs[i][0])

        elif hh[i] > 120 and rr[i] <= 40:
            yellowsqx.append(xlocs[i][0])
            yellowsqy.append(ylocs[i][0])

        elif hh[i] > 120 and rr[i] <= 60:
            greensqx.append(xlocs[i][0])
            greensqy.append(ylocs[i][0])

        elif hh[i] > 120 and rr[i] > 60:
            bluesqx.append(xlocs[i][0])
            bluesqy.append(ylocs[i][0])

        else:
            noplotx.append(xlocs[i][0])
            noploty.append(ylocs[i][0])

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(redcx, redcy, s=10, c='r', marker="o")
    ax1.scatter(yellowcx, yellowcy, s=10, c='y', marker="o")
    ax1.scatter(greencx, greency, s=10, c='g', marker="o")
    ax1.scatter(bluecy, bluecy, s=10, c='b', marker="o")
    ax1.scatter(redtrx, redtry, s=10, c='r', marker="^")
    ax1.scatter(yellowtrx, yellowtry, s=10, c='y', marker="^")
    ax1.scatter(greentrx, greentry, s=10, c='g', marker="^")
    ax1.scatter(bluetrx, bluetry, s=10, c='b', marker="^")
    ax1.scatter(redrhx, redrhy, s=10, c='r', marker="d")
    ax1.scatter(yellowrhx, yellowrhy, s=10, c='y', marker="d")
    ax1.scatter(greenrhx, greenrhy, s=10, c='g', marker="d")
    ax1.scatter(bluerhy, bluerhy, s=10, c='b', marker="d")
    ax1.scatter(redsqx, redsqy, s=10, c='r', marker="s")
    ax1.scatter(yellowsqx, yellowsqy, s=10, c='y', marker="s")
    ax1.scatter(greensqx, greensqy, s=10, c='g', marker="s")
    ax1.scatter(bluesqx, bluesqy, s=10, c='b', marker="s")

    for i in range(len(xlocs)):
        ax1.annotate(i, (xlocs[i][0], ylocs[i][0]))
    plt.ylabel('Position (m)')
    plt.xlabel('Position (m)')
    plt.title(str('Optimization of ' + str(len(xlocs)) + ' Turbines'))
    plt.show()
    plt.savefig('output_layout.png')


def create_output_file(variables, values, objective_output,
                       optimization_output):
    with open('BigFan_Output.txt', 'w+') as outputfile:
        outputfile.write('***** Simulation Inputs *****')
        # sort inputs alphabetically
        for i in range(len(values)):
            if callable(values[i]):
                if values[i] == obj.profit:
                    values[i] = 'profit'
                elif values[i] == obj.AEP:
                    values[i] = 'AEP'
                elif values[i] == obj.COP:
                    values[i] = 'COP'
                elif values[i] == obj.cost:
                    values[i] = 'cost'
                elif values[i] == obj.LCOE:
                    values[i] = 'LCOE'
                elif values[i] == oa.EPS:
                    values[i] = 'EPS'
                elif values[i] == oa.EPS_disc:
                    values[i] = 'discretized EPS'
                elif values[i] == oa.GA:
                    values[i] = 'GA'
                elif values[i] == oa.PSO:
                    values[i] = 'PSO'
                elif values[i] == cm.offshore_cost:
                    values[i] = 'onshore cost model'
                elif values[i] == cm.onshore_cost:
                    values[i] = 'offshore cost model'
                elif values[i] == wm.PARK_2D:
                    values[i] = '2D PARK'
                elif values[i] == wm.PARK_3D:
                    values[i] = '3D PARK'
        all_out = [(i, j) for i, j in zip(variables, values)]
        all_out.sort(key=lambda x: x[0])
        for i in all_out:
            outputfile.write(i[0] + ': ' + str(i[1]) + '\n')
        outputfile.write('\n\n\n')
        outputfile.write('***** Simulation Outputs *****\n')
        outputfile.write('final objective: '
                         + str(objective_output[0]) + '\n')
        outputfile.write('final turbine power outputs: '
                         + str(objective_output[1]) + '\n')
        outputfile.write('final turbine windspeeds: '
                         + str(objective_output[2]) + '\n')
        outputfile.write('total cost: ' + str(objective_output[3]) + '\n')
        outputfile.write('final turbine x-locations: '
                         + str(optimization_output[0]) + '\n')
        outputfile.write('final turbine y-locations: '
                         + str(optimization_output[1]) + '\n')
        outputfile.write('number of evaluations made: '
                         + str(optimization_output[4]) + '\n')
        outputfile.write('analysis time: ' + str(optimization_output[5])
                         + ' minutes')


if __name__ == "__main__":
    variables, values = read_inputs()
    identify_erroneous_inputs(variables, values)
    variables, values = identify_defaults_needed(variables, values)
    analysis = values[variables.index('analysis_type')]
    if analysis == 'eps':
        output = set_up_EPS(variables, values)
    elif analysis == 'disceps':
        output = set_up_discEPS(variables, values)
    elif analysis == 'ga':
        output = set_up_GA(variables, values)
    elif analysis == 'pso':
        output = set_up_PSO(variables, values)
    elif analysis == 'hardcode':
        output = [values[variables.index('XLocations')],
                  values[variables.index('YLocations')]]
    # regardless of analysis chosen, do final analysis for all info
    start_time = time()
    outobj = set_up_hardcode(variables, values, output[0], output[1],
                             values[variables.index('hh')],
                             values[variables.index('rr')], True)
    if analysis == 'hardcode':
        output = output + ['blank', 'blank', 1, (time() - start_time) / 60.]
    plot_turbines(output[0], output[1],
                  values[variables.index('hh')],
                  values[variables.index('rr')])
    create_output_file(variables, values, outobj, output)
