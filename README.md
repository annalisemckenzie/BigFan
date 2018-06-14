## BigFan [![Build Status](https://travis-ci.org/SoftwareDevEngResearch/BigFan.svg?branch=master)](https://travis-ci.org/SoftwareDevEngResearch/BigFan)
Welcome to BigFan, a program for wind farm optimization and Analysis!

# Interacting with BigFan
There are two ways to interact with BigFan
1) enter the file BigFan/bigfan and open the inputs.csv file
   supply the requested variables and settings for analysis or optimization
   open a new python script:
	import bigfan
	bigfan.main.set_up_csv(<path_to_inputs.csv>)
   run the python script

2) Use the documentation for each function within the modules of BigFan to create your own analysis

# BigFan Outputs
Outputs from the inputs.csv apprach:
   BigFan_Output.txt :: a file containing a summary of input parameters as well as the results of analysis
   output_layout.png :: a figure file plotting the final location of turbines in the field

# BigFan File Structure
bigfan
|-- __init__.py
|-- _version.py
|-- cost_models.py
|-- main.py
|-- inputs.csv
|-- objectives.py
|-- optimization_algorithms.py
|-- wake_models.py
|-- tests
|  |-- __init__.py
|  |-- test_cost_models.py
|  |-- test_objectives.py
|  |-- test_optimization_algorithms.py
|  |-- test_wake_models.py


## Functions in BigFan (by module)

