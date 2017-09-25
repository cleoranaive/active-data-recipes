from __future__ import print_function, absolute_import

import importlib
import logging
import os
import sys
from argparse import ArgumentParser

from .formatter import all_formatters

here = os.path.abspath(os.path.dirname(__file__))

log = logging.getLogger('adr')
log.setLevel(logging.DEBUG)
log.addHandler(logging.StreamHandler())

QUIET = False
RECIPE_DIR = os.path.join(here, 'recipes')


class RecipeParser(ArgumentParser):

    def __init__(self, *args, **kwargs):
        ArgumentParser.__init__(self, *args, **kwargs)

        self.add_argument('recipe', nargs='?', help="Recipe to run.")
        self.add_argument('-l', '--list', action='store_true', default=False,
                          help="List available recipes.")
        self.add_argument('-f', '--format', dest='fmt', default='table',
                          choices=all_formatters.keys(),
                          help="Format to print data in, defaults to 'table'.")
        self.add_argument('-q', '--quiet', action='store_true', default=False,
                          help="Don't print query.")


def cli(args=sys.argv[1:]):
    parser = RecipeParser()
    args, remainder = parser.parse_known_args(args)

    if args.quiet:
        log.setLevel(logging.INFO)

    for path in sorted(os.listdir(RECIPE_DIR)):
        if not path.endswith('.py') or path == '__init__.py':
            continue

        name = os.path.splitext(path)[0]
        if args.list:
            log.info(name)
            continue

        if args.recipe != name:
            continue

        modname = '.recipes.{}'.format(args.recipe)
        mod = importlib.import_module(modname, package='adr')
        output = mod.run(remainder)

        formatter = all_formatters[args.fmt]
        log.debug("Result:")
        return(formatter(output))

    if not args.list:
        log.error("recipe '{}' not found!".format(args.recipe))


if __name__ == '__main__':
    sys.exit(cli())