import re

with open('index.html', 'r') as f:
    code = f.read()

# Fix HUD onclick
code = code.replace("onclick=\"show('oChar')\"", "onclick=\"show('oChar'); loadChars();\"")

# Fix loadChars selection logic
# (It was already correct in the script, but I'll make it more robust)

with open('index.html', 'w') as f:
    f.write(code)
