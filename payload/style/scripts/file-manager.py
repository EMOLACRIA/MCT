#!/usr/bin/env python3
"""Open Dolphin through the same desktop entry used by the application launcher."""
import os
from pathlib import Path
import shutil
import sys

DESKTOP_ID = 'org.kde.dolphin.desktop'


def data_directories(env):
    home = Path(env.get('HOME') or Path.home())
    data_home = Path(env.get('XDG_DATA_HOME') or home / '.local/share')
    yield data_home if data_home.is_absolute() else home / '.local/share'
    for value in (env.get('XDG_DATA_DIRS') or '/usr/local/share:/usr/share').split(':'):
        if value and Path(value).is_absolute():
            yield Path(value)


def launch_command(arguments, env=None):
    env = os.environ if env is None else env
    for directory in data_directories(env):
        desktop = directory / 'applications' / DESKTOP_ID
        if desktop.is_file():
            gio = shutil.which('gio', path=env.get('PATH'))
            if not gio:
                raise RuntimeError('Missing gio (Arch package: glib2). Cannot open the configured Dolphin entry.')
            # Let GIO handle Exec field codes, quoting and the entry's environment.
            # Do not fall back to a plain command when a configured entry fails.
            return [gio, 'launch', str(desktop), *arguments]
    dolphin = shutil.which('dolphin', path=env.get('PATH'))
    if not dolphin:
        raise RuntimeError('Dolphin and its desktop entry were not found.')
    return [dolphin, *arguments]


def main(arguments):
    try:
        command = launch_command(arguments)
        os.execvpe(command[0], command, os.environ)
    except (OSError, RuntimeError) as exc:
        print('File manager: ' + str(exc), file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
