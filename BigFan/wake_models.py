# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 15:37:20 2018

@author: Annalise

ME 599 Project
Spring 2018
Wake Models
"""

try:
#    from dolfin import near
#    from dolfin import grad
#    from dolfin import inner
#    from dolfin import dx
#    from dolfin import div
#    from dolfin import Constant
#    from dolfin import Expression
#    from dolfin import Function
#    from dolfin import project
#    from dolfin import SubDomain
#    from dolfin import RectangleMesh
#    from dolfin import Point
#    from dolfin import VectorElement
#    from dolfin import FiniteElement
#    from dolfin import FunctionSpace
#    from dolfin import MixedElement
#    from dolfin import VectorFunctionSpace
#    from dolfin import CellFunction
#    from dolfin import cells
#    from dolfin import SpatialCoordinate
#    from dolfin import refine
#    from dolfin import DirichletBC
#    from dolfin import TestFunctions
#    from dolfin import NonlinearVariationalProblem
#    from dolfin import derivative
#    from dolfin import NonlinearVariationalSolver
#    from dolfin import split
    nofenics = False
except ModuleNotFoundError:
    print('warning: fenics is not installed or the fenicsproject nvironment '
          + 'is not activated. The CFD wake model is not available')
    nofenics = True
import numpy as np

# NOTES TO ANNALISE:
#     Change CFD inputs to get rid of axle spin


def PARK_3D(xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah,
            ro, aif, farm_y, cut_in, rated, cut_out, Cp,
            availability, nwp=False, extra=False):
    """Compute the turbine power generation (and optionally turbine wind speed)
        using 3D Jensen (PARK) wake model

    Args:
        xlocs: list of x-coordinates of wind turbines where each item in the
                list is a list of that turbine's x-coordinate at each
                wind onset angle
        ylocs: list of y-coordinates of wind turbines where each item in the
                list is a list of that turbine's y-coordinate at each
                wind onset angle
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        probwui: list of probabilities of onset wind conditions
            first index represets onset wind direction index
            second index represents onset wind speed index
        Zref: Wind speed reference height
        alphah: power law exponent
        ro: air density (float)
        aif: axial induction factor (float)
        farm_y: length of wind farm in y direction in meters (float)
        cut_in: turbine cut-in wind speed (float)
        rated: turbine rated wind speed (float)
        cut-out: turbine cut-out speed (float)
        Cp: power coefficient (float)
        availability: turbine availability (float)
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
    Returns:
        list of turbine power output by [turbine no.][onset angle index]
        windspeeds: windspeed by [turbine no.][onset angle index] (optional)
    """
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
    """Compute the turbine power generation (and optionally turbine wind speed)
        using 2D Jensen (PARK) wake model

    Args:
        xlocs: list of x-coordinates of wind turbines where each item in the
                list is a list of that turbine's x-coordinate at each
                wind onset angle
        ylocs: list of y-coordinates of wind turbines where each item in the
                list is a list of that turbine's y-coordinate at each
                wind onset angle
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        probwui: list of probabilities of onset wind conditions
            first index represets onset wind direction index
            second index represents onset wind speed index
        Zref: Wind speed reference height
        alphah: power law exponent
        ro: air density (float)
        aif: axial induction factor (float)
        farm_y: length of wind farm in y direction in meters (float)
        cut_in: turbine cut-in wind speed (float)
        rated: turbine rated wind speed (float)
        cut-out: turbine cut-out speed (float)
        Cp: power coefficient (float)
        availability: turbine availability (float)
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
    Returns:
        list of turbine power output by [turbine no.][onset angle index]
        windspeeds: windspeed by [turbine no.][onset angle index] (optional)
    """
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
    """Discretize rotor swept area of a specific turbine and return x- and z-
        coordinates

    Args:
        xlocs: x-location of turbine in question at onset angle in question
        hh: hub height of turbine in question
        rad: rotor radius of turbine in question
        D2: whether a 2D representation is desired (True) or a 3D
            representation (False)
    Returns:
        xcoords: x-coordinates of discretized rotor swept area
        zcoords: z-coordinates of discretized rotor swept area
    """
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


'''
def create_mesh(mx, my, mz, ma, rad2, site_x, site_y, numx, numy, numRefine,
                print_mesh=False, adaptive_meshing=True):
    """Create farm mesh for use in CFD wind speed calculation

    Args:
        mx: list of x-coordinates of wind turbines from 0-degree onset wind
            angle
        my: list of y-coordinates of wind turbines from 0-degree onset wind
            angle
        ma: list of turbine axial induction factors
        site_x: wind farm length in meters in x-directions (float)
        site_y: wind farm length in meters in y-direction(float)
        numx: number of pre-refinement mesh points in x-direction
        numy: number of pre-refinement mesh points in y-directions
        numRefine: numb of times all mesh points within the circle of the
            wind farm are refined
        print_mesh: whether to print the final farm mesh
        adaptive_meshing: whether to further refine the mesh size
            in the immediate vecinity of individual turbines
    Returns:
        wind farm mesh for CFD analysis
    """
    Lx = site_x * 6.
    Ly = site_y * 6.
    mesh = RectangleMesh(Point(-Lx/2., -Ly/2.), Point(Lx/2., Ly/2.),
                         numx, numy)
    # h = mesh.hmin()
    # refine mesh twice in circumradius of farm
    for nums in range(numRefine):
        # print 'refining mesh'
        mesh = refine_mesh(mesh, site_x, site_y, 'farm', mx, my, mz, ma, rad2)
        # h = mesh.hmin()
    if print_mesh:
        mesh1 = []
        for each in mesh.coordinates():
            if abs(each[0]) < site_x and abs(each[1]) < site_y:
                mesh1.append((float(each[0]), float(each[1])))
    if adaptive_meshing:
        mesh = refine_mesh(mesh, site_x, site_y, 'turbines', mx, my, mz,
                           ma, rad2)
    if print_mesh:
        meshx2 = []
        meshy2 = []
        for each in mesh.coordinates():
            in_X = abs(each[0]) < site_x
            in_Y = abs(each[1]) < site_y
            not_in = ((each[0], each[1]) not in mesh1)
            if (in_X and in_Y and not_in):
                meshx2.append(float(each[0]))
                meshy2.append(float(each[1]))
        plt.figure()
        plt.scatter([iii[0] for iii in mesh1], [iii[1] for iii in mesh1],
                    s=1, c='k')
        plt.scatter(meshx2, meshy2, s=1, c='r')
        plt.axis('equal')
        # plt.scatter(mx,my,color = 'r', marker='*')
        plt.savefig('mesh_vis_discEPS.png')
    print('mesh size: ', len(mesh.coordinates()))
    # h = mesh.hmin()
    # somehow setting up the mesh to store the values we need
    # function spaces, mixed function space syntax not backwards compatible
    V = VectorElement('Lagrange', mesh.ufl_cell(), 2)
    Q = FiniteElement('Lagrange', mesh.ufl_cell(), 1)
    VQ = FunctionSpace(mesh, MixedElement([V, Q]))
    # NSE equations
    V = VectorFunctionSpace(mesh, 'Lagrange', 2)
    Q = FunctionSpace(mesh, 'Lagrange', 1)
    return V, Q, VQ, mesh


def refine_mesh(mesh, site_x, site_y, refine_where, mx, my, mz, ma, rad2):
    """Refine farm mesh for use in CFD wind speed calculation

    Args:
        mesh: current mesh for refinement
        site_x: wind farm length in meters in x-directions (float)
        site_y: wind farm length in meters in y-direction(float)
        refine_where: refine about the 'farm' or about 'turbines'
        mx: list of x-coordinates of wind turbines from 0-degree onset wind
            angle
        my: list of y-coordinates of wind turbines from 0-degree onset wind
            angle
        my: list of z-coordinates of wind turbines
        ma: list of turbine axial induction factors
        rad2: radius about turbines in which to refine mes
    Returns:
        wind farm mesh for CFD analysis
    """
    # refines the mesh around the site boundaries
    h = mesh.hmin()
    numturbs = len(mx)
    cell_f = CellFunction('bool', mesh, False)
    # create a mesh of the same size, where every cell is set to 'False'
    if refine_where == 'farm':
        for cell in cells(mesh):
            dotdis = cell.midpoint()[0]**2 + cell.midpoint()[1]**2
            if dotdis < (site_x**2 + site_y**2 + h):
                cell_f[cell] = True
                # if the midpoint of the cell is within the circumradius
                # of the farm, change the cell's value to true
    else:
        for cell in cells(mesh):  # cycle through each cell
            for i in range(numturbs):  # cycle through each turbine
                xdis = pow(cell.midpoint()[0] - mx[i], 2)
                ydis = pow(cell.midpoint()[1] - my[i], 2)
                if (xdis + ydis) < (pow(rad2, 2) + h):
                    cell_f[cell] = True
                    # if the midpoint of the cell is within a radius of a
                    # turbine
    mesh = refine(mesh, cell_f)
    # refine the cells within the circumradius of the farm
    return mesh


def createRotatedTurbineForce(mx, my, ma, A, beta, numturbs, alpha, V, mesh,
                              WTGexp, thickness, Ct, radius, checkpts=False):
    """Use Actuator disc theory to determine the force turbines
        amass on the environment

    Args:
        mx: list of x-coordinates of wind turbines from 0-degree onset wind
            angle
        my: list of y-coordinates of wind turbines from 0-degree onset wind
            angle
        my: list of z-coordinates of wind turbines
        ma: list of turbine axial induction factors
        A: rotor swept area of turbine in meters squared (float)
        numbturbs: number of turbines in the field
        alpha: wind onset angle
        V: functional space defined over mesh
        mesh: farm mesh
        WTGexp: smoothing kernal exponent
        thickness: smoothing kernal thickness parameter
        Ct: thrust coefficient
        radius: turbine rotor radius
        checkpts: optionally print current turbine locations
    Returns:
        turbine forces across mesh
    """
    # beta = integral over actuator disk area in x and y: used to normalize
    x = SpatialCoordinate(mesh)
    WTGbase = project(Expression(("1.0", "0.0"), degree=2), V)
    tf = Function(V)
    # print(tf)
    if checkpts:
        check_it = project(tf, V)
        n = [check_it(np.cos(alpha)*mx[i] - np.sin(alpha)*my[i],
                      np.sin(alpha)*mx[i] + np.cos(alpha)*my[i]) for i in range(numturbs)]
        nx = [(np.cos(alpha)*mx[i]
               - np.sin(alpha)*my[i]) for i in range(numturbs)]
        ny = [(np.sin(alpha)*mx[i]
               + np.cos(alpha)*my[i]) for i in range(numturbs)]
        fig, ax = plt.subplots()
        ax.scatter(nx, ny)
        for i, txt in enumerate(n):
            ax.annotate(txt, (nx[i], ny[i]))
        plt.savefig('initial_tf.png', bbox_inches='tight')
    for i in range(numturbs):
        # rotation
        xrot = np.cos(alpha)*mx[i] - np.sin(alpha)*my[i]
        yrot = np.sin(alpha)*mx[i] + np.cos(alpha)*my[i]
        # print((xrot, yrot))
        tf = tf + (0.5 * A * Ct / ((1. - ma[i]) ** 2)
                   / beta * np.exp(-(((x[0] - xrot)/thickness)**WTGexp
                                   + ((x[1] - yrot)/radius)**WTGexp))
                   * WTGbase.copy(deepcopy=True))
    if checkpts:
        check_it = project(tf, V)
        n = [check_it(np.cos(alpha)*mx[i] - np.sin(alpha)*my[i],
                      np.sin(alpha)*mx[i] + np.cos(alpha)*my[i]) for i in range(numturbs)]
        fig, ax = plt.subplots()
        ax.scatter(nx, ny)
        for i, txt in enumerate(n):
            ax.annotate(txt, (nx[i], ny[i]))
        plt.savefig('final_tf.png', bbox_inches='tight')
    return tf


def main(tf, wind_case, VQ, radius, wind_cases, Lx, Ly, mlDenom):
    """Determine wind speeds across field

    Args:
        tf: turbine force exerted across mesh
        VQ: mixed element functional stuff I don't totally understand
        wind_cases: list of tuples with onset angle [0], and speed [1]
        Lx: length of the extent of the mesh in the x-direction
        Ly: Length of the extent of the mesh in the y-direction
        mlDenom: mixing length denominator
    Returns:
        wind speed and pressure across mesh
    """
    nu = Constant(.00005)  # kinematic viscosity
    f = Constant((0., 0.))
    up_next = Function(VQ)
    # up_next becomes tuple of vector and finite elements for wind speed
    # and pressure
    u_next, p_next = split(up_next)
    # split vector (wind speed) and finite (pressure) elements?
    v, q = TestFunctions(VQ)

    class InitialConditions(Expression):
        # inherits from Expression class in fenics

        def __init__(self, **kwargs):
            rd.seed(2)  # WHY IS THIS HERE?

        def eval(self, values, x):
            values[0] = wind_cases[wind_case][1]
            values[1] = 0.0
            values[2] = 0.0

        def value_shape(self):
            return (3,)

    # boundary conditions
    class NoSlipBoundary(SubDomain):
        def inside(self, x, on_boundary):
            # windspeed has w = 0 at top and bottom
            return near(x[1]**2 - (Ly/2.)**2, 0.) and on_boundary

    class InflowBoundary(SubDomain):
        # windspeeed has u = inflow velocity and w = 0 at locations of inflow
        def inside(self, x, on_boundary):
            return near(x[0], -(Lx/2.)) and on_boundary

    class PeriodicBoundary(SubDomain):

        def inside(self, x, on_boundary):
            # return True if on left or bottom boundary
            # AND NOT on one of the two slave edges
            return bool((near(x[0], -(Lx/2.)) or near(x[1], -(Ly/2.)))
                        and (not (near(x[0], (Lx/2.)) or near(x[1], (Ly/2.))))
                        and on_boundary)

        def map(self, x, y):
            if near(x[0], (Lx/2.)) and near(x[1], (Ly/2.)):
                y[0] = x[0] - 2*(Lx/2.)
                y[1] = x[1] - 2*(Ly/2.)
            elif near(x[0], (Lx/2.)):
                y[0] = x[0] - 2*(Lx/2.)
                y[1] = x[1]
            else:  # near(x[1], (Ly/2.)):
                y[0] = x[0]
                y[1] = x[1] - 2*(Ly/2.)

    u0 = InitialConditions(degree=2)
    up_next.interpolate(u0)

    lmix = radius/mlDenom  # mixing lenth
    # mean rate of strain tensor ... so confused
    S = np.sqrt(2. * inner(0.5 * (grad(u_next)+grad(u_next).T),
                           0.5 * (grad(u_next)+grad(u_next).T)))
    nu_T = (lmix ** 2.) * S  # eddie viscosity

    F = (inner(grad(u_next)*u_next, v) * dx
         + (nu+nu_T)*inner(grad(u_next), grad(v)) * dx
         - inner(div(v), p_next) * dx
         - inner(div(u_next), q) * dx
         - inner(f, v)*dx
         + inner(tf*u_next[0]**2, v) * dx)
    # lateral BC
    bc1a = DirichletBC(VQ.sub(0).sub(1), Constant(0.0), NoSlipBoundary())

    # inflow BC
    bc2 = DirichletBC(VQ.sub(0), Constant((wind_cases[wind_case][1], 0.0)),
                      InflowBoundary())
    bc = [bc1a, bc2]
    J = derivative(F, up_next)
    problem = NonlinearVariationalProblem(F, up_next, bc, J=J)
    solver = NonlinearVariationalSolver(problem)
    prm = solver.parameters
    solver.nonlinear_variational_solver = 'newton_solver'
    prm["newton_solver"]["absolute_tolerance"] = 1E-8
    prm["newton_solver"]["relative_tolerance"] = 1E-7
    prm["newton_solver"]["maximum_iterations"] = 25
    prm["newton_solver"]["relaxation_parameter"] = 1.0
    prm["newton_solver"]["linear_solver"] = 'mumps'
    solver.solve()
    u_next, p_next = split(up_next)
    return u_next, up_next


def rotatedPowerFunction(alpha, A, beta, mx, my, ma, up,
                         numturbs, V, mesh, air_density,
                         Cp, checkpts, radius, heat=False):
    """Determine power output by turbine

    Args:
        alpha: wind onset angle
        A: turbine rotor swept area in meters squared (float)
        beta:
        mx: list of x-coordinates of wind turbines from 0-degree onset wind
            angle
        my: list of y-coordinates of wind turbines from 0-degree onset wind
            angle
        ma: list of turbine axial induction factors
        up: windspeed and pressure across mesh
        numturbs: number of turbines
        V:
        mesh: input mesh
        air_density: air density at farm
        Cp: power coefficient (float)
        checkpts: whether to print current turbine location
        radius: turbine rotor radius
        heat: whether to produce farm-wide heat map of wind speeds
    Returns:
        list of power output by turbine
    """
    J = []
    if checkpts:
        nx = [(np.cos(alpha)*mx[i]
               - np.sin(alpha)*my[i]) for i in range(numturbs)]
        ny = [(np.sin(alpha)*mx[i]
               + np.cos(alpha)*my[i]) for i in range(numturbs)]
        fig, ax = plt.subplots()
        ax.scatter(nx, ny)
        n = [up.sub(0)(nx[i], ny[i])[0] for i in range(numturbs)]
        for i, txt in enumerate(n):
            ax.annotate(txt, (nx[i], ny[i]))
        plt.savefig('windspeeds.png', bbox_inches='tight')
        plt.close()
    for i in range(numturbs):
        # rotation
        xrot = np.cos(alpha) * mx[i] - np.sin(alpha) * my[i]
        # -5 added by Annalise 12/14 to understand effects of smoothing kernal
        yrot = np.sin(alpha)*mx[i] + np.cos(alpha)*my[i]
        # print(up.sub(0)(xrot, yrot)[0])
        J.append(0.5 * air_density * np.pi * (radius ** 2) * Cp
                 / ((1. - float(ma[i])) ** 3) * (up.sub(0)(xrot, yrot)[0]**3))
        # up.sub(0)(xrot,yrot)[0] --> up == u and p combined
        # --> sub(0) == just u
        # --> (xrot, yrot) == position of interest (center pt)
        # --> [0] == x-velocity
    if heat:
        heat_out = [[]]
        outvals = 500
        nx = [(np.cos(alpha)*mx[i]
               - np.sin(alpha)*my[i]) for i in range(numturbs)]
        ny = [(np.sin(alpha)*mx[i]
               + np.cos(alpha)*my[i]) for i in range(numturbs)]
        interval_x = (max(nx) - min(nx)) * 2. / outvals
        if interval_x > 0.01:
            x_start = min(nx) - (max(nx) - min(nx)) * 0.5 + interval_x / 2.
            x1 = min(nx) - (max(nx) - min(nx)) * 0.5
            x2 = max(nx) + (max(nx) - min(nx)) * 0.5
        else:
            x_start = min(nx) - 100. + 200. / (2. * outvals)
            interval_x = 200. / outvals
            x1 = min(nx) - 100.
            x2 = max(nx) + 100.
        interval_y = (max(ny) - min(ny)) * 2. / outvals
        if interval_y > 0.01:
            y_start = min(ny) - (max(ny) - min(ny)) * 0.5 + interval_y / 2.
            y1 = min(ny) - (max(ny) - min(ny)) * 0.5
            y2 = max(ny) + (max(ny) - min(ny)) * 0.5
        else:
            y_start = min(ny) - 100. + 200. / (2. * outvals)
            interval_y = 200. / outvals
            y1 = min(ny) - 100.
            y2 = max(ny) + 100.
        spacing_outx = [i * interval_x + x_start for i in range(outvals)]
        sp_y = [i * interval_y + y_start for i in range(outvals)]
        spacing_outy = [sp_y[-i] for i in range(1, len(sp_y) + 1)]
        for j in spacing_outy:
            heat_out[0].append([up.sub(0)(i, j)[0] for i in spacing_outx])
        heat_out.append([x1, x2, y1, y2])
        # print(heat_out)
        return J, heat_out
    else:
        return J


def CFD_wake(xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah,
             ro, aif, farm_y, cut_in, rated, cut_out, Cp,
             availability, rad2, nwp=False, extra=False, adaptive_mesh=True):
    """Compute the turbine power generation (and optionally turbine wind speed)
        using WindSE2D CFD wake model

    Args:
        xlocs: list of x-coordinates of wind turbines where each item in the
                list is a list of that turbine's x-coordinate at each
                wind onset angle
        ylocs: list of y-coordinates of wind turbines where each item in the
                list is a list of that turbine's y-coordinate at each
                wind onset angle
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        probwui: list of probabilities of onset wind conditions
            first index represets onset wind direction index
            second index represents onset wind speed index
        Zref: Wind speed reference height
        alphah: power law exponent
        ro: air density (float)
        aif: axial induction factor (float)
        farm_y: length of wind farm in y direction in meters (float)
        cut_in: turbine cut-in wind speed (float)
        rated: turbine rated wind speed (float)
        cut-out: turbine cut-out speed (float)
        Cp: power coefficient (float)
        availability: turbine availability (float)
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
    Returns:
        list of turbine power output by [turbine no.][onset angle index]
        windspeeds: windspeed by [turbine no.][onset angle index] (optional)
    """
    if nofenics:
        raise ModuleNotFoundError('The fenicsproject environment is not '
                                  + 'available. Ensure project is installed '
                                  + 'and environemt is activated')
    if len(set(hh)) != 1:
        raise ValueError('More than one hub height specified for '
                         + '2D simulation')
    if hh[0] != Zref:
        # INCORPORATE POWER LAW!
        for ws in range(len(U0)):
            U0[ws] = U0[ws] * ((hh[0] / Zref) ** alphah)
    J = 0.
    cumulative_power = [0.] * len(xlocs)
    for i in range(len(xlocs[0])):  # for each wind direction
        mx = [k[i] for k in xlocs]
        my = [k[i] for k in ylocs]
        ma = [aif] * len(mx)
        for j in range(len(U0)):  # for each wind speed
            V, Q, VQ, mesh = create_mesh(mx, my, hh, ma, rad2)
            # print(wind_cases)
            tf_rot = createRotatedTurbineForce(mx, my, ma, A, B, numturbs,
                                               wind_cases[i][0], V, mesh)
            # calculate force imparted by turbines
            u_rot, up_rot = main(tf_rot, i, VQ)  # RANS solver
            if heat and i == 0:
                # only calc heat for wind from left
                power_dev, heat_out = rotatedPowerFunction(wind_cases[i][0], A,
                                                           beta, mx, my, ma,
                                                           up_rot, numturbs, V,
                                                           mesh, True)
            else:
                power_dev = rotatedPowerFunction(wind_cases[i][0], A, beta, mx,
                                                 my, ma, up_rot, numturbs, V,
                                                 mesh)
            J = J - (weights[i] * sum(power_dev))
            cumulative_power = [(k * weights[i]
                                 + jj) for k, jj in zip(power_dev,
                                                        cumulative_power)]
'''
