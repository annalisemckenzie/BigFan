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


# NOTES TO ANNALISE:
#     Change inputs to Objective_Eval
#     Change inputs to EPS
#     Fix GA Check_Interference
#     Change inputs to GA


def Check_Interference(xlocation, ylocation, index, turbine_sep_distance):
    interference = False  # Is a constraint violated?
    if index != 'pop':
        # identify turbine of interest
        xold = xlocation[index]
        yold = ylocation[index]
        # check for inerference with all other turbines
        for j, k in enumerate(xlocation):
            if k != index:  # don't check turbine's interference with self
                checkx = xold - k
                checky = yold - ylocation[j]
                # calculate distance between 2 turbines
                checkrad = np.sqrt(checkx ** 2.0 + checky ** 2.0)
                # if constraint is violated
                if checkrad < turbine_sep_distance:
                    interference = True
                    return interference
    else:
        for i in range(len(xlocation) - 1):
            for j in range(i + 1, len(xlocation)):
                checkx = xlocation[i] - xlocation[j]
                checky = ylocation[i] - ylocation[j]
                # calculate distance between 2 turbines
                checkrad = np.sqrt(checkx ** 2.0 + checky ** 2.0)
                if checkrad < turbine_sep_distance:
                    interference = True
                    return interference
    return interference


def translate_x(xlocation, ylocation, step_size, index, farm_x,
                turbine_sep_distance):
    transflag = False
    xstart = xlocation[index]
    # print(xstart, step_size)
    # find preliminary new x-location given step size
    xfinish = xstart + step_size
    # check for turbine interference
    interference = Check_Interference(xlocation, ylocation, index,
                                      turbine_sep_distance)
    # if this new x-location is not out of bounds,
    # and does not violate constraints, translate it
    if xfinish >= 0 and xfinish <= farm_x and not interference:
        xlocation[index] = xfinish  # update turbine coordinates
        return transflag  # return no error
    else:
        transflag = True  # return error
        return transflag, xlocation


def translate_y(xlocation, ylocation, step_size, index, farm_y,
                turbine_sep_distance):
    transflag = False
    ystart = ylocation[index]
    # find preliminary new y-location given step size
    yfinish = ystart + step_size
    # check for turbine interference
    interference = Check_Interference(xlocation, ylocation, index,
                                      turbine_sep_distance)
    # if this new x-location is not out of bounds,
    # and does not violate constraints, translate it
    if yfinish >= 0 and yfinish <= farm_y and not interference:
        ylocation[index] = yfinish  # update turbine coordinates
        return transflag
    else:
        transflag = True
        return transflag, ylocation


def Rand_Vector(initial_num):
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


