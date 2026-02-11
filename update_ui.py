import sys

def replace_in_file(filename, search, replace):
    with open(filename, 'r') as f:
        content = f.read()
    if search not in content:
        print(f"Search string not found in {filename}")
        return
    new_content = content.replace(search, replace)
    with open(filename, 'w') as f:
        f.write(new_content)

replacements = [
    (
        """        @media (max-width: 640px) {
            #hLeft { transform: scale(0.65); transform-origin: top left; }
            #hRight { transform: scale(0.65); transform-origin: top right; }
            #BTNS { bottom: 10px; right: 10px; transform: scale(0.7); transform-origin: bottom right; flex-direction: column-reverse; align-items: flex-end; }
            .btn-act { width: 50px; height: 50px; font-size: 20px; }
            #joyBound { width: 120px; height: 120px; bottom: 30px; left: 30px; }
            #joyStick { width: 50px; height: 50px; }
            #SOCIAL { width: 95%; max-width: none; height: 80%; }
        }""",
        """        @media (max-width: 640px) {
            #hLeft { transform: scale(0.5); transform-origin: top left; top: 10px; left: 10px; }
            #hRight { transform: scale(0.5); transform-origin: top right; top: 10px; right: 10px; }
            #BTNS { bottom: 20px; right: 15px; transform: scale(0.6); transform-origin: bottom right; flex-direction: column-reverse; gap: 12px; }
            #joyBound { transform: scale(0.75); transform-origin: bottom left; bottom: 25px; left: 25px; }
            #socialInner { width: 95% !important; height: 92% !important; max-height: none !important; }
            #CDOWN { font-size: 4rem; }
            #SIDE { transform: scale(0.7); transform-origin: top left; top: 75px; left: 10px; }
            .tab-btn { padding: 8px 12px !important; font-size: 14px !important; }
        }"""
    ),
    (
        """    <div id="SOCIAL" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div class="bg-slate-900 w-full max-w-2xl h-[500px] rounded-3xl border-4 border-white/20 overflow-hidden flex flex-col shadow-2xl">""",
        """    <div id="SOCIAL" class="hidden fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm">
        <div id="socialInner" class="bg-slate-900 w-full max-w-2xl h-[500px] rounded-3xl border-4 border-white/20 overflow-hidden flex flex-col shadow-2xl">"""
    ),
    (
        """                        <button onclick="changeSocialTab('friends')" class="tab-btn px-6 py-3 font-bold text-white/60 hover:text-white transition-all border-b-2 border-transparent">Friends</button>
                        <button onclick="changeSocialTab('explore')" class="tab-btn px-6 py-3 font-bold text-white/60 hover:text-white transition-all border-b-2 border-transparent">Explore</button>
                        <button onclick="changeSocialTab('requests')" class="tab-btn px-6 py-3 font-bold text-white/60 hover:text-white transition-all border-b-2 border-transparent">Requests</button>""",
        """                        <button onclick="changeSocialTab('friends')" class="tab-btn px-6 py-3 font-bold text-white/60 hover:text-white transition-all border-b-4 border-transparent uppercase tracking-widest">Friends</button>
                        <button onclick="changeSocialTab('explore')" class="tab-btn px-6 py-3 font-bold text-white/60 hover:text-white transition-all border-b-4 border-transparent uppercase tracking-widest">Explore</button>
                        <button onclick="changeSocialTab('requests')" class="tab-btn px-6 py-3 font-bold text-white/60 hover:text-white transition-all border-b-4 border-transparent uppercase tracking-widest">Requests</button>"""
    ),
    (
        """    function changeSocialTab(tab) {
        socialTab = tab;
        document.querySelectorAll('.tab-btn').forEach(b => {
            b.classList.remove('text-white', 'border-white');
            b.classList.add('text-white/60', 'border-transparent');
            if (b.innerText.toLowerCase() === tab) {
                b.classList.add('text-white', 'border-white');
                b.classList.remove('text-white/60', 'border-transparent');
            }
        });
        renderSocial();
    }""",
        """    function changeSocialTab(tab) {
        socialTab = tab;
        document.querySelectorAll('.tab-btn').forEach(b => {
            b.classList.remove('text-white', 'border-cyan-400', 'bg-white/5');
            b.classList.add('text-white/60', 'border-transparent');
            if (b.innerText.toLowerCase() === tab) {
                b.classList.add('text-white', 'border-cyan-400', 'bg-white/5');
                b.classList.remove('text-white/60', 'border-transparent');
            }
        });
        renderSocial();
    }"""
    )
]

for s, r in replacements:
    replace_in_file('index.html', s, r)
