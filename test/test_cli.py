import os
import unittest

import example_module.__main__
from simppl.cli import CommandLineInterface


class TestCli(unittest.TestCase):
    ascii_logo = '''

                   ____                       ___                         ,--,                                           
                 ,'  , `.                   ,--.'|_                     ,--.'|             ,---,                         
              ,-+-,.' _ |                   |  | :,'   ,---.     ,---.  |  | :           ,---.'|      ,---.              
           ,-+-. ;   , ||                   :  : ' :  '   ,'\   '   ,'\ :  : '           |   | :     '   ,'\ ,--,  ,--,  
          ,--.'|'   |  ||    .--,         .;__,'  /  /   /   | /   /   ||  ' |           :   : :    /   /   ||'. \/ .`|  
         |   |  ,', |  |,  /_ ./|         |  |   |  .   ; ,. :.   ; ,. :'  | |           :     |,-..   ; ,. :'  \/  / ;  
         |   | /  | |--', ' , ' :         :__,'| :  '   | |: :'   | |: :|  | :           |   : '  |'   | |: : \  \.' /   
         |   : |  | ,  /___/ \: |           '  : |__'   | .; :'   | .; :'  : |__         |   |  / :'   | .; :  \  ;  ;   
         |   : |  |/    .  \  ' |           |  | '.'|   :    ||   :    ||  | '.'|        '   : |: ||   :    | / \  \  \  
         |   | |`-'      \  ;   :           ;  :    ;\   \  /  \   \  / ;  :    ;        |   | '/ : \   \  /./__;   ;  \ 
         |   ;/           \  \  ;           |  ,   /  `----'    `----'  |  ,   /         |   :    |  `----' |   :/\  \ ; 
         '---'             :  \  \           ---`-'                      ---`-'          /    \  /          `---'  `--`  
                            \  ' ;                                                       `-'----'                        
                             `--`                                                                                       
             '''

    def test_cli_no_params(self):
        cli = CommandLineInterface(example_module.__main__.__file__, self.ascii_logo)
        cli.run(['my_tool_box'])

    def test_cli_add_two_numbers_example(self):
        cli = CommandLineInterface(example_module.__main__.__file__, self.ascii_logo)
        return_value = cli.run(['my_tool_box', 'add_two_numbers', '1.5', '2'])
        self.assertEqual(0, return_value)

    def test_cli_analyze_file_pipeline_example(self):
        cli = CommandLineInterface(example_module.__main__.__file__, self.ascii_logo)
        project_dir = os.path.dirname(os.path.dirname(__file__))
        return_value = cli.run(['my_tool_box', 'analyze_file_pipeline', f'{project_dir}/example_module/resources/analyze_file_pipeline_input.txt', 'test_outputs'])
        self.assertEqual(0, return_value)
