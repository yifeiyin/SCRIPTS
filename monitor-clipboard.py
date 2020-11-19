# Monitor and save clipboard content to a file.
#
# Internally uses pbcopy and pbpaste thus macOS only.
#
# Usage:
#   python3 monitor-clipboard.py FILE

import subprocess
import time
import sys

l = set()
prev = None

o = open(sys.argv[1], 'w+')

print('Clearing clipboard')
subprocess.run(['pbcopy'], stdin=subprocess.DEVNULL)

while True:
    time.sleep(0.1)
    clipboard = subprocess.run(['pbpaste'], stdout=subprocess.PIPE).stdout.decode()
    clipboard = clipboard.strip()

    if len(clipboard) == 0:
        continue

    if clipboard != prev:
        if clipboard in l:
            print('--> (exists)')
        else:
            l.add(clipboard)
            print('--> ' + clipboard)
            o.write(clipboard)
            if not clipboard.endswith('\n'):
                o.write('\n')
                o.flush()

        prev = clipboard
