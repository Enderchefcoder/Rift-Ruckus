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

social_css = """
    #socialTabs { background: rgba(0,0,0,0.4); box-shadow: inset 0 2px 10px rgba(0,0,0,0.5); }
    .social-row { background: linear-gradient(135deg, rgba(255,255,255,0.05) 0%, rgba(255,255,255,0.02) 100%); transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1); }
    .social-row:hover { transform: translateX(5px); background: rgba(255,255,255,0.08); border-color: rgba(242,242,13,0.3); }
    .status-dot { width: 8px; height: 8px; border-radius: 50%; display: inline-block; margin-right: 5px; }
    .status-online { background: #4ade80; box-shadow: 0 0 10px #4ade80; animation: pulse-green 2s infinite; }
    @keyframes pulse-green { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
"""

replace_in_file('index.html', '.overlay.show { display: flex; }', '.overlay.show { display: flex; }\n' + social_css)

new_load_social = """
    window.loadSocial = (tab = 'friends') => {
        const el = $('socialList'), tabs = $('socialTabs'); if (!el || !tabs) return;
        tabs.innerHTML = ['friends', 'explore', 'req'].map(t => `<button onclick="loadSocial('${t}')" class="flex-1 py-3 rounded-2xl text-[10px] font-black tracking-widest transition-all ${tab===t?'bg-primary text-black shadow-[0_0_20px_rgba(242,242,13,0.3)]':'text-white/40 hover:bg-white/5'}">${t.toUpperCase()}</button>`).join('');
        el.innerHTML = `
            <div class="relative mb-6">
                <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 text-sm">search</span>
                <input type="text" placeholder="Search rifts..." class="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-xs font-bold focus:border-primary/50 outline-none transition-all focus:bg-white/10">
            </div>
            <div id="socialContent" class="space-y-3"></div>
        `;
        const cont = $('socialContent');
        if (tab === 'friends') {
            if (P.friends.length === 0) cont.innerHTML = '<div class="py-12 text-center text-gray-500 font-bold uppercase tracking-widest text-[10px] opacity-30">No party members found</div>';
            else P.friends.forEach(name => {
                const isInv = P.invited.includes(name); const row = document.createElement('div'); row.className = 'social-row flex items-center justify-between p-4 rounded-[2rem] border border-white/5';
                row.innerHTML = `<div class="flex items-center gap-4"><div class="size-12 rounded-2xl bg-gradient-to-br from-gray-700 to-gray-800 flex items-center justify-center border border-white/10 shadow-lg"><span class="material-symbols-outlined text-white/30">person</span></div><div class="flex flex-col"><span class="font-black italic tracking-tighter text-base leading-none mb-1">${esc(name)}</span><div class="flex items-center"><span class="status-dot status-online"></span><span class="text-[9px] font-bold text-green-400 uppercase tracking-widest">Active</span></div></div></div><button class="px-6 py-2.5 rounded-full text-[10px] font-black tracking-widest transition-all ${isInv ? 'bg-primary text-black' : 'bg-white/10 text-white hover:bg-white/20'}" onclick="toggleInvite(this)" data-name="${esc(name)}">${isInv ? 'INVITED' : 'INVITE'}</button>`;
                cont.appendChild(row);
            });
        } else if (tab === 'explore') {
            cont.innerHTML = '<div class="text-[9px] font-black text-white/20 uppercase tracking-[0.2em] mb-4 ml-2">Trending Runners</div><div id="exItems" class="space-y-3"></div>';
            const ex = $('exItems');
            [{n:'Turbo', r:12}, {n:'Sparky', r:5}, {n:'Glimmer', r:42}, {n:'Nova', r:8}, {n:'Echo', r:15}].forEach(p => {
                const row = document.createElement('div'); row.className = 'social-row flex items-center justify-between p-4 rounded-[2rem] border border-white/5';
                row.innerHTML = `<div class="flex items-center gap-4"><div class="size-12 rounded-2xl bg-gradient-to-br from-primary/10 to-transparent flex items-center justify-center border border-white/10 shadow-lg"><span class="material-symbols-outlined text-primary/40">rocket_launch</span></div><div class="flex flex-col"><span class="font-black italic tracking-tighter text-base leading-none mb-1">${esc(p.n)}</span><span class="text-[9px] font-bold text-white/30 uppercase tracking-widest">World Rank #${p.r}</span></div></div><button class="size-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center hover:bg-primary hover:text-black transition-all" onclick="addFriend(this)" data-name="${esc(p.n)}"><span class="material-symbols-outlined text-xl">person_add</span></button>`;
                ex.appendChild(row);
            });
        } else cont.innerHTML = '<div class="py-12 text-center text-gray-500 font-bold uppercase tracking-widest text-[10px] opacity-30">No Rift requests</div>';
    }
"""

# Find the old loadSocial and replace it
import re
with open('index.html', 'r') as f:
    content = f.read()

# Match the old function
pattern = r'function loadSocial\(tab = \'friends\'\) \{.*?\}'
content = re.sub(pattern, new_load_social, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
