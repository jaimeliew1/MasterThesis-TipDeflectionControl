Master Thesis - Active Tip Deflection Control For Wind Turbines
===============================================================

 

This repository contains the Python code used in my Master Thesis titled *Active
Tip Deflection Control For Wind Turbines*. to perform the control design loop.

 

An attempt to describe the content of each folder is presented.

### JaimesThesisModule

Helper modules for the design and analysis in this project. This includes tools
for controller SISO controller design, A framework for generating HAWC2
simulations, a framework for analysing HAWC2 simulation output data, and the
HAWC2-Python interface module.

### Modelling

This folder contains scripts which are used to estimate a linear blade model. In
particular, a transfer function between blade pitching and blade tip deflection
is found using system identification methods.

### Controllers

This folder contains the controller transfer functions designed in this project
as well as some tools for creating the design.

### Preprocessing

This folder contains scripts for generating design load cases in HAWC2. That is,
it generates many HTC files based on a template and some parameters to change.

### Manifests

This folder contains spreadsheets (.csv files) describing the parameters of each
simulation generated in the ‘preprocessing’ folder. It also contains the
template HTC files and some data files from the postprocessing.

 

### Postprocessing

Perhaps better named ‘plots and tables’, this folder contains the scripts to
generate each plot in my thesis report.

The first steps are designing a continuous control transfer function to achieve
performance and robust stability. This takes use of the modelled turbine system
and the measured open loop plant response (the tip deflection spectrum). Uses
configuration information from the ‘configuration’ folder (such as HAWC2 result
directory location, output file format etc).

 

### Chapters

Runs and saves all the figures for a particular chapter in my thesis report.
This is done by running the scripts in ‘Postprocessing’.

### Other

Scripts which don’t have a home in any of the other folders.

 
