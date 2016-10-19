"""Handles CLI entry into the application."""

import sys
import os

def parse_args():
    """Parses command line arguments and executes the appropriate code."""

    sys.path.insert(0, os.getcwd())

    try:
      from netshape_conf import conf
    except ImportError:
      from .config import conf

    args = conf.parser.parse_args()
    args.func(vars(args))


if __name__ == '__main__':
    parse_args()
