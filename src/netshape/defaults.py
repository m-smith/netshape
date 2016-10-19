import argparse
import sys

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