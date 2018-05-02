# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 14:58:46 2018

@author: Annalise Miller

ME 599 Project
Spring 2018
Objective Evaluation Options
"""


def cost(Compute_Wake, Compute_Cost,
         xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro, aif,
         farm_y, cut_in, rated, cut_out, Cp, availability, nwp, extra,
         depth, yrs, WCOE, distance_to_shore, a):
    """Compute the total cost of a farm

    Args:
        xlocs: list of x-coordinates of wind turbines at one wind onset angle
        ylocs: list of y-coordinates of wind turbines at one wind onset angle
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        probwui: list of lists for probability of onset wind conditions
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
        depth: water depth in meters (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
    Returns:
        total farm cost
        list of turbine power output by onset angle
        windspeeds: windspeed at each turbine (optional)
        total farm cost (optional)
    """
    costlocx = [i[0] for i in xlocs]
    costlocy = [i[0] for i in ylocs]
    costc, costa = Compute_Cost(costlocx, costlocy, rr, hh, ro, rated, Cp,
                                depth, yrs, WCOE, availability,
                                distance_to_shore)
    if extra:
        power, windspeeds = Compute_Wake(xlocs, ylocs, rr, hh, z0, U0, probwui,
                                         Zref, alphah, ro, aif, farm_y, cut_in,
                                         rated, cut_out, Cp, availability,
                                         nwp, extra)
        return (costc + costa), power, windspeeds, (costc + costa)
    else:
        power = Compute_Wake(xlocs, ylocs, rr, hh, z0, U0, probwui,
                             Zref, alphah, ro, aif, farm_y, cut_in,
                             rated, cut_out, Cp, availability,
                             nwp, extra)
        return (costc + costa), power


def profit(Compute_Wake, Compute_Cost,
           xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro, aif,
           farm_y, cut_in, rated, cut_out, Cp, availability, nwp, extra,
           depth, yrs, WCOE, distance_to_shore, a):
    """Compute the lifetime profit of a farm

    Args:
        xlocs: list of x-coordinates of wind turbines at one wind onset angle
        ylocs: list of y-coordinates of wind turbines at one wind onset angle
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        probwui: list of lists for probability of onset wind conditions
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
        depth: water depth in meters (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
    Returns:
        total farm cost
        list of turbine power output by onset angle
        windspeeds: windspeed at each turbine (optional)
        total farm cost (optional)
    """
    costlocx = [i[0] for i in xlocs]
    costlocy = [i[0] for i in ylocs]
    costc, costa = Compute_Cost(costlocx, costlocy, rr, hh, ro, rated, Cp,
                                depth, yrs, WCOE, availability,
                                distance_to_shore)
    if extra:
        power, windspeeds = Compute_Wake(xlocs, ylocs, rr, hh, z0, U0, probwui,
                                         Zref, alphah, ro, aif, farm_y, cut_in,
                                         rated, cut_out, Cp, availability,
                                         nwp, extra)
        tot_power = 0.
        for i in power:
            tot_power += sum(i)
        profit = tot_power * 8760. * yrs * WCOE - (costc + costa)
        return profit, power, windspeeds, (costc + costa)
    else:
        power = Compute_Wake(xlocs, ylocs, rr, hh, z0, U0, probwui,
                             Zref, alphah, ro, aif, farm_y, cut_in,
                             rated, cut_out, Cp, availability,
                             nwp, extra)
        tot_power = 0.
        for i in power:
            tot_power += sum(i)
        profit = -(tot_power * 8760. * yrs * WCOE) + (costc + costa)
        return profit, power


def COP(Compute_Wake, Compute_Cost,
        xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro, aif,
        farm_y, cut_in, rated, cut_out, Cp, availability, nwp, extra,
        depth, yrs, WCOE, distance_to_shore, a):
    """Compute the cost per killowatt of a farm

    Args:
        xlocs: list of x-coordinates of wind turbines at one wind onset angle
        ylocs: list of y-coordinates of wind turbines at one wind onset angle
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        probwui: list of lists for probability of onset wind conditions
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
        depth: water depth in meters (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
    Returns:
        total farm cost
        list of turbine power output by onset angle
        windspeeds: windspeed at each turbine (optional)
        total farm cost (optional)
    """
    costlocx = [i[0] for i in xlocs]
    costlocy = [i[0] for i in ylocs]
    costc, costa = Compute_Cost(costlocx, costlocy, rr, hh, ro, rated, Cp,
                                depth, yrs, WCOE, availability,
                                distance_to_shore)
    if extra:
        power, windspeeds = Compute_Wake(xlocs, ylocs, rr, hh, z0, U0, probwui,
                                         Zref, alphah, ro, aif, farm_y, cut_in,
                                         rated, cut_out, Cp, availability,
                                         nwp, extra)
        tot_power = 0.
        for i in power:
            tot_power += sum(i)
        return (costc + costa) / tot_power, power, windspeeds, (costc + costa)
    else:
        power = Compute_Wake(xlocs, ylocs, rr, hh, z0, U0, probwui,
                             Zref, alphah, ro, aif, farm_y, cut_in,
                             rated, cut_out, Cp, availability,
                             nwp, extra)
        tot_power = 0.
        for i in power:
            tot_power += sum(i)
        return (costc + costa) / tot_power, power


def LCOE(Compute_Wake, Compute_Cost,
         xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro, aif,
         farm_y, cut_in, rated, cut_out, Cp, availability, nwp, extra,
         depth, yrs, WCOE, distance_to_shore, a):
    """Compute the levelized cost of energy of a farm

    Args:
        xlocs: list of x-coordinates of wind turbines at one wind onset angle
        ylocs: list of y-coordinates of wind turbines at one wind onset angle
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        probwui: list of lists for probability of onset wind conditions
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
        depth: water depth in meters (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
    Returns:
        total farm cost
        list of turbine power output by onset angle
        windspeeds: windspeed at each turbine (optional)
        total farm cost (optional)
    """
    costlocx = [i[0] for i in xlocs]
    costlocy = [i[0] for i in ylocs]
    costc, costa = Compute_Cost(costlocx, costlocy, rr, hh, ro, rated, Cp,
                                depth, yrs, WCOE, availability,
                                distance_to_shore)
    if extra:
        power, windspeeds = Compute_Wake(xlocs, ylocs, rr, hh, z0, U0, probwui,
                                         Zref, alphah, ro, aif, farm_y, cut_in,
                                         rated, cut_out, Cp, availability,
                                         nwp, extra)
        tot_power = 0.
        for i in power:
            tot_power += sum(i)
        LCOE = (costc / (a * tot_power * 8760.)
                + costa / (yrs * tot_power * 8760.))
        return LCOE, power, windspeeds, (costc + costa)
    else:
        power = Compute_Wake(xlocs, ylocs, rr, hh, z0, U0, probwui,
                             Zref, alphah, ro, aif, farm_y, cut_in,
                             rated, cut_out, Cp, availability,
                             nwp, extra)
        tot_power = 0.
        for i in power:
            tot_power += sum(i)
        LCOE = (costc / (a * tot_power * 8760.)
                + costa / (yrs * tot_power * 8760.))
        return LCOE, power


def AEP(Compute_Wake, Compute_Cost,
        xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro, aif,
        farm_y, cut_in, rated, cut_out, Cp, availability, nwp, extra,
        depth, yrs, WCOE, distance_to_shore, a):
    """Compute the annual energy production of a farm

    Args:
        xlocs: list of x-coordinates of wind turbines at one wind onset angle
        ylocs: list of y-coordinates of wind turbines at one wind onset angle
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        probwui: list of lists for probability of onset wind conditions
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
        depth: water depth in meters (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
    Returns:
        total farm cost
        list of turbine power output by onset angle
        windspeeds: windspeed at each turbine (optional)
        total farm cost (optional)
    """
    if extra:
        power, windspeeds = Compute_Wake(xlocs, ylocs, rr, hh, z0, U0, probwui,
                                         Zref, alphah, ro, aif, farm_y, cut_in,
                                         rated, cut_out, Cp, availability,
                                         nwp, extra)
        tot_power = 0.
        for i in power:
            tot_power += sum(i)
        AEP = -tot_power * 8760.
        costlocx = [i[0] for i in xlocs]
        costlocy = [i[0] for i in ylocs]
        costc, costa = Compute_Cost(costlocx, costlocy, rr, hh, ro, rated, Cp,
                                    depth, yrs, WCOE, availability,
                                    distance_to_shore)
        return AEP, power, windspeeds, (costc, costa)
    else:
        power = Compute_Wake(xlocs, ylocs, rr, hh, z0, U0, probwui,
                             Zref, alphah, ro, aif, farm_y, cut_in,
                             rated, cut_out, Cp, availability,
                             nwp, extra)
        tot_power = 0.
        for i in power:
            tot_power += sum(i)
        AEP = -tot_power * 8760.
        return AEP, power
