from example_module import add_two_numbers
from simppl.cli import command_line_tool


@command_line_tool
def run(argv):
    """
    adds to numbers and prints the results
    """
    add_two_numbers.run(argv)
