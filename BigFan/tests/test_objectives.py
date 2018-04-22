# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 11:00:38 2018

@author: Annalise

Unit tests for objectives.py
ME 599 Project - Spring 2018
"""

from BigFan import objectives as obj
from BigFan import cost_models as cm
from BigFan import wake_models as wm


# test Cost
def test_cost_offshore():
    Compute_Wake = wm.PARK_2D
    Compute_Cost = cm.offshore_cost
    xlocs = [[-400.], [-200.], [0.], [200.], [400.]]
    ylocs = [[-40.], [-40.], [-40.], [-40.], [-40.]]
    rr = [40., 40., 40., 40., 40.]
    hh = [80., 80., 80., 80., 80.]
    z0 = 0.005
    U0 = [0., 10.]
    probwui = [[0.5, 0.5]]
    Zref = 80.
    aif = 0.4
    alphah = 0.1
    ro = 1.225
    farm_y = 2000.
    cut_in = 3.
    rated = 10.
    cut_out = 25.
    Cp = 0.5
    availability = 1.
    depth = 200.
    yrs = 20.
    WCOE = 0.1
    distance_to_shore = 0.
    a = 1.
    extra = False
    nwp = False
    power = [[0., 769.6902001294994] for i in range(5)]
    c = (22578013.001942493 + 20478074.51458269)
    assert obj.cost(Compute_Wake, Compute_Cost,
                    xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro,
                    aif, farm_y, cut_in, rated, cut_out, Cp, availability, nwp,
                    extra, depth, yrs, WCOE, distance_to_shore, a) == (c,
                                                                       power)


def tets_cost_onshore():
    Compute_Wake = wm.PARK_2D
    Compute_Cost = cm.onshore_cost
    xlocs = [[-400.], [-200.], [0.], [200.], [400.]]
    ylocs = [[-40.], [-40.], [-40.], [-40.], [-40.]]
    rr = [40., 40., 40., 40., 40.]
    hh = [80., 80., 80., 80., 80.]
    z0 = 0.005
    U0 = [0., 10.]
    probwui = [[0.5, 0.5]]
    Zref = 80.
    aif = 0.4
    alphah = 0.1
    ro = 1.225
    farm_y = 2000.
    cut_in = 3.
    rated = 10.
    cut_out = 25.
    Cp = 0.5
    availability = 1.
    depth = 200.
    yrs = 20.
    WCOE = 0.1
    distance_to_shore = 0.
    a = 1.
    extra = False
    nwp = False
    power = [[0., 769.6902001294994] for i in range(5)]
    c = (46671600.0 + 471974030.7194091)
    assert obj.cost(Compute_Wake, Compute_Cost,
                    xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro,
                    aif, farm_y, cut_in, rated, cut_out, Cp, availability, nwp,
                    extra, depth, yrs, WCOE, distance_to_shore, a) == (c,
                                                                       power)


# Test Profit
def test_profit_offshore():
    Compute_Wake = wm.PARK_2D
    Compute_Cost = cm.offshore_cost
    xlocs = [[-400.], [-200.], [0.], [200.], [400.]]
    ylocs = [[-40.], [-40.], [-40.], [-40.], [-40.]]
    rr = [40., 40., 40., 40., 40.]
    hh = [80., 80., 80., 80., 80.]
    z0 = 0.005
    U0 = [0., 10.]
    probwui = [[0.5, 0.5]]
    Zref = 80.
    aif = 0.4
    alphah = 0.1
    ro = 1.225
    farm_y = 2000.
    cut_in = 3.
    rated = 10.
    cut_out = 25.
    Cp = 0.5
    availability = 1.
    depth = 200.
    yrs = 20.
    WCOE = 0.1
    distance_to_shore = 0.
    a = 1.
    extra = False
    nwp = False
    power = [[0., 769.6902001294994] for i in range(5)]
    tot_power = 0.
    for i in power:
        tot_power += sum(i)
    c = (-(tot_power * yrs * 8760 * WCOE)
         + (22578013.001942493 + 20478074.51458269))
    assert obj.profit(Compute_Wake, Compute_Cost,
                      xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro,
                      aif, farm_y, cut_in, rated, cut_out, Cp, availability,
                      nwp, extra, depth, yrs, WCOE, distance_to_shore,
                      a) == (c, power)


def test_profit_onshore():
    Compute_Wake = wm.PARK_2D
    Compute_Cost = cm.onshore_cost
    xlocs = [[-400.], [-200.], [0.], [200.], [400.]]
    ylocs = [[-40.], [-40.], [-40.], [-40.], [-40.]]
    rr = [40., 40., 40., 40., 40.]
    hh = [80., 80., 80., 80., 80.]
    z0 = 0.005
    U0 = [0., 10.]
    probwui = [[0.5, 0.5]]
    Zref = 80.
    aif = 0.4
    alphah = 0.1
    ro = 1.225
    farm_y = 2000.
    cut_in = 3.
    rated = 10.
    cut_out = 25.
    Cp = 0.5
    availability = 1.
    depth = 200.
    yrs = 20.
    WCOE = 0.1
    distance_to_shore = 0.
    a = 1.
    extra = False
    nwp = False
    power = [[0., 769.6902001294994] for i in range(5)]
    tot_power = 0.
    for i in power:
        tot_power += sum(i)
    c = (-tot_power * yrs * 8760 * WCOE
         + (46671600.0 + 9439480.614388183))
    assert obj.profit(Compute_Wake, Compute_Cost,
                      xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro,
                      aif, farm_y, cut_in, rated, cut_out, Cp, availability,
                      nwp, extra, depth, yrs, WCOE, distance_to_shore,
                      a) == (c, power)


# Test COP
def test_COP_offshore():
    Compute_Wake = wm.PARK_2D
    Compute_Cost = cm.offshore_cost
    xlocs = [[-400.], [-200.], [0.], [200.], [400.]]
    ylocs = [[-40.], [-40.], [-40.], [-40.], [-40.]]
    rr = [40., 40., 40., 40., 40.]
    hh = [80., 80., 80., 80., 80.]
    z0 = 0.005
    U0 = [0., 10.]
    probwui = [[0.5, 0.5]]
    Zref = 80.
    aif = 0.4
    alphah = 0.1
    ro = 1.225
    farm_y = 2000.
    cut_in = 3.
    rated = 10.
    cut_out = 25.
    Cp = 0.5
    availability = 1.
    depth = 200.
    yrs = 20.
    WCOE = 0.1
    distance_to_shore = 0.
    a = 1.
    extra = False
    nwp = False
    power = [[0., 769.6902001294994] for i in range(5)]
    tot_power = 0.
    for i in power:
        tot_power += sum(i)
    c = (22578013.001942493 + 20478074.51458269) / tot_power
    assert obj.COP(Compute_Wake, Compute_Cost,
                   xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro,
                   aif, farm_y, cut_in, rated, cut_out, Cp, availability, nwp,
                   extra, depth, yrs, WCOE, distance_to_shore, a) == (c, power)


def test_COP_onshore():
    Compute_Wake = wm.PARK_2D
    Compute_Cost = cm.onshore_cost
    xlocs = [[-400.], [-200.], [0.], [200.], [400.]]
    ylocs = [[-40.], [-40.], [-40.], [-40.], [-40.]]
    rr = [40., 40., 40., 40., 40.]
    hh = [80., 80., 80., 80., 80.]
    z0 = 0.005
    U0 = [0., 10.]
    probwui = [[0.5, 0.5]]
    Zref = 80.
    aif = 0.4
    alphah = 0.1
    ro = 1.225
    farm_y = 2000.
    cut_in = 3.
    rated = 10.
    cut_out = 25.
    Cp = 0.5
    availability = 1.
    depth = 200.
    yrs = 20.
    WCOE = 0.1
    distance_to_shore = 0.
    a = 1.
    extra = False
    nwp = False
    power = [[0., 769.6902001294994] for i in range(5)]
    tot_power = 0.
    for i in power:
        tot_power += sum(i)
    c = (46671600.0 + 9439480.614388183) / tot_power
    assert obj.COP(Compute_Wake, Compute_Cost,
                   xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro,
                   aif, farm_y, cut_in, rated, cut_out, Cp, availability,
                   nwp, extra, depth, yrs, WCOE, distance_to_shore,
                   a) == (c, power)


# Test LCOE
def test_LCOE_offshore():
    Compute_Wake = wm.PARK_2D
    Compute_Cost = cm.offshore_cost
    xlocs = [[-400.], [-200.], [0.], [200.], [400.]]
    ylocs = [[-40.], [-40.], [-40.], [-40.], [-40.]]
    rr = [40., 40., 40., 40., 40.]
    hh = [80., 80., 80., 80., 80.]
    z0 = 0.005
    U0 = [0., 10.]
    probwui = [[0.5, 0.5]]
    Zref = 80.
    aif = 0.4
    alphah = 0.1
    ro = 1.225
    farm_y = 2000.
    cut_in = 3.
    rated = 10.
    cut_out = 25.
    Cp = 0.5
    availability = 1.
    depth = 200.
    yrs = 20.
    WCOE = 0.1
    distance_to_shore = 0.
    a = 1.
    extra = False
    nwp = False
    power = [[0., 769.6902001294994] for i in range(5)]
    c = (22578013.001942493 + 20478074.51458269)
    tot_energy = 0.
    for i in power:
        tot_energy += sum(i) * 8760
    c = (22578013.001942493 / (a * tot_energy)
         + 20478074.51458269 / (tot_energy * yrs))
    assert obj.LCOE(Compute_Wake, Compute_Cost,
                    xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro,
                    aif, farm_y, cut_in, rated, cut_out, Cp, availability, nwp,
                    extra, depth, yrs, WCOE, distance_to_shore, a) == (c,
                                                                       power)


def test_LCOE_onshore():
    Compute_Wake = wm.PARK_2D
    Compute_Cost = cm.onshore_cost
    xlocs = [[-400.], [-200.], [0.], [200.], [400.]]
    ylocs = [[-40.], [-40.], [-40.], [-40.], [-40.]]
    rr = [40., 40., 40., 40., 40.]
    hh = [80., 80., 80., 80., 80.]
    z0 = 0.005
    U0 = [0., 10.]
    probwui = [[0.5, 0.5]]
    Zref = 80.
    aif = 0.4
    alphah = 0.1
    ro = 1.225
    farm_y = 2000.
    cut_in = 3.
    rated = 10.
    cut_out = 25.
    Cp = 0.5
    availability = 1.
    depth = 200.
    yrs = 20.
    WCOE = 0.1
    distance_to_shore = 0.
    a = 1.
    extra = False
    nwp = False
    power = [[0., 769.6902001294994] for i in range(5)]
    tot_e = 0.
    for i in power:
        tot_e += sum(i) * 8760.
    c = 46671600.0 / (tot_e * a) + 9439480.614388183 / (yrs * tot_e)
    assert obj.LCOE(Compute_Wake, Compute_Cost,
                    xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro,
                    aif, farm_y, cut_in, rated, cut_out, Cp, availability,
                    nwp, extra, depth, yrs, WCOE, distance_to_shore,
                    a) == (c, power)


# Test AEP
def test_AEP_offshore():
    Compute_Wake = wm.PARK_2D
    Compute_Cost = cm.offshore_cost
    xlocs = [[-400.], [-200.], [0.], [200.], [400.]]
    ylocs = [[-40.], [-40.], [-40.], [-40.], [-40.]]
    rr = [40., 40., 40., 40., 40.]
    hh = [80., 80., 80., 80., 80.]
    z0 = 0.005
    U0 = [0., 10.]
    probwui = [[0.5, 0.5]]
    Zref = 80.
    aif = 0.4
    alphah = 0.1
    ro = 1.225
    farm_y = 2000.
    cut_in = 3.
    rated = 10.
    cut_out = 25.
    Cp = 0.5
    availability = 1.
    depth = 200.
    yrs = 20.
    WCOE = 0.1
    distance_to_shore = 0.
    a = 1.
    extra = False
    nwp = False
    power = [[0., 769.6902001294994] for i in range(5)]
    # c = (22578013.001942493 + 20478074.51458269)
    tot_e = 0.
    for i in power:
        tot_e += sum(i) * 8760
    assert obj.AEP(Compute_Wake, Compute_Cost,
                   xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro,
                   aif, farm_y, cut_in, rated, cut_out, Cp, availability, nwp,
                   extra, depth, yrs, WCOE, distance_to_shore, a) == (-tot_e,
                                                                      power)


def test_AEP_onshore():
    Compute_Wake = wm.PARK_2D
    Compute_Cost = cm.onshore_cost
    xlocs = [[-400.], [-200.], [0.], [200.], [400.]]
    ylocs = [[-40.], [-40.], [-40.], [-40.], [-40.]]
    rr = [40., 40., 40., 40., 40.]
    hh = [80., 80., 80., 80., 80.]
    z0 = 0.005
    U0 = [0., 10.]
    probwui = [[0.5, 0.5]]
    Zref = 80.
    aif = 0.4
    alphah = 0.1
    ro = 1.225
    farm_y = 2000.
    cut_in = 3.
    rated = 10.
    cut_out = 25.
    Cp = 0.5
    availability = 1.
    depth = 200.
    yrs = 20.
    WCOE = 0.1
    distance_to_shore = 0.
    a = 1.
    extra = False
    nwp = False
    power = [[0., 769.6902001294994] for i in range(5)]
    tot_e = 0.
    for i in power:
        tot_e += sum(i) * 8760.
    # c = (46671600.0 + 9439480.614388183))
    assert obj.AEP(Compute_Wake, Compute_Cost,
                   xlocs, ylocs, rr, hh, z0, U0, probwui, Zref, alphah, ro,
                   aif, farm_y, cut_in, rated, cut_out, Cp, availability,
                   nwp, extra, depth, yrs, WCOE, distance_to_shore,
                   a) == (-tot_e, power)


if __name__ == '__main__':
    pass
