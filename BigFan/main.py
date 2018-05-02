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
    possible_strings = ['on', 'off']
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
    need_defaults = []  # collect variables that need default values
    while 'ErrorUseDefault' in inputs:
        index = inputs.index('ErrorUseDefault')
        inputs[index] = get_defaults(variables[index], shore)
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
    float_values = ['aif', 'farm_x', 'farm_y', 'cut_in', 'rated', 'ro', 'a',
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
    shore = inputs[variables.index('shore')]
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
    if type(RandStart) == bool:
        if RandStart:
            if initial_num != 'ErrorUseDefault':
                initial_num = get_defaults('initial_num', shore)
                return random_layout(int(initial_num), site_x, site_y,
                                     turb_sep, directions)
            else:
                warnings.warn('No initial number of turbines specified, '
                              + 'assuming default value and random '
                              + 'initial layout')
                return random_layout(int(initial_num), site_x, site_y,
                                     turb_sep, directions)
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
                             directions)


def random_layout(initial_num, site_x, site_y, turb_sep, directions):
    xloc = [[0.] for i in range(initial_num)]
    yloc = [[0.] for i in range(initial_num)]
    for n in range(0, initial_num):
        reset = 0
        checkx = 0
        while checkx == 0 and reset < 50000:
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
    default_variables = ['rr', 'hh', 'aif', 'farm_x', 'farm_y', 'cut_in',
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


if __name__ == "__main__":
    variables, values = read_inputs()
    identify_erroneous_inputs(variables, values)
    variables, values = identify_defaults_needed(variables, values)
    xlocations, ylocations = starting_locations(variables, values)
