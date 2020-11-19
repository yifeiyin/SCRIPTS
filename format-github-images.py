"""
Format images uploaded to github issues

function yy-fgi() { pbpaste | python3 $YY_SCRIPTS/format-github-images.py | pbcopy }
"""

import re

with open('/dev/stdin') as i, open('/dev/stdout', 'w') as o, open('/dev/stderr', 'w') as e:
    text = i.read()
    if len(text) < 20:
        e.write('Refuse to process: text too short\n')
        exit(1)

    if len(text) > 500:
        e.write('Refuse to process: text too long\n')
        exit(1)

    urls = []
    for line in text.split():
        result = re.search(r'https://user-images\.githubusercontent\.com[^\)]+', line)
        if result is None: continue
        urls.append(result.group(0))

    if len(urls) == 0:
        e.write('Aborted: no url detected\n')
        exit(1)


    o.write('<p>\n')
    for url in urls:
        o.write(f'<img float="left" width="32%" src="{url}" />\n')
    o.write('<p>\n')

    o.write('<!--\n')
    o.write(text)
    if not text.endswith('\n'):
        o.write('\n')
    o.write('-->\n')
