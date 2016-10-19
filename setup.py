import sys
from setuptools import setup

INSTALL_REQUIRES = ['numpy', 'networkx', 'python-louvain', 'pystache']

setup(name='netshape',
      version='0.0.1',
      packages=['netshape'],
      package_dir={'netshape': 'src/netshape'},
      package_data={'netshape': ['tpl/*']},
      include_package_data=True,
      install_requires= INSTALL_REQUIRES,
      entry_points={
          'console_scripts':['netshape=netshape.cli:parse_args']
      }
     )
