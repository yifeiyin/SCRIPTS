''' Use this bash/zsh script to make it work with pbcopy and pbpaste.

# !zsh
input=$(pbpaste)
urls=$(grep -Eoi '(http|https)://[^\)]+' <<< "$input")
python3 format-github-images.py <<< "$urls" | pbcopy
'''

a = open(0).read()

if len(a) < 20 or len(a) > 500:
    print("Content size is " + len(a));
    exit(1);

print('<p>')
for line in a.split():
    print('<img float="left" width="32%" src="' + line + '" />')

print('</p>')
print('<!--')
print(a, end='')
print('-->')
