.. Netshape documentation master file, created by
   sphinx-quickstart on Wed Oct 19 00:13:19 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Netshape
====================================

Quickstart
------------------------------------

:code:`netshape` is a versatile tool designed to build interactive, browser-based,
and deployable visualizations of networks. This enables a more collaborative and more informative visualization process.

With :code:`netshape`, a network edgelist is turned into a web-ready interactive visualization with just one command, and we can view that visualization with just a few more:

.. code-block:: bash

   > netshape build AwesomeNetwork.csv
   > cd dist
   > netshape server
   > echo "let the visualization begin"


Netshape is also highly configurable and hackable; it supports custom commands,
which enables the development of complex visualization pipelines.

Dependencies
~~~~~

Before installing, ensure that python is installed on your computer.

Installation
~~~~~

Once the dependencies have been installed, in order to install :code:`netshape`, simply run:

.. code-block:: bash

   > git clone https://github.com/m-smith/netshape
   > cd netshape
   > make install

.. toctree::
   :maxdepth: 2
