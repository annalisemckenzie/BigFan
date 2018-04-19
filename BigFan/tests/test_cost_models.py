# -*- coding: utf-8 -*-
"""
Created on Fri Apr 13 08:57:53 2018

@author: Annalise

Unit tests for cost_models.py
ME 599 Project - Spring 2018
"""

import unittest
import cost_models


class Testcost_models(unittest.TestCase):

    def test_offshore_cost(self):
        xlocs = [0., 100., 0., -100., 0.]
        ylocs = [0., 0., -100., 0., 100.]
        rr = [40.] * len(xlocs)
        hh = [80.] * len(xlocs)
        ro = 1.225
        Uref = 10.
        Cp = 0.4
        depth = 200.
        yrs = 20.
        WCOE = 0.1
        availability = 0.9
        distance_to_shore = 0.
        a = cost_models.offshore_cost(xlocs, ylocs, rr, hh, ro, Uref, Cp,
                                      depth, yrs, WCOE, availability,
                                      distance_to_shore)
        self.assertEqual(a, (20146142.401553992, 16382114.39637511))

    def test_onshore_cost(self):
        xlocs = [0., 100., 0., -100., 0.]
        ylocs = [0., 0., -100., 0., 100.]
        rr = [40.] * len(xlocs)
        hh = [80.] * len(xlocs)
        ro = 1.225
        Uref = 10.
        Cp = 0.4
        depth = 200.
        yrs = 20.
        WCOE = 0.1
        availability = 0.9
        distance_to_shore = 0.
        a = cost_models.onshore_cost(xlocs, ylocs, rr, hh, ro, Uref, Cp, depth,
                                     yrs, WCOE, availability,
                                     distance_to_shore)
        self.assertEqual(a[0], 46671600)
        self.assertEqual(int(a[1]), 339821302)

    def test_calcicl(self):
        xlocs = [0., 100., 0., -100., 0.]
        ylocs = [0., 0., -100., 0., 100.]
        self.assertEqual(cost_models.calcicl(xlocs, ylocs)[0], 0.4)
        xlocs = [3., 4., -3., -4., 0.]
        ylocs = [4., -3., -4., 3., 0.]
        self.assertEqual(cost_models.calcicl(xlocs, ylocs)[0], 20 / 1000.)


if __name__ == '__main__':
    unittest.main()
