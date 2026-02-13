')" class="flex-1 py-3 rounded-2xl text-[10px] font-black tracking-widest transition-all ${tab===t?'bg-primary text-black shadow-lg shadow-primary/20':'text-white/40 hover:bg-white/5'}">${t.toUpperCase()}</button>`).join('');
        el.innerHTML = `
            <div class="relative mb-6">
                <span class="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-gray-500 text-sm">search</span>
                <input type="text" placeholder="Find players..." class="w-full bg-white/5 border border-white/10 rounded-2xl py-4 pl-12 pr-4 text-xs font-bold focus:border-primary outline-none transition-all">
            </div>
            <div id="socialContent" class="space-y-3"></div>
        `;
        const cont = $('socialContent');
        if (tab === 'friends') {
            if (P.friends.length === 0) cont.innerHTML = '<div class="py-12 text-center text-gray-500 font-bold uppercase tracking-widest text-[10px] opacity-40">No friends yet</div>';
            else P.friends.forEach(name => {
                const isInv = P.invited.includes(name); const row = document.createElement('div'); row.className = 'flex items-center justify-between p-4 bg-white/5 rounded-3xl border border-white/5';
                row.innerHTML = `<div class="flex items-center gap-4"><div class="size-12 rounded-2xl bg-gradient-to-br from-gray-700 to-gray-900 flex items-center justify-center border border-white/10"><span class="material-symbols-outlined text-white/50">person</span></div><div class="flex flex-col"><span class="font-black italic tracking-tighter text-base">${esc(name)}</span><span class="text-[9px] font-bold text-green-400 uppercase tracking-widest">Online</span></div></div><button class="px-6 py-2.5 rounded-full text-[10px] font-black tracking-widest transition-all ${isInv ? 'bg-primary text-black' : 'bg-white/10 text-white'}" onclick="toggleInvite(this)" data-name="${esc(name)}">${isInv ? 'INVITED' : 'INVITE'}</button>`;
                cont.appendChild(row);
            });
        } else if (tab === 'explore') {
            ['Turbo', 'Sparky', 'Glimmer', 'Nova', 'Echo'].forEach(name => {
                const row = document.createElement('div'); row.className = 'flex items-center justify-between p-4 bg-white/5 rounded-3xl border border-white/5';
                row.innerHTML = `<div class="flex items-center gap-4"><div class="size-12 rounded-2xl bg-white/5 flex items-center justify-center border border-white/10"><span class="material-symbols-outlined text-white/30">smart_toy</span></div><div class="flex flex-col"><span class="font-black italic tracking-tighter text-base">${esc(name)}</span><span class="text-[9px] font-bold text-primary uppercase tracking-widest">Level ${Math.floor(Math.random()*15)+1}</span></div></div><button class="size-10 rounded-full bg-white/5 border border-white/10 flex items-center justify-center hover:bg-primary hover:text-black transition-all" onclick="addFriend(this)" data-name="${esc(name)}"><span class="material-symbols-outlined text-xl">person_add</span></button>`;
                cont.appendChild(row);
            });
        } else cont.innerHTML = '<div class="py-12 text-center text-gray-500 font-bold uppercase tracking-widest text-[10px] opacity-40">No pending requests</div>';
    }
