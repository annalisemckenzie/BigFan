# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 15:41:05 2018

@author: Annalise

ME 599 Project
Spring 2018
Wake Models
"""

import numpy as np


def offshore_cost(xlocs, ylocs, rr, hh, ro, Uref, Cp, depth, yrs,
                  WCOE, availability, distance_to_shore):
    costc = 0.0
    costa = 0.0
    Capital_Cost = 0
    Cabling_Cost = 0
    Mooring_Cost = 0
    O_M = 0
    Substation_Cost = 0
    Installation_Cost = 977620.0
    Leasing_Cost = 0
    # if adding in multi-size manipulate to get RR and HH here
    for i in range(0, len(xlocs)):
        Area = np.pi * pow(rr[i], 2)
        # calculate rated power in Watts
        Prated = 0.5 * ro * Area * (Uref ** 3.0) * Cp
        # print('Prated = ', Prated)
        Capital_Cost = Prated * 1.48
        O_M = (Prated * 133.0 / 1000.0) * yrs
        Substation_Cost = 0.02 * Prated
        Leasing_Cost = ((Prated / 1000000.0) * 8760.0 * availability
                        * WCOE * (8.0 * 0.02 + (yrs - 8.0) * 0.04))
        Mooring_Cost = 4.0 * (140148.0 + 274.0 * depth)
        costc += (Capital_Cost + Substation_Cost
                  + Mooring_Cost + Installation_Cost)
        costa += O_M + Leasing_Cost
    # print('cost before cabline = ', cost)
    d_t, networks = calcicl(xlocs, ylocs)
    # print(d_t, d_s)
    Cabling_Cost = d_t * 307000 + distance_to_shore * 492000
    # print('cabling cost = ' + str(Cabling_Cost))
    costc += Cabling_Cost + 2000000.0
    return costc, costa


def closest(j, xlocs, ylocs, hood_size):
    dist = []
    turb = []
    for count in range(len(xlocs)):
        if count != j:
            term1 = (xlocs[j] - xlocs[count]) ** 2
            term2 = (ylocs[j] - ylocs[count]) ** 2
            space = np.sqrt(term1 + term2)
            turb.append(count)
            dist.append(space)

    current_trb = [j] * (len(xlocs) - 1)
    # Create tuple to identify turbine number
    Dist_Order = list(zip(current_trb, turb, dist))
    Dist_Order = sorted(Dist_Order, key=lambda x: x[2])
    closest = []
    for i in range(0, hood_size):
        closest.append(Dist_Order[i])

    return closest


def calcicl(xlocs, ylocs):
    all_opt = []
    hood_size = min([5, len(xlocs) - 1])
    for i in range(len(xlocs)):
        all_opt.extend(closest(i, xlocs, ylocs, hood_size))
    # print(all_opt)
    # sorted list of near-by connections
    all_opt = sorted(all_opt, key=lambda x: x[2])
    networks = []
    networks.append([all_opt[0]])
    first = all_opt[0][0]
    second = all_opt[0][1]
    # print(len(all_opt))
    deletables = []
    for k in range(0, len(all_opt)):
        if first == all_opt[k][0] and second == all_opt[k][1]:
            deletables.append(k)  # eliminate looping options in mesh
        if first == all_opt[k][1] and second == all_opt[k][0]:
            deletables.append(k)  # eliminate looping options in mesh
    deletables.sort()
    for i in range(1, len(deletables) + 1):
            j = len(deletables) - i
            delete = deletables[j]
            del all_opt[delete]
    # print(len(all_opt))
    while len(all_opt) > 0:
        # network.append(all_opt[0])
        sets = []
        first = all_opt[0][0]
        second = all_opt[0][1]
        # Create List of all values in a mesh
        for j in range(0, len(networks)):
            m = []
            n = len(networks[j])
            for i in range(0, n):
                m.append(networks[j][i][0])
                m.append(networks[j][i][1])
            b = list(set(m))
            sets.append(b)
        # print('sets')
        # print(sets)
        # print('networks')
        # print(networks)
        maxcount = 0
        maxsets = []
        # maxsetscheck = []
        for j in range(0, len(networks)):
            counta = 0
            countb = 0
            if first in sets[j] or second in sets[j]:
                counta = 1
                if j not in maxsets:
                    maxsets.append(j)
            for i in range(0, len(networks)):
                if i != j:
                    if first in sets[i] or second in sets[i]:
                        countb = 1
                        if i not in maxsets:
                            maxsets.append(i)
            if (counta + countb) > maxcount:
                maxcount = counta + countb

        deletables = []
        if maxcount == 0:  # form a new mesh
            networks.append([all_opt[0]])
            # print('count was 0')
            for k in range(0, len(all_opt)):
                if first == all_opt[k][0] and second == all_opt[k][1]:
                    deletables.append(k)  # eliminate looping options in mesh
                if first == all_opt[k][1] and second == all_opt[k][0]:
                    deletables.append(k)  # eliminate looping options in mesh
        # if one of the coordinates is already in a mesh, add to mesh
        elif maxcount == 1:
            a = maxsets[0]
            networks[a].append(all_opt[0])
            # print('count was 1')
            if first not in sets[a]:
                # print('enter part 1')
                f = len(sets[a])
                for h in range(0, f):
                    third = sets[a][h]
                    for k in range(0, len(all_opt)):
                        if first == all_opt[k][0] and third == all_opt[k][1]:
                            # eliminate looping options in mesh
                            deletables.append(k)
                        if first == all_opt[k][1] and third == all_opt[k][0]:
                            # eliminate looping options in mesh
                            deletables.append(k)
            if second not in sets[a]:
                # print('enter part 2')
                f = len(sets[a])
                for h in range(0, f):
                    third = sets[a][h]
                    for k in range(0, len(all_opt)):
                        if second == all_opt[k][0] and third == all_opt[k][1]:
                            # eliminate looping options in mesh
                            deletables.append(k)
                        if second == all_opt[k][1] and third == all_opt[k][0]:
                            # eliminate looping options in mesh
                            deletables.append(k)

        elif maxcount == 2:
            # if one number is in one mesh, and other is in another mesh,
            # combine meshes and delete second mesh
            a = maxsets[0]
            b = maxsets[1]
            c = len(networks[b])
            for each in range(0, c):  # combine meshes
                networks[a].append(networks[b][each])
            networks[a].append(all_opt[0])
            del networks[b]

            # print('count was 2')
            c = len(sets[a])
            d = len(sets[b])
            for each in range(0, c):
                # eliminate looping options between meshes
                third = sets[a][each]
                for every in range(0, d):
                    fourth = sets[b][every]
                    for k in range(0, len(all_opt)):
                        if third == all_opt[k][0] and fourth == all_opt[k][1]:
                            # eliminate looping options in mesh
                            deletables.append(k)
                        if third == all_opt[k][1] and fourth == all_opt[k][0]:
                            # eliminate looping options in mesh
                            deletables.append(k)
        # else:  # something went wrong
        #     print('oh Shit')

        # print('deletables')
        # print(deletables)
        # print('all_opt length: ' +  str(len(all_opt)))
        deletables.sort()
        for i in range(1, len(deletables) + 1):
            j = len(deletables) - i
            delete = deletables[j]
            del all_opt[delete]
        # print('all_opt length: ' = str(len(all_opt)))

    # print(networks[0])
    icl = 0.
    a = len(networks[0])
    for i in range(0, a):
        icl += networks[0][i][2]
    icl = icl/1000.  # m to km
    # print(str(icl) + 'm of interior cable needed')
    # cableout = open('cablein.txt', 'w')
    # cableout.write(str(str(icl) + '\n'))
    # cableout.write(str('connections\n'))
    # cableout.write(str(networks))
    return icl, networks


def onshore_cost(xlocs, ylocs, rr, hh, ro, Uref, Cp, depth, yrs,
                 WCOE, availability, distance_to_shore):
    Project = 0.
    Ptot = 0.
    for l in range(len(xlocs)):
        r = rr[l]
        h = hh[l]
        Project += (2454000. - (216100. * r) - (12030. * h)
                    + (6039. * (r ** 2)) + (2455. * r * h)
                    - (161.2 * (h ** 2)))
        Ptot += 0.5 * ro * (np.pi * pow(r, 2)) * (Uref ** 3.0) * Cp
    Energy = (Ptot) * 8760. * availability
    O_M = 0.007 * Energy
    return Project, O_M
