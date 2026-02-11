import sys

def replace_in_file(filename, search, replace):
    with open(filename, 'r') as f:
        content = f.read()
    if search not in content:
        print(f"Search string not found")
        return False
    new_content = content.replace(search, replace)
    with open(filename, 'w') as f:
        f.write(new_content)
    return True

# Fix updateSB
old_sb = 'd.innerHTML = `<span>${i + 1}. ${e.name}</span><span>${e.score}</span>`;'
new_sb = 'd.innerHTML = `<span>${i + 1}. ${esc(e.name)}</span><span>${e.score}</span>`;'
replace_in_file('index.html', old_sb, new_sb)

# Check loadModes
old_modes = 'c.innerHTML = `<div class="size-16 rounded-2xl bg-white/5 flex items-center justify-center border border-white/10"><span class="material-symbols-outlined text-primary text-3xl">${m.icon}</span></div><div class="flex-1"><h4 class="font-black italic text-lg tracking-tighter group-hover:text-primary transition-colors">${m.name}</h4><p class="text-[10px] text-gray-500 font-bold uppercase tracking-widest">${m.desc}</p></div>`;'
new_modes = 'c.innerHTML = `<div class="size-16 rounded-2xl bg-white/5 flex items-center justify-center border border-white/10"><span class="material-symbols-outlined text-primary text-3xl">${esc(m.icon)}</span></div><div class="flex-1"><h4 class="font-black italic text-lg tracking-tighter group-hover:text-primary transition-colors">${esc(m.name)}</h4><p class="text-[10px] text-gray-500 font-bold uppercase tracking-widest">${esc(m.desc)}</p></div>`;'
replace_in_file('index.html', old_modes, new_modes)
