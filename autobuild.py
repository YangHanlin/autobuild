import sys
import os
import argparse
import shutil


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
    configuration['configuration-path'] = expand_path('`/default.autobuildrc')
    configuration['program-version'] = 'v0.0'
    configuration['program-ignored-arg-header'] = '+'
    configuration['cc-base-flags'] = '{source} -o {target}'


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
                        version='{} {}'.format(parser.prog, configuration['program-version']),
                        help='show version information and exit')
    return parser


def gen_makefile():
    print('Going to generate Makefile from {}'.format(expand_path(configuration['makefile-template'])))


def make_command():
    return '{} {} {}'.format(
        configuration['make'],
        configuration['make-flags'],
        configuration['make_flags'][len(configuration['program-ignored-arg-header']):]
    ).format(**configuration)


def cc_command():
    return '{} {} {} {}'.format(
        configuration['cc'],
        configuration['cc-base-flags'],
        configuration['cc-flags'],
        configuration['cc_flags'][len(configuration['program-ignored-arg-header']):]
    ).format(**configuration)


def is_project():
    return os.path.exists('.project')


def makefile_exists():
    return os.path.exists('Makefile')


def show_error_for_direct_run(recommended):
    print('Error: this script cannot be directly run', file=sys.stderr, end='')
    if recommended is not None:
        print('; try \'{}\' instead'.format(recommended), file=sys.stderr)


def expand_path(path):
    return os.path.expanduser(path.replace('`', configuration['program-path']))


if __name__ == '__main__':
    main()
