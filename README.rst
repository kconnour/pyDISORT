pyDISORT
========
This project is designed to allow you to compile the latest DISORT code into an
importable Python binary file.

Installation
------------
Before installing this project, you must have a FORTRAN compiler installed on
your computer. Once you've done that, you can simply install this package from
Terminal via: ``pip install .``. Then, you can import the package in Python
with: ``import disort``. You can call any of the subroutines used in the DISORT
code from the disort package, but you will most likely be primarily calling the
main algorithm with: ``disort.disort(<50+ args>)``.

During the installation process, numpy's f2py module will compile the DISORT
source files into a single interface file. The meson build backend will then
compile code into an importable .so file. This will make the installation take
slightly longer than a project comprised of bytecode files, but it should be
clearer where source code originates in case you want to make modifications to
the source code to suit your needs.

Modifications
-------------
I made a small number of changes to the DISORT source code, largely to get it
compatible with f2py. These are outlined below.

DISORT.f
~~~~~~~~
* (lines 388--395) I added f2py code to inform it what the output variables
  should be. These are interpreted by fortran as comments so it didn't change
  anything about how the fortran code works.
* (line 435) I modified RHOU's 1st dimension to be MAXCMU instead of MAXUMU.
  This allows DISOBRDF.f to make RHOU.

DISOBRDF.f
~~~~~~~~~~
* (lines 101--105) I added f2py code to inform it what the output variables
  should be. These are interpreted by fortran as comments so it didn't change
  anything about how the fortran code works.
* (line 83) I changed REAL BRDF_ARG(4) to REAL BRDF_ARG(6). This allows me to
  add 6 parameters to custom surface phase functions.

BDREF.f
~~~~~~~
* (line 60) I changed REAL BRDF_ARG(4) to REAL BRDF_ARG(6). This allows me to
  add 6 parameters to a surface phase function.
* (lines 71--72) I added a line at the top REAL ASYM, FRAC, ROUGHNESS to
  accommodate these parameters.
* (lines 157--169) I added ELSEIF (IREF.eq.5) to handle a Hapke HG2 phase
  function.
* (lines 170--183) I added ELSEIF (IREF.eq.6) to handle a Hapke HG2 + surface
  roughness phase function.
* (lines 505 onward) I added the 2 Hapke surface phase functions.

pyRT_DISORT
-----------
This project is usable (and hopefully helpful) as is. However, it is often
beneficial to have helper routines to create a number of the variables needed as
inputs to the main DISORT algorithm. `pyRT_DISORT
<https://github.com/kconnour/pyRT_DISORT>`_ is a companion project to create
those arrays. Check it out if desired.
