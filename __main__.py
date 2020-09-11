import importlib
import os
import re
import sys

from colorama import Fore  # , Back, Style


def print_usage(tools):
    print(Fore.GREEN + """
                                   _     _       
                                  | |   (_)      
          ___ ___  _ __ ___  _ __ | |__  _  ___  
         / __/ _ \| '_ ` _ \| '_ \| '_ \| |/ _ \ 
        | (_| (_) | | | | | | |_) | |_) | | (_) |
         \___\___/|_| |_| |_| .__/|_.__/|_|\___/ 
                            | |                  
                            |_|                  
          """)
    print(Fore.RED + '\tUsage: python -m compbio <tool_name> <arg1, arg2, ...>\n')
    print(Fore.RESET + 'Tools list:')
    print('-----------\n')
    for package_name in sorted(tools):
        print(Fore.LIGHTMAGENTA_EX + f'package {package_name}:')
        for tool_name in sorted(tools[package_name]):
            print(Fore.CYAN + f'\t{tool_name}:')
            description = tools[package_name][tool_name].__doc__
            description = description.strip()
            lines = description.split('\n')
            for line in lines:
                print(Fore.RESET + f'\t\t{line.strip()}')
            print('')
    return ''


def run_tool(tool_name: str, package: dict):
    argv = [tool_name] + sys.argv[2:]
    package[tool_name](argv)


# Add new tools to and return as map<package, tool_name, compbio_tool_run_method>
def load_tools():
    compbio_tools = {}
    tool_name_to_package = {}
    script_dir = os.path.dirname(__file__)
    root_dir = os.path.dirname(script_dir) + '/'

    for subdir, dirs, files in os.walk(script_dir):
        # skip non python package dirs
        if '__init__.py' not in files:
            continue

        for file in files:
            file_path = subdir + os.sep + file

            if file_path.endswith(".py"):
                found_tool_definition = False
                module_str = file_path.replace(root_dir, '').replace(os.sep, '.')
                module_str = re.sub('.py$', '', module_str)
                for line in open(file_path, encoding='utf8'):
                    line = line.strip()
                    if line == '@compbio_tool':
                        found_tool_definition = True
                    if found_tool_definition:
                        module = importlib.import_module(module_str)
                        package_name = module_str.split('.')[-2]
                        module_name = module_str.split('.')[-1]
                        if package_name not in compbio_tools:
                            compbio_tools[package_name] = {}
                        try:
                            if module.run.__doc__ is None:
                                raise RuntimeError(f'Must define a docstring for compbio_tool: {module_str}')
                        except AttributeError:
                            raise RuntimeError(f'compbio_tool module {module_str} must implement a run method.')

                        compbio_tools[package_name][module_name] = module.run

                        tool_name_to_package[module_name] = package_name
    return compbio_tools, tool_name_to_package


def main():
    compbio_tools, tool_name_to_package = load_tools()

    if len(sys.argv) == 1:
        print_usage(compbio_tools)
        exit(0)

    tool_name = sys.argv[1]
    package = compbio_tools[tool_name_to_package[tool_name]]

    if tool_name in package:
        run_tool(tool_name, package)
    else:
        sys.exit(f'Could not find tool: {tool_name} \n{print_usage(compbio_tools)}')


if __name__ == '__main__':
    #logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"), stream=sys.stdout,
    #                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    main()
