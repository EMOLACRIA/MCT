#!/usr/bin/env python3
"""Legacy shortcut entrypoint routed to the single QuickShell panel state."""
import argparse
import sys
from shellctl import toggle
if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('kind',choices=['launcher','power']);a=p.parse_args()
    try:toggle(a.kind)
    except Exception as e:print(str(e),file=sys.stderr);sys.exit(1)
