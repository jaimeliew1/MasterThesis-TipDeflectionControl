HAWC2 design load case (DLC) generator files. See PreProc_dlc_template.py to see
how you can use the script to generate your own HAWC2 input files. The DLCs are
described below. They are based in IEC 64100.

 

Normal Turbulence Model (DLC11)
-------------------------------

### DLC11 0

Benchmark simulations without IPC (just the standard wind turbine controller).

### DLC11 1

Simulations with tip deflection based IPC (including PI, single frequency
controllers, two frequency controller, and some others)

### DLC11 2

Although you can’t see it in this branch, this DLC is for IPC using STRAIN
GAUGES instead of tip deflection sensors.

### DLC11 3

Simulations with tip deflection based IPC and tip trajectory tracking.

 

Extreme Turbulence Model (DLC13)
--------------------------------

### DLC13 0

Benchmark simulations without IPC.

### DLC13 1

Simulations with tip deflection based IPC

 

Inverse Shear (DLC15)
---------------------

### DLC15 0

Benchmark simulations without IPC.

### DLC15 1

Simulations with tip deflection based IPC

### DLC15 2

Simulations with tip deflection based IPC and tip trajectory tracking.
