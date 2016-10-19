""" Module for writing netshape-config.py files"""
from __future__ import print_function

import argparse
import sys
import select

from .main import Netshape
from .defaults import build_args
from . import node_props
from .utils import serve

ns = Netshape()

class Config(object):
    """docstring for Config"""
    def __init__(self):
        super(Config, self).__init__()
        self.commands = {}
        self.parser = argparse.ArgumentParser(
            description='Generate a browser-based visualization of a network.')
        self.parser.set_defaults(func=self.parser.print_help)
        self.subparsers = self.parser.add_subparsers(title='subcommands',
                                                     description='valid subcommands')

    def register_command(self, command_name, help=None, command_args=None):
        """Registers a subcommand and returns a command object which can
        """
        command_args = [command_args] if not hasattr(command_args, '__iter__') else command_args
        self.commands[command_name] = Command()
        subparser = self.subparsers.add_parser(command_name,
                                               help=help if help else command_name)
        for i in command_args:
            if not i:
                continue
            print(i)
            name = i["name"]
            del i["name"]
            subparser.add_argument(*name, **i)
        subparser.set_defaults(func=self.commands[command_name].run_pipeline)
        return self.commands[command_name]


class Command(object):
    """docstring for Command"""
    def __init__(self):
        super(Command, self).__init__()
        self.pipeline = []

    def read_edges(self, argname):
        def edgeread(ns, _, cl_args):
            if not select.select([cl_args[argname], ], [], [], 0.0)[0]:
                print("Missing argument: {}".format(argname))
                conf.parser.print_help()
                sys.exit(1)

            ns.from_edgelist(cl_args[argname], sep=cl_args["sep"], directed=cl_args["directed"])
        self.pipeline.append((None, edgeread, None))
        return self

    def add_node_prop(self, name, func, *args, **kwargs):
        """Adds a property to nodes in the network

        Positional arguments:
        name -- the name of the property to be added
        func -- a function which accepts a netshape object as the first
                argument, the name of the property as the second,
                and the command line arguments as the third,
                as well as any additional arguments,
                and returns a mapping from node ids to property values
        """
        self.pipeline.append((name, func, (args, kwargs)))
        return self

    def run_pipeline(self, cl_args):
        """Executes the pipeline"""
        for (name, func, args) in self.pipeline:
            if args:
                func(ns, name, cl_args, *(args[0]), **(args[1]))
            else:
                func(ns, name, cl_args)
        try:
            ns.build_visualization(cl_args["out"],cl_args["name"])
        except KeyError:
            try:
                ns.build_visualization(cl_args["out"])
            except KeyError:
                try:
                    ns.build_visualization(cl_args["name"])
                except KeyError:
                    ns.build_visualization()

conf = Config()
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
)