from setuptools import setup, find_packages, Extension, Command
try:
    from Cython.Build import cythonize
except ImportError:
    raise ImportError("Having Cython installed is required")
import os

__author__ = "Dario Balboni"
__email__ = "dario.balboni.96+gepy@gmail.com"
__copyright__ = "Copyright 2018 Dario Balboni"
__license__ = "GPLv3"
__status__ = "development"
__version__ = "0.2"

projectName = "gepy"
shortDescription = "Generative Expression Programming for Python"
longDescription = """
TODO
"""

def find_file_by_extension(path='.', ext='.pyx'):
    files = []
    for root, dirs, filenames in os.walk(path):
        for fname in filenames:
            if fname.endswith(ext):
                files.append(os.path.join(root, fname))
    return files

def find_directories(path='.', names=None):
    directories = []
    if names is not None and isinstance(names, list):
        for root, dirs, filenames in os.walk(path):
            if len(dirs) > 0 and dirs[0] in names:
                dname = "%s/%s" % (root, dirs[0])
                if not dname in directories:
                    directories.append(dname)
    return directories


def find_pyx(path='.'):
    return find_file_by_extension(path, ext='.pyx')

def find_py(path='.'):
    return find_file_by_extension(path, ext='.py')

def find_so(path='.'):
    return find_file_by_extension(path, ext='.so')

# FIXME: it is call in all commands, even when 'clean'
def build_extension():
    """
        This method can be simply:
        return cythonize(find_pyx(), language_level=3)
        But, this way we will be able to add libraries and includes for each
        of the files if need be.
    """
    extensions = []
    files = find_pyx() + find_py()
    for file in files:
        source = cythonize(file)
        extensions += source
    return extensions


class CleanCommand(Command):
    """Modify the clean command to remove the cythonized files."""
    user_options = []

    def initialize_options(self):
         pass

    def finalize_options(self):
        pass

    def run(self):
        sources = ['./build', './*.egg-info']
        files = []
        for fileName in find_pyx():
            files.append(fileName.replace('.pyx', '.c'))
        for soFile in find_so():
            files.append(soFile)
        for pyc in find_file_by_extension(ext='.pyc'):
            files.append(pyc)
        for file in files:
            os.system('rm -vrf %s' % file)
        for directory in find_directories(names=['__pycache__']):
            os.system('rm -vrf %s' % directory)

cmdclass = {}
cmdclass.update({'clean': CleanCommand})

setup(
    name=projectName,
    version=__version__,
    license=__license__,
    description=shortDescription,
    long_description=longDescription,
    author=__author__,
    author_email=__email__,
    setup_requires=['cython'],
    ext_modules=build_extension(),
    cmdclass=cmdclass,
    packages=find_packages(),
)
