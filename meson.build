# I don't know why this is needed, as I define the most relevant info in the
#  pyproject.toml file
project('pyDISORT', 'c',
  meson_version: '>=1.5.0',
)

# Tell meson that it needs to find a FORTRAN compiler
add_languages('fortran')

# Tell meson to find the correct Python installation
py_mod = import('python')
py = py_mod.find_installation(pure: false)
py_dep = py.dependency()

# Do the f2py module build
run_command(py, '-m numpy.f2py *.f -m disort')

# Tell meson that it needs to know about numpy (I don't know why this is
#  necessary, but the numpy docs suggest it is)
incdir_numpy = run_command(py,
  ['-c', 'import os; os.chdir(".."); import numpy; print(numpy.get_include())'],
  check : true
).stdout().strip()

incdir_f2py = run_command(py,
    ['-c', 'import os; os.chdir(".."); import numpy.f2py; print(numpy.f2py.get_include())'],
    check : true
).stdout().strip()

inc_np = include_directories(incdir_numpy, incdir_f2py)

# Tell meson what .f files are needed for its build
disort_source = custom_target('disortmodule.c',
  input : ['BDREF.f', 'DISOBRDF.f', 'DISORT.f', 'ERRPACK.f', 'LAPACK.f', 'LINPAK.f', 'RDI1MACH.f'],
  output : ['disortmodule.c', 'disort-f2pywrappers.f'],
  command : [py, '-m', 'numpy.f2py', '@INPUT@', '-m', 'disort', '--lower']
)

# Tell meson to compile the .f files into a .so file
py.extension_module('disort',
  ['BDREF.f', 'DISOBRDF.f', 'DISORT.f', 'ERRPACK.f', 'LAPACK.f', 'LINPAK.f', 'RDI1MACH.f', disort_source],
  incdir_f2py / 'fortranobject.c',
  include_directories: inc_np,
  dependencies : py_dep,
  install : true,
)
