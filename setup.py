import sys
from setuptools import setup

INSTALL_REQUIRES = ['numpy', 'networkx', 'python-louvain', 'pystache']
if sys.version_info[0] <= 2 and sys.version_info[1] < 7:
    INSTALL_REQUIRES.append('argparse>=1.2.1')


setup(name='netshape',
      version='0.0.1',
      packages=['netshape'],
      package_dir={'netshape': 'src/netshape'},
      package_data={'netshape': ['tpl/*']},
      include_package_data=True,
      INSTALL_REQUIRES=INSTALL_REQUIRES,
      entry_points={
          'console_scripts':['netshape=netshape.cli:parse_args']
      }
     )
