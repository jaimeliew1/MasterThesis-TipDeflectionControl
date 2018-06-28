This folder contains the scripts which generate the controllers used in this
project. Each script generates a continuous transfer function describing the
controller dynamics. ControllerEvaluation script is used to analyse each
controller. The IPCPI, IPC04 and IPC07 are the main controllers used in this
project.

 

Single frequency controllers
----------------------------

IPC04, IPC09, IPC10, IPC11 controllers are used to target 1P, 2P, 3P and 4P
oscillations respectively.

Two frequency controllers
-------------------------

From the analysis of the single frequency controllers, a hybrid controller is
made. The IPC07 controller targets 1P and 2P frequencies (in the rotating
frame).

 

IPC08 is the same controller modified to target the same frequencies at minimum
rotor speed. It did not work very well.

 

Other
-----

IPC05 targets 1P, 2P and 4P frequencies.

 

IPC06 targets 1P and 2P frequencies for 10m/s wind speed operation. This
controllerwas not used at all and can be removed.
