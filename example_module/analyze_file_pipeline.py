import os

from simppl.command_line_tool import command_line_tool
import simppl.command_line_tool


@command_line_tool
def run(argv):
    """
    runs some unix file analysis commands
    """
    parser = simppl.command_line_tool.get_parser(argv[0], __doc__)
    parser.add_argument('input_file')
    parser.add_argument('out_dir')
    args = parser.parse_args(argv[1:])

    simple_pipeline = simppl.command_line_tool.get_simple_pipeline(parser, argv, argv[0])
    input_file = args.input_file
    out_dir = args.out_dir

    os.makedirs(out_dir, exist_ok=True)
    simple_pipeline.print_and_run(f'wc {input_file} > {out_dir}/wc.txt')
    simple_pipeline.print_and_run(f'ls -l {input_file} > {out_dir}/ls.txt')
    simple_pipeline.print_and_run(f"sed 's/\\s/\\n/g' {input_file} | sort | uniq -c | sort -n > {out_dir}/word_count.txt")
