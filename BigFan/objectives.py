# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 14:58:46 2018

@author: Annalise Miller

ME 599 Project
Spring 2018
Objective Evaluation Options
"""

# NOTES TO ANNALISE:
#     None


def cost(Compute_Wake, Compute_Cost,
         xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro, aif,
         farm_y, cut_in, rated, cut_out, Cp, availability, nwp, extra,
         depth, yrs, WCOE, distance_to_shore, a):
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
    print('evaluating the objective')
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
