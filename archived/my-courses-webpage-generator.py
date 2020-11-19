# file.py
# 2019 Jan 13 Yifei Yin

# -----------------------------------------------------------------
# README
# -----------------------------------------------------------------
# Time Spent On This: 2.3 hours, including writing html files
#
# Three files will be prompt for input:
# **EXMAPLE FILES**: https://gist.github.com/yifeiyin/b6c6124c375d799fbdb52bd079a07c4b
#
# - Webpage Template
#       - Should be a html page, have a "{}" somewhere in the body
# - Item Template
#       - Should be the html for the section, something like this
#       "<div><a onclick="closeWithDelay()" href="{}"> {} </a></div>"
# - Items
#       - Should be comma-seperated string, like this
#       "/Users/dummy/University/2019/Course1    ,    Course 1"
#       - Spaces in-between will be trimed
#       - Text before comma is the path to the file
#       - Text after comma is what gets displayed on the webpage
# -----------------------------------------------------------------

import urllib.parse
def urlencode(str):
    return urllib.parse.quote(str)

webpage_template = ""
with open(input("Webpage Template Path: ")) as f:
    webpage_template = f.read()

item_template = ""
with open(input("Item Template Path: ")) as f:
    item_template = f.read()

items = []
with open(input("Items Path: ")) as f:
    for line in f:
        if line.strip() == "":
            break
        items_to_append = line.split(",")
        assert len(items_to_append) == 2
        items_to_append[0] = urlencode(items_to_append[0].strip())
        items_to_append[1] = items_to_append[1].strip()
        items.append(items_to_append)

final_items = ""
for item in items:
    this_item = item_template.format(*item)
    final_items += this_item + "\n"

# Need to split the webpage first to avoid the curly braces in css
split_point = webpage_template.find("<body>")
first_half = webpage_template[:split_point]
second_half = webpage_template[split_point:]
final_result = first_half + second_half.format(final_items)

print(final_result)

webpage_output_path = input("Webpage Output Path (empty to abort): ")
if webpage_output_path == "":
    print("Aborted")
else:
    output_file = open(webpage_output_path, 'w')
    output_file.write(final_result)
    output_file.close()
    print("Saved")

