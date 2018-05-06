# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 12:00:41 2018

@author: Annalise Miller

ME 599 Project
Spring 2018
Algorithm Options
"""

import numpy as np
import random
import matplotlib.pyplot as plt


def Check_Interference(xlocation, ylocation, index, turbine_sep_distance):
    """Check interference between turbines

    Args:
        xlocation: list of x-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        ylocation: list of y-coordinates of wind turbines where each item
            is a list of y-locations for each onset wind angle
        index: index number of turbine being checked for constraint violation
        turbine_sep_distance: required turbine separation distance
    Returns:
        constraint violation flag
    """
    interference = False  # No constraint violated
    if index != 'pop':
        # identify turbine of interest
        xold = xlocation[index][0]
        yold = ylocation[index][0]
        # check for inerference with all other turbines
        for j, k in enumerate(xlocation):
            if j != index:  # don't check turbine's interference with self
                checkx = xold - k[0]
                checky = yold - ylocation[j][0]
                # calculate distance between 2 turbines
                checkrad = np.sqrt(checkx ** 2.0 + checky ** 2.0)
                # if constraint is violated
                if checkrad < turbine_sep_distance:
                    interference = True
                    return interference
    else:
        for i in range(len(xlocation) - 1):
            for j in range(i + 1, len(xlocation)):
                checkx = xlocation[i][0] - xlocation[j][0]
                checky = ylocation[i][0] - ylocation[j][0]
                # calculate distance between 2 turbines
                checkrad = np.sqrt(checkx ** 2.0 + checky ** 2.0)
                if checkrad < turbine_sep_distance:
                    interference = True
                    return interference
    return interference


def translate_x(xlocation, ylocation, step_size, index, farm_x,
                turbine_sep_distance, directions):
    """Translate a specific turbine in the x-direction

    Args:
        xlocation: list of x-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        ylocation: list of y-coordinates of wind turbines where each item
            is a list of y-locations for each onset wind angle
        step_size: distance you're moving turbine
        index: index number of turbine
        farm_x: length of farm in the x-direction
        turbine_sep_distance: required turbine separation distance
        directions: onset wind angles
    Returns:
        constraint violation flag
        new turbine xlocations for each onset angle
        new turbine ylocations for each onset angle
    """
    transflag = False
    xstart = xlocation[index]
    # find preliminary new x-location given step size
    xfinish = xstart[0] + step_size
    # if this new x-location is not out of bounds,
    # and does not violate constraints, translate it
    # check for turbine interference
    xlocation[index] = [xfinish]
    interference = Check_Interference(xlocation, ylocation, index,
                                      turbine_sep_distance)
    if xfinish >= 0 and xfinish <= farm_x and not interference:
        newx = []
        newy = []
        for rads in directions:
            newx.append(np.cos(rads) * xfinish
                        - np.sin(rads) * ylocation[index][0])
            newy.append(np.sin(rads) * xfinish
                        + np.cos(rads) * ylocation[index][0])
        xlocation[index] = newx  # update turbine coordinates
        ylocation[index] = newy
        return transflag, xlocation, ylocation  # return no error
    else:
        xlocation[index] = xstart
        transflag = True  # return error
        return transflag, xlocation, ylocation


def translate_y(xlocation, ylocation, step_size, index, farm_y,
                turbine_sep_distance, directions):
    """Translate a specific turbine in the y-direction

    Args:
        xlocation: list of x-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        ylocation: list of y-coordinates of wind turbines where each item
            is a list of y-locations for each onset wind angle
        step_size: distance you're moving turbine
        index: index number of turbine
        farm_y: length of farm in the y-direction
        turbine_sep_distance: required turbine separation distance
        directions: onset wind angles
    Returns:
        constraint violation flag
        new turbine xlocations for each onset angle
        new turbine ylocations for each onset angle
    """
    transflag = False
    ystart = ylocation[index]
    # find preliminary new y-location given step size
    yfinish = ystart[0] + step_size
    ylocation[index] = [yfinish]
    # if this new x-location is not out of bounds,
    # and does not violate constraints, translate it
    # check for turbine interference
    interference = Check_Interference(xlocation, ylocation, index,
                                      turbine_sep_distance)
    if yfinish >= 0 and yfinish <= farm_y and not interference:
        newx = []
        newy = []
        for rads in directions:
            newx.append(np.cos(rads) * xlocation[index][0]
                        - np.sin(rads) * yfinish)
            newy.append(np.sin(rads) * xlocation[index][0]
                        + np.cos(rads) * yfinish)
        xlocation[index] = newx  # update turbine coordinates
        ylocation[index] = newy
        return transflag, xlocation, ylocation
    else:
        ylocation[index] = ystart
        transflag = True
        return transflag, xlocation, ylocation


def Rand_Vector(initial_num):
    """Create random turbine order for EPS

    Args:
        initial_num: number of turbines being optimized
    Returns:
        random order of those turbines
    """
    if initial_num < 1:
        raise ValueError('Rand_Vector: fewer than one turbine '
                         + 'being optimized')
    if type(initial_num) != int:
            raise ValueError('Rand_Vector: non-integer number of '
                             + 'turbines being optimized')
    random_vec = []
    for i in range(0, initial_num):
        random_vec.append(i)

    # shuffle elements by randomly exchanging each with one other
    for i in range(0, len(random_vec)):
        # select random other value in vector and flip the two
        r = random.randint(0, len(random_vec)-1)
        temp = random_vec[i]
        random_vec[i] = random_vec[r]
        random_vec[r] = temp
    return random_vec


def EPS(xlocation, ylocation, init_step, minstep,
        z0, U0, Zref, alphah, ro, yrs, WCOE, num_pops,
        max_pop_tries, aif, farm_x, farm_y, turb_sep, Eval_Objective,
        Compute_Wake, Compute_Cost, probwui, rr, hh, cut_in, rated, cut_out,
        Cp, availability, nwp, extra, depth, distance_to_shore, a, directions):
    """Extended Pattern Search

    Args:
        xlocation: list of x-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        ylocation: list of y-coordinates of wind turbines where each item
            is a list of y-locations for each onset wind angle
        init_step: initial step size for EPS
        minstep: smallest step size for EPS
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        Zref: Wind speed reference height
        alphah: power law exponent
        ro: air density (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        num_pops: number of poor performing turbines popped each round
        max_pop_tries: number of times a single turbine may attempt
            a new location in the popping algorithm
        aif: axial induction factor (float)
        farm_x: length of wind farm in x direction in meters (float)
        farm_y: length of wind farm in y direction in meters (float)
        turb_sep: minimum tubine separation requirement
        Eval_Objective: objective being minimized by EPS
        Compute_Wake: function encapsulating wake model
        Compute_Cost: function encapsulating cost model
        probwui: list of lists for probability of onset wind conditions
            first index represets onset wind direction index
            second index represents onset wind speed index
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        cut_in: turbine cut-in wind speed (float)
        rated: turbine rated wind speed (float)
        cut-out: turbine cut-out speed (float)
        Cp: power coefficient (float)
        availability: turbine availability (float)
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
        depth: water depth in meters (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
        directions: list of onset wind angles
    Returns:
        optimized turbine xlocation
        optimized turbine ylocation
        optimized turbine power
        optimized objctive
        Number of objective evaluations until convergence
    """
    plt.figure()
    plt.scatter([i[0] for i in xlocation], [i[0] for i in ylocation])
    initial_num = len(xlocation)
    stopped = [0] * initial_num
    # Clear_Vectors()
    tot_evals = 0
    num_EPS_repeats = 1  # number of times you completely reset EPS
    for h in range(0, num_EPS_repeats):
        # develop preliminary objective for comparison purposes
        tot_evals += 1
        nomove, power = Eval_Objective(Compute_Wake, Compute_Cost, xlocation,
                                       ylocation, rr, hh, z0, U0, probwui,
                                       Zref, alphah, ro, aif, farm_y, cut_in,
                                       rated, cut_out, Cp, availability,
                                       nwp, extra, depth, yrs, WCOE,
                                       distance_to_shore, a)
        step2 = init_step
        while step2 >= minstep:
            # create a randomly ordered vector of turbines
            random_vec = Rand_Vector(initial_num)
            for j in range(0, len(random_vec)):
                i = random_vec[j]
                stopped[i] = 0  # indicates turbine has not stopped moving
                # print('Turbine ' + str(i) + ' is being tested.')
                flag = False  # indicates move was taken
                innerflag = 0  # indicates move not taken
                transflag = 0  # indicates
                # print('The nomove value for turbine ', i, ' is ', nomove)
                # print('stepped into while loop')
                # If turbine is in back half of filed, move backwards first
                if ylocation[i][0] >= (farm_y / 2.0):
                    if innerflag == 0 and not flag:
                        (transflag,
                         xlocation,
                         ylocation) = translate_y(xlocation, ylocation, step2,
                                                  i, farm_y, turb_sep,
                                                  directions)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 1  # move 1 was attempted
                            # move 1 failed
                            # print('turbine not moved up.')
                        # if there is no interference, evaluate and store
                        else:
                            tot_evals += 1
                            move1, power = Eval_Objective(Compute_Wake,
                                                          Compute_Cost,
                                                          xlocation,
                                                          ylocation,
                                                          rr, hh, z0, U0,
                                                          probwui, Zref,
                                                          alphah, ro, aif,
                                                          farm_y, cut_in,
                                                          rated, cut_out, Cp,
                                                          availability,
                                                          nwp, extra, depth,
                                                          yrs, WCOE,
                                                          distance_to_shore, a)
                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move1 >= nomove:
                                (transflag,
                                 xlocation,
                                 ylocation) = translate_y(xlocation, ylocation,
                                                          -step2, i, farm_y,
                                                          turb_sep, directions)
                                innerflag = 1
                                # print('turbine not moved up.')
                            # evaluation is better,
                            # keep move, go to next turbine
                            else:
                                flag = True
                                nomove = move1 * 1.
                                # print('turbine ' + str(i)
                                #       + ' moved up.' + str(move1))
                                # Add Hubheight search here in future
                                # HubHeight_Search(etc...)
                    # move 1 was just unsucessfully attempted
                    if innerflag == 1 and not flag:
                        (transflag,
                         xlocation,
                         ylocation) = translate_x(xlocation, ylocation, -step2,
                                                  i, farm_y, turb_sep,
                                                  directions)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 2  # move 2 was attempted and failed
                            # print('turbine not left.')
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move2, power = Eval_Objective(Compute_Wake,
                                                          Compute_Cost,
                                                          xlocation,
                                                          ylocation,
                                                          rr, hh, z0, U0,
                                                          probwui, Zref,
                                                          alphah, ro, aif,
                                                          farm_y, cut_in,
                                                          rated, cut_out, Cp,
                                                          availability,
                                                          nwp, extra, depth,
                                                          yrs, WCOE,
                                                          distance_to_shore, a)
                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move2 >= nomove:
                                (transflag,
                                 xlocation,
                                 ylocation) = translate_x(xlocation, ylocation,
                                                          step2, i, farm_y,
                                                          turb_sep, directions)
                                innerflag = 2
                                # print('turbine not moved left.')
                            # evaluation is better,
                            # keep move, go to next turbine
                            else:
                                flag = True
                                nomove = move2 * 1.
                                # print('turbine ' + str(i)
                                #       + ' moved left.' + str(move2))
                                # Add Hubheight search here in future
                                # HubHeight_Search(etc...)
                    # move 2 was just unsucessfully attempted
                    if innerflag == 2 and not flag:
                        (transflag,
                         xlocation,
                         ylocation) = translate_y(xlocation, ylocation, -step2,
                                                  i, farm_y, turb_sep,
                                                  directions)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 3  # move3 was attempted
                            # print('turbine not moved down.')
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move3, power = Eval_Objective(Compute_Wake,
                                                          Compute_Cost,
                                                          xlocation,
                                                          ylocation,
                                                          rr, hh, z0, U0,
                                                          probwui, Zref,
                                                          alphah, ro, aif,
                                                          farm_y, cut_in,
                                                          rated, cut_out, Cp,
                                                          availability,
                                                          nwp, extra, depth,
                                                          yrs, WCOE,
                                                          distance_to_shore, a)

                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move3 >= nomove:
                                (transflag,
                                 xlocation,
                                 ylocation) = translate_y(xlocation, ylocation,
                                                          step2, i, farm_y,
                                                          turb_sep, directions)
                                innerflag = 3
                                # print('turbine not moved down.')
                            # evaluation is better,
                            # keep move, go to next turbine
                            else:
                                flag = True
                                nomove = move3 * 1.
                                # print('turbine ' + str(i)
                                #       + ' moved down.' + str(move3))
                                # Add Hubheight search here in future
                                # HubHeight_Search(etc...)
                    if innerflag == 3 and not flag:
                        # move the turbine one step right
                        (transflag,
                         xlocation,
                         ylocation) = translate_x(xlocation, ylocation, step2,
                                                  i, farm_y, turb_sep,
                                                  directions)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 4  # signifies move 1 was attempted
                            # print('Turbine not moved right.')
                        # if there is the turbine is in bounds,
                        # evaluate and store
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move4, power = Eval_Objective(Compute_Wake,
                                                          Compute_Cost,
                                                          xlocation,
                                                          ylocation,
                                                          rr, hh, z0, U0,
                                                          probwui, Zref,
                                                          alphah, ro, aif,
                                                          farm_y, cut_in,
                                                          rated, cut_out, Cp,
                                                          availability,
                                                          nwp, extra, depth,
                                                          yrs, WCOE,
                                                          distance_to_shore, a)

                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move4 >= nomove:
                                (transflag,
                                 xlocation,
                                 ylocation) = translate_x(xlocation, ylocation,
                                                          -step2, i, farm_y,
                                                          turb_sep, directions)
                                innerflag = 4
                                # print('Turbine not moved right.')
                            else:
                                flag = True  # move kept
                                nomove = move4 * 1.
                            # print('turbine ' + str(i)
                            #       + ' moved right.' + str(move4))
                            # Add Hubheight search here in future
                            # HubHeight_Search(etc...)
                    # no moves for this turbine at this step size
                    if innerflag == 4 and not flag:
                        stopped[i] = 1
                        # Add Hubheight search here in future
                        # HubHeight_Search(etc...)
                # if turbine is in front half of field, move forward first
                elif ylocation[i][0] < (farm_y / 2.0):
                    if innerflag == 0 and not flag:
                        (transflag,
                         xlocation,
                         ylocation) = translate_y(xlocation, ylocation, -step2,
                                                  i, farm_y, turb_sep,
                                                  directions)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 1  # move 1 was attempted
                            # print('turbine not moved down.')
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move1, power = Eval_Objective(Compute_Wake,
                                                          Compute_Cost,
                                                          xlocation,
                                                          ylocation,
                                                          rr, hh, z0, U0,
                                                          probwui, Zref,
                                                          alphah, ro, aif,
                                                          farm_y, cut_in,
                                                          rated, cut_out, Cp,
                                                          availability,
                                                          nwp, extra, depth,
                                                          yrs, WCOE,
                                                          distance_to_shore, a)

                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move1 >= nomove:
                                (transflag,
                                 xlocation,
                                 ylocation) = translate_y(xlocation, ylocation,
                                                          step2, i, farm_y,
                                                          turb_sep, directions)
                                innerflag = 1
                                print('turbine not moved up.')
                            # evaluation is better,
                            # keep move, go to next turbine
                            else:
                                flag = True
                                nomove = move1 * 1.
                                print('turbine ' + str(i)
                                      + ' moved up.' + str(move1))
                                # Add Hubheight search here in future
                                # HubHeight_Search(etc...)
                    # move 2 was just unsucessfully attempted
                    if innerflag == 1 and not flag:
                        (transflag,
                         xlocation,
                         ylocation) = translate_x(xlocation, ylocation, -step2,
                                                  i, farm_y, turb_sep,
                                                  directions)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 2  # move 2 was attempted
                            print('turbine not left.')
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move2, power = Eval_Objective(Compute_Wake,
                                                          Compute_Cost,
                                                          xlocation,
                                                          ylocation,
                                                          rr, hh, z0, U0,
                                                          probwui, Zref,
                                                          alphah, ro, aif,
                                                          farm_y, cut_in,
                                                          rated, cut_out, Cp,
                                                          availability,
                                                          nwp, extra, depth,
                                                          yrs, WCOE,
                                                          distance_to_shore, a)

                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move2 >= nomove:
                                (transflag,
                                 xlocation,
                                 ylocation) = translate_x(xlocation, ylocation,
                                                          step2, i, farm_y,
                                                          turb_sep, directions)
                                innerflag = 2
                                print('turbine not moved left.')
                            # evaluation is better,
                            # keep move, go to next turbine
                            else:
                                flag = True
                                nomove = move2 * 1.
                                print('turbine ' + str(i)
                                      + ' moved left.' + str(move2))
                                # Add Hubheight search here in future
                                # HubHeight_Search(etc...)
                    # move 3 was just unsucessfully attempted
                    if innerflag == 2 and not flag:
                        (transflag,
                         xlocatin,
                         ylocation) = translate_y(xlocation, ylocation, step2,
                                                  i, farm_y, turb_sep,
                                                  directions)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 3  # move 3 was attempted
                            print('turbine not moved up.')
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move3, power = Eval_Objective(Compute_Wake,
                                                          Compute_Cost,
                                                          xlocation,
                                                          ylocation,
                                                          rr, hh, z0, U0,
                                                          probwui, Zref,
                                                          alphah, ro, aif,
                                                          farm_y, cut_in,
                                                          rated, cut_out, Cp,
                                                          availability,
                                                          nwp, extra, depth,
                                                          yrs, WCOE,
                                                          distance_to_shore, a)

                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move3 >= nomove:
                                (transflag,
                                 xlocation,
                                 ylocation) = translate_y(xlocation, ylocation,
                                                          -step2, i, farm_y,
                                                          turb_sep, directions)
                                innerflag = 3
                                print('turbine not moved down.')
                            # evaluation is better,
                            # keep move, go to next turbine
                            else:
                                flag = True
                                nomove = move3 * 1.
                                print('turbine ' + str(i)
                                      + ' moved down.' + str(move3))
                                # Add Hubheight search here in future
                                # HubHeight_Search(etc...)
                    if innerflag == 3 and not flag:
                        # move the turbine one step right
                        (transflag,
                         xlocation,
                         ylocation) = translate_x(xlocation, ylocation, step2,
                                                  i, farm_y, turb_sep,
                                                  directions)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 4  # signifies move 4 was attempted
                            print('Turbine not moved right.')
                        # if there is the turbine is in bounds,
                        # evaluate and store
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move4, power = Eval_Objective(Compute_Wake,
                                                          Compute_Cost,
                                                          xlocation,
                                                          ylocation,
                                                          rr, hh, z0, U0,
                                                          probwui, Zref,
                                                          alphah, ro, aif,
                                                          farm_y, cut_in,
                                                          rated, cut_out, Cp,
                                                          availability,
                                                          nwp, extra, depth,
                                                          yrs, WCOE,
                                                          distance_to_shore, a)

                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move4 >= nomove:
                                (transflag,
                                 xlocation,
                                 ylocation) = translate_x(xlocation, ylocation,
                                                          -step2, i, farm_y,
                                                          turb_sep, directions)
                                innerflag = 4
                                print('Turbine not moved right.')
                            else:
                                flag = True  # signifies movement was kept
                                nomove = move4 * 1.
                            print('turbine ', i, ' moved right.', move4)
                            # Add Hubheight search here in future
                            # HubHeight_Search(etc...)
                    # no moves for this turbine at this step size
                    if innerflag == 4 and not flag:
                        stopped[i] = 1
                        # Add Hubheight search here in future
                        # HubHeight_Search(etc...)

            # count how many turbines have stopped moving
            exit_css = sum(stopped)
            print(exit_css)
            if exit_css == initial_num:
                # all turbines have stopped moving at this step size
                # find worst performing turbine and randomly assign elsewhere
                for b in range(0, num_pops):
                    # print("No moves at step size "
                    #       + str(step2)
                    #       + " are possible. Popping weakest turbine.")
                    min_power = 5000000.  # dummy large value for min calc
                    # create a randomly ordered vector of turbines
                    random_vec2 = Rand_Vector(initial_num)
                    for j in range(0, initial_num):
                        randorder = random_vec2[j]
                        # determine turbine with lowest power production
                        if sum(power[randorder]) < min_power:
                            min_power = sum(power[randorder])
                            min_turb = randorder
                    initialx = xlocation[min_turb]
                    initialy = ylocation[min_turb]
                    k = 0
                    flag = False
                    while not flag and k < max_pop_tries:
                        k += 1
                        startx = random.uniform(0, farm_x)
                        starty = random.uniform(0, farm_y)
                        xnew = []
                        ynew = []
                        for rads in directions:
                            xnew.append(np.cos(rads) * startx
                                        - np.sin(rads) * starty)
                            ynew.append(np.sin(rads) * startx
                                        + np.cos(rads) * starty)
                        xlocation[min_turb] = xnew
                        ylocation[min_turb] = ynew
                        interference = Check_Interference(xlocation,
                                                          ylocation,
                                                          min_turb,
                                                          turb_sep)
                        if interference:
                            xlocation[min_turb] = initialx
                            ylocation[min_turb] = initialy
                            # print('Turbine cannot be relocated without '
                            #       + 'interference, trying agian.')
                        else:
                            tot_evals += 1
                            new_eval, power = Eval_Objective(Compute_Wake,
                                                             Compute_Cost,
                                                             xlocation,
                                                             ylocation,
                                                             rr, hh, z0, U0,
                                                             probwui, Zref,
                                                             alphah, ro, aif,
                                                             farm_y, cut_in,
                                                             rated, cut_out,
                                                             Cp, availability,
                                                             nwp, extra, depth,
                                                             yrs, WCOE,
                                                             distance_to_shore,
                                                             a)

                            if new_eval < nomove:
                                flag = True
                                nomove = new_eval * 1.
                                # NOTE: Hubheight and Rotor Radius Search are
                                #       not implimented in this version of code
                                #       Should you wish to add it, this would
                                #       be an appropriate place to do so
                                # HubHeight_Search(etc...)
                                # print('Move has improved the evaluation.'
                                #       + 'Continuing pattern serach.')
                            else:
                                xlocation[min_turb] = initialx
                                ylocation[min_turb] = initialy
                                # print('Move did not improve evaluation.'
                                #       + 'Trying new moves.')
                # halving step size
                step2 = step2 / 2.0
    return xlocation, ylocation, power, nomove, tot_evals


def EPS_disc(xlocation, ylocation, init_step, minstep, z0, U0, Zref,
             alphah, ro, yrs, WCOE, num_pops, max_pop_tries, aif, farm_x,
             farm_y, turb_sep, Eval_Objective, Compute_Wake, Compute_Cost,
             probwui, rr, hh, cut_in, rated, cut_out, Cp, availability, nwp,
             extra, depth, distance_to_shore, a, directions, mesh_width):
    """Discretized Extended Pattern Search

    Args:
        xlocation: list of x-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        ylocation: list of y-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        init_step: initial step size for EPS
        minstep: smallest step size for EPS
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        Zref: Wind speed reference height
        alphah: power law exponent
        ro: air density (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        num_pops: number of poor performing turbines popped each round
        max_pop_tries: number of times a single turbine may attempt
            a new location in the popping algorithm
        aif: axial induction factor (float)
        farm_x: length of wind farm in x direction in meters (float)
        farm_y: length of wind farm in y direction in meters (float)
        turb_sep: minimum tubine separation requirement
        Eval_Objective: objective being minimized by EPS
        Compute_Wake: function encapsulating wake model
        Compute_Cost: function encapsulating cost model
        probwui: list of lists for probability of onset wind conditions
            first index represets onset wind direction index
            second index represents onset wind speed index
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        cut_in: turbine cut-in wind speed (float)
        rated: turbine rated wind speed (float)
        cut-out: turbine cut-out speed (float)
        Cp: power coefficient (float)
        availability: turbine availability (float)
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
        depth: water depth in meters (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
        directions: list of onset wind angles
    Returns:
        optimized turbine xlocation
        optimized turbine ylocation
        optimized turbine power
        optimized objctive
        Number of objective evaluations until convergence
    """
    initial_num = len(xlocation)
    eval_ct = 0
    Stopped = [0 for i in range(initial_num)]
    for h in range(0, 1):
        nomove, power = Eval_Objective(Compute_Wake, Compute_Cost, xlocation,
                                       ylocation, rr, hh, z0, U0, probwui,
                                       Zref, alphah, ro, aif, farm_y, cut_in,
                                       rated, cut_out, Cp, availability,
                                       nwp, extra, depth, yrs, WCOE,
                                       distance_to_shore, a)
        if farm_x % mesh_width == 0:
            # if space is evenly divisable by mesh size, add one point to
            # account for both edges
            x_opts = int(farm_x / mesh_width) + 1
            y_opts = int(farm_y / mesh_width) + 1
        else:
            # if space is not evenly divisable by mesh size, do not add point
            # because the final point will be outside the farm space
            x_opts = int(farm_x / mesh_width)
            y_opts = int(farm_y / mesh_width)
        eval_ct += 1

        step2 = init_step * mesh_width
        while step2 >= minstep:
            random_vec = Rand_Vector(initial_num)
            # creates a randomly ordered vector of turbines
            for j in range(0, len(random_vec)):
                i = random_vec[j]
                Stopped[i] = 0
                # print('Turbine ', i, ' is being tested.', nomove)
                flag = 0
                innerflag = 0
                transflag = 0

                if innerflag == 0 and flag == 0:
                    # move 1 was just unsucessfully attempted
                    transflag, xlocation, ylocation = translate_y(xlocation,
                                                                  ylocation,
                                                                  step2,
                                                                  i,
                                                                  farm_y,
                                                                  turb_sep,
                                                                  directions)
                    if transflag == 1:
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        innerflag = 1
                        # move2 was attempted
                        # print('turbine not moved up. '
                        #       + 'Out of bounds or interference')
                    else:
                        # if there is no interference, evaluate and store
                        move2, power = Eval_Objective(Compute_Wake,
                                                      Compute_Cost,
                                                      xlocation,
                                                      ylocation,
                                                      rr, hh, z0, U0,
                                                      probwui, Zref,
                                                      alphah, ro, aif,
                                                      farm_y, cut_in,
                                                      rated, cut_out, Cp,
                                                      availability,
                                                      nwp, extra, depth,
                                                      yrs, WCOE,
                                                      distance_to_shore, a)
                        eval_ct += 1
                        if move2 >= nomove:
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            (transflag,
                             xlocation,
                             ylocation) = translate_y(xlocation, ylocation,
                                                      -step2, i, farm_y,
                                                      turb_sep, directions)
                            innerflag = 1
                            # print('turbine not moved up. Worse Evaluation')
                        else:
                            # evaluation is better, keep move,
                            # go to next turbine
                            flag = 1
                            nomove = move2 * 1.
                            # print('turbine ', i, ' moved up.', move2)
                            # print('new y-location: ', ylocation[i])
                            # print(nomove)
                            # HubHeight_Search(etc...)
                if innerflag == 1 and flag == 0:
                    # move 2 was just unsucessfully attempted
                    (transflag,
                     xlocation,
                     ylocation) = translate_x(xlocation, ylocation, -step2,
                                              i, farm_y, turb_sep, directions)
                    if transflag == 1:
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        innerflag = 2
                        # move3 was attempted
                        # print('turbine not moved left. out of bounds')
                    else:
                        # if there is no interference, evaluate and store
                        move3, power = Eval_Objective(Compute_Wake,
                                                      Compute_Cost,
                                                      xlocation,
                                                      ylocation,
                                                      rr, hh, z0, U0,
                                                      probwui, Zref,
                                                      alphah, ro, aif,
                                                      farm_y, cut_in,
                                                      rated, cut_out, Cp,
                                                      availability,
                                                      nwp, extra, depth,
                                                      yrs, WCOE,
                                                      distance_to_shore, a)
                        eval_ct += 1
                        if move3 >= nomove:
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            (transflag,
                             xlocation,
                             ylocation) = translate_x(xlocation, ylocation,
                                                      step2, i, farm_y,
                                                      turb_sep, directions)
                            innerflag = 2
                            # print('turbine not moved left. Worse Evaluation')
                        else:
                            # evaluation is better, keep move,
                            # go to next turbine
                            flag = 1
                            nomove = move3 * 1.
                            # print('turbine ', i, ' moved left.', move3)
                            # print('new x-location: ', xlocation[i])
                            # print(nomove)
                            # HubHeight_Search(etc...)

                if innerflag == 2 and flag == 0:
                    # move 3 was just unsucessfully attempted
                    (transflag,
                     xlocation,
                     ylocation) = translate_y(xlocation, ylocation, -step2,
                                              i, farm_y, turb_sep, directions)
                    if transflag == 1:
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        innerflag = 3
                        # move3 was attempted
                        # print('turbine not moved down. out of bounds')
                    else:
                        # if there is no interference, evaluate and store
                        move4, power = Eval_Objective(Compute_Wake,
                                                      Compute_Cost,
                                                      xlocation,
                                                      ylocation,
                                                      rr, hh, z0, U0,
                                                      probwui, Zref,
                                                      alphah, ro, aif,
                                                      farm_y, cut_in,
                                                      rated, cut_out, Cp,
                                                      availability,
                                                      nwp, extra, depth,
                                                      yrs, WCOE,
                                                      distance_to_shore, a)
                        eval_ct += 1
                        if move4 >= nomove:
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            (transflag,
                             xlocation,
                             ylocation) = translate_y(xlocation, ylocation,
                                                      step2, i, farm_y,
                                                      turb_sep, directions)
                            innerflag = 3
                            # print('turbine not moved down.')
                        else:
                            # evaluation is better, keep move,
                            # go to next turbine
                            flag = 1
                            nomove = move4 * 1.
                            # print(nomove)
                            # print('turbine ', i, ' moved down.', move4)
                            # print('new y-location: ', ylocation[i])
                            # HubHeight_Search(etc...)
                if innerflag == 3 and flag == 0:
                    (transflag,
                     xlocation,
                     ylocation) = translate_x(xlocation, ylocation, step2, i,
                                              farm_y, turb_sep, directions)
                    if transflag == 1:
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        innerflag = 4
                        # signifies move 1 was attempted
                        # print('Turbine not moved right. out of bounds')

                    else:
                        # if there is no interference, evaluate and store
                        move1, power = Eval_Objective(Compute_Wake,
                                                      Compute_Cost,
                                                      xlocation,
                                                      ylocation,
                                                      rr, hh, z0, U0,
                                                      probwui, Zref,
                                                      alphah, ro, aif,
                                                      farm_y, cut_in,
                                                      rated, cut_out, Cp,
                                                      availability,
                                                      nwp, extra, depth,
                                                      yrs, WCOE,
                                                      distance_to_shore, a)
                        eval_ct += 1
                        if move1 >= nomove:
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            (transflag,
                             xlocation,
                             ylocation) = translate_x(xlocation,
                                                      ylocation,
                                                      -step2,
                                                      i,
                                                      farm_y,
                                                      turb_sep,
                                                      directions)
                            innerflag = 4
                            # print('Turbine not moved right.')
                        else:
                            flag = 1
                            # signifies movement was kept
                            nomove = move1 * 1.
                            # print('turbine ', i, ' moved right.', move1)
                            # print('new x-location: ', xlocation[i])
                            # print(nomove)
                        # HubHeight_Search(etc...)

                if innerflag == 4 and flag == 0:
                    # translation at this step size has resulted in no moves
                    # for this turbine
                    Stopped[i] = 1
                    # HubHeight_Search(etc...)
            exit_css = 0
            # exit current step size
            for i in range(0, initial_num):
                exit_css += Stopped[i]
            print(exit_css)
            if exit_css == initial_num:
                plt.figure()
                plt.scatter(xlocation, ylocation)
                for i in range(len(xlocation)):
                    plt.annotate(i, (xlocation[i][0], ylocation[i][0]))
                # all turbines have stopped moving at this step size,
                # halving step size.
                # find worst performing turbine and randomly assign elsewhere
                # print("No moves at step size ", step2, " are possible. "
                #       + "Popping weakest turbine.")
                for b in range(0, num_pops):
                    min_power = 5000000.
                    # initialized to first turbine power output
                    random_vec2 = Rand_Vector(initial_num)
                    # creates a randomly ordered vector of turbines
                    for j in range(0, initial_num):
                        randorder = random_vec2[j]
                        Power = sum([sum(i) for i in power])
                        if Power < min_power:
                            min_power = Power
                            min_turb = randorder

                    initialx = xlocation[min_turb]
                    initialy = ylocation[min_turb]
                    k = 0
                    flag = 0
                    while flag == 0 and k < max_pop_tries:
                        k += 1
                        # will try random locations until one has no
                        # interference
                        newx = [(int(random.uniform(0, x_opts))
                                 * mesh_width)]
                        newy = [(int(random.uniform(0, y_opts))
                                 * mesh_width)]
                        xlocation[min_turb] = newx
                        ylocation[min_turb] = newy
                        interference = Check_Interference(xlocation,
                                                          ylocation,
                                                          min_turb,
                                                          turb_sep)
                        if not interference:
                            # No interference
                            # place turbine and exit poping loop
                            for j in range(1, len(directions)):
                                theta = directions[j]
                                newx.append((newx[0] * np.cos(theta))
                                            - (newy[0] * np.sin(theta)))
                                newy.append((newx[0] * np.sin(theta))
                                            + (newy[0] * np.cos(theta)))
                            xlocation[min_turb] = newx
                            ylocation[min_turb] = newy

                            new_eval, power = Eval_Objective(Compute_Wake,
                                                             Compute_Cost,
                                                             xlocation,
                                                             ylocation,
                                                             rr, hh, z0, U0,
                                                             probwui, Zref,
                                                             alphah, ro, aif,
                                                             farm_y, cut_in,
                                                             rated, cut_out,
                                                             Cp, availability,
                                                             nwp, extra, depth,
                                                             yrs, WCOE,
                                                             distance_to_shore,
                                                             a)
                            eval_ct += 1
                            if new_eval < nomove:
                                flag = 1
                                nomove = new_eval * 1.
                                # keep eval
                                # HubHeight_Search(etc...)
                                # print('Move has improved the evaluation')
                                # print(nomove)
                            else:
                                xlocation[min_turb] = initialx
                                ylocation[min_turb] = initialy
                        else:
                            xlocation[min_turb] = initialx
                            ylocation[min_turb] = initialy
                            # print('Move did not improve evaluation.')
                if init_step > 1. and init_step < 2.:
                    # make sure it tries one mesh distance
                    init_step = int(1)
                else:
                    init_step = int(init_step / 2.)
                step2 = init_step * mesh_width

    return xlocation, ylocation, power, nomove, eval_ct


def translate_chromosome(chromosome, binary_x, options_x,
                         binary_y, options_y, mesh_size, directions):
    """Translate binary chromosome to cardinal coordinates

    Args:
        chromosome: binary list to be converted to turbine layout
        binary_x: number of binary values in an x-coordinate
        options_x: number of positions a turbine can take in the x-direction
        binary_y: number of binary values in a y-coordinate
        options_y: number of positions a turbine can take in the y-direction
        mesh_size: width of square of mesh
        directions: onset wind angles
    Returns:
        xlocations of chromosome from every onset angle
        ylocations of chromosome from every onset angle
    """
    for i in list(set(chromosome)):
        if i != 0 and i != 1:
            raise ValueError('chromosome composed of values other '
                             + 'than 1 and 0')

    x = []  # xlocs
    y = []  # ylocs
    k = 0  # actual gene you're on
    # print(chromosome)
    # coord = 0  # counter for x vs y coordinate
    while k < len(chromosome):  # go for all genes
        # print('translating x coordinate')
        binary_add = 0.
        for j in range(binary_x):  # iterate through this many genes
            binary_add += (2 ** j) * chromosome[k]  # add the points
            k += 1
        if binary_add < options_x:
            # don't need further manipulation
            match_point = (float(binary_add) * mesh_size)
        else:
            binary_add -= (options_x + 1)
            # if value is too high, split evenly among possible points
            equiv_ratio = binary_add / ((2 ** binary_x) - options_x - 1.)
            match_point = float(int(equiv_ratio * (options_x)) * mesh_size)
            # print('binary sum greater than possible points')
            # print(match_point)
        x.append(match_point)
        # coord += 1 # tell code you're switching to y coordinate

        # print('translating y coordinate')
        binary_add = 0.
        for j in range(binary_y):  # iterate through this many genes
            binary_add += (2 ** j) * chromosome[k]  # add the points
            k += 1
        if binary_add < (options_y):
            # don't need further manipulation
            match_point = (float(binary_add) * mesh_size)
        else:
            binary_add -= (options_y + 1)
            # if value is too high, split evenly among possible points
            equiv_ratio = binary_add / ((2 ** binary_y) - options_y - 1.)
            match_point = float(int(equiv_ratio * (options_y)) * mesh_size)
            # print('binary sum greater than possible points')
            # print(match_point)
        y.append(match_point)
        # coord += 1 # tell code you're switching to x coordinate
    for index in range(len(x)):
        newx = []
        newy = []
        for rads in directions:
            newx.append(np.cos(rads) * x[index]
                        - np.sin(rads) * y[index])
            newy.append(np.sin(rads) * x[index]
                        + np.cos(rads) * y[index])
        x[index] = newx  # update turbine coordinates
        y[index] = newy
    return x, y


def GA(mesh_size, elite, mateable_range, mutation_rate,
       z0, U0, Zref, alphah, ro, yrs, WCOE, population_size,
       generations_to_converge, aif, farm_x, farm_y, turb_sep, Eval_Objective,
       Compute_Wake, Compute_Cost, probwui, rr, hh, cut_in,
       rated, cut_out, Cp, availability, nwp, extra, depth,
       distance_to_shore, a, directions):
    """Genetic Algorithm

    Args:
        mesh_size: width of mesh for GA
        elite: proportion of best chromosomes copied from last generation
        mateable_range: proportion of best chromosomes that are allowed to mate
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        Zref: Wind speed reference height
        alphah: power law exponent
        ro: air density (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        population_size: population size
        generations_to_convergence: number of generations with same best layout
            before algorithm is considered converged
        aif: axial induction factor (float)
        farm_x: length of wind farm in x direction in meters (float)
        farm_y: length of wind farm in y direction in meters (float)
        turb_sep: minimum tubine separation requirement
        Eval_Objective: objective being minimized by EPS
        Compute_Wake: function encapsulating wake model
        Compute_Cost: function encapsulating cost model
        probwui: list of lists for probability of onset wind conditions
            first index represets onset wind direction index
            second index represents onset wind speed index
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        cut_in: turbine cut-in wind speed (float)
        rated: turbine rated wind speed (float)
        cut-out: turbine cut-out speed (float)
        Cp: power coefficient (float)
        availability: turbine availability (float)
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
        depth: water depth in meters (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
        directions: list of onset wind angles
    Returns:
        optimized turbine xlocation
        optimized turbine ylocation
        optimized turbine power
        optimized objctive
        Number of objective evaluations until convergence
    """
    if farm_x % mesh_size != 0 or farm_y % mesh_size != 0:
        raise ValueError('error: one or more farm dimension is not '
                         + 'evenly divisible by the mesh size')
    evals = 0
    options_x = (farm_x / mesh_size + 1)
    binary_x = np.log(options_x) / np.log(2)
    if binary_x % 1 > 1e-5:
        binary_x = int(binary_x) + 1
    options_y = (farm_y / mesh_size + 1)
    binary_y = np.log(options_y) / np.log(2)
    if binary_y % 1 > 0e-5:
        binary_y = int(binary_y) + 1
    length_gene = int(binary_x) + int(binary_y)
    adults = []
    for i in range(population_size):
        new_adult = [random.randint(0, 1) for ii in range(length_gene)]
        xloc, yloc = translate_chromosome(new_adult, binary_x, options_x,
                                          binary_y, options_y, mesh_size,
                                          directions)
        obje, power = Eval_Objective(Compute_Wake, Compute_Cost, xloc,
                                     yloc, rr, hh, z0, U0, probwui, Zref,
                                     alphah, ro, aif, farm_y, cut_in, rated,
                                     cut_out, Cp, availability, nwp, extra,
                                     depth, yrs, WCOE, distance_to_shore, a)
        evals += 1
        adults.append(obje, new_adult)
    adults = sorted(adults, key=lambda x: x[0])
    k = 0  # iteration counter
    same_best = 0  # stopping criteria
    adults_kept = int(len(population_size) * elite)
    adults_mated = int(len(population_size) * mateable_range)
    if adults_mated % 2 != 0:
        adults_mated -= 1
    mating_pairs = int(adults_mated / 2)
    mutating_kids = int(len(population_size) * mutation_rate)

    while same_best < generations_to_converge:  # start the ga
        # keep elite
        old_best = adults[0]  # save the best formation found
        children = adults[:adults_kept]
        maybe_kids = []
        # crossover time - trying one crossover point
        # create a new population of children
        for crosses in range(mating_pairs):
            mom = adults[2 * crosses][1]  # select mom
            dad = adults[2 * crosses + 1][1]  # select dad as next in line

            cross_point = int(random.random() * length_gene)
            cross1 = mom[0:cross_point] + dad[cross_point:]
            cross2 = dad[0:cross_point] + mom[cross_point:]
            # add children new ones
            maybe_kids.append(cross1)
            maybe_kids.append(cross2)

        # mutation time - tying 1 mutation - only to mated kids
        for i in range(mutating_kids):
            this_kid = int(random.random() * len(maybe_kids))
            mutant_child = maybe_kids[this_kid]
            mutant_gene = int(random.random() * length_gene)
            if mutant_child[mutant_gene] == 0:
                mutant_child[mutant_gene] = 1
            else:
                mutant_child[mutant_gene] = 0
            maybe_kids[this_kid] = mutant_child

        for i in range(len(maybe_kids)):
            xloc, yloc = translate_chromosome(cross2, binary_x, options_x,
                                              binary_y, options_y, mesh_size,
                                              directions)
            interference = Check_Interference(xloc, yloc, 'pop', turb_sep)
            if not interference:
                obje, power = Eval_Objective(Compute_Wake, Compute_Cost,
                                             xloc, yloc, rr, hh, z0,
                                             U0, probwui, Zref, alphah, ro,
                                             aif, farm_y, cut_in, rated,
                                             cut_out, Cp, availability, nwp,
                                             extra, depth, yrs, WCOE,
                                             distance_to_shore, a)
                evals += 1
                # keep kids that don't violate constraints
                children.append((obje, maybe_kids[i]))
        # immigration
        while population_size - len(children) > 0:
            # fill the rest in with new random gens
            new_guy = [random.randint(0, 1) for ii in range(length_gene)]
            xloc, yloc = translate_chromosome(new_guy, binary_x, options_x,
                                              binary_y, options_y, mesh_size,
                                              directions)
            interference = Check_Interference(xloc, yloc, 'pop', turb_sep)
            if not interference:
                obje, power = Eval_Objective(Compute_Wake, Compute_Cost,
                                             xloc, yloc, rr, hh, z0,
                                             U0, probwui, Zref, alphah, ro,
                                             aif, farm_y, cut_in, rated,
                                             cut_out, Cp, availability, nwp,
                                             extra, depth, yrs, WCOE,
                                             distance_to_shore, a)
                evals += 1
                # keep kids that don't violate constraints
                children.append((obje, new_guy))

        adults = [i for i in children]  # make kids adults and start again
        adults = sorted(adults, key=lambda x: x[0])
        if adults[0] == old_best:
            same_best += 1
        else:
            same_best = 0
        k += 1
    xloc, yloc = translate_chromosome(old_best[0][1], binary_x, options_x,
                                      binary_y, options_y, mesh_size,
                                      directions)
    obje, power, windspeeds, cost = Eval_Objective(Compute_Wake, Compute_Cost,
                                                   xloc, yloc, rr,
                                                   hh, z0, U0, probwui, Zref,
                                                   alphah, ro, aif, farm_y,
                                                   cut_in, rated, cut_out, Cp,
                                                   availability, nwp, extra,
                                                   depth, yrs, WCOE,
                                                   distance_to_shore, a)
    return xloc, yloc, power, obje, evals, windspeeds, cost, k


def PSO(self_weight, global_weight, swarm_size, initial_num,
        farm_x, farm_y, turb_sep, generations_to_converge,
        Eval_Objective, constraint_scale, z0, U0, Zref, alphah, ro, aif, yrs,
        WCOE, Compute_Wake, Compute_Cost, probwui, rr, hh, cut_in, rated,
        cut_out, Cp, availability, nwp, extra, depth, distance_to_shore,
        a, directions):
    """Compute the total cost of a farm

    Args:
        self_weight: weight given to individual's best past evaluation
        global_weight: weight given to the swarm's best past evaulation
        swarm_size: number of individuals in the swarm
        initial_num: number of turbines being optimized
        farm_x: length of wind farm in x direction in meters (float)
        farm_y: length of wind farm in y direction in meters (float)
        turb_sep: minimum tubine separation requirement
        generations_to_converge: number of generations without improvement
            before algorithm is considered converged
        Eval_Objective: objective being minimized by EPS
        constraint_scale: the weight given to constraint violations in
            calculating the objective evaluation
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        Zref: Wind speed reference height
        alphah: power law exponent
        ro: air density (float)
        aif: axial induction factor (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        Compute_Wake: function encapsulating wake model
        Compute_Cost: function encapsulating cost model
        probwui: list of lists for probability of onset wind conditions
            first index represets onset wind direction index
            second index represents onset wind speed index
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        cut_in: turbine cut-in wind speed (float)
        rated: turbine rated wind speed (float)
        cut-out: turbine cut-out speed (float)
        Cp: power coefficient (float)
        availability: turbine availability (float)
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
        depth: water depth in meters (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
        directions: list of onset wind angles
    Returns:
        optimized turbine xlocation
        optimized turbine ylocation
        optimized turbine power
        optimized objctive
        Number of objective evaluations until convergence
    """
    evals = 0
    # create random layouts for swarm members
    current_x = []  # population x-coordinates
    current_y = []  # population y-coordinates
    current_evals = []  # hold swarm evaluations
    self_bestx = []  # hold self best x
    self_besty = []  # hold self best y
    self_best_eval = []  # hold self best eval
    self_best_violation = []
    # hold constraint violations for best self layouts
    for i in range(swarm_size):
        xlocs = [0.] * initial_num
        ylocs = [0.] * initial_num
        for j in range(initial_num):
            interference = True  # step into while loop to place turbine
            ctr = 0
            while interference and ctr < 5000:
                ctr += 1
                xlocs[j] = random.uniform(0, farm_x)
                ylocs[j] = random.uniform(0, farm_y)
                interference = Check_Interference(xlocs, ylocs, j, turb_sep)
            if ctr == 5000:
                return 'cannot find non-interfering turbine location'
        current_x.append(xlocs)
        current_y.append(ylocs)
        self_bestx.append(xlocs)
        self_besty.append(ylocs)
        newx = []
        newy = []
        xlocation = []
        ylocation = []
        for index in range(len(xlocs)):
            for rads in directions:
                newx.append(np.cos(rads) * xlocs[index]
                            - np.sin(rads) * ylocs[index])
                newy.append(np.sin(rads) * xlocs[index]
                            + np.cos(rads) * ylocs[index])
            xlocation.append(newx)  # update turbine coordinates
            ylocation.append(newy)
        obje, power = Eval_Objective(Compute_Wake, Compute_Cost, xlocation,
                                     ylocation, rr, hh, z0, U0, probwui,
                                     Zref, alphah, ro, aif, farm_y, cut_in,
                                     rated, cut_out, Cp, availability, nwp,
                                     extra, depth, yrs, WCOE,
                                     distance_to_shore, a)
        evals += 1
        current_evals.append(obje)
        self_best_eval.append(obje)
        self_best_violation.append(0.)
    same_best = 0  # change convergence criteria
    k = 0  # generation counter
    best_index = current_evals.index(min(current_evals))
    best_x = current_x[best_index]
    best_y = current_y[best_index]
    best_eval = current_evals[best_index]
    last_vx = []
    last_vy = []
    for j in (swarm_size):
        subx = []
        suby = []
        for i in initial_num:
            subx.append(random.random() * farm_x / 1000
                        * (-1 ** int(random.random() * 2)))
            suby.append(random.random() * farm_y / 1000
                        * (-1 ** int(random.random() * 2)))
        last_vx.append(subx)
        last_vy.append(suby)
    while same_best < generations_to_converge:
        for i in range(swarm_size):
            x_new = []
            y_new = []
            r1 = random.random()
            r2 = random.random()
            # shit_check = 0
            constraint_error = 0
            for j in range(initial_num):
                # v0x = cuurent_x[i][j]
                v_same_x = self_bestx[i][j] - current_x[i][j]
                v_global_x = best_x[j] - current_x[i][j]
                new_vx = (last_vx[i][j] + (r1 * self_weight * v_same_x)
                          + (r2 * global_weight * v_global_x))
                next_x = current_x[i][j] + new_vx
                x_new.append(next_x)
                # print(x_new)
                v_same_y = self_besty[i][j] - current_y[i][j]
                v_global_y = best_y[j] - current_y[i][j]
                new_vy = (last_vy[i][j] + (r1 * self_weight * v_same_y)
                          + (r2 * global_weight * v_global_y))
                next_y = current_y[i][j] + new_vy
                y_new.append(next_y)
                if next_y > farm_y:
                    constraint_error += abs(next_y - farm_y)
                if next_y < 0.:
                    constraint_error += abs(next_y)
                if next_x > farm_x:
                    constraint_error += abs(next_x - farm_x)
                if next_x < 0.:
                    constraint_error += abs(next_x)

            # print(x_new)
            # print(layout[i].XLocations) #not XLocation
            current_x[i] = x_new  # save current xlocations
            current_y[i] = y_new  # save current ylocations
            last_vx[i][j] = new_vx
            last_vy[i][j] = new_vy
            # assign penalties for turbines outside of space or within 200 m
            for j in range(len(x_new)):
                for jj in range(j + 1, len(x_new)):
                    space = np.sqrt(((x_new[j] - x_new[jj]) ** 2)
                                    + ((y_new[j] - y_new[jj]) ** 2))
                    if space < turb_sep:
                        constraint_error += (turb_sep - space)

            newx = []
            newy = []
            xlocation = []
            ylocation = []
            for index in range(len(xlocs)):
                for rads in directions:
                    newx.append(np.cos(rads) * x_new[index]
                                - np.sin(rads) * y_new[index])
                    newy.append(np.sin(rads) * x_new[index]
                                + np.cos(rads) * y_new[index])
                xlocation.append(newx)  # update turbine coordinates
                ylocation.append(newy)
            new_objective, power = Eval_Objective(Compute_Wake, Compute_Cost,
                                                  xlocation, ylocation, rr, hh,
                                                  z0, U0, probwui, Zref,
                                                  alphah, ro, aif, farm_y,
                                                  cut_in, rated, cut_out, Cp,
                                                  availability, nwp, extra,
                                                  depth, yrs, WCOE,
                                                  distance_to_shore, a)
            evals += 1
            new_objective = (new_objective
                             * (1 + constraint_error * constraint_scale))
            # print(layout[i].objective_eval)
            # print(new_objective)
            # print(layout[i].best_self)
            # if new objective is better keep it (don't care about constraints)
            if new_objective < self_best_eval[i]:
                self_bestx[i] = x_new
                self_besty[i] = y_new
                self_best_eval[i] = new_objective
                self_best_violation[i] = constraint_error
                # print('personal improvement')
        # AFTER everything's been changed for this generation
        # if new objective is better AND fits constraints, keep it
        for i in range(swarm_size):
            if self_best_eval[i] < best_eval and constraint_error[i] < 1e-5:
                # only accept global best if no constraint violations
                best_eval = self_best_eval[i]
                best_x = self_bestx[i]
                best_y = self_besty[i]
                same_best = 0
                # print('wooo!! improvement!!')
                # print('iteration no. = ', k)
        same_best += 1
        k += 1
    newx = []
    newy = []
    xlocation = []
    ylocation = []
    for index in range(len(xlocs)):
        for rads in directions:
            newx.append(np.cos(rads) * best_x[index]
                        - np.sin(rads) * best_y[index])
            newy.append(np.sin(rads) * best_x[index]
                        + np.cos(rads) * best_y[index])
        xlocation.append(newx)  # update turbine coordinates
        ylocation.append(newy)
    new_objective, power, windspeeds, cost = Eval_Objective(Compute_Wake,
                                                            Compute_Cost,
                                                            xlocation,
                                                            ylocation, rr, hh,
                                                            z0, U0, probwui,
                                                            Zref, alphah, ro,
                                                            aif, farm_y,
                                                            cut_in, rated,
                                                            cut_out, Cp,
                                                            availability, nwp,
                                                            extra, depth, yrs,
                                                            WCOE,
                                                            distance_to_shore,
                                                            a)
    return best_x, best_y, power, new_objective, evals, windspeeds, cost, k
