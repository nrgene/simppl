import sys
from simppl.cli import CommandLineInterface
from example_module.__main__ import ascii_logo

if __name__ == '__main__':
    cli = CommandLineInterface(__file__, ascii_logo)
    cli.run(sys.argv)
