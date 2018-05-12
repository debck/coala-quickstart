#!/usr/bin/env python3

import locale
import platform
import sys
from subprocess import call

import setuptools.command.build_py
from setuptools import find_packages, setup
from setuptools.command.test import test as TestCommand

try:
    lc = locale.getlocale()
    pf = platform.system()
    if pf != 'Windows' and lc == (None, None):
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
except (ValueError, UnicodeError):
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

VERSION = '0.4.0'


class PyTestCommand(TestCommand):
    """
    From https://pytest.org/latest/goodpractices.html
    """
    user_options = [('pytest-args=', 'a', 'Arguments to pass to py.test')]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.pytest_args = []

    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.pytest_args)
        sys.exit(errno)


class BuildDocsCommand(setuptools.command.build_py.build_py):
    apidoc_command = (
        'sphinx-apidoc', '-f', '-o', 'docs',
        'coala_quickstart'
    )
    make_command = ('make', '-C', 'docs', 'html', 'SPHINXOPTS=-W')

    def run(self):
        err_no = call(self.apidoc_command)
        if not err_no:
            err_no = call(self.make_command)
        sys.exit(err_no)


with open('requirements.txt') as requirements:
    required = requirements.read().splitlines()

with open('test-requirements.txt') as requirements:
    test_required = requirements.read().splitlines()

with open('README.rst') as readme:
    long_description = readme.read()

extras_require = None
data_files = None

if __name__ == '__main__':
    setup(name='coala-quickstart',
          version=VERSION,
          description='A quickstart tool for coala',
          author='The coala developers',
          author_email='coala.analyzer@gmail.com',
          maintainer='Satwik Kansal, Adrian Zatreanu, Alexandros Dimos, Adhityaa Chandrasekar',
          maintainer_email=('satwikkansal@gmail.com, '
                            'adrianzatreanu1@gmail.com, '
                            'alexandros.dimos.95@gmail.com, '
                            'c.adhityaa@gmail.com'),
          url='https://github.com/coala/coala-quickstart',
          platforms='any',
          packages=find_packages(exclude=('build.*', 'tests', 'tests.*')),
          install_requires=required,
          extras_require=extras_require,
          tests_require=test_required,
          package_data={'coala_quickstart': ['VERSION']},
          license='AGPL-3.0',
          data_files=data_files,
          long_description=long_description,
          entry_points={
              'console_scripts': [
                  'coala-quickstart = coala_quickstart.coala_quickstart:main',
              ],
          },
          # from http://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=[
              'Development Status :: 4 - Beta',

              'Environment :: Console',
              'Environment :: MacOS X',
              'Environment :: Win32 (MS Windows)',
              'Environment :: X11 Applications :: Gnome',

              'Intended Audience :: Science/Research',
              'Intended Audience :: Developers',

              'License :: OSI Approved :: GNU Affero General Public License '
              'v3 or later (AGPLv3+)',

              'Operating System :: OS Independent',

              'Programming Language :: Python :: Implementation :: CPython',
              'Programming Language :: Python :: 3.4',
              'Programming Language :: Python :: 3.5',
              'Programming Language :: Python :: 3 :: Only',

              'Topic :: Scientific/Engineering :: Information Analysis',
              'Topic :: Software Development :: Quality Assurance',
              'Topic :: Text Processing :: Linguistic'],
          cmdclass={'docs': BuildDocsCommand,
                    'test': PyTestCommand})
