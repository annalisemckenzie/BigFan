# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 11:21:06 2018

@author: Annalise

Unit tests for wake_models.py
ME 599 Project - Spring 2018
"""

import pytest
from .. import wake_models as wm


def test_Jensen_3D():
    # Test without nwp
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
    power = [[0., 769.6902001294994] for i in range(5)]
    assert wm.PARK_3D(xlocs, ylocs, rr, hh, z0, U0, probwui,
                      Zref, alphah, ro, aif, farm_y,
                      cut_in, rated, cut_out, Cp, availability,
                      nwp=False, extra=False) == power

    # Test 3 in triangle, no overlap
    xlocs = [[0.], [80.], [160.]]
    ylocs = [[200.], [300.], [200.]]
    hh = [80., 80., 80.]
    rr = [40., 40., 40.]
    probwui = [[0.5, 0.5]]
    power = [[0., 769.6902001294994], [0., 707.17227660650678],
             [0., 769.6902001294994]]
    assert wm.PARK_3D(xlocs, ylocs, rr, hh, z0, U0, probwui,
                      Zref, alphah, ro, aif, farm_y,
                      cut_in, rated, cut_out, Cp, availability,
                      nwp=False, extra=False) == power

    # Test 3 nested with nwp and windspeed output
    xlocs = [[0., 0.], [0., 0.], [0., 0.]]
    ylocs = [[200., 600.], [400., 400.], [600., 200.]]
    hh = [80., 80., 80.]
    rr = [40., 40., 40.]
    probwui = [[0.25, 0.25], [0.25, 0.25]]
    windspeeds = [[[0., 10.], [0., 3.9414109332807392],
                   [0., 1.5534720144984946]],
                  [[0., 1.5534720144984946], [0., 3.9414109332807392],
                   [0., 10.]]]
    power = [[0.0, 384.8451000647497, 0.0, 0.0],
             [0.0, 23.563571268469847, 0.0, 23.563571268469847],
             [0.0, 0.0, 0.0, 384.8451000647497]]
    assert wm.PARK_3D(xlocs, ylocs, rr, hh, z0, U0, probwui,
                      Zref, alphah, ro, aif, farm_y,
                      cut_in, rated, cut_out, Cp, availability,
                      nwp=True, extra=True) == (power, windspeeds)
    windspeeds = [[[0., 10.], [0., 3.9414109332807392],
                   [0., 2.3048471463211131]],
                  [[0., 2.3048471463211131], [0., 3.9414109332807392],
                   [0., 10.]]]
    power = [[0.0, 384.8451000647497, 0.0, 0.0],
             [0.0, 23.563571268469847, 0.0, 23.563571268469847],
             [0.0, 0.0, 0.0, 384.8451000647497]]
    # Test 3 nested without nwp
    assert wm.PARK_3D(xlocs, ylocs, rr, hh, z0, U0, probwui,
                      Zref, alphah, ro, aif, farm_y,
                      cut_in, rated, cut_out, Cp, availability,
                      nwp=False, extra=True) == (power, windspeeds)


def test_Jensen_2D():
    # Test without nwp
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
    power = [[0., 769.6902001294994] for i in range(5)]
    assert wm.PARK_2D(xlocs, ylocs, rr, hh, z0, U0, probwui,
                      Zref, alphah, ro, aif, farm_y,
                      cut_in, rated, cut_out, Cp, availability,
                      nwp=False, extra=False) == power

    # Test 3 in triangle, no overlap
    xlocs = [[0.], [80.], [160.]]
    ylocs = [[200.], [300.], [200.]]
    hh = [80., 80., 80.]
    rr = [40., 40., 40.]
    probwui = [[0.5, 0.5]]
    power = [[0., 769.6902001294994], [0., 581.03931130427259],
             [0., 769.6902001294994]]
    assert wm.PARK_2D(xlocs, ylocs, rr, hh, z0, U0, probwui,
                      Zref, alphah, ro, aif, farm_y,
                      cut_in, rated, cut_out, Cp, availability,
                      nwp=False, extra=False) == power

    # Test with nwp
    xlocs = [[0., 0.], [0., 0.], [0., 0.]]
    ylocs = [[200., 600.], [400., 400.], [600., 200.]]
    hh = [80., 80., 80.]
    rr = [40., 40., 40.]
    probwui = [[0.25, 0.25], [0.25, 0.25]]
    windspeeds = [[[0., 10.], [0., 3.9414109332807392],
                   [0., 1.5534720144984946]],
                  [[0., 1.5534720144984946], [0., 3.9414109332807392],
                   [0., 10.]]]
    power = [[0.0, 384.8451000647497, 0.0, 0.0],
             [0.0, 23.563571268469847, 0.0, 23.563571268469847],
             [0.0, 0.0, 0.0, 384.8451000647497]]
    assert wm.PARK_2D(xlocs, ylocs, rr, hh, z0, U0, probwui,
                      Zref, alphah, ro, aif, farm_y,
                      cut_in, rated, cut_out, Cp, availability,
                      nwp=True, extra=True) == (power, windspeeds)
    windspeeds = [[[0., 10.], [0., 3.9414109332807392],
                   [0., 2.303332134437631]],
                  [[0., 2.303332134437631], [0., 3.9414109332807392],
                   [0., 10.]]]
    power = [[0.0, 384.8451000647497, 0.0, 0.0],
             [0.0, 23.563571268469847, 0.0, 23.563571268469847],
             [0.0, 0.0, 0.0, 384.8451000647497]]
    # Test 3 nested without nwp
    assert wm.PARK_2D(xlocs, ylocs, rr, hh, z0, U0, probwui,
                      Zref, alphah, ro, aif, farm_y,
                      cut_in, rated, cut_out, Cp, availability,
                      nwp=False, extra=True) == (power, windspeeds)


def test_Discretize_RSA():
    # Test negative hub height input
    with pytest.raises(ValueError):
        wm.Discretize_RSA(0., -3., 40., D2=True)
    # Test negative rotor radius input
    with pytest.raises(ValueError):
        wm.Discretize_RSA(0., 80., -40., D2=True)
    # Test 2D input (full postive x)
    xcoords = [60., 70., 50., 80., 40., 90., 30., 100., 20.]
    zcoords = [80., 80., 80., 80., 80., 80., 80., 80., 80.]
    assert wm.Discretize_RSA(60., 80., 40., D2=True) == (xcoords, zcoords)
    # Test 2D input (mixed negative x)
    xcoords = [20., 30., 10., 40., 0., 50., -10., 60., -20.]
    zcoords = [80., 80., 80., 80., 80., 80., 80., 80., 80.]
    assert wm.Discretize_RSA(20., 80., 40., D2=True) == (xcoords, zcoords)

    # Test 3D input (mixed negative x)
    xcoords = [20., 30., 10., 40., 0., 50., -10., 60., -20.,
               20., 30., 10., 40., 0., 50., -10.,
               20., 30., 10., 40., 0., 50., -10.,
               20., 30., 10., 40., 0., 50., -10.,
               20., 30., 10., 40., 0., 50., -10.,
               20., 30., 10., 40., 0.,
               20., 30., 10., 40., 0.,
               20.,
               20.]
    zcoords = [80., 80., 80., 80., 80., 80., 80., 80., 80.,
               90., 90., 90., 90., 90., 90., 90.,
               70., 70., 70., 70., 70., 70., 70.,
               100., 100., 100., 100., 100., 100., 100.,
               60., 60., 60., 60., 60., 60., 60.,
               110., 110., 110., 110., 110.,
               50., 50., 50., 50., 50.,
               120.,
               40.]
    assert wm.Discretize_RSA(20., 80., 40., D2=False) == (xcoords, zcoords)
