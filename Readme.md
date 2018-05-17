Master Thesis - Active Tip Deflection Control For Wind Turbines
===============================================================

 

This repository contains the Python code used in my Master Thesis titled *Active
Tip Deflection Control For Wind Turbines*. to perform the control design loop.

 

The first steps are designing a continuous control transfer function to achieve
performance and robust stability. This takes use of the modelled turbine system
and the measured open loop plant response (the tip deflection spectrum).

The second step is to discretise the chosen controller and to save it in a
format which can be understood in HAWC2

The third step is to integrate this controller into a design load case for
HAWC2. This requires generating many simulation .htc files.

The fourth step is to evaulate the output of the simulation to ensure the
controlled system achieves various goals.

The final step is to repeat these steps in an iterative process.
