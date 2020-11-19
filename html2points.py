#!/usr/bin/env python3

"""
Converts html to plain text bullet points

function yy-h2p() { pbpaste | python3 $YY_SCRIPTS/html2points.py | pbcopy }
"""

import re

with open('/dev/stdin') as fin, open('/dev/stdout', 'w') as fout:
    for line in fin:
        line = line.strip()
        line = re.sub(r'\<\!\-\-.*?\-\-\>', '', line)
        line = re.sub(r'\<.*?\>', '', line)
        line = line.strip()
        if len(line) == 0:
            continue
        fout.write('● ' + line + '\n')
