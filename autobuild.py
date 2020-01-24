#!/usr/bin/env python3

import sys
import os
import argparse
import shutil
import subprocess


def main():
    global configuration, parser
    configuration = dict()
    init_configuration()
    load_configuration()
    parser = init_parser()
    commandline_modify_configuration()
    os.chdir(configuration['change_dir'])
    command = ''
    if is_project():
        if not makefile_exists():
            gen_makefile()
        command = make_command()
    else:
        command = cc_command()
    print('> {}'.format(command))
    sys.exit(os.system(command))


def init_configuration():
    configuration['program-path'] = sys.path[0]
    configuration['configuration-path'] = expand_path('~/.autobuildrc')
    configuration['program-version'] = 'v1.0'
    configuration['program-ignored-arg-header'] = '+'
    configuration['cc-base-flags'] = '{source} -o {target}'
    configuration['temp-configuration-keys'] = []


def load_configuration():
    configuration_path = configuration['configuration-path']
    if not os.path.exists(configuration_path):
        shutil.copy(expand_path('`/default.autobuildrc'), configuration_path)
    with open(configuration_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if not line or line.startswith('#'):
                continue
            tokens = line.split('=')
            configuration[tokens[0]] = '='.join(tokens[1:])


def commandline_modify_configuration():
    for i in range(1, len(sys.argv) - 1):
        if sys.argv[i] in ('-c', '--cc-flags', '-m', '--make-flags'):
            sys.argv[i + 1] = configuration['program-ignored-arg-header'] + sys.argv[i + 1]
    args = vars(parser.parse_args())
    for key in args:
        configuration[key] = args[key]
    configuration['cc_flags'] = configuration['cc_flags'][len(configuration['program-ignored-arg-header']):]
    configuration['make_flags'] = configuration['make_flags'][len(configuration['program-ignored-arg-header']):]


def init_parser():
    parser = argparse.ArgumentParser(description=configuration['program-description'],
                                     allow_abbrev=False)
    parser.add_argument('source', metavar='SOURCE',
                        help='filename or path of (one of) the source file(s)')
    parser.add_argument('-t', '--target', metavar='TARGET', required=True,
                        help='filename or path of the built target')
    parser.add_argument('-d', '--change-dir', metavar='DIR', default='.',
                        help='change the working directory to the specified one before building')
    parser.add_argument('-c', '--cc-flags', metavar='FLAGS', default='',
                        help='additional flags passed to the compiler')
    parser.add_argument('-m', '--make-flags', metavar='FLAGS', default='',
                        help='additional flags passed to Make')
    parser.add_argument('-V', '--version', action='version',
                        version='{} {} from {}'.format(
                            parser.prog,
                            configuration['program-version'],
                            configuration['program-path']
                        ),
                        help='show version information and exit')
    return parser


def gen_makefile():
    template = expand_path(configuration['makefile-template'])
    detect_environment()
    with open(template, 'r', encoding='utf-8') as file:
        head, repeat, tail = file.read().split('# -autobuild-repeat\n')
    with open('Makefile', 'w', encoding='utf-8') as file:
        file.write(head.format(**configuration))
        for source in configuration['-sources'].split():
            for key in configuration['-per-source'][source]:
                configuration[key] = configuration['-per-source'][source][key]
            file.write(repeat.format(**configuration))
            for key in configuration['-per-source'][source]:
                del configuration[key]
        file.write(tail.format(**configuration))
    clear_temp_configuration_keys()


def detect_environment():
    cpp_units = filter_cpp_units(get_files(configuration['change_dir']))
    sources = []
    object_files = []
    per_source = {}
    for filename, cpp_unit in cpp_units:
        sources.append(filename)
        object_file = filename[:len(filename) - len(cpp_unit)] + '.o'
        object_files.append(object_file)
        cc_solved_dependencies = subprocess.run(
            [configuration['cc'], filename, '-MM'], stdout=subprocess.PIPE, check=True
        ).stdout.decode().replace('\r\n', '\n').strip()  # loses compatibility?
        per_source[filename] = {
            '-object-file': object_file,
            '-source': filename,
            '-cc-solved-dependencies': cc_solved_dependencies
        }
    configuration['-sources'] = ' '.join(sources)
    configuration['-object-files'] = ' '.join(object_files)
    configuration['-per-source'] = per_source
    configuration['temp-configuration-keys'].extend(
        ['-sources', '-object-files', '-per-source']
    )


def make_command():
    return '{} {} {}'.format(
        configuration['make'],
        configuration['make-flags'],
        configuration['make_flags']
    ).format(**configuration)


def cc_command():
    return '{} {} {} {}'.format(
        configuration['cc'],
        configuration['cc-base-flags'],
        configuration['cc-flags'],
        configuration['cc_flags']
    ).format(**configuration)


def get_files(path):
    res = []
    for filename in os.listdir(path):
        if os.path.isfile('/'.join((path, filename))):
            res.append(filename)
    return res


def filter_cpp_units(files):
    cpp_units = configuration['cpp-units'].split()
    res = []
    for filename in files:
        for cpp_unit in cpp_units:
            if filename.endswith(cpp_unit):
                res.append([filename, cpp_unit])
    return res


def is_project():
    return os.path.exists('.project')


def makefile_exists():
    return os.path.exists('Makefile')


def expand_path(path):
    return os.path.expanduser(path.replace('`', configuration['program-path']))


def clear_temp_configuration_keys():
    for key in configuration['temp-configuration-keys']:
        del configuration[key]
    configuration['temp-configuration-keys'].clear()


if __name__ == '__main__':
    main()
