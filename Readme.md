Master Thesis - Active Tip Deflection Control For Wind Turbines
===============================================================

 

This repository contains the Python3 code used in my Master Thesis titled [*Active
Tip Deflection Control For Wind Turbines*](https://pdfs.semanticscholar.org/8b67/ea1d7c62821554c0b0b820ed3fe7c762ab0d.pdf). The main external packages required
are Numpy, Scipy and Matplotlib. Anaconda or Miniconda installations of Python3
should suffice.

*Note: This package requires the HAWC2 simulation output data to work. Please
contact me directly to obtain this data.*

An attempt to describe the content of each folder is presented below.

### JaimesThesisModule

Helper modules for the design and analysis in this project. This includes tools
for controller SISO controller design, A framework for generating HAWC2
simulations, a framework for analysing HAWC2 simulation output data, and the
HAWC2-Python interface module.

### Configuration
Contains some important configuration data of this script. Most importantly,
the directory name containing the HAWC2 output data which is necessary to run
the majority of these scripts. Please contact me directly to obtain this data.

### Modelling

This folder contains scripts which are used to estimate a linear blade model. In
particular, a transfer function between blade pitching and blade tip deflection
is found using system identification methods.

Note: Some of the scripts are written in MATLAB in order to use the
SystemIdentification toolbox.

### Controllers

This folder contains the controller transfer functions designed in this project
as well as some tools for creating the controllers.

### Preprocessing

This folder contains scripts for generating design load cases in HAWC2. That is,
it generates many HTC files based on a template and some parameters to change.

### Manifests

This folder contains spreadsheets (.csv files) describing the parameters of each
simulation generated in the ‘preprocessing’ folder. It also contains the
template HTC files and some data files from the postprocessing.

### Postprocessing

Perhaps better named ‘plots and tables’, this folder contains the scripts to
generate each plot in my thesis report. The majority of the project's analysis
is performed in these scripts.

### Chapters

Runs scripts in the 'Postprocessing folder pertaining to particular chapters in
the final report. All figures which have not already been saved are saved in a
Figures folders (not included in this repository to save space).

### Other
Scripts which don’t have a home in any of the other folders.

 
