import sys
# Handles entry into the application
def main():
    from netshape.main import Netshape
    import argparse

    parser = argparse.ArgumentParser(
        description='Generate a browser-based visualization of a network.')

    parser.add_argument('path', help="the path to the network, formatted as an edgelist")
    parser.add_argument('-s', '--sep', dest='sep', default=",",
                    help="the string delimiter between values in the edgelist (default: \",\")")

    args = parser.parse_args()

    Netshape(args.path, sep=args.sep)

if __name__ == '__main__':
    main()