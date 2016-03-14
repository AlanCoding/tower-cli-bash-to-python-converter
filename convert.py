import sys
import shlex

def main(in_file, out_file):
    sys.stdout.write(str(in_file) + " : " + str(out_file) + '\n')
    with open(in_file, 'r') as f:
        script_text = f.read()
    sys.stdout.write('Snippet of file being converted: \n')
    sys.stdout.write(' script content ' + str(script_text[:100]) + '\n\n')
    script_lines = script_text.split('\n')
    res_list = [
        'user', 'team', 'organization', 'inventory',
        'host', 'group', 'project', 'job_template', 'credential',
        'job'
    ]
    with open(out_file, 'w') as f:
        f.write('import tower-cli\n\n')
        for res in res_list:
            f.write(str(res) + '_res = tower_cli.get_resource("' + str(res) + '")\n')
        f.write('\n')
        for line in script_lines:
            if line.startswith('tower-cli'):
                my_splitter = shlex.shlex(line, posix=True)
                my_splitter.whitespace += '='
                my_splitter.whitespace_split = True
                args = list(my_splitter)
                if len(args) < 3:
                    continue
                if args[1] == 'config':
                    continue
                if args[1] not in res_list:
                    sys.stdout.write('\nERROR: unknown resource: ' + str(args[1]) + '\n')
                    raise Exception
                f.write(str(args[1]) + '_res.' + str(args[2]) + '(')
                inner = ''
                for i in range(2, len(args)):
                    param = args[i]
                    if param.startswith('-'):
                        if (i + 1 < len(args)) and not args[i+1].startswith('-'):
                            param_str = str(param.strip('-'))
                            param_str = param_str.replace('-', '_')
                            value_str = str(args[i+1])
                            if ' ' in value_str or '@' in value_str:
                                value_str = '"' + value_str + '"'
                            inner += param_str + '=' + value_str + ','
                f.write(str(inner.strip(',')))
                f.write(')\n')


if __name__ == "__main__":
    args = sys.argv
    if len(args) < 3:
        sys.stdout.write("Usage:\npython convert.py input_script.sh output_python.py")
    main(*args[1:])
    