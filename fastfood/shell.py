# -*- coding: utf-8 -*-
"""fastfood - cookbook wizardry"""
from __future__ import print_function
from __future__ import unicode_literals

import json
import logging
import os
import sys
import threading

_local = threading.local()
LOG = logging.getLogger(__name__)


def _fastfood_gen(args):
    print(args)


def _fastfood_new(args):
    print(args)


def _fastfood_build(args):
    print(args)


def main():
    """fastfood command line interface."""
    import argparse
    import traceback

    class HelpfulParser(argparse.ArgumentParser):
        def error(self, message, print_help=False):
            if 'too few arguments' in message:
                sys.argv.insert(0, os.path.basename(sys.argv.pop(0)))
                message = ("%s. Try getting help with `%s -h`"
                           % (message, " ".join(sys.argv)))
            if print_help:
                self.print_help()
            sys.stderr.write('\nerror: %s\n' % message)
            sys.exit(2)

    parser = HelpfulParser(
        description=__doc__.splitlines()[0],
        epilog="\n".join(__doc__.splitlines()[1:]),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        )

    verbose = parser.add_mutually_exclusive_group()
    verbose.add_argument('-v', dest='loglevel', action='store_const',
                         const=logging.INFO,
                         help="Set log-level to INFO.")
    verbose.add_argument('-vv', dest='loglevel', action='store_const',
                         const=logging.DEBUG,
                         help="Set log-level to DEBUG.")
    parser.set_defaults(loglevel=logging.WARNING)

    subparsers = parser.add_subparsers(
        dest='_subparsers', title='fastfood commands',
        description='operations...',
        help='...')
    #
    # `fastfood gen`
    #
    gen_parser = subparsers.add_parser(
        'gen', help='Create a new recipe for an existing cookbook.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    gen_parser.add_argument('stencil_set',
                            help="Stencil set to use.")
    gen_parser.add_argument('options', type=str, nargs='*',
                            metavar='option',
                            help="Stencil options.")
    gen_parser.set_defaults(func=_fastfood_gen)


    #
    # `fastfood new`
    #
    gen_parser = subparsers.add_parser(
        'new', help='Create a new recipe for an existing cookbook.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    gen_parser.add_argument('stencil_set',
                            help="Stencil set to use.")
    gen_parser.add_argument('options', type=str, nargs='*',
                            metavar='option',
                            help="Stencil options.")
    gen_parser.set_defaults(func=_fastfood_new)


    #
    # `fastfood build`
    #
    gen_parser = subparsers.add_parser(
        'build', help='Create a new recipe for an existing cookbook.',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    gen_parser.add_argument('stencil_set',
                            help="Stencil set to use.")
    gen_parser.add_argument('options', type=str, nargs='*',
                            metavar='option',
                            help="Stencil options.")
    gen_parser.set_defaults(func=_fastfood_build)


    setattr(_local, 'argparser', parser)
    args = parser.parse_args()

    try:
        result = args.func(args)
    except Exception as err:
        traceback.print_exc()
        # todo: tracack in -v or -vv mode?
        sys.stderr.write("%s\n" % repr(err))
        sys.stderr.flush()
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit("\nStahp")
    else:
        import ipdb;ipdb.set_trace()
        # result

if __name__ == '__main__':
    main()