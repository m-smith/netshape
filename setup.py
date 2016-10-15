import sys
import os
from setuptools import setup, find_packages

install_requires = ['numpy>=1.1', 'networkx','python-louvain','pystache']
if sys.version_info[0] <= 2 and sys.version_info[1] < 7:
    install_requires.append('argparse>=1.2.1')


setup(name='netshape',
    version = '0.0.1',
    packages=['netshape'],
    package_dir = {'netshape': 'src/netshape'},
    package_data={'netshape': ['tpl/*']},
    include_package_data=True,
    install_requires=install_requires,
    entry_points={
        'console_scripts':['netshape=netshape.cli:parse_args']
    }

)
