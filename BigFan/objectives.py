# -*- coding: utf-8 -*-
"""
Created on Sat Apr  7 14:58:46 2018

@author: Annalise Miller

ME 599 Project
Spring 2018
Objective Evaluation Options
"""

# NOTES TO ANNALISE:
#     Change inputs to Compute_Wake
#     Change inputs to Compute_Cost


def cost(Compute_Wake, Compute_Cost,
         compute_wake_stuff,
         compute_cost_stuff,
         extra_needed=False):
    costc, costa = Compute_Cost(initial_num, ro, yrs, WCOE, condition, depth)
    if extra_needed:
        power, windspeeds = Compute_Wake(initial_num, z0, U0, Zref, alphah,
                                         ro, aif, True)
        return (costc + costa), power, windspeeds, (costc + costa)
    else:
        power = Compute_Wake(initial_num, z0, U0, Zref, alphah,
                                         ro, aif)
        return (costc + costa), power


def profit(Compute_Wake, Compute_Cost,
           compute_wake_stuff,
           compute_cost_stuff,
           extra_needed=False):
    costc, costa = Compute_Cost(initial_num, ro, yrs, WCOE, condition, depth)
    if extra_needed:
        power, windspeeds = Compute_Wake(initial_num, z0, U0, Zref, alphah,
                                         ro, aif, True)
        profit = power * 8760. * farm_life * WCOE - (costc + costa)
        return profit, power, windspeeds, (costc + costa)
    else:
        power = Compute_Wake(initial_num, z0, U0, Zref, alphah, ro, aif)
        profit = power * 8760. * farm_life * WCOE - (costc + costa)
        return profit, power


def COP(Compute_Wake, Compute_Cost,
        compute_wake_stuff,
        compute_cost_stuff,
        extra_needed=False):
    costc, costa = Compute_Cost(initial_num, ro, yrs, WCOE, condition, depth)
    if extra_needed:
        power, windspeeds = Compute_Wake(initial_num, z0, U0, Zref,
                                         alphah, ro, aif, True)
        return sum(power) / (costc + costa), power, windspeeds, (costc + costa)
    else:
        power = Compute_Wake(initial_num, z0, U0, Zref, alphah, ro, aif)
        return sum(power) / (costc + costa), power


def LCOE(Compute_Wake, Compute_Cost,
         compute_wake_stuff,
         compute_cost_stuff,
         extra_needed=False):
    costc, costa = Compute_Cost(initial_num, ro, yrs, WCOE, condition, depth)
    if extra_needed:
        power, windspeeds = Compute_Wake(initial_num, z0, U0, Zref,
                                         alphah, ro, aif, True)
        LCOE = costc / (a * power * 8760.) + costa / (power * 8760.)
        return LCOE, power, windspeeds, (costc + costa)
    else:
        power = Compute_Wake(initial_num, z0, U0, Zref, alphah, ro, aif)
        LCOE = costc / (a * power * 8760.) + costa / (power * 8760.)
        return LCOE, power


def AEP(Compute_Wake, Compute_Cost,
        compute_wake_stuff,
        compute_cost_stuff,
        extra_needed=False):
    if extra_needed:
        power, windspeeds = Compute_Wake(initial_num, z0, U0, Zref,
                                         alphah, ro, aif, True)
        AEP = power * 8760.
        costc, costa = Compute_Cost(initial_num, ro, yrs, WCOE,
                                    condition, depth)
        return AEP, power, windspeeds, (costc, costa)
    else:
        power = Compute_Wake(initial_num, z0, U0, Zref, alphah, ro, aif)
        AEP = power * 8760.
        return LCOE, power    
