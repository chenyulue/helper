import sys

file = sys.argv[1]

with open(file, 'r+', encoding="utf-8") as f:
    content = f.read()
    f.seek(0)
    f.write(content.replace("import resources_rc", "from . import resources_rc"))
    f.truncate()