# cost_models.py
*offshore_cost*:Compute Cost of Farm using Forinash offshore cost model
    Args:
        xlocs: list of x-coordinates of wind turbines at one wind onset angle
        ylocs: list of y-coordinates of wind turbines at one wind onset angle
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        ro: air density (float)
        Uref: ambient wind speed (float)
        Cp: power coefficient (float)
        depth: water depth in meters (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        availability: turbine availability (float)
        distance_to_shore: distance from farm to shore (float)
    Returns:
        costc: capital costs of farm
        costa: cumulative annual farm costs

*closest*:Find the closest turbines to a given turbine for use in minimum spanning
        tree
    Args:
        j: index of turbine in question
        xlocs: list of x-coordinates of wind turbines at one wind onset angle
        ylocs: list of y-coordinates of wind turbines at one wind onset angle
        hood_size: number of closest turbines to return
    Returns:
        closest: ordered lost of closest turbines and the distance between them

*calcicl*: Compute the minimum distance to connect all turbines in a farm
    Args:
        xlocs: list of x-coordinates of wind turbines at one wind onset angle
        ylocs: list of y-coordinates of wind turbines at one wind onset angle
    Returns:
        icl: required array cable length
        networks: turbine connections to achieve minimum spanning tree

*onshore_cost*: Compute Cost of Farm using DuPont onshore cost surface derived from
        JEDI model

    Args:
        xlocs: list of x-coordinates of wind turbines at one wind onset angle
        ylocs: list of y-coordinates of wind turbines at one wind onset angle
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        ro: air density (float)
        Uref: ambient wind speed (float)
        Cp: power coefficient (float)
        depth: water depth in meters (float) - not used
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        availability: turbine availability (float)
        distance_to_shore: distance from farm to shore (float) - not used
    Returns:
        costc: capital costs of farm
        costa: cumulative annual farm costs

# main.py
*set_up_csv* :: runs wind farm analysis using the inputs.csv file inputs
  inputs: 
    path: path to inputs.csv file
  outputs:
    BigFan_Output.txt: output text file summarizing input information and model results
    output_layout.png: output figure file showing turbine locations

# objectives.py
*cost*: Compute the total cost of a farm

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
        Ct: thrust coefficient
        rad2: radius around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
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

*profit*: Compute the lifetime profit of a farm

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
        Ct: thrust coefficient
        rad2: radius around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
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

*COP*: Compute the cost per killowatt of a farm

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
        Ct: thrust coefficient
        rad2: radius around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
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

*LCOE*: Compute the levelized cost of energy of a farm

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
        Ct: thrust coefficient
        rad2: radius around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
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

*AEP*: Compute the annual energy production of a farm

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
        Ct: thrust coefficient
        rad2: radius around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
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

#optimization_algorithms.py
*Check_Interference*: Check interference between turbines
    Args:
        xlocation: list of x-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        ylocation: list of y-coordinates of wind turbines where each item
            is a list of y-locations for each onset wind angle
        index: index number of turbine being checked for constraint violation
        turbine_sep_distance: required turbine separation distance
    Returns:
        constraint violation flag

*translate_x*: Translate a specific turbine in the x-direction
    Args:
        xlocation: list of x-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        ylocation: list of y-coordinates of wind turbines where each item
            is a list of y-locations for each onset wind angle
        step_size: distance you're moving turbine
        index: index number of turbine
        farm_x: length of farm in the x-direction
        turbine_sep_distance: required turbine separation distance
        directions: onset wind angles
    Returns:
        constraint violation flag
        new turbine xlocations for each onset angle
        new turbine ylocations for each onset angle

*translate_y*: Translate a specific turbine in the y-direction
    Args:
        xlocation: list of x-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        ylocation: list of y-coordinates of wind turbines where each item
            is a list of y-locations for each onset wind angle
        step_size: distance you're moving turbine
        index: index number of turbine
        farm_y: length of farm in the y-direction
        turbine_sep_distance: required turbine separation distance
        directions: onset wind angles
    Returns:
        constraint violation flag
        new turbine xlocations for each onset angle
        new turbine ylocations for each onset angle

*Rand_Vector*: Create random turbine order for EPS
    Args:
        initial_num: number of turbines being optimized
    Returns:
        random order of those turbines

*EPS*:Extended Pattern Search
    Args:
        xlocation: list of x-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        ylocation: list of y-coordinates of wind turbines where each item
            is a list of y-locations for each onset wind angle
        init_step: initial step size for EPS
        minstep: smallest step size for EPS
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        Zref: Wind speed reference height
        alphah: power law exponent
        ro: air density (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        num_pops: number of poor performing turbines popped each round
        max_pop_tries: number of times a single turbine may attempt
            a new location in the popping algorithm
        aif: axial induction factor (float)
        farm_x: length of wind farm in x direction in meters (float)
        farm_y: length of wind farm in y direction in meters (float)
        turb_sep: minimum tubine separation requirement
        Eval_Objective: objective being minimized by EPS
        Compute_Wake: function encapsulating wake model
        Compute_Cost: function encapsulating cost model
        probwui: list of lists for probability of onset wind conditions
            first index represets onset wind direction index
            second index represents onset wind speed index
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        cut_in: turbine cut-in wind speed (float)
        rated: turbine rated wind speed (float)
        cut-out: turbine cut-out speed (float)
        Cp: power coefficient (float)
        availability: turbine availability (float)
        Ct: thrust coefficient
        rad2: number or radii around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
        depth: water depth in meters (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
        directions: list of onset wind angles
    Returns:
        optimized turbine xlocation
        optimized turbine ylocation
        optimized turbine power
        optimized objctive
        Number of objective evaluations until convergence

*EPS_disc*: Discretized Extended Pattern Search

    Args:
        xlocation: list of x-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        ylocation: list of y-coordinates of wind turbines where each item
            is a list of x-locations for each onset wind angle
        init_step: initial step size for EPS
        minstep: smallest step size for EPS
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        Zref: Wind speed reference height
        alphah: power law exponent
        ro: air density (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        num_pops: number of poor performing turbines popped each round
        max_pop_tries: number of times a single turbine may attempt
            a new location in the popping algorithm
        aif: axial induction factor (float)
        farm_x: length of wind farm in x direction in meters (float)
        farm_y: length of wind farm in y direction in meters (float)
        turb_sep: minimum tubine separation requirement
        Eval_Objective: objective being minimized by EPS
        Compute_Wake: function encapsulating wake model
        Compute_Cost: function encapsulating cost model
        probwui: list of lists for probability of onset wind conditions
            first index represets onset wind direction index
            second index represents onset wind speed index
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        cut_in: turbine cut-in wind speed (float)
        rated: turbine rated wind speed (float)
        cut-out: turbine cut-out speed (float)
        Cp: power coefficient (float)
        availability: turbine availability (float)
        Ct: thrust coefficient
        rad2: number or radii around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
        depth: water depth in meters (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
        directions: list of onset wind angles
    Returns:
        optimized turbine xlocation
        optimized turbine ylocation
        optimized turbine power
        optimized objctive
        Number of objective evaluations until convergence

*translate_chromosome*: Translate binary chromosome to cardinal coordinates

    Args:
        chromosome: binary list to be converted to turbine layout
        binary_x: number of binary values in an x-coordinate
        options_x: number of positions a turbine can take in the x-direction
        binary_y: number of binary values in a y-coordinate
        options_y: number of positions a turbine can take in the y-direction
        mesh_size: width of square of mesh
        directions: onset wind angles
    Returns:
        xlocations of chromosome from every onset angle
        ylocations of chromosome from every onset angle

*GA*: Optimize turbine layout using a Genetic Algorithm

    Args:
        mesh_size: width of mesh for GA
        elite: proportion of best chromosomes copied from last generation
        mateable_range: proportion of best chromosomes that are allowed to mate
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        Zref: Wind speed reference height
        alphah: power law exponent
        ro: air density (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        population_size: population size
        generations_to_convergence: number of generations with same best layout
            before algorithm is considered converged
        aif: axial induction factor (float)
        farm_x: length of wind farm in x direction in meters (float)
        farm_y: length of wind farm in y direction in meters (float)
        turb_sep: minimum tubine separation requirement
        Eval_Objective: objective being minimized by EPS
        Compute_Wake: function encapsulating wake model
        Compute_Cost: function encapsulating cost model
        probwui: list of lists for probability of onset wind conditions
            first index represets onset wind direction index
            second index represents onset wind speed index
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        cut_in: turbine cut-in wind speed (float)
        rated: turbine rated wind speed (float)
        cut-out: turbine cut-out speed (float)
        Cp: power coefficient (float)
        availability: turbine availability (float)
        Ct: thrust coefficient
        rad2: number or radii around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
        depth: water depth in meters (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
        directions: list of onset wind angles
    Returns:
        optimized turbine xlocation
        optimized turbine ylocation
        optimized turbine power
        optimized objctive
        Number of objective evaluations until convergence

*PSO*: Optimize farm layout using a particle swarm optimization
    Args:
        self_weight: weight given to individual's best past evaluation
        global_weight: weight given to the swarm's best past evaulation
        swarm_size: number of individuals in the swarm
        initial_num: number of turbines being optimized
        farm_x: length of wind farm in x direction in meters (float)
        farm_y: length of wind farm in y direction in meters (float)
        turb_sep: minimum tubine separation requirement
        generations_to_converge: number of generations without improvement
            before algorithm is considered converged
        Eval_Objective: objective being minimized by EPS
        constraint_scale: the weight given to constraint violations in
            calculating the objective evaluation
        z0: wind farm surface roughness in meters (float)
        U0: list of onset wind speeds in m/s
        Zref: Wind speed reference height
        alphah: power law exponent
        ro: air density (float)
        aif: axial induction factor (float)
        yrs: lifetime of wind farm in years (float)
        WCOE: wholesale cost of energy in USD per killowatt-hour (float)
        Compute_Wake: function encapsulating wake model
        Compute_Cost: function encapsulating cost model
        probwui: list of lists for probability of onset wind conditions
            first index represets onset wind direction index
            second index represents onset wind speed index
        rr: list of rotor radii for each turbine
        hh: list of hub heights for each turbine
        cut_in: turbine cut-in wind speed (float)
        rated: turbine rated wind speed (float)
        cut-out: turbine cut-out speed (float)
        Cp: power coefficient (float)
        availability: turbine availability (float)
        Ct: thrust coefficient
        rad2: number or radii around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
        depth: water depth in meters (float)
        distance_to_shore: distance from farm to shore (float)
        a: annuity factor (float)
        directions: list of onset wind angles
    Returns:
        optimized turbine xlocation
        optimized turbine ylocation
        optimized turbine power
        optimized objctive
        Number of objective evaluations until convergence

#wake_models.py
*PARK_3D*:Compute the turbine power generation (and optionally turbine wind speed)
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
        Ct: thrust coefficient
        rad2: radius around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
    Returns:
        list of turbine power output by [turbine no.][onset angle index]
        windspeeds: windspeed by [turbine no.][onset angle index] (optional)

*PARK_2D*: Compute the turbine power generation (and optionally turbine wind speed)
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
        Ct: thrust coefficient
        rad2: radius around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
    Returns:
        list of turbine power output by [turbine no.][onset angle index]
        windspeeds: windspeed by [turbine no.][onset angle index] (optional)

*Discretize_RSA*: Discretize rotor swept area of a specific turbine and return x- and z-
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

*create_mesh*: Create farm mesh for use in CFD wind speed calculation

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

*refine_mesh*: Refine farm mesh for use in CFD wind speed calculation

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
        rad2: radius about turbines in which to refine mesh
    Returns:
        wind farm mesh for CFD analysis

*createRotatedTurbineForce*: Use Actuator disc theory to determine the force turbines
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

*mainCFD*: Determine wind speeds across field
    Args:
        tf: turbine force exerted across mesh
        VQ: mixed element functional stuff I don't totally understand
        wind_speed: ambient wind speed
        Lx: length of the extent of the mesh in the x-direction
        Ly: Length of the extent of the mesh in the y-direction
        mlDenom: mixing length denominator
    Returns:
        wind speed and pressure across mesh

*rotatedPowerFunction*: Determine power output by turbine
    Args:
        alpha: wind onset angle
        A: turbine rotor swept area in meters squared (float)
        beta: smoothing kernel
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

*CFD_2D*: Compute the turbine power generation (and optionally turbine wind speed)
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
        Ct: thrust coefficient
        rad2: radius around each turbine to reduce mesh size
        numx: initial number of mesh points in x-direction
        numy: initial number of mesh points in y-direction
        Lx: length of analysis area for CFD in x-direction
        Ly: length of analysis area for CFD in y-direction
        mlDenom: mixing length denominator for CFD
        nwp: whether to use the nested wake provision (True/False)
        extra: whether to provide turbine windspeeds and total cost
            in addition to objective and power output
    Returns:
        list of turbine power output by [turbine no.][onset angle index]
        windspeeds: windspeed by [turbine no.][onset angle index] (optional)