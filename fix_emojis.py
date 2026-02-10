import re

with open('index.html', 'r') as f:
    code = f.read()

# Improved SVG encoding for data URI
new_helper = "const getGvEmoji = e => `data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='50%25' x='50%25' dy='.35em' text-anchor='middle' font-size='80'%3E${e}%3C/text%3E%3C/svg%3E`;"

code = re.sub(r"const getGvEmoji = e => `.*?`;", new_helper, code)

with open('index.html', 'w') as f:
    f.write(code)
