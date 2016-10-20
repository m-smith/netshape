# Netshape [![Build Status](https://travis-ci.org/m-smith/netshape.svg?branch=master)](https://travis-ci.org/m-smith/netshape)  [![Docs Status](https://readthedocs.org/projects/netshape/badge/?version=latest)](http://netshape.readthedocs.io/en/latest/)

`netshape` is a versatile tool designed to build interactive, browser-based,
and deployable visualizations of networks. This enables a more collaborative and more informative visualization process.

With `netshape`, a network edgelist is turned into a web-ready interactive visualization with just one command, and we can view that visualization with just a few more:

```
> netshape build AwesomeNetwork.csv
> cd dist
> netshape server
> echo "let the visualization begin"
```

Netshape is also highly configurable and hackable; it supports custom commands,
which enables the development of complex visualization pipelines.

[read the full documentation here](http://netshape.readthedocs.io/en/latest/?)
### Key Features

**Web-ready visualization:**
    Building and sharing visualizations of networks can help convey complex
    or technical properties of a network to non-technical users. `netshape` enables
    the instantanious sharing of these visualizations.

**Flexible configuration:**
    `netshape` commands are configured through a  `netshape_conf.py`
    file, which is *just a python file*. This means that any normal python code
    can be included or imported in you visualization pipeline.

### Dependencies


Before installing, ensure that python is installed on your computer, and is at
least version 2.7.

### Contributing / Testing
Some rudimentary tests have been written, though many more could be made.
Any contribution to this project is highly appreciated.

In order to run the existing tests, just use: `make test` from the project root

### Installation


Once the dependencies have been installed, in order to install `netshape`, simply run:
```
> git clone https://github.com/m-smith/netshape
> cd netshape
> make install
```
