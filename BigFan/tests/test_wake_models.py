# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 11:21:06 2018

@author: Annalise

Unit tests for wake_models.py
ME 599 Project - Spring 2018
"""

import unittest as ut
import wake_models as wm


class Testwake_models(ut.TestCase):
    # test Cost
    def test_Jensen_3D(self):
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
        self.assertEqual(wm.PARK_3D(xlocs, ylocs, rr, hh, z0, U0, probwui,
                                    Zref, alphah, ro, aif, farm_y,
                                    cut_in, rated, cut_out, Cp, availability,
                                    nwp=False, extra=False), power)

        # Test 3 nested with nwp
        xlocs = [[0.], [0.], [0.]]
        ylocs = [[200.], [200.], [200.]]
        hh = [80., 80., 80.]
        rr = [40., 40., 40.]
        power = 12.  # dummy value for now
        self.assertEqual(wm.PARK_3D(xlocs, ylocs, rr, hh, z0, U0, probwui,
                                    Zref, alphah, ro, aif, farm_y,
                                    cut_in, rated, cut_out, Cp, availability,
                                    nwp=False, extra=False), power)

#        # Test 3 in triangle, no overlap
#        xlocs = [[0.], [0.], [0.]]
#        ylocs = [[200.], [200.], [200.]]
#        hh = [80., 80., 80.]
#        rr = [40., 40., 40.]
#        power = 12.  # dummy value for now
#        self.assertEqual(wm.PARK_3D(xlocs, ylocs, rr, hh, z0, U0, probwui,
#                                    Zref, alphah, ro, aif, farm_y,
#                                    cut_in, rated, cut_out, Cp, availability,
#                                    nwp=False, extra=False), power)

#        # Test with windspeed output
#        power = 12.  # dummy value for now
#        self.assertEqual(wm.PARK_3D(xlocs, ylocs, rr, hh, z0, U0, probwui,
#                                    Zref, alphah, ro, aif, farm_x, farm_y,
#                                    cut_in, rated, cut_out, Cp, availability,
#                                    nwp=False, extra=False), power)
#
    def test_Jensen_2D(self):
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
        self.assertEqual(wm.PARK_2D(xlocs, ylocs, rr, hh, z0, U0, probwui,
                                    Zref, alphah, ro, aif, farm_y,
                                    cut_in, rated, cut_out, Cp, availability,
                                    nwp=False, extra=False), power)
#        # Test with nwp
#        power = 12.  # dummy value for now
#        self.assertEqual(wm.PARK_2D(xlocs, ylocs, rr, hh, z0, U0, probwui,
#                                    Zref, alphah, ro, aif, farm_x, farm_y,
#                                    cut_in, rated, cut_out, Cp, availability,
#                                    nwp=False, extra=False), power)
#        # Test with windspeed output
#        power = 12.  # dummy value for now
#        self.assertEqual(wm.PARK_2D(xlocs, ylocs, rr, hh, z0, U0, probwui,
#                                    Zref, alphah, ro, aif, farm_x, farm_y,
#                                    cut_in, rated, cut_out, Cp, availability,
#                                    nwp=False, extra=False), power)

    def test_Discretize_RSA(self):
        # Test negative hub height input
        with self.assertRaises(ValueError):
            wm.Discretize_RSA(0., -3., 40., D2=True)
        # Test negative rotor radius input
        with self.assertRaises(ValueError):
            wm.Discretize_RSA(0., 80., -40., D2=True)
        # Test 2D input (full postive x)
        xcoords = [60., 70., 50., 80., 40., 90., 30., 100., 20.]
        zcoords = [80., 80., 80., 80., 80., 80., 80., 80., 80.]
        self.assertEqual(wm.Discretize_RSA(60., 80., 40., D2=True),
                         (xcoords, zcoords))
        # Test 2D input (mixed negative x)
        xcoords = [20., 30., 10., 40., 0., 50., -10., 60., -20.]
        zcoords = [80., 80., 80., 80., 80., 80., 80., 80., 80.]
        self.assertEqual(wm.Discretize_RSA(20., 80., 40., D2=True),
                         (xcoords, zcoords))

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
        self.assertEqual(wm.Discretize_RSA(20., 80., 40., D2=False),
                         (xcoords, zcoords))


if __name__ == '__main__':
    ut.main()
