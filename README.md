Netshape[![Build Status](https://travis-ci.org/m-smith/netshape.svg?branch=master)](https://travis-ci.org/m-smith/netshape)

Quickstart
------------------------------------

`netshape` is a versatile tool designed to build interactive, browser-based,
and deployable visualizations of networks. This enables a more collaborative and more informative visualization process.

With `netshape`, a network edgelist is turned into a web-ready interactive visualization with just one command, and we can view that visualization with just a few more:

   > netshape build AwesomeNetwork.csv
   > cd dist
   > netshape server
   > echo "let the visualization begin"

Netshape is also highly configurable and hackable; it supports custom commands,
which enables the development of complex visualization pipelines.

Key Features
~~~~~~~~~~~~~~~~~

Dependencies
~~~~~~~~~~~~~~~~~

Before installing, ensure that python is installed on your computer, and is at
least version 2.7.

Installation
~~~~~

Once the dependencies have been installed, in order to install `netshape`, simply run:

   > git clone https://github.com/m-smith/netshape
   > cd netshape
   > make install

