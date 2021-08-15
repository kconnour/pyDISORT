from pathlib import Path
import setuptools
from numpy import f2py


class DISORT:
    """A class to hold the DISORT source code and operate on it.

    This class finds the DISORT source code on this computer and provides
    methods for compiling it into .so files.

    """

    def __init__(self):
        self._source_dirname = 'disort4.0.99'
        self._source_path = self._get_source_code_path()
        self._modules = ['BDREF.f', 'DISOBRDF.f', 'ERRPACK.f', 'LAPACK.f',
                         'LINPAK.f', 'RDI1MACH.f']

    def _get_source_code_path(self) -> Path:
        project_path = Path(__file__).parent
        return project_path.joinpath(self._source_dirname)

    def compile_disort_into_binary_file(self, name: str = 'disort') -> None:
        """Compile the entire DISORT distribution into a single .so file.

        Parameters
        ----------
        name
            The name to call the importable .so file.

        Notes
        -----
        All subroutines within all modules will be callable from the top level
        namespace of the resultant file. For instance, the first subroutine
        in LAPACK.f is DGEMM. If :code:`name=='disort'` and the resultant file
        is imported, this subroutine can be called via :code:`disort.dgemm()`.

        """
        mod_paths = self._make_relative_module_paths()
        disort_file = self._source_path.joinpath('DISORT.f')
        with open(disort_file) as disort:
            f2py.compile(disort.read(), modulename=name, extra_args=mod_paths)

    def _make_relative_module_paths(self) -> list[Path]:
        return [Path(self._source_dirname).joinpath(m) for m in self._modules]


if __name__ == '__main__':
    d = DISORT()
    d.compile_disort_into_binary_file()
    setuptools.setup()
    # If no python package is present, the install fails
