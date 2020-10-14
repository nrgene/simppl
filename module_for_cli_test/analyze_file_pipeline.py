from example_module import analyze_file_pipeline
from simppl.cli import command_line_tool


@command_line_tool
def run(argv):
    """
    runs some unix file analysis commands
    """
    analyze_file_pipeline.run(argv)
