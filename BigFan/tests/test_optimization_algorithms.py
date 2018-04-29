# -*- coding: utf-8 -*-
"""
Created on Sun Apr 29 15:45:57 2018

@author: Annalise

Unit tests for optimization_algorithms.py
ME 599 Project - Spring 2018
"""

from .. import optimization_algorithms as op_al

# test Cost
def test_check_interference():
    xlocation = [0., 200., -100.]
    ylocation = [0., 200., 100.]
    index = 1
    turb_sep = 200.
    exp_val = op_al.Check_Interference(xlocation, ylocation, index, turb_sep)
    assert exp_val == False
    turb_sep = 300.
    exp_val = op_al.Check_Interference(xlocation, ylocation, index, turb_sep)
    assert exp_val == True