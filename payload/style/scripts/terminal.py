#!/usr/bin/env python3
"""Use the same terminal preference for Super+Q and launcher terminal applications."""
import argparse
import os
import shutil
import sys
from preferences import effective as read


def launch_command(arguments,cwd=None,env=None):
    env=os.environ if env is None else env
    terminal=read(env)['terminal']
    executable=shutil.which(terminal,path=env.get('PATH'))
    if not executable:raise RuntimeError('Selected terminal is not installed: '+terminal)
    command=[executable]
    if cwd:command += ['--directory' if terminal=='kitty' else '--working-directory',cwd]
    if arguments:command += ['-e' if terminal=='alacritty' else '--',*arguments]
    return command


def main(arguments):
    parser=argparse.ArgumentParser();parser.add_argument('--cwd');parser.add_argument('command',nargs=argparse.REMAINDER)
    args=parser.parse_args(arguments);command=args.command
    if command[:1]==['--']:command=command[1:]
    try:
        launch=launch_command(command,args.cwd);os.execvpe(launch[0],launch,os.environ)
    except (OSError,RuntimeError,ValueError) as error:
        print('Terminal: '+str(error),file=sys.stderr);return 1


if __name__=='__main__':sys.exit(main(sys.argv[1:]))
