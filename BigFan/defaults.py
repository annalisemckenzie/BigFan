# -*- coding: utf-8 -*-
"""
Created on Wed Apr 18 17:07:59 2018

@author: Annalise
ME 599 Project
Spring 2018
Default input Values
"""

from objectives import LCOE
from wake_models import PARK_3D
from cost_models import offshore_cost

# Default turbine locations and settings
YLocations = [[(i % 10) * 200.] for i in range(10)]
XLocations = [[int(i / 10) * 1000.] for i in range(10)]
rr = [77. / 2. for i in range(10)]
hh = [80. for i in range(10)]
aif = 0.314
farm_x = 2000.  # length of farm in crosswind dierection
farm_y = 2000.  # length of farm in downwind direction
cut_in = 3.5  # m/s - default GE 1.5 sle turbine
rated = 12  # m/s - default GE 1.5 sle turbine
cut_out = 25  # m/s - default GE 1.5 sle turbine
Cp = 0.5
availability = 0.95  # common assumption for turbine availability
depth = 200.  # ocean depth (m)
yrs = 20.  # farm life (years)
WCOE = 0.1  # electrical price per kilowatt-hour
distance_to_shore = 32.  # distance to shore (length of export cable) - km
turb_sep = 200.  # minimum turbine separation distance (m)
directions = [0.]  # onset angle in degrees

# Default environmental variables
shore = 'off'  # default to offshore
if shore == 'off':
    z0 = 0.0005  # surface roughness (m)
elif shore == 'on':
    z0 = 0.05
U0 = [10.]  # constant speed conditions
probwui = [[1.]]  # unidirectional, constant speed conditions
Zref = hh[0]  # reference height is at hub height
condition = 'NEUTRAL'
if condition == "NEUTRAL":
    APow = 0.08835  # Neutral Conditions: WDC(h) = APow*h^BPow
    BPow = -0.1521
    if shore == 'off':
        alphah = 0.11  # Power Law Exponent (averaged over seasons)
    elif shore == 'on':
        alphah = 0.15567  # Power Law Exponent (averaged over seasons)

elif condition == "STABLE":
    APow = 0.07535
    BPow = -0.1496
    alphah = 0.14

elif condition == "UNSTABLE":
    APow = 0.09759
    BPow = -0.1352
    alphah = 0.08
ro = 1.225  # air density (kg/m^3)
nwp = False
extra = False

# Optimization Defaults
a = 17.19  # annuity factor for 1.5% interest rate
# (US Fed Reserve rate Jan 2018)
Eval_Objective = LCOE
Compute_Wake = PARK_3D
Compute_Cost = offshore_cost
# EPS
num_pops = 5  # number of turbines popped
max_pop_tries = 1000  # number of popping attempts per turbine
init_step = 400.  # initial step-size (m)
minstep = 5.  # minimum step size (m)
# GA
mesh_size = 5  # mesh size (m)
elite = 0.1  # percent of best scoring adults kept from last generation
mateable_range = 0.8  # percent of best scoring adults allowed to mate
mutation_rate = 0.05  # percent of chromosomes subject to random mutation
population_size = 100  # number of layouts in each generation/swarm
# GA/PSO
generations_to_converge = 100  # number of generations with same best layout
# before GA/PSO considered converged
# PSO
self_weight = 0.001
global_weight = 0.001
swarm_size = 100  # same as population size but for pso
initial_num = 30.
constraint_scale = 0.5  # I haven't found the best value for this