def EPS(xlocation, ylocation, init_step, minstep, initial_num,
        z0, U0, Zref, alphah, ro, yrs, WCOE, condition, num_pops,
        max_pop_tries, aif, farm_x, farm_y, turb_sep, Eval_Objective):
    stopped = [0] * initial_num
    # Clear_Vectors()
    tot_evals = 0
    num_EPS_repeats = 1  # number of times you completely reset EPS
    for h in range(0, num_EPS_repeats):
        # print('objective eval: ' + str(objective))
        # print('h= ' + str(h))
        # develop preliminary objective for comparison purposes
        tot_evals += 1
        nomove, power = Eval_Objective(initial_num, z0, U0, Zref,
                                       alphah, ro, yrs, WCOE,
                                       condition, aif)
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
                # Clear_Vectors()
                # print('The nomove value for turbine ', i, ' is ', nomove)
                # print('stepped into while loop')
                # If turbine is in back half of filed, move backwards first
                if ylocation[i] >= (farm_y / 2.0):
                    if innerflag == 0 and not flag:
                        transflag, ylocation = translate_y(xlocation,
                                                           ylocation,
                                                           step2,
                                                           i,
                                                           farm_y,
                                                           turb_sep)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 1  # move 1 was attempted
                            # move 1 failed
                            # print('turbine not moved up.')
                        # if there is no interference, evaluate and store
                        else:
                            tot_evals += 1
                            move1, power = Eval_Objective(initial_num, z0, U0,
                                                          Zref, alphah, ro,
                                                          yrs, WCOE,
                                                          condition, aif)
                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move1 >= nomove:
                                transflag, ylocation = translate_y(xlocation,
                                                                   ylocation,
                                                                   step2,
                                                                   i,
                                                                   farm_y,
                                                                   turb_sep)
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
                        transflag, xlocation = translate_x(xlocation,
                                                           ylocation,
                                                           step2,
                                                           i,
                                                           farm_y,
                                                           turb_sep)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 2  # move 2 was attempted and failed
                            # print('turbine not left.')
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move2, power = Eval_Objective(initial_num, z0, U0,
                                                          Zref, alphah, ro,
                                                          yrs, WCOE,
                                                          condition, aif)
                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move2 >= nomove:
                                transflag, xlocation = translate_x(xlocation,
                                                                   ylocation,
                                                                   step2,
                                                                   i,
                                                                   farm_y,
                                                                   turb_sep)
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
                        transflag, ylocation = translate_y(xlocation,
                                                           ylocation,
                                                           step2,
                                                           i,
                                                           farm_y,
                                                           turb_sep)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 3  # move3 was attempted
                            # print('turbine not moved down.')
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move3, power = Eval_Objective(initial_num, z0, U0,
                                                          Zref, alphah, ro,
                                                          yrs, WCOE,
                                                          condition, aif)

                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move3 >= nomove:
                                transflag, ylocation = translate_y(xlocation,
                                                                   ylocation,
                                                                   step2,
                                                                   i,
                                                                   farm_y,
                                                                   turb_sep)
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
                        transflag, xlocation = translate_x(xlocation,
                                                           ylocation,
                                                           step2,
                                                           i,
                                                           farm_y,
                                                           turb_sep)
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
                            move4, power = Eval_Objective(initial_num, z0, U0,
                                                          Zref, alphah, ro,
                                                          yrs, WCOE,
                                                          condition, aif)

                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move4 >= nomove:
                                transflag, xlocation = translate_x(xlocation,
                                                                   ylocation,
                                                                   step2,
                                                                   i,
                                                                   farm_y,
                                                                   turb_sep)
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
                elif ylocation[i] < (farm_y / 2.0):
                    if innerflag == 0 and not flag:
                        transflag, ylocation = translate_y()
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 1  # move 1 was attempted
                            # print('turbine not moved up.')
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move1, power = Eval_Objective(initial_num, z0, U0,
                                                          Zref, alphah, ro,
                                                          yrs, WCOE,
                                                          condition, aif)

                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move1 >= nomove:
                                transflag, ylocation = translate_y(xlocation,
                                                                   ylocation,
                                                                   step2,
                                                                   i,
                                                                   farm_y,
                                                                   turb_sep)
                                innerflag = 1
                                # print('turbine not moved up.')
                            # evaluation is better,
                            # keep move, go to next turbine
                            else:
                                flag = True
                                nomove = move1 * 1.
                                # print('turbine ' + str(i)
                                #      + ' moved up.' + str(move1))
                                # Add Hubheight search here in future
                                # HubHeight_Search(etc...)
                    # move 2 was just unsucessfully attempted
                    if innerflag == 1 and not flag:
                        transflag, xlocation = translate_x(xlocation,
                                                           ylocation,
                                                           step2,
                                                           i,
                                                           farm_y,
                                                           turb_sep)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 2  # move 2 was attempted
                            # print('turbine not left.')
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move2, power = Eval_Objective(initial_num, z0, U0,
                                                          Zref, alphah, ro,
                                                          yrs, WCOE,
                                                          condition, aif)

                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move2 >= nomove:
                                transflag, xlocation = translate_x(xlocation,
                                                                   ylocation,
                                                                   step2,
                                                                   i,
                                                                   farm_y,
                                                                   turb_sep)
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
                    # move 3 was just unsucessfully attempted
                    if innerflag == 2 and not flag:
                        transflag, ylocation = translate_y(xlocation,
                                                           ylocation,
                                                           step2,
                                                           i,
                                                           farm_y,
                                                           turb_sep)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 3  # move 3 was attempted
                            # print('turbine not moved down.')
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move3, power = Eval_Objective(initial_num, z0, U0,
                                                          Zref, alphah, ro,
                                                          yrs, WCOE,
                                                          condition, aif)

                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move3 >= nomove:
                                transflag, ylocation = translate_y(xlocation,
                                                                   ylocation,
                                                                   step2,
                                                                   i,
                                                                   farm_y,
                                                                   turb_sep)
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
                        transflag, xlocation = translate_x(xlocation,
                                                           ylocation,
                                                           step2,
                                                           i,
                                                           farm_y,
                                                           turb_sep)
                        # if the translation moved the turbine out of bounds,
                        # go to next translation
                        if transflag:
                            innerflag = 4  # signifies move 4 was attempted
                            # print('Turbine not moved right.')
                        # if there is the turbine is in bounds,
                        # evaluate and store
                        else:
                            tot_evals += 1
                            # if there is no interference, evaluate and store
                            move4, power = Eval_Objective(initial_num, z0, U0,
                                                          Zref, alphah, ro,
                                                          yrs, WCOE,
                                                          condition, aif)

                            # Clear_Vectors()
                            # if evaluation is worse than initial,
                            # move back, go to next translation
                            if move4 >= nomove:
                                transflag, xlocation = translate_x(xlocation,
                                                                   ylocation,
                                                                   step2,
                                                                   i,
                                                                   farm_y,
                                                                   turb_sep)
                                innerflag = 4
                                # print('Turbine not moved right.')
                            else:
                                flag = True  # signifies movement was kept
                                nomove = move4 * 1.
                            # print('turbine ', i, ' moved right.', move4)
                            # Add Hubheight search here in future
                            # HubHeight_Search(etc...)
                    # no moves for this turbine at this step size
                    if innerflag == 4 and not flag:
                        stopped[i] = 1
                        # Add Hubheight search here in future
                        # HubHeight_Search(etc...)

            # count how many turbines have stopped moving
            exit_css = sum(stopped)
            # print(exit_css)
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
                        if power[randorder] < min_power:
                            min_power = power[randorder]
                            min_turb = randorder

                    # print('The weakest turbine is turbine '
                    #       + str(min_turb)
                    #       + ' with power currently at '
                    #       + str(min_power))
                    # start_eval, power = Eval_Objective(initial_num, z0, U0,
                    #                                    Zref, alphah, ro, yrs,
                    #                                    WCOE, condition, aif)

                    # Clear_Vectors()
                    initialx = xlocation[min_turb]
                    initialy = ylocation[min_turb]
                    checkx = 0
                    k = 0
                    flag = False
                    while not flag and k < max_pop_tries:
                        checkx = 0
                        # try random locations until one has no interference
                        while checkx != 1:
                            xlocation[min_turb] = random.uniform(0, farm_x)
                            ylocation[min_turb] = random.uniform(0, farm_y)

                            interference = Check_Interference(xlocation,
                                                              ylocation,
                                                              i, turb_sep)
                            if not interference:  # No interference
                                # place turbine and exit poping loop
                                checkx = 1
                                # print('Turbine '
                                #       + str(min_turb)
                                #       + ' has moved to a new location.')
                            else:
                                xlocation[min_turb] = initialx
                                ylocation[min_turb] = initialy
                                # print('Turbine cannot be relocated without'
                                #       + 'interference, trying agian.')
                        tot_evals += 1
                        new_eval, power = Eval_Objective(initial_num, z0, U0,
                                                         Zref, alphah, ro,
                                                         yrs, WCOE,
                                                         condition, aif)

                        # Clear_Vectors()
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
                            #        + 'Trying new moves.')
                        k += 1
                # halving step size
                step2 = step2 / 2.0
    return xlocation, ylocation, power, nomove, tot_evals


