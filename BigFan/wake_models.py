# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 15:37:20 2018

@author: Annalise

ME 599 Project
Spring 2018
Wake Models
"""

import numpy as np

# NOTES TO ANNALISE:
#     Add CFD model


def PARK_3D(xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah,
            ro, aif, farm_y, cut_in, rated, cut_out, Cp,
            availability, nwp=False, extra=False):
    initial_num = len(xlocs)
    num_directions = len(xlocs[0])
    wdsp_list = [[0.] * len(U0) for ii in range(initial_num)]
    windspeeds = [wdsp_list for ii in range(num_directions)]
    usturbines = [[] for ii in range(initial_num)]
    wakewidths = [[] for ii in range(initial_num)]
    distances = [[] for ii in range(initial_num)]
    percent = [[] for ii in range(initial_num)]
    xcoords = [[] for ii in range(initial_num)]
    zcoords = [[] for ii in range(initial_num)]
    power = [[] for ii in range(initial_num)]
    # figure out which turbines are downstream of which other turbines
    # and how far downstream they are
    for j in range(initial_num):  # downstream turbine
        upstrm = []
        distanceus = []
        wakewidthds = []
        for direction in range(num_directions):
            In_Wakek = []
            # turbine j's X Location
            khub = xlocs[j][direction]
            krad = rr[j]
            # define left most point of rotor swept area of turbine j
            kleft = khub - krad
            # define right most point of rotor swept area of turbine k
            kright = khub + krad
            wake_d = []
            disty = []

            for i in range(0, initial_num):  # upstream turbine
                if j != i:
                    hubheight = hh[i]
                    alpha = 0.5 / (np.log(hubheight / z0))
                    y = ylocs[i][direction]
                    x = xlocs[i][direction]
                    # Sets dis to max downstream distance
                    dis = farm_y - y
                    Rr = rr[i]
                    # Calculate maximum ds wake radius
                    r1 = (alpha * dis) + Rr
                    space1 = x + r1
                    space2 = x - r1
                    # check left and right side for overlap
                    # if wake extended to end of farm
                    kleft_cond = (kleft >= space2 and kleft <= space1)
                    kright_cond = (kright >= space2 and kright <= space1)
                    if kleft_cond or kright_cond:
                        if ylocs[i][direction] < ylocs[j][direction]:
                            Y = ylocs[j][direction]
                            # distance between turbines
                            dist = Y - y
                            # print(dist)  # code check
                            # define radius of triangular wake
                            wake_rad = (alpha * dist) + Rr
                            # kz is the z coordinate of the rotor j's hub
                            kz = hh[j]
                            # jz is the z coordinate of the wake's center
                            jz = hh[i]
                            # distance between the centerline
                            # of wake and rotor hub
                            cd = np.sqrt((x - khub) ** 2.0 + (jz - kz) ** 2.0)
                            if cd < (wake_rad + krad):
                                # if distance between centers is less than the
                                # sum of the two radii, the rotor swept area
                                # is in the wake
                                In_Wakek.append(i)
                                wake_d.append(wake_rad * 2.0)
                                disty.append(dist)
            upstrm.append(In_Wakek)
            distanceus.append(disty)
            wakewidthds.append(wake_d)
        usturbines[j] = upstrm
        wakewidths[j] = wakewidthds
        distances[j] = distanceus

        # print('usturbines for ', i, ': ',turbines[i].usturbines)
        # print('wakewidth for ', j, ': ',turbines[j].wakewidth)
        # print('distances for ', j, ': ',turbines[j].distance)

    #    for i in range(0, initial_num):
    #        dsds = []
    #        for d in range(0, direction):
    #            dsone = []
    #            for j in range(0, initial_num):
    #                if j != i:
    #                    if i in turbines[j].usturbines[d]:
    #                        dsone.append(j)
    #            dsds.append(dsone)
    #        turbines[i].dsturbines = dsds
    #        # print('dsturbines for ', j, ': ',turbines[j].dsturbines)

    #    code check
    #    print(turbines[7].dsturbines[0])
    #    print(turbines[7].dsturbinesrec)
    #    print(turbines[7].usturbines[0])
    #    print(turbines[7].usturbinesrec)
    #    print(turbines[7].wakewidth)
    #    print(turbines[7].distance)
    #    print(turbines[4].dsturbines[0])
    #    print(turbines[4].dsturbinesrec)
    #    print(turbines[4].usturbines[0])
    #    print(turbines[4].usturbinesrec)
    #    print(turbines[4].wakewidth)
    #    print(turbines[4].distance)

    # Now that we know which turbines are downstream of others,
    # calculate the percentage of the rotor swept area that is within the wake
    for i in range(0, initial_num):
        complete_percent = []
        dummyx = [[] for ii in range(num_directions)]
        dummyz = [[] for ii in range(num_directions)]
        for wd in range(num_directions):
            parpercent = []
            overlap_flag = 0
            kz = hh[i]  # turbine k's hub height (z-location)
            kx = xlocs[i][wd]  # turbine k's x location
            # ky = turbines[i].YLocation[wd]  # turbine k's y location
            krad = rr[i]  # turbine k's rotor radius
            # if the turbine has one upstream turbine
            if len(usturbines[i][wd]) == 1:
                j = usturbines[i][wd][0]
                # z coordinate of the wake's center
                jz = hh[j]
                # x coordinate of the wake's center
                jx = xlocs[j][wd]
                # y coordinate of the wake's center
                # jy = turbines[j].YLocation[wd]
                # radius of wake width
                jwakerad = (wakewidths[i][wd][0]) / 2.0
                dist = distances[i][wd][0]
                # distance between centerline of wake and rotor hub
                cd = np.sqrt(((jx-kx) ** 2.0) + ((jz - kz) ** 2.0))
                int1_den = 2.0 * cd * krad
                # if dsturbine is completely in usturbine wake, overlap = 100%
                if cd + krad <= jwakerad:
                    parpercent.append(1.0)
                    # print('works')

                elif cd + jwakerad <= krad:
                    # if the wake is fully encompassed by the rotor diameter
                    wakearea = np.pi * (jwakerad ** 2.0)
                    percentwake = wakearea / (np.pi * (krad ** 2.0))
                    parpercent.append(percentwake)

                else:
                    integrand1 = ((cd ** 2.0) + (krad ** 2.0)
                                  - (jwakerad ** 2.0)) / int1_den
                    # print(integrand1)
                    int2_den = 2.0 * cd * jwakerad
                    integrand2 = ((cd ** 2.0) + (jwakerad ** 2.0)
                                  - (krad ** 2.0)) / int2_den
                    # print(integrand2)
                    q = (krad ** 2.0) * (np.arccos(integrand1))
                    b = (jwakerad ** 2.0) * (np.arccos(integrand2))
                    c = 0.5 * np.sqrt((-cd + krad + jwakerad)
                                      * (cd + krad - jwakerad)
                                      * (cd - krad + jwakerad)
                                      * (cd + krad + jwakerad))
                    AOverlap = q + b - c
                    RSA = ((np.pi) * (krad ** 2.0))
                    z = AOverlap / RSA
                    # percentage of RSA that has wake interaction
                    parpercent.append(z)

            elif len(usturbines[i][wd]) == 2:
                # if the turbine has two upstream turbines
                first = usturbines[i][wd][0]
                second = usturbines[i][wd][1]
                firstx = xlocs[first][wd]
                firstz = hh[first]
                firstrad = wakewidths[i][wd][0] / 2.0
                secondx = xlocs[second][wd]
                secondz = hh[second]
                secondrad = wakewidths[i][wd][1] / 2.0
                # distance between the centerline of wake and rotor hub
                cd2 = np.sqrt(((firstx - secondx) ** 2.0)
                              + ((firstz - secondz) ** 2.0))
                # if wakes do not overlap at all within the rotor swept area
                if cd2 > (firstrad + secondrad):
                    overlap_flag = 1
                    for q in range(len(usturbines[i][wd])):
                        j = usturbines[i][wd][q]
                        jz = hh[j]  # z coordinate of the wake's center
                        jx = xlocs[j][wd]  # x location of the wake's center
                        # y location of the wake's center
                        # jy = turbines[j].YLocation[wd]
                        jwakerad = (wakewidths[i][wd][q]) / 2.0
                        dist = distances[i][wd][q]
                        # distance between the centerline of wake and rotor hub
                        cd = np.sqrt(((jx - kx) ** 2.0) + ((jz - kz) ** 2.0))
                        if cd + krad <= jwakerad:
                            parpercent.append(1.0)

                        elif cd + jwakerad <= krad:
                            # if the wake is fully encompassed
                            # by the rotor diameter
                            wakearea = np.pi * (jwakerad ** 2.0)
                            percentwake = wakearea / (np.pi * (krad ** 2.0))
                            parpercent.append(percentwake)

                        else:
                            integrand1 = ((cd ** 2.0) + (krad ** 2.0)
                                          - (jwakerad ** 2.0))
                            integrand1 = integrand1 / (2.0 * cd * krad)
                            integrand2 = ((cd ** 2.0) + (jwakerad ** 2.0)
                                          - (krad ** 2.0))
                            integrand2 = integrand2 / (2.0 * cd * jwakerad)
                            d = (krad ** 2.0) * (np.arccos(integrand1))
                            b = (jwakerad ** 2.0) * (np.arccos(integrand2))
                            c = 0.5 * np.sqrt((-cd + krad + jwakerad)
                                              * (cd + krad - jwakerad)
                                              * (cd - krad + jwakerad)
                                              * (cd + krad + jwakerad))
                            AOverlap = d + b - c
                            RSA = np.pi * (krad ** 2.0)
                            z = AOverlap / RSA
                            # percentage of RSA that has wake interaction
                            parpercent.append(z)
            # if there are overlapping wakes or more than 2 turbines,
            # discretize space instead of calculating percent
            if len(usturbines[i][wd]) >= 2 and overlap_flag != 1:
                # if there are at least 2 upstream turbines whose
                # wakes overlap, discretize the RSA and evaluate each point
                xx, zz = Discretize_RSA(xlocs[i][wd], hh[i], rr[i])
                # dummyx = discretized x-locations for each wind direction for
                # a single turbine
                dummyx[wd] = xx
                dummyz[wd] = zz
            complete_percent.append(parpercent)
        percent[i] = complete_percent
        xcoords[i] = dummyx
        zcoords[i] = dummyz
    # Code Check
    # Compute_Wake(initial_num, z0, U0, Zref, alphah, ro, aif)

    # calculate wind speed for each downstream turbine based
    # on downstream distance
    for wd in range(num_directions):
        wdsp_byturb = []
        analysis_order = [(i, ylocs[i][wd]) for i in range(initial_num)]
        analysis_order.sort(key=lambda x: x[1])
        analysis_order = [i[0] for i in analysis_order]
        for k in analysis_order:
            wdsp = []
            for u0i in range(0, len(U0)):
                if U0[u0i] > 0:
                    if len(usturbines[k][wd]) == 0:
                        # if turbine has no upstream turbines,
                        # INCORPORATE POWER LAW
                        hubheight = hh[k]
                        # corrects wind speed for hub height
                        Uz = U0[u0i] * ((hubheight / Zref) ** alphah)
                        wdsp.append(Uz)

                    elif len(usturbines[k][wd]) == 1:
                        # if turbine has 1 upstream turbine
                        total = 0.0
                        # USturb = usturbines[k][wd][0]
                        # USht = hh[USturb]
                        x = distances[k][wd][0]
                        hubheight = hh[k]
                        alpha = (0.5 / np.log(hubheight / z0))
                        Rr = rr[k]

                        # Grady Model
                        r1 = Rr * np.sqrt((1 - aif) / (1 - 2*aif))
                        EWU = (U0[u0i]
                               * (1 - (2 * aif)/((1 + alpha*(x/r1))**(2))))
                        Uz = EWU * ((hubheight / Zref) ** alphah)
                        # print(turbines[k].percent[wd][0])
                        portion = Uz * percent[k][wd][0]
                        remainder = (U0[u0i] * (1.0 - percent[k][wd][0])
                                     * ((hubheight / Zref) ** alphah))
                        # weighted average of windspeeds
                        total = portion + remainder
                        wdsp.append(total)

                    elif (len(usturbines[k][wd]) == 2
                          and len(percent[k][wd]) != 0):
                        # if the turbine has two upstream turbines
                        # whose wakes do not overlap
                        portion = 0.0
                        total = 0.0
                        for j in range(0, len(usturbines[k][wd])):
                            x = distances[k][wd][j]
                            # USturb = turbines[k].usturbines[wd][j]
                            hubheight = hh[k]
                            alpha = 0.5 / np.log(hubheight / z0)
                            Rr = rr[k]
                            r1 = Rr * np.sqrt((1 - aif) / (1 - 2 * aif))
                            wake_red = ((1 - (2 * aif)
                                        / ((1 + alpha*(x / r1))**(2))))
                            EWU = U0[u0i] * wake_red
                            Uz = EWU * ((hubheight / Zref) ** alphah)
                            portion += Uz * percent[k][wd][j]
                        rem_perc = 1.0 - percent[k][wd][0] - percent[k][wd][1]
                        remainder = U0[u0i] * rem_perc
                        # INCORPORATE POWER LAW
                        remainder = remainder * ((hubheight / Zref) ** alphah)
                        # weighted average of windspeeds
                        total = portion + remainder
                        wdsp.append(total)
                    # turbine has at least two upstream turbines
                    # whos wakes overlap
                    elif (len(usturbines[k][wd]) >= 2
                          and len(percent[k][wd]) == 0):
                        coordWS = []
                        usturbcoord = [[] for i in range(len(xcoords[k][wd]))]
                        for i in range(0, len(xcoords[k][wd])):
                            # xcoords created in Discretize_RSA
                            decWS = []
                            xval = xcoords[k][wd][i]
                            zval = zcoords[k][wd][i]
                            khub = hh[k]
                            Rr = rr[k]
                            for j in range(len(usturbines[k][wd])):
                                x = distances[k][wd][j]
                                US = usturbines[k][wd][j]
                                r2 = wakewidths[k][wd][j] / 2.0
                                xc = xlocs[US][wd]
                                zhubc = hh[US]
                                xturb = xval
                                zhubturb = zval
                                # height of the triangular portion of
                                # the chord area in z
                                rt2 = abs(zhubturb - zhubc)
                                # height of the triangluar portion of
                                # the chord area in x
                                rt1 = abs(xturb - xc)
                                # distance between wake center
                                # and discritized point
                                space = np.sqrt((rt2 ** 2) + (rt1 ** 2))

                                if space <= r2:  # if point is within wake
                                    Rr = rr[k]
                                    alpha = 0.5 / np.log(zval / z0)
                                    # Grady's a
                                    r1 = (Rr
                                          * np.sqrt((1 - aif) / (1 - 2 * aif)))
                                    denom = ((1 + alpha*(x / r1))**2)
                                    wake = (1 - (2 * aif) / denom)
                                    Uz = U0[u0i] * wake
                                    decWS.append(Uz)
                                    usturbcoord[i].append(US)

                            coordui = 0.0
                            if len(decWS) != 0:
                                # if the point only has one wake acting on it
                                if len(decWS) == 1:
                                    coordui = (decWS[0]
                                               * ((zval / Zref) ** alphah))
                                    coordWS.append(coordui)
                                # if the pint has more than one
                                # wake acting on it
                                elif len(decWS) > 1:
                                    tally = 0.0
                                    for l in range(0, len(decWS)):
                                        u = decWS[l]
                                        tally += ((1.0 - (u / U0[u0i])) ** 2.0)

                                    coordui = U0[u0i] * (1 - (np.sqrt(tally)))
                                    # INCORPORATE POWER LAW
                                    coordui = (coordui
                                               * ((zval / Zref) ** alphah))
                                    coordWS.append(coordui)
                            # if the point has no wakes acting on it
                            else:
                                Uz = U0[u0i] * ((zval / Zref) ** alphah)
                                coordui = Uz
                                coordWS.append(coordui)
                        # nested wake provision
                        # if every point has the same upstream turbines
                        # AND the user has specified the nwp
                        subset = [usturbcoord[0] == i for i in usturbcoord]
                        all_set = set(subset)
                        if all_set == {True} and nwp:
                            # find index of closest upstream wake
                            ustbs = distances[k][wd]
                            x = min(ustbs)
                            usindex = ustbs.index(x)
                            usindex = usturbines[k][wd][usindex]
                            hubheight = hh[k]
                            alpha = (0.5 / np.log(hubheight / z0))
                            Rr = rr[k]
                            # Grady Model
                            r1 = Rr * np.sqrt((1-aif) / (1 - 2*aif))
                            EWU = (wdsp_byturb[usindex][u0i]
                                   * (1 - (2*aif)/((1+alpha*(x/r1))**(2))))
                            wdsp.append(EWU * ((hubheight / Zref) ** alphah))
                        # no nested wake provision
                        else:
                            # Sum discretized wind speeds
                            tally2 = 0.0
                            percentage = 1.0 / 49.0
                            for f in range(0, len(coordWS)):
                                tally2 += percentage * coordWS[f]
                            wdsp.append(tally2)
                elif int(U0[u0i]) == 0:
                    wdsp.append(0.)
                else:
                    raise ValueError('negative windspeed encountered')
            wdsp_byturb.append(wdsp)
        order_wdsp = list(zip(analysis_order, wdsp_byturb))
        order_wdsp.sort(key=lambda x: x[0])
        wdsp_byturb = [ii[1] for ii in order_wdsp]
        windspeeds[wd] = wdsp_byturb
        # print('windspeeds end')
        # print(windspeeds)

    # calculate power developed for each turbine
    for i in range(0, initial_num):
        pwr = []
        rorad = rr[i]
        Area = (rorad ** 2.0) * np.pi
        for wd in range(num_directions):
            for spd in range(len(U0)):
                # incorporating power curve suggested by Pat,
                # June 10th <-- Bryony
                less_rated = windspeeds[wd][i][spd] < rated
                greater_cutin = windspeeds[wd][i][spd] >= cut_in
                if less_rated and greater_cutin:
                    # cubic region of curve
                    temp1 = (0.5 * ro * Area * (windspeeds[wd][i][spd] ** 3.0)
                             * Cp * availability / 1000.)
                    p1 = temp1 * probwui[wd][spd]
                    pwr.append(p1)

                elif not greater_cutin or windspeeds[wd][i][spd] >= cut_out:
                    # wind below cut-in speed or above cut-out = 0 kW
                    pwr.append(0.0)
                # constant for rated power and above
                elif not less_rated and windspeeds[wd][i][spd] < cut_out:
                    temp1 = (0.5 * ro * Area * (rated ** 3.0)
                             * Cp * availability / 1000.)
                    p1 = temp1 * probwui[wd][spd]
                    pwr.append(p1)
        power[i] = [this_power for this_power in pwr]
    # print(percent)
    if extra:
        return power, windspeeds
    else:
        return power


def PARK_2D(xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah,
            ro, aif, farm_y, cut_in, rated, cut_out, Cp,
            availability, nwp=False, extra=False):
    if len(set(hh)) != 1:
        raise ValueError('multiple hub heights in 2D Park calculation')
    initial_num = len(xlocs)
    num_directions = len(xlocs[0])
    wdsp_list = [[0.] * len(U0) for ii in range(initial_num)]
    windspeeds = [wdsp_list for ii in range(num_directions)]
    usturbines = [[] for ii in range(initial_num)]
    wakewidths = [[] for ii in range(initial_num)]
    distances = [[] for ii in range(initial_num)]
    percent = [[] for ii in range(initial_num)]
    xcoords = [[] for ii in range(initial_num)]
    zcoords = [[] for ii in range(initial_num)]
    power = [[] for ii in range(initial_num)]
    for j in range(initial_num):  # downstream turbine
        upstrm = []
        distanceus = []
        wakewidthds = []
        for direction in range(num_directions):
            In_Wakek = []
            # turbine j's X Location
            khub = xlocs[j][direction]
            krad = rr[j]
            # define left most point of rotor swept area of turbine j
            kleft = khub - krad
            # define right most point of rotor swept area of turbine k
            kright = khub + krad
            wake_d = []
            disty = []

            for i in range(0, initial_num):  # upstream turbine
                if j != i:
                    hubheight = hh[i]
                    alpha = 0.5 / (np.log(hubheight / z0))
                    y = ylocs[i][direction]
                    x = xlocs[i][direction]
                    # Sets dis to max downstream distance
                    dis = farm_y - y
                    Rr = rr[i]
                    # Calculate maximum ds wake radius
                    r1 = (alpha * dis) + Rr
                    space1 = x + r1
                    space2 = x - r1
                    # check left and right side for overlap
                    # if wake extended to end of farm
                    kleft_cond = (kleft >= space2 and kleft <= space1)
                    kright_cond = (kright >= space2 and kright <= space1)
                    if kleft_cond or kright_cond:
                        if ylocs[i][direction] < ylocs[j][direction]:
                            Y = ylocs[j][direction]
                            # distance between turbines
                            dist = Y - y
                            # print(dist)  # code check
                            # define radius of triangular wake
                            wake_rad = (alpha * dist) + Rr
                            # kz is the z coordinate of the rotor j's hub
                            kz = hh[j]
                            # jz is the z coordinate of the wake's center
                            jz = hh[i]
                            # distance between the centerline
                            # of wake and rotor hub
                            cd = np.sqrt((x - khub) ** 2.0 + (jz - kz) ** 2.0)
                            if cd < (wake_rad + krad):
                                # if distance between centers is less than the
                                # sum of the two radii, the rotor swept area
                                # is in the wake
                                In_Wakek.append(i)
                                wake_d.append(wake_rad * 2.0)
                                disty.append(dist)
            upstrm.append(In_Wakek)
            distanceus.append(disty)
            wakewidthds.append(wake_d)
        usturbines[j] = upstrm
        wakewidths[j] = wakewidthds
        distances[j] = distanceus

        # print('usturbines for ', i, ': ',turbines[i].usturbines)
        # print('wakewidth for ', j, ': ',turbines[j].wakewidth)
        # print('distances for ', j, ': ',turbines[j].distance)

    #    for i in range(0, initial_num):
    #        dsds = []
    #        for d in range(0, direction):
    #            dsone = []
    #            for j in range(0, initial_num):
    #                if j != i:
    #                    if i in turbines[j].usturbines[d]:
    #                        dsone.append(j)
    #            dsds.append(dsone)
    #        turbines[i].dsturbines = dsds
    #        # print('dsturbines for ', j, ': ',turbines[j].dsturbines)

    #    code check
    #    print(turbines[7].dsturbines[0])
    #    print(turbines[7].dsturbinesrec)
    #    print(turbines[7].usturbines[0])
    #    print(turbines[7].usturbinesrec)
    #    print(turbines[7].wakewidth)
    #    print(turbines[7].distance)
    #    print(turbines[4].dsturbines[0])
    #    print(turbines[4].dsturbinesrec)
    #    print(turbines[4].usturbines[0])
    #    print(turbines[4].usturbinesrec)
    #    print(turbines[4].wakewidth)
    #    print(turbines[4].distance)

    # Now that we know which turbines are downstream of others,
    # calculate the percentage of the rotor swept area that is within the wake
    for i in range(0, initial_num):
        complete_percent = []
        dummyx = [[] for ii in range(num_directions)]
        dummyz = [[] for ii in range(num_directions)]
        for wd in range(num_directions):
            parpercent = []
            overlap_flag = 0
            kz = hh[i]  # turbine k's hub height (z-location)
            kx = xlocs[i][wd]  # turbine k's x location
            # ky = turbines[i].YLocation[wd]  # turbine k's y location
            krad = rr[i]  # turbine k's rotor radius
            # if the turbine has one upstream turbine
            if len(usturbines[i][wd]) == 1:
                j = usturbines[i][wd][0]
                # z coordinate of the wake's center
                jz = hh[j]
                # x coordinate of the wake's center
                jx = xlocs[j][wd]
                # y coordinate of the wake's center
                # jy = turbines[j].YLocation[wd]
                # radius of wake width
                jwakerad = (wakewidths[i][wd][0]) / 2.0
                dist = distances[i][wd][0]
                # distance between centerline of wake and rotor hub
                cd = abs(jx-kx)
                # if dsturbine is completely in usturbine wake, overlap = 100%
                if cd + krad <= jwakerad:
                    parpercent.append(1.0)
                    # print('works')

                elif cd + jwakerad <= krad:
                    # if the wake is fully encompassed by the rotor diameter
                    # flattened to 2D
                    percentwake = jwakerad / (krad * 2.)
                    parpercent.append(percentwake)

                else:
                    # flattened to 2D
                    z = (krad + jwakerad - cd) / krad
                    # percentage of RSA that has wake interaction
                    parpercent.append(z)

            elif len(usturbines[i][wd]) == 2:
                # if the turbine has two upstream turbines
                first = usturbines[i][wd][0]
                second = usturbines[i][wd][1]
                firstx = xlocs[first][wd]
                # firstz = hh[first]
                firstrad = wakewidths[i][wd][0] / 2.0
                secondx = xlocs[second][wd]
                # secondz = hh[second]
                secondrad = wakewidths[i][wd][1] / 2.0
                # distance between the centerline of wake and rotor hub
                cd2 = abs(firstx - secondx)
                # if wakes do not overlap at all within the rotor swept area
                if cd2 > (firstrad + secondrad):
                    overlap_flag = 1
                    for q in range(len(usturbines[i][wd])):
                        j = usturbines[i][wd][q]
                        jz = hh[j]  # z coordinate of the wake's center
                        jx = xlocs[j][wd]  # x location of the wake's center
                        # y location of the wake's center
                        # jy = turbines[j].YLocation[wd]
                        jwakerad = (wakewidths[i][wd][q]) / 2.0
                        dist = distances[i][wd][q]
                        # distance between the centerline of wake and rotor hub
                        cd = abs(jx - kx)
                        if cd + krad <= jwakerad:
                            # turbine is totally within the upstream wake
                            parpercent.append(1.0)

                        elif cd + jwakerad <= krad:
                            # if the wake is fully encompassed
                            # by the rotor diameter
                            # condensed to 2D
                            percentwake = jwakerad / (krad * 2.)
                            parpercent.append(percentwake)

                        else:
                            # flattened to 2D
                            z = (krad + jwakerad - cd) / (krad * 2.)
                            print(jwakerad)
                            print(cd)
                            print(krad)
                            # percentage of RSA that has wake interaction
                            parpercent.append(z)

            if len(usturbines[i][wd]) >= 2 and overlap_flag != 1:
                # if there are at least 2 upstream turbines whose
                # wakes overlap, discretize the RSA and evaluate each point
                xx, zz = Discretize_RSA(xlocs[i][wd], hh[i], rr[i], True)
                # dummyx = discretized x-locations for each wind direction for
                # a single turbine
                dummyx[wd] = xx
                dummyz[wd] = zz
            complete_percent.append(parpercent)
        percent[i] = complete_percent
        xcoords[i] = dummyx
        zcoords[i] = dummyz
    # Code Check
    # Compute_Wake(initial_num, z0, U0, Zref, alphah, ro, aif)
    # calculate wind speed for each downstream turbine based
    # on downstream distance
    for wd in range(num_directions):
        wdsp_byturb = []
        analysis_order = [(i, ylocs[i][wd]) for i in range(initial_num)]
        analysis_order.sort(key=lambda x: x[1])
        analysis_order = [i[0] for i in analysis_order]
        for k in analysis_order:
            wdsp = []
            for u0i in range(0, len(U0)):
                if U0[u0i] > 0.:
                    if len(usturbines[k][wd]) == 0:
                        # if turbine has no upstream turbines,
                        # INCORPORATE POWER LAW
                        hubheight = hh[k]
                        # corrects wind speed for hub height
                        Uz = U0[u0i] * ((hubheight / Zref) ** alphah)
                        wdsp.append(Uz)

                    elif len(usturbines[k][wd]) == 1:
                        # if turbine has 1 upstream turbine
                        total = 0.0
                        # USturb = usturbines[k][wd][0]
                        # USht = hh[USturb]
                        x = distances[k][wd][0]
                        hubheight = hh[k]
                        temp = (0.5 / np.log(hubheight / z0))
                        # turbines[k].alpha = temp
                        alpha = temp
                        Rr = rr[k]

                        # Grady Model
                        r1 = Rr * np.sqrt((1 - aif) / (1 - 2*aif))
                        EWU = (U0[u0i]
                               * (1 - (2 * aif)/((1 + alpha*(x/r1))**(2))))
                        Uz = EWU * ((hubheight / Zref) ** alphah)
                        # print(turbines[k].percent[wd][0])
                        portion = Uz * percent[k][wd][0]
                        remainder = (U0[u0i] * (1.0 - percent[k][wd][0])
                                     * ((hubheight / Zref) ** alphah))
                        # weighted average of windspeeds
                        total = portion + remainder
                        wdsp.append(total)

                    elif (len(usturbines[k][wd]) == 2
                          and len(percent[k][wd]) != 0):
                        # if the turbine has two upstream turbines
                        # whose wakes do not overlap
                        portion = 0.0
                        total = 0.0
                        for j in range(0, len(usturbines[k][wd])):
                            x = distances[k][wd][j]
                            # USturb = turbines[k].usturbines[wd][j]
                            hubheight = hh[k]
                            alpha = 0.5 / np.log(hubheight / z0)
                            Rr = rr[k]
                            r1 = Rr * np.sqrt((1 - aif) / (1 - 2 * aif))
                            denom = (1 + alpha*(x/r1))**(2)
                            wake_red = (1 - (2 * aif) / denom)
                            EWU = U0[u0i] * wake_red
                            Uz = EWU * ((hubheight / Zref) ** alphah)
                            portion += Uz * percent[k][wd][j]
                        rem_perc = 1.0 - percent[k][wd][0] - percent[k][wd][1]
                        remainder = U0[u0i] * rem_perc
                        # INCORPORATE POWER LAW
                        remainder = remainder * ((hubheight / Zref) ** alphah)
                        # weighted average of windspeeds
                        total = portion + remainder
                        wdsp.append(total)
                    # turbine has at least two upstream turbines
                    # whos wakes overlap
                    elif (len(usturbines[k][wd]) >= 2
                          and len(percent[k][wd]) == 0):
                        coordWS = []
                        usturbcoord = [[] for i in range(len(xcoords[k][wd]))]
                        for i in range(0, len(xcoords[k][wd])):
                            # xcoords created in Discretize_RSA
                            decWS = []
                            xval = xcoords[k][wd][i]
                            zval = zcoords[k][wd][i]
                            khub = hh[k]
                            Rr = rr[k]
                            for j in range(len(usturbines[k][wd])):
                                x = distances[k][wd][j]
                                US = usturbines[k][wd][j]
                                r2 = wakewidths[k][wd][j] / 2.0
                                xc = xlocs[US][wd]
                                zhubc = hh[US]
                                xturb = xval
                                zhubturb = zval
                                # height of the triangular portion of
                                # the chord area in z
                                rt2 = abs(zhubturb - zhubc)
                                # height of the triangluar portion of
                                # the chord area in x
                                rt1 = abs(xturb - xc)
                                # distance between wake center
                                # and discritized point
                                space = np.sqrt((rt2 ** 2) + (rt1 ** 2))

                                if space <= r2:  # if point is within wake
                                    Rr = rr[k]
                                    alpha = 0.5 / np.log(zval / z0)
                                    # Grady's a
                                    r1 = (Rr
                                          * np.sqrt((1 - aif) / (1 - 2 * aif)))
                                    denom = (1 + alpha * (x / r1))**(2)
                                    wake = (1 - (2*aif)/denom)
                                    Uz = U0[u0i] * wake
                                    decWS.append(Uz)
                                    usturbcoord[i].append(US)

                            coordui = 0.0
                            if len(decWS) != 0:
                                # if the point only has one wake acting on it
                                if len(decWS) == 1:
                                    coordui = (decWS[0]
                                               * ((zval / Zref) ** alphah))
                                    coordWS.append(coordui)
                                # if the pint has more than one
                                # wake acting on it
                                elif len(decWS) > 1:
                                    tally = 0.0
                                    for l in range(0, len(decWS)):
                                        u = decWS[l]
                                        tally += ((1.0 - (u / U0[u0i])) ** 2.0)
                                    coordui = U0[u0i] * (1 - (np.sqrt(tally)))
                                    # INCORPORATE POWER LAW
                                    coordui = (coordui
                                               * ((zval / Zref) ** alphah))
                                    coordWS.append(coordui)
                            # if the point has no wakes acting on it
                            else:
                                Uz = U0[u0i] * ((zval / Zref) ** alphah)
                                coordui = Uz
                                coordWS.append(coordui)
                        # nested wake provision
                        # if every point has the same upstream turbines
                        # AND the user has specified the nwp
                        subset = [usturbcoord[0] == i for i in usturbcoord]
                        all_set = set(subset)
                        if all_set == {True} and nwp:
                            # find index of closest upstream wake
                            ustbs = distances[k][wd]
                            x = min(ustbs)
                            usindex = ustbs.index(x)
                            usindex = usturbines[k][wd][usindex]
                            hubheight = hh[k]
                            alpha = (0.5 / np.log(hubheight / z0))
                            Rr = rr[k]
                            # Grady Model
                            r1 = Rr * np.sqrt((1-aif) / (1 - 2*aif))
                            EWU = (wdsp_byturb[usindex][u0i]
                                   * (1 - (2*aif)/((1+alpha*(x/r1))**(2))))
                            wdsp.append(EWU * ((hubheight / Zref) ** alphah))
                        # no nested wake provision
                        else:
                            # Sum discretized wind speeds
                            tally2 = 0.0
                            percentage = 1.0 / len(xcoords[k][wd])
                            for f in range(0, len(coordWS)):
                                tally2 += percentage * coordWS[f]
                            wdsp.append(tally2)
                elif int(U0[u0i]) == 0:
                    wdsp.append(0.)
                else:
                    raise ValueError('negative windspeed encountered')
            wdsp_byturb.append(wdsp)
        order_wdsp = list(zip(analysis_order, wdsp_byturb))
        order_wdsp.sort(key=lambda x: x[0])
        wdsp_byturb = [ii[1] for ii in order_wdsp]
        windspeeds[wd] = wdsp_byturb

    # calculate power developed for each turbine
    for i in range(0, initial_num):
        pwr = []
        rorad = rr[i]
        Area = (rorad ** 2.0) * np.pi
        for wd in range(num_directions):
            for spd in range(len(U0)):
                # incorporating power curve suggested by Pat,
                # June 10th <-- Bryony
                less_rated = windspeeds[wd][i][spd] < rated
                greater_cutin = windspeeds[wd][i][spd] >= cut_in
                if less_rated and greater_cutin:
                    # cubic region of curve
                    temp1 = (0.5 * ro * Area * (windspeeds[wd][i][spd] ** 3.0)
                             * Cp * availability / 1000.)
                    p1 = temp1 * probwui[wd][spd]
                    pwr.append(p1)

                elif not greater_cutin or windspeeds[wd][i][spd] >= cut_out:
                    # wind below cut-in speed or above cut-out = 0 kW
                    pwr.append(0.0)
                # constant for rated power and above
                elif not less_rated and windspeeds[wd][i][spd] < cut_out:
                    temp1 = (0.5 * ro * Area * (rated ** 3.0)
                             * Cp * availability / 1000.)
                    p1 = temp1 * probwui[wd][spd]
                    pwr.append(p1)
        power[i] = [this_power for this_power in pwr]
    if extra:
        return power, windspeeds
    else:
        return power


def Discretize_RSA(xloc, hh, rad, D2=False):
    if hh < 0:
        raise ValueError('Hub height specified is less than 0 m')
    if rad < 0.:
        raise ValueError('Radius specified is less than 0 m')
    xcoords = []
    zcoords = []
    # center row
    # center point
    xcoords.append(xloc)
    zcoords.append(hh)
    for j in range(1, 5):
        xcoords.append(xloc + (j * (rad / 4.0)))
        xcoords.append(xloc - (j * (rad / 4.0)))
        zcoords.append(hh)
        zcoords.append(hh)
    if not D2:
        # only add next points to 3D
        # next rows
        # + in Z-Direction
        # center Point
        xcoords.append(xloc)
        zcoords.append(hh + (rad / 4.0))
        for j in range(1, 4):
            xcoords.append(xloc + (j * (rad / 4.0)))
            xcoords.append(xloc - (j * (rad / 4.0)))
            zcoords.append(hh + (rad / 4.0))
            zcoords.append(hh + (rad / 4.0))

        # - in Z-Direction
        # center Point
        xcoords.append(xloc)
        zcoords.append(hh - (rad / 4.0))
        for j in range(1, 4):
            xcoords.append(xloc + (j * (rad / 4.0)))
            xcoords.append(xloc - (j * (rad / 4.0)))
            zcoords.append(hh - (rad / 4.0))
            zcoords.append(hh - (rad / 4.0))

        # next rows
        # + in Z-Direction
        # center Point
        xcoords.append(xloc)
        zcoords.append(hh + (rad / 2.0))
        for j in range(1, 4):
            xcoords.append(xloc + (j * (rad / 4.0)))
            xcoords.append(xloc - (j * (rad / 4.0)))
            zcoords.append(hh + (rad / 2.0))
            zcoords.append(hh + (rad / 2.0))

        # - in Z-Direction
        # center Point
        xcoords.append(xloc)
        zcoords.append(hh - (rad / 2.0))
        for j in range(1, 4):
            xcoords.append(xloc + (j * (rad / 4.0)))
            xcoords.append(xloc - (j * (rad / 4.0)))
            zcoords.append(hh - (rad / 2.0))
            zcoords.append(hh - (rad / 2.0))

        # next rows
        # + in Z-Direction
        # center Point
        xcoords.append(xloc)
        zcoords.append(hh + (rad * (3.0 / 4.0)))
        for j in range(1, 3):
            xcoords.append(xloc + (j * (rad / 4.0)))
            xcoords.append(xloc - (j * (rad / 4.0)))
            zcoords.append(hh + (rad * (3.0 / 4.0)))
            zcoords.append(hh + (rad * (3.0 / 4.0)))

        # - in Z-Direction
        # center Point
        xcoords.append(xloc)
        zcoords.append(hh - (rad * (3.0 / 4.0)))
        for j in range(1, 3):
            xcoords.append(xloc + (j * (rad / 4.0)))
            xcoords.append(xloc - (j * (rad / 4.0)))
            zcoords.append(hh - (rad * (3.0 / 4.0)))
            zcoords.append(hh - (rad * (3.0 / 4.0)))

        # last points: Top Center & Bottom Center
        xcoords.append(xloc)
        zcoords.append(hh + rad)
        xcoords.append(xloc)
        zcoords.append(hh - rad)
    return xcoords, zcoords
