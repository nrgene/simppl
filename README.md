# simppl
##### Package for writing simple command-line pipelines, and organized command-line toolboxes. 

The package is composed of two separate but intertwined modules:
1. **simple_pipeline** - aids writing command-line pipelines with minimal overhead. Can be integrated into any python script.
2. **cli** - aids converting a collection of cli python scripts into an organized toolbox cli

These two modules are packed together, and can be naturally used together. 
Each module has functionalities that use the other.

## simple_pipeline
The simple_pipeline module defines the SimplePipeline class. <br>
SimplePipeline conveniently enables turning a python cli script (executed from terminal) into a pipeline of os commands.
- It enables running os commands sequentially / concurrently.
- Uses multiprocessing to easily imple:wqment scatter-gather pattern 
- Each command / commands-batch is given an index.
- The user can run a sub-sequence of commands by specifying -fc (first_command) and -lc (last_command) flags.
- Has option to dry_run the pipeline using -d flag.
- Each command is printed before execution, and is also optionally timed.
- outputs/errors from sub-commands are collected and logged.

### Using simple_pipeline
The simplest usage will look like this:
~~~
from simppl.simple_pipeline import SimplePipeline
sp = SimplePipeline(start=0, end=100):
sp.print_and_run('<YOUR_FIRST_OS_COMMAND>')
sp.print_and_run('<YOUR_SECOND_OS_COMMAND>')
~~~
To run multiple commands concurrently use:
~~~
commands = ['<YOUR_FIRST_OS_COMMAND>', '<YOUR_SECOND_OS_COMMAND>']
max_number_of_processes = 4
sp.run_parallel(commands, max_number_of_processes)
~~~
Finally if your project uses the cli module, you can run directly another command_line_tool as part of a pipeline.
The other tool will be run from the same process, but it will appear from the logs as another command in the pipeline. 
This enables smoother debugging and refactoring of tools calling other tools.
~~~
from example_module import example_tool
sp.print_and_run_clt(example_tool.run, ['first_number', 'second_nmber'], 
                             {'-key1': 'val1', '-key2': 'val2'},
                             {'--flag'})
~~~

#### Note that in order to see the commands printed, you will need to configure logging. See example_module/logging_config.ini for example.

## cli
cli enables turning a collection of python executable scripts into a unified cli.
- Creates a single entrypoint for running the command-line tools
- Standardized tool development and documentation
- Adds a manual printout listing all available tools and packages with minimal development overhead

### Using cli:
- example_module gives an example of how to use CommandLineInterface in your project
- requirements:
    - __main__.py - define toolbox logo, constructs and runs the CommandLineInterface. 
    - __init__.py - set logging configuration
    - logging_config.ini - python.logging configuration
    - tools - each script defined as command_line_tool will be automatically added to the toolbox

Defining a script as command_line_tool:
~~~
from simppl.cli import command_line_tool

@command_line_tool
def run(argv):
    """
    Tool description that will appear in main man printout
    """
    # Do something here using any python code
~~~

Printing manual (run the package with no arguments):
~~~
python -m your_toolbox_package_name 
~~~
Where your_toolbox_package_name is the name of the folder containing __main__.py

Running a specific tool:
~~~
python -m your_toolbox_package_name tool_name <tool_args>
~~~
Where tool_name is the name of the py file which contains the @command_line_tool definition
    

## Examples 
### Command-line-tool example:
- See example_module/add_two_numbers.py
~~~
python -m example_module add_two_numbers 5 6
~~~
- Should print 11.0 to stdout  

### Example for running command-line-tool using SimplePipeline
~~~
python -m example_module analyze_file_pipeline resources/analyze_file_pipeline_input.txt test_outputs
~~~
- Should print the following (except date-time) to stdout:
~~~
python -m <module_name> analyze_file_pipeline  resources/analyze_file_pipeline_input.txt  test_outputs 
2020-09-11 14:31:05,639 - analyze_file_pipeline - INFO - 1) wc resources/analyze_file_pipeline_input.txt > test_outputs/wc.txt
2020-09-11 14:31:05,643 - analyze_file_pipeline - INFO - Time elapsed wc: 0 s
2020-09-11 14:31:05,643 - analyze_file_pipeline - INFO - 2) ls -l resources/analyze_file_pipeline_input.txt > test_outputs/ls.txt
2020-09-11 14:31:05,648 - analyze_file_pipeline - INFO - Time elapsed ls: 0 s
2020-09-11 14:31:05,649 - analyze_file_pipeline - INFO - 3) sed 's/\s/\n/g' resources/analyze_file_pipeline_input.txt | sort | uniq -c | sort -n > test_outputs/word_count.txt
2020-09-11 14:31:05,653 - analyze_file_pipeline - INFO - Time elapsed sed: 0 s
~~~
## Distribution
Distribution to pypi was done by following this manual:
https://packaging.python.org/tutorials/packaging-projects/
