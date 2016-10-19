:tocdepth: 2
.. Netshape documentation master file, created by
   sphinx-quickstart on Wed Oct 19 00:13:19 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Overview
====================================

:code:`netshape` is a versatile command-line tool designed to build interactive, browser-based,
and deployable visualizations of networks. This enables a more collaborative and more informative visualization process.

With :code:`netshape`, a network edgelist is turned into a web-ready interactive visualization with just one command, and we can view that visualization with just a few more:

.. code-block:: bash

   > netshape build AwesomeNetwork.csv
   > cd dist
   > netshape server
   > echo "let the visualization begin"


Netshape is also highly configurable and hackable; it supports custom commands,
which enables the development of complex visualization pipelines.

Key Features
~~~~~~~~~~~~~~~~~

**Web-ready visualization:**
    Building and sharing visualizations of networks can help convey complex
    or technical properties of a network to non-technical users. :code:`netshape` enables
    the instantanious sharing of these visualizations.

**Flexible configuration:**
    :code:`netshape` commands are configured through a  :code:`netshape_conf.py`
    file, which is *just a python file*. This means that any normal python code
    can be included or imported in you visualization pipeline.

Dependencies
~~~~~~~~~~~~~~~~~

Before installing, ensure that python is installed on your computer, and is at
least version 2.7.

Installation
~~~~~~~~~~~~~~~

Once the dependencies have been installed, in order to install :code:`netshape`, simply run:

.. code-block:: bash

   > git clone https://github.com/m-smith/netshape
   > cd netshape
   > make install

Contributing / Testing
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Some rudimentary tests have been written, though many more could be made.
Any contribution to this project is highly appreciated.

In order to run the existing tests, just use: :code:`make test` from the project root

Documentation
----------------
.. toctree::

    self
    introduction
    configuration
    api




