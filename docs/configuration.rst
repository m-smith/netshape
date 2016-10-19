Configuration
====================================
In addition to the previously mentioned options, :code:`netshape` will
optionally and automatically load a :code:`netshape_conf.py` file in the directory
where netshape is being run. This file allows a user to write custom functions
for computing network properties, add additional subcommands, or modify existing ones.

The :code:`netshape_conf.py` file
------------------------------------
The :code:`netshape_conf.py` is simply a python module that is imported before
the command line arguments are parsed. This allows this module to define additional
command line arguments or change the meaning of existing ones before they are used
to build the network visualization.

The :code:`conf` object
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Every :code:`netshape_conf.py` imports a global :code:`conf` object from
the :code:`netshape.config` module that is shared across the :code:`netshape` application.
:code:`conf` object maintains and exposes the configuration state using an internal dictionary of
:code:`Command` objects, each of which represents a single subcommand of the application.
This dictionary can be accessed as the :code:`commands` property of the :code:`conf` object.
:code:`Command`'s are indexed by the name of the command itself (e.g. for :code:`netshape build`, it would be :code:`conf.commands["build"]`).

The :code:`conf` object also exposes a method to add commands to the application.
This could be useful if a user wanted to make different visualizations of the same network,
or required other side effects, like outputting node properties in csv format.
This function is accessed via :code:`conf.register_command()`, and accepts a required :code:`command_name` argument, as well as optional :code:`help` which is a string representing the help message for that subcommand, and :code:`command_args`, a list of dicts of arguments to be passed to the :code:`argparse` module's :code:`add_argument` function, as well as the additional 'name' key, which specifies the list of possible names for that parameter.

This enables us to build custom command line arguments which can be used gracefully
in the network visualization pipeline.

The :code:`Command` class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The command class allows us to construct and modify visualization pipelines that
serve a common purpose. Currently it is somewhat underdeveloped, and as such,
only exposes two methods: :code:`Command.read_edges()`, which builds builds the original network or adds edges to an existing one. It accepts a single parameter, which is the name of the command line argument
that was used to capture the edgelist file. The other method, :code:`Command.add_node_prop`() can be used to add a property to the network. It accepts a name for the property as it's first argument,
a function as it's second argument, which has some restrictions on it's arguments, and, additional args and kwargs to pass to that function when it is being called. The function must receive a netshape object as it's first argument, the name of the property being added as the second, and a dictionary of command line arguments as the third argument. This function then can compute a network statistic, and call,
 :code:`Netshape.add_node_prop()` to add it to the netshape object. These methods are added in order, and executed sequentially to compute all desired network statistics. Then, internal methods are used to
 build the directory for the web page.


A sample :code:`netshape_conf.py`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
In order to reduce the potential confusion  of the above examples, we give an example of a :code:`netshape_conf.py` file which would result in the default commands. The :code:`node_props` module
adds utility functions that compute various node properties of the network, according to the function
format described above. For more details on specific functions, see the :doc:`Full API </api>`

.. code-block:: python

    import argparse
    import sys

    from netshape.config import conf
    from netshape import node_props

    (conf
     .register_command('build', help="build a static visualization of a network",
                       command_args=build_args)
     .read_edges('network')
     .add_node_prop('Eigenvector Centrality', node_props.eigenvector_centrality)
     .add_node_prop('Community', node_props.modularity_community)
     .add_node_prop('Degree', node_props.degree)
    )
    (conf
     .register_command('serve', help="utility function to view a network visualization", command_args=[{
            "name": ['-p', '--port'],
            "dest": 'p',
            "default":8000,
            "help": "The port to serve on."
      }])
     .add_node_prop('', serve)

     build_args = [{
                  'name': ['network'],
                  'nargs': "?",
                  'help':"the network, formatted as a csv edgelist - "
                         "accepts a path or from stdin",
                  "type":argparse.FileType('r'),
                  "default":sys.stdin
              }, {
                  "name": ['-s', '--seps'],
                  "dest": 'sep',
                  "default":",",
                  "help": "the string delimiter between values in the edgelist"
                          " (default: \",\")"
              }, {
                  "name": ['-d', '--directed'],
                  "dest": 'directed',
                  "default":"True",
                  "help": "Boolean indicator that is True if the network is directed, "
                          "and False otherwise (default: True)"
              }, {
                  "name": ['-o', '--out'],
                  "dest": 'out',
                  "default":"dist",
                  "help": "The name of the file to build the web visualization in "
                          "(default: \"dist\")"
              }, {
                  "name": ['-n', '--name'],
                  "dest": 'name',
                  "default":"Network",
                  "help": "The name of the file to build the web visualization in "
                          "(default: \"Network\")"
              }]