def translate_chromosome(chromosome, binary_x, options_x,
                         binary_y, options_y, mesh_size):
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
    return x, y


def GA(mesh_size, elite, mateable_range, mutation_rate,
       z0, U0, Zref, alphah, ro, yrs, WCOE, condition, population_size,
       generations_to_converge, aif, farm_x, farm_y, turb_sep, Eval_Objective):
    if farm_x % mesh_size != 0 or farm_y % mesh_size != 0:
        return ('error: one or more farm dimension is not '
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
                                          binary_y, options_y, mesh_size)
        obje, power = Eval_Objective(xloc, yloc)
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
                                              binary_y, options_y, mesh_size)
            interference = Check_Interference(xloc, yloc, 'pop', turb_sep)
            if not interference:
                obje, power = Eval_Objective(xloc, yloc)
                evals += 1
                # keep kids that don't violate constraints
                children.append((obje, maybe_kids[i]))
        # immigration
        while population_size - len(children) > 0:
            # fill the rest in with new random gens
            new_guy = [random.randint(0, 1) for ii in range(length_gene)]
            xloc, yloc = translate_chromosome(new_guy, binary_x, options_x,
                                              binary_y, options_y, mesh_size)
            interference = Check_Interference(xloc, yloc, 'pop', turb_sep)
            if not interference:
                obje, power = Eval_Objective(xloc, yloc)
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
                                      binary_y, options_y, mesh_size)
    obje, power, windspeeds, cost = Eval_Objective(xloc, yloc)
    return xloc, yloc, power, obje, evals, windspeeds, cost, k


def PSO(self_weight, global_weight, swarm_size, initial_num,
        farm_x, farm_y, turb_sep, generations_to_converge,
        Eval_Objective, constraint_scale):
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
        obje, power = Eval_Objective(xlocs, ylocs)
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
            # print(layout[i].objective_eval)
            new_objective, power = Eval_Objective(x_new, y_new)
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
    # print(list(zip(best_x, best_y)))
    new_objective, power, windspeeds, cost = Eval_Objective(x_new, y_new)
    return best_x, best_y, power, new_objective, evals, windspeeds, cost, k
