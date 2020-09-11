import argparse
import sys
from argparse import ArgumentParser
from functools import wraps

from simppl.simple_pipeline import SimplePipeline


def print_args(argv):
    sys.stderr.write('python -m <module_name>')
    key = None
    for field in argv:
        if field.startswith('-'):
            if key is None:
                key = field
            else:
                sys.stderr.write(f' {key}')
                key = field
        else:
            if key is None:
                sys.stderr.write(f' {field} ')
            else:
                sys.stderr.write(f' {key} {field}')
                key = None
    sys.stderr.write('\n')


def command_line_tool(run_function):
    @wraps(run_function)
    def wrapper(argv):
        # print command if not internal_tool (which was ran from another tool)
        if argv[0] != 'internal_tool':
            print_args(argv)

        if run_function.__doc__ is None:
            raise RuntimeError(f'Must define a docstring for command_line_tool: {run_function.__module__}')
        if run_function.__name__ != 'run':
            raise RuntimeError(f'only functions named "run" can be a command_line_tool, got: {run_function.__name__}')
        run_function(argv)
    return wrapper


def get_simple_pipeline(arg_parser: ArgumentParser, argv: list, name):
    """
    :param arg_parser: argument parser, will add SimplePipeline arguments to it
    :param argv: arguments list of command_line_tool
    :param name: __name__ of calling module, used in logging
    :return: simple_pipeline object
    """
    SimplePipeline.add_parse_args(arg_parser)
    args = arg_parser.parse_args(argv[1:])
    return SimplePipeline(args.d, args.fc, args.lc, True, name=name)


def get_parser(prog, description):
    """
    :param prog: command_line_tool name (argv[0])
    :param description: command_line_tool description (__doc__)
    :return: argument parser
    """
    return argparse.ArgumentParser(description=description, prog=prog, formatter_class=argparse.ArgumentDefaultsHelpFormatter)