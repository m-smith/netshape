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

    def serve(args):
        """Utility yo """
        import http.server
        import socketserver
        port = args.p
        handler = http.server.SimpleHTTPRequestHandler
        httpd = socketserver.TCPServer(("", port), handler)
        print("serving at port", port)
        print("type ^C to exit")
        httpd.serve_forever()
"""
    #def nshape(args):
    #    if not select.select([args.network, ], [], [], 0.0)[0]:
    #        print("Missing argument: network")
    #        parser.print_help()
    #        sys.exit(1)

    #    net_shape = Netshape(args.network, sep=args.sep)
    #    net_shape.generate_graph().add_eigenvector_centrality().add_community().add_degree()
    #    net_shape.build_visualization()

    #def community(args):
    #    if not select.select([args.network, ], [], [], 0.0)[0]:
    #        print("Missing argument: network")
    #        parser.print_help()
    #        sys.exit(1)
    #    net_shape = Netshape(args.network, sep=args.sep)
    #    net_shape.generate_graph().add_community()
    #    net_shape.write_node_props(["id", "Community"], file=args.file)


    #def print_help(_):
    #    parser.print_help()

    #parser = argparse.ArgumentParser(
    #    description='Generate a browser-based visualization of a network.')
    #parser.set_defaults(func=print_help)

    #subparsers = parser.add_subparsers(title='subcommands', description='valid subcommands')

    # build parser
    #build_parser = subparsers.add_parser('build', help="build a static visualization of a network")
    #build_parser.add_argument('network', nargs="?",
    #                          help="the network, formatted as a csv edgelist - "
    #                          "accepts a path or from stdin",
    #                          type=argparse.FileType('r'), default=sys.stdin)

    #build_parser.add_argument('-s', '--sep',
    #                          dest='sep', default=",",
    #                          help="the string delimiter between values in the edgelist"
    #                          " (default: \",\")")
    #build_parser.set_defaults(func=nshape)

    # server parser
    #server_parser = subparsers.add_parser('server', help="serve the static "
    #                                      "visualization on a localhost server")
    #server_parser.add_argument('-p', type=int, default=8000,
    #                           help="the port to serve the visualization from")
    #server_parser.set_defaults(func=serve)

    # community parser
    community_parser = subparsers.add_parser('community',
                                             help="detects communities in the network "
                                             "and outputs the results in csv format")
    community_parser.add_argument('network', nargs="?",
                                  help="the network, formatted as a csv edgelist - "
                                  "accepts a path or from stdin",
                                  type=argparse.FileType('r'), default=sys.stdin)
    community_parser.add_argument('-s', '--sep', dest='sep', default=",",
                                  help="the string delimiter between values in the edgelist"
                                  " (default: \",\")")
    community_parser.add_argument('-f', '--file', dest='file', default=False,
                                  help="write communities to a file -"
                                  " otherwise writes to stdout")
    community_parser.set_defaults(func=community)
"""

if __name__ == '__main__':
    parse_args()
