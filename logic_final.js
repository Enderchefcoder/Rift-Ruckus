    const $ = id => document.getElementById(id);
    const esc = t => String(t).replace(/[&<>"']/g, m => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[m]));
    const getGvEmoji = e => `data:image/svg+xml;charset=utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'%3E%3Ctext y='50%25' x='50%25' dominant-baseline='central' text-anchor='middle' font-size='80'%3E${encodeURIComponent(e)}%3C/text%3E%3C/svg%3E`;
    const sMesh = (g, m) => { const e = new THREE.Mesh(g, m); e.castShadow = e.receiveShadow = true; return e; };
    const addMesh = (m, isL = false) => { scene.add(m); (isL ? lobbyMeshes : gameMeshes).push(m); };
    window.show = id => { const e=$(id); if(e) e.classList.add('show'); };
    window.hide = id => { const e=$(id); if(e) e.classList.remove('show'); };
    window.setText = (id, t) => { const e=$(id); if(e) e.textContent=t; };
    const rnd = (a, b) => a + Math.random() * (b - a);
    const shuffle = a => [...a].sort(() => Math.random() - .5);
    const d2 = (a, b) => Math.sqrt((a.x - b.x) ** 2 + (a.z - b.z) ** 2);
    const d3 = (a, b) => Math.sqrt((a.x - b.x) ** 2 + ((a.y || 0) - (b.y || 0)) ** 2 + (a.z - b.z) ** 2);
    const clamp = (v, lo, hi) => Math.max(lo, Math.min(hi, v));

    function notify(msg, type = 'inf') {
        const c = $('NOTIFS'); if (!c) return;
        const n = document.createElement('div');
        const colors = {inf:'bg-blue-500/20 border-blue-500 text-blue-300', ok:'bg-primary/20 border-primary text-primary', bad:'bg-red-500/20 border-red-500 text-red-300'};
        n.className = `px-6 py-3 rounded-2xl font-bold text-xs uppercase tracking-widest shadow-2xl backdrop-blur-xl border-2 transition-all duration-300 ${colors[type] || colors.inf}`;
        n.textContent = msg; c.appendChild(n);
        setTimeout(() => { n.style.opacity = '0'; n.style.transform = 'translateY(-10px)'; setTimeout(() => n.remove(), 300); }, 2500);
    }

    function flash(id, ms) { const e=$(id); if(e) { e.classList.add('on'); setTimeout(() => e.classList.remove('on'), ms); } }

    const CHARS = [{"id": "glitch", "name": "Glitch", "emoji": "😎", "role": "Speed", "color": 6056896, "spd": 95, "pow": 50, "jmp": 80, "skill": "Blink", "sType": "tele", "sCD": 5}, {"id": "harold", "name": "Harold", "emoji": "🦣", "role": "Tank", "color": 7951688, "spd": 45, "pow": 95, "jmp": 40, "skill": "Quake", "sType": "stun", "sCD": 8}, {"id": "sally", "name": "Sally", "emoji": "🐍", "role": "Speed", "color": 5025616, "spd": 90, "pow": 60, "jmp": 70, "skill": "Venom Dash", "sType": "dash", "sCD": 4}, {"id": "blobby", "name": "Blobby", "emoji": "🟣", "role": "Jumper", "color": 10233776, "spd": 65, "pow": 50, "jmp": 100, "skill": "Super Bounce", "sType": "jump", "sCD": 3}, {"id": "nampy", "name": "Nampy", "emoji": "🥷", "role": "Stealth", "color": 2171169, "spd": 85, "pow": 60, "jmp": 90, "skill": "Smoke Screen", "sType": "smoke", "sCD": 6}, {"id": "panee", "name": "Panee", "emoji": "🦔", "role": "Defender", "color": 16754470, "spd": 70, "pow": 80, "jmp": 60, "skill": "Spike Blast", "sType": "knock", "sCD": 5}, {"id": "santa", "name": "Santa", "emoji": "🎅", "role": "Special", "color": 15158332, "spd": 75, "pow": 70, "jmp": 70, "skill": "Gift", "sType": "buff", "sCD": 10}];
    const GAMES = [
        { id: 'stars', name: '⭐ STAR COLLECTOR', tip: 'COLLECT STARS! GOLD = 30 PTS!', dur: 50, type: 'collect' },
        { id: 'sumo', name: '💪 SUMO RING', tip: 'PUSH ENEMIES OUT OF THE RING!', dur: 55, type: 'sumo' },
        { id: 'hill', name: '👑 KING OF HILL', tip: 'STAY ON HILL! PULSE EVERY 5S!', dur: 50, type: 'hill' },
        { id: 'tag', name: '🏷️ TAG FRENZY', tip: "GRAB TO PASS THE TAG! DON'T BE IT!", dur: 45, type: 'tag' },
        { id: 'pads', name: '🪑 MUSICAL PADS', tip: 'STAND ON GREEN PAD WHEN MUSIC STOPS!', dur: 70, type: 'pads' }
    ];

    const ST = { LOAD: 0, LOBBY: 1, CDOWN: 2, GAME: 3, RES: 4 };
    let state = ST.LOAD;
    let P = { gems: 500, crowns: 10, charId: 'glitch', score: 0, isIt: false, tagImmune: 0, skillCD: 0, grabCD: 0, stunned: 0, stamina: 100, sprinting: false, hillTime: 0, lv: 1, xp: 0, buffTime: 0, friends: [], invited: [], preset: 'hd', settings: { shadows: true, ai: 'medium', leftHand: false, acc: false, debug: false } };

    function saveData() { localStorage.setItem('RR_DATA', JSON.stringify({ gems: P.gems, crowns: P.crowns, lv: P.lv, xp: P.xp, charId: P.charId, friends: P.friends, invited: P.invited, preset: P.preset, settings: P.settings })); }
    function loadData() {
        const d = localStorage.getItem('RR_DATA');
        if (d) { try { const j = JSON.parse(d); if (j.settings) Object.assign(P.settings, j.settings); if (j.friends) P.friends = j.friends; if (j.invited) P.invited = j.invited; ['gems', 'crowns', 'lv', 'xp', 'charId', 'preset'].forEach(k => { if (j[k] !== undefined) P[k] = j[k]; }); } catch (e) {} }
        if (!CHARS.find(c => c.id === P.charId)) P.charId = CHARS[0].id;
        setText('hGems', P.gems); setText('hLv', P.lv); setText('hName', curC().name.toUpperCase());
        const cur = curC(), av = $('hAvatar'); if (av) av.style.backgroundImage = `url('${getGvEmoji(cur.emoji)}')`;
        document.documentElement.style.fontSize = P.settings.acc ? "40px" : "16px";
        applyLayout();
    }
    function applyLayout() {
        const jL = $('joyL'), bt = $('BTNS'); const isMob = window.innerWidth < 640; const margin = isMob ? '10px' : '40px';
        if (P.settings.leftHand) { if (jL) { jL.style.left = 'auto'; jL.style.right = margin; } if (bt) { bt.style.right = 'auto'; bt.style.left = margin; } }
        else { if (jL) { jL.style.right = 'auto'; jL.style.left = margin; } if (bt) { bt.style.left = 'auto'; bt.style.right = margin; } }
    }

    let selChar = 'glitch', scene, cam, ren, clk, sun, camAng = 0, pVel = { x: 0, y: 0, z: 0 }, grounded = true, near = null, curGame = null, gTimer = 0, gActive = false, rGames = [], rIdx = 0, musicOn = true, padCount = 16, scoreT = 0, shakeAmt = 0;
    const BOT_NAMES = ['ZIPPY', 'BOUNCER', 'SPARKY', 'GLIMMER', 'TURBO', 'RIFTY', 'ECHO', 'NOVA', 'PIXEL', 'GLITCHY', 'TANKER', 'FROSTY', 'SHADOW', 'BLAZE', 'BOLT', 'AURA', 'RUSTY', 'COMET', 'PULSE', 'ZEN'];
    var player, bots = [], lobbyMeshes = [], gameMeshes = [], stars = [], pads = [], solidPlatforms = [], hillMesh = null, interacts = [], particles3d = [];
    const G = .025, SPD = .12, JMP = .38, FRC = .86; const joy = { l: { x: 0, y: 0 }, r: { x: 0, y: 0 } };
    function getC(id) { return CHARS.find(c => c.id === id) || CHARS[0]; }
    function curC() { return getC(P.charId); }

    function initThree() {
        scene = new THREE.Scene(); let skyCol = 0x1a2a4a; scene.background = new THREE.Color(skyCol); scene.fog = new THREE.FogExp2(skyCol, .005);
        cam = new THREE.PerspectiveCamera(55, innerWidth / innerHeight, .1, 800);
        ren = new THREE.WebGLRenderer({ canvas: $('C'), antialias: true }); ren.setSize(innerWidth, innerHeight); ren.setPixelRatio(Math.min(devicePixelRatio, 2));
        ren.shadowMap.enabled = P.settings.shadows; ren.shadowMap.type = THREE.PCFSoftShadowMap;
        clk = new THREE.Clock(); scene.add(new THREE.AmbientLight(0xFFE0B2, 0.5));
        sun = new THREE.DirectionalLight(0xfff5e0, 1.1); sun.position.set(80, 120, 80); if (P.settings.shadows) { sun.castShadow = true; sun.shadow.mapSize.width = sun.shadow.mapSize.height = 1024; }
        scene.add(sun); scene.add(new THREE.HemisphereLight(0x6699cc, 0x334455, .5));
    }
    function mat(c, r = .5) { return new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: 0.1 }); }
    function makeNameTag(name) {
        const canvas = document.createElement('canvas'); canvas.width = 256; canvas.height = 64; const ctx = canvas.getContext('2d');
        ctx.fillStyle = 'rgba(0,0,0,0.6)'; ctx.roundRect(0, 0, 256, 64, 32); ctx.fill(); ctx.font = '900 34px Spline Sans, sans-serif'; ctx.fillStyle = '#f2f20d'; ctx.textAlign = 'center'; ctx.fillText(name, 128, 44);
        const tex = new THREE.CanvasTexture(canvas); const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true })); sprite.scale.set(3, 0.75, 1); sprite.position.y = 3.2; return sprite;
    }
    function makeChar(ch, name = '', isBot = false) {
        const g = new THREE.Group(), col = ch.color, bm = mat(col, .3);
        const body = sMesh(new THREE.CylinderGeometry(.4, .44, .7, 12), bm); body.position.y = 1; g.add(body);
        const top = sMesh(new THREE.SphereGeometry(.4, 12, 10), bm); top.position.y = 1.35; g.add(top);
        const bot = sMesh(new THREE.SphereGeometry(.44, 12, 10), bm); bot.position.y = .65; g.add(bot);
        const head = sMesh(new THREE.SphereGeometry(.36, 16, 14), mat(0xFFDFC4, .45)); head.position.y = 1.85; g.add(head);
        [-1, 1].forEach(s => { const eye = sMesh(new THREE.SphereGeometry(.07, 8, 6), mat(0x111111)); eye.position.set(s * .12, 1.9, .3); g.add(eye); });
        if (ch.id === 'glitch') { const glass = sMesh(new THREE.BoxGeometry(.6, .2, .1), mat(0x111111)); glass.position.set(0, 1.95, .3); g.add(glass); }
        else if (ch.id === 'harold') { [-1, 1].forEach(s => { const t = sMesh(new THREE.ConeGeometry(.08, .4, 8), mat(0xFFFFFF)); t.position.set(s * .25, 1.7, .35); t.rotation.x = 1.5; g.add(t); }); }
        else if (ch.id === 'nampy') { const mask = sMesh(new THREE.BoxGeometry(.7, .3, .1), mat(0x333333)); mask.position.set(0, 1.85, .3); g.add(mask); }
        const t = sMesh(new THREE.SphereGeometry(.15, 8, 8), bm); t.position.set(0, .8, -.45); g.add(t);
        if (isBot) { const a = sMesh(new THREE.CylinderGeometry(.015, .015, .28, 6), mat(0x444444)); a.position.y = 2.45; g.add(a); const bl = sMesh(new THREE.SphereGeometry(.05, 8, 6), mat(0xFF4444)); bl.position.y = 2.55; g.add(bl); }
        if (name) g.add(makeNameTag(name)); return g;
    }

    function buildLobby() {
        lobbyMeshes.forEach(o => scene.remove(o)); lobbyMeshes = []; gameMeshes.forEach(o => scene.remove(o)); gameMeshes = []; interacts = []; stars = []; pads = []; solidPlatforms = [];
        const gnd = sMesh(new THREE.CircleGeometry(110, 60), mat(0x388E3C, 0.5)); gnd.rotation.x = -1.57; addMesh(gnd, true);
        const pR = 20, pH = 1.5, pl = sMesh(new THREE.CylinderGeometry(pR, pR, pH, 32), mat(0xCFD8DC)); pl.position.y = pH / 2; addMesh(pl, true); solidPlatforms.push({ mesh: pl, radius: pR, topY: pH });
        buildPortal(0, 0, -45); buildMirror(45, 0, 0); buildArcade(-45, 0, 0); buildSocial(0, 0, 45);
    }
    function buildSocial(x, y, z) { const g = new THREE.Group(); g.position.set(x, 0, z); g.add(sMesh(new THREE.CylinderGeometry(4, 4.5, 1, 24), mat(0x27ae60))); const t = sMesh(new THREE.TorusGeometry(3.5, 0.3, 12, 32), mat(0x2ecc71)); t.rotation.x = 1.57; t.position.y = 0.5; g.add(t); const i = sMesh(new THREE.IcosahedronGeometry(1.5, 0), mat(0xffffff, .2)); i.position.y = 4.5; i.userData.spin = true; i.userData.bob = true; i.userData.baseY = 4.5; g.add(i); g.userData = { type: 'social', icon: 'group', text: 'SOCIAL HUB' }; addMesh(g, true); interacts.push(g); }
    function buildPortal(x, y, z) { const g = new THREE.Group(); g.position.set(x, y, z); const r = sMesh(new THREE.TorusGeometry(3, .6, 10, 20), mat(0x9C27B0, .3)); r.position.y = 5; r.userData.spin = true; g.add(r); const o = sMesh(new THREE.SphereGeometry(1.6, 14, 12), mat(0x00E5FF, .2)); o.position.y = 5; o.userData.bob = true; o.userData.baseY = 5; g.add(o); g.userData = { type: 'portal', text: 'PLAY GAME', icon: 'rocket_launch', r: 12 }; addMesh(g, true); interacts.push(g); }
    function buildMirror(x, y, z) { const g = new THREE.Group(); g.position.set(x, y, z); g.add(sMesh(new THREE.BoxGeometry(5, 7, .7), mat(0xFFD700, .2))); g.children[0].position.y = 4; const m = sMesh(new THREE.BoxGeometry(4.2, 6, .15), new THREE.MeshStandardMaterial({ color: 0xE8EAF6, metalness: .95, roughness: .05 })); m.position.set(0, 4, .45); g.add(m); g.rotation.y = -1.57; g.userData = { type: 'char', text: 'AVATARS', icon: 'person', r: 10 }; addMesh(g, true); interacts.push(g); }
    function buildArcade(x, y, z) { const g = new THREE.Group(); g.position.set(x, y, z); g.add(sMesh(new THREE.BoxGeometry(5, 6.5, 3), mat(0x1A237E, .5))); g.children[0].position.y = 3.25; const s = sMesh(new THREE.BoxGeometry(3.5, 2.5, .15), mat(0x00E676, .3)); s.position.set(0, 4.5, 1.6); g.add(s); g.rotation.y = 1.57; g.userData = { type: 'arcade', text: 'PRACTICE', icon: 'joystick', r: 10 }; addMesh(g, true); interacts.push(g); }

    function spawnPlayer() { if (player) scene.remove(player); player = makeChar(curC(), 'YOU'); player.position.set(0, 3.5, 22); scene.add(player); }
    function spawnBots(n) { bots.forEach(b => scene.remove(b.mesh)); bots = []; const pool = CHARS.filter(c => c.id !== P.charId); for (let i = 0; i < n; i++) { const ch = pool[i % pool.length], name = BOT_NAMES[i % BOT_NAMES.length], mesh = makeChar(ch, name, true); mesh.position.set(Math.cos(i / n * 6.28) * 25, 5, Math.sin(i / n * 6.28) * 25); bots.push({ mesh, ch, name, emoji: ch.emoji, score: 0, stunned: 0, vel: { x: 0, y: 0, z: 0 }, grounded: false, mem: { bad: [] } }); scene.add(mesh); } }

    function getGroundY(pos) { let gy = 0; solidPlatforms.forEach(sp => { if (d2(pos, sp.mesh.position) < sp.radius) gy = Math.max(gy, sp.topY); }); return gy; }
    function applyPhysics(pos, vel) { if (!grounded) vel.y -= G; pos.x += vel.x; pos.y += vel.y; pos.z += vel.z; const gy = getGroundY(pos); if (pos.y <= gy) { pos.y = gy; vel.y = 0; grounded = true; } else grounded = false; vel.x *= FRC; vel.z *= FRC; }
    function applyBotPhysics(b) {
        if (!b.grounded) b.vel.y -= G;
        b.mesh.position.x += b.vel.x; b.mesh.position.y += b.vel.y; b.mesh.position.z += b.vel.z;
        const gy = getGroundY(b.mesh.position);
        if (b.mesh.position.y <= gy) {
            b.mesh.position.y = gy; b.vel.y = 0; b.grounded = true;
        } else {
            b.grounded = false;
            if (b.mesh.position.y < -20) {
                b.mem.bad.push({ x: b.mesh.position.x, z: b.mesh.position.z });
                b.mesh.position.set(0, 10, 0); b.vel.x = b.vel.y = b.vel.z = 0;
            }
        }
        b.vel.x *= FRC; b.vel.z *= FRC;
    }

    function initControls() {
        mkJoy('joyL', 'knobL', 'l'); mkJoy('joyR', 'knobR', 'r');
        const tap = (id, fn) => { const e=$(id); if (!e) return; e.addEventListener('touchstart', ev => { ev.preventDefault(); fn(); }, { passive: false }); e.addEventListener('click', ev => { ev.preventDefault(); fn(); }); };
        tap('prGo', doInteract); tap('bJump', doJump); tap('bGrab', doGrab); tap('bSkill', doSkill);
    }
    function mkJoy(aId, kId, key) {
        const a = $(aId), k = $(kId); if (!a || !k) return; let tid = null, cx = 0, cy = 0;
        const upd = (x, y) => { let dx = x - cx, dy = y - cy, d = Math.sqrt(dx * dx + dy * dy), r = 50; if (d > r) { dx *= r / d; dy *= r / d; } k.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`; joy[key] = { x: dx / r, y: dy / r }; };
        a.addEventListener('touchstart', ev => { ev.preventDefault(); const t = ev.changedTouches[0]; tid = t.identifier; const r = a.getBoundingClientRect(); cx = r.left + r.width / 2; cy = r.top + r.height / 2; upd(t.clientX, t.clientY); }, { passive: false });
        a.addEventListener('touchmove', ev => { ev.preventDefault(); for (let t of ev.changedTouches) if (t.identifier === tid) upd(t.clientX, t.clientY); }, { passive: false });
        a.addEventListener('touchend', ev => { for (let t of ev.changedTouches) if (t.identifier === tid) { tid = null; k.style.transform = 'translate(-50%,-50%)'; joy[key] = { x: 0, y: 0 }; } }, { passive: false });
        a.addEventListener('mousedown', ev => { const r = a.getBoundingClientRect(); cx = r.left + r.width / 2; cy = r.top + r.height / 2; upd(ev.clientX, ev.clientY); const mv = e => upd(e.clientX, e.clientY), up = () => { document.removeEventListener('mousemove', mv); document.removeEventListener('mouseup', up); k.style.transform = 'translate(-50%,-50%)'; joy[key] = { x: 0, y: 0 }; }; document.addEventListener('mousemove', mv); document.addEventListener('mouseup', up); });
    }

    window.openSocial = function() { show("oSocial"); window.loadSocial(); }
    function doInteract() { if (!near) return; const t = near.userData.type; if (t === 'portal') { show('oPortal'); loadModes(); } else if (t === 'char') { show('oChar'); window.loadChars(); } else if (t === 'arcade') { show('oArcade'); loadArcade(); } else if (t === 'social') { show('oSocial'); window.loadSocial(); } hide('PROMPT'); }


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
    function toggleInvite(btn) {
        const name = btn.dataset.name; const idx = P.invited.indexOf(name);
        if (idx > -1) { P.invited.splice(idx, 1); btn.textContent = 'INVITE'; btn.className = 'px-6 py-2.5 rounded-full text-[10px] font-black tracking-widest transition-all bg-white/10 text-white'; }
        else { if (P.invited.length >= 8) { notify('Lobby Full!', 'bad'); return; } P.invited.push(name); btn.textContent = 'INVITED'; btn.className = 'px-6 py-2.5 rounded-full text-[10px] font-black tracking-widest transition-all bg-primary text-black'; }
        saveData();
    }
    function addFriend(btn) { const name = btn.dataset.name; if (!P.friends.includes(name)) { P.friends.push(name); saveData(); notify('Added ' + name, 'ok'); } btn.innerHTML = '<span class="material-symbols-outlined text-green-400">check</span>'; btn.disabled = true; }

    function loadModes() {
        const el = $('modeList'); if (!el) return; el.innerHTML = '<div class="space-y-4 pt-4"></div>'; const ml = el.firstChild;
        [{ name: 'QUICK PLAY', desc: 'Single random rift', icon: 'bolt' }, { name: 'PARTY MODE', desc: 'Three rift series', icon: 'celebration' }].forEach(m => {
            const c = document.createElement('div'); c.className = 'group p-6 bg-white/5 rounded-[2rem] border-2 border-transparent hover:border-primary transition-all cursor-pointer flex items-center gap-5';
            c.innerHTML = `<div class="size-16 rounded-2xl bg-white/5 flex items-center justify-center border border-white/10"><span class="material-symbols-outlined text-primary text-3xl">${esc(m.icon)}</span></div><div class="flex-1"><h4 class="font-black italic text-lg tracking-tighter group-hover:text-primary transition-colors">${esc(m.name)}</h4><p class="text-[10px] text-gray-500 font-bold uppercase tracking-widest">${esc(m.desc)}</p></div>`;
            c.onclick = () => { hide('oPortal'); rGames = shuffle(GAMES).slice(0, m.name.includes('PARTY') ? 3 : 1); rIdx = 0; startMinigame(rGames[0]); }; ml.appendChild(c);
        });
    }
    function loadArcade() {
        const el = $('oArcade');
        if (!el) return;
        notify('Practice Mode Coming Soon!', 'inf');
    }
    window.loadChars = function() {
        const el = $('charList'); if (!el) return; el.innerHTML = '';
        CHARS.forEach(c => {
            const isSel = c.id === selChar; const item = document.createElement('div'); item.className = 'flex flex-col items-center gap-2';
            item.innerHTML = `<button class="w-full aspect-square bg-white/5 rounded-2xl border-2 ${isSel ? 'border-primary' : 'border-transparent'} transition-all flex items-center justify-center"><img src="${getGvEmoji(c.emoji)}" class="size-8 transform scale-125"></button><span class="text-[9px] font-black ${isSel ? 'text-primary' : 'text-gray-500'} uppercase">${esc(c.name)}</span>`;
            item.onclick = () => { selChar = c.id; window.loadChars(); }; el.appendChild(item);
        });
        updateCharDetail(getC(selChar));
    }
    function updateScoreboard() {
        const sc = [{"name": "YOU", "score": Math.floor(P.score), "emoji": curC().emoji}].concat(bots.map(b => ({ "name": b.name, "score": Math.floor(b.score), "emoji": b.emoji }))).sort((a, b) => b.score - a.score);
        const b = $("sbBody"); if (b) { b.innerHTML = ""; sc.forEach(s => { const row = document.createElement("div"); row.className = "flex items-center justify-between text-[10px] font-black italic tracking-tighter"; row.innerHTML = `<div class="flex items-center gap-2"><img src="${getGvEmoji(s.emoji)}" class="size-4"><span>${esc(s.name)}</span></div><span>${Math.floor(s.score)}</span>`; b.appendChild(row); }); }
    }
    function updateCharDetail(c) {
        const el = $('charDetail'); if (!el) return;
        el.innerHTML = `<h2 class="text-4xl font-black italic tracking-tighter mb-1">${esc(c.name.toUpperCase())}</h2><p class="text-primary text-[10px] font-black tracking-[0.4em] uppercase mb-6">${esc(c.role)}</p><div class="w-full bg-white/5 border border-white/10 rounded-3xl p-5 flex items-center justify-between"><div class="flex items-center gap-4"><div class="size-12 rounded-2xl bg-primary/10 flex items-center justify-center"><img src="${getGvEmoji(c.emoji)}" class="size-8"></div><div class="flex flex-col"><span class="text-[9px] text-gray-500 font-black uppercase">Ability</span><span class="text-white font-black italic text-xl tracking-tighter uppercase">${esc(c.skill)}</span></div></div></div>`;
        $('btnPlayAs').onclick = () => { P.charId = selChar; saveData(); spawnPlayer(); loadData(); hide('oChar'); };
    }

    function doJump() { if (P.stunned > 0 || !grounded) return; pVel.y = JMP * (curC().jmp / 80); grounded = false; }
    function doGrab() { if (P.grabCD > 0) return; P.grabCD = 0.8; bots.forEach(b => { if (d3(player.position, b.mesh.position) < 4) { const dx = b.mesh.position.x - player.position.x, dz = b.mesh.position.z - player.position.z, m = Math.sqrt(dx*dx+dz*dz)||1; b.vel.x += (dx/m) * 0.8; b.vel.z += (dz/m) * 0.8; b.vel.y = 0.2; b.stunned = 1.0; } }); }
    function doSkill() {
        if (P.skillCD > 0 || P.stunned > 0) return; const c = curC(); P.skillCD = c.sCD; cooldown('bSkill', 'cdSkill', c.sCD, 'skillCD');
        const f = new THREE.Vector3(0, 0, -1).applyAxisAngle(new THREE.Vector3(0, 1, 0), player.rotation.y);
        mkParts(player.position.x, 1, player.position.z, c.color, 20);
        showEmoji(player, c.emoji);
        switch (c.sType) {
            case 'tele': player.position.add(f.multiplyScalar(10)); break;
            case 'dash': pVel.x += f.x * 1.5; pVel.z += f.z * 1.5; break;
            case 'jump': pVel.y = .8; grounded = false; break;
            case 'stun': bots.forEach(b => { if (d3(player.position, b.mesh.position) < 10) { b.stunned = 2.5; b.vel.y = .2; } }); break;
            case 'smoke': bots.forEach(b => { if (d3(player.position, b.mesh.position) < 10) { b.stunned = 2; } }); break;
            case 'knock': bots.forEach(b => { if (d3(player.position, b.mesh.position) < 8) { const dx = b.mesh.position.x-player.position.x, dz = b.mesh.position.z-player.position.z, m = Math.sqrt(dx*dx+dz*dz)||1; b.vel.x += (dx/m)*1.5; b.vel.z += (dz/m)*1.5; b.vel.y = 0.4; b.stunned = 1.5; } }); break;
            case 'buff': P.buffTime = 5; notify('POWER UP!', 'ok'); break;
        }
        notify(c.skill.toUpperCase(), 'ok');
    }
    function cooldown(bId, cId, dur, prop) { const b=$(bId); if(b) b.classList.add('cd'); let r=dur; const iv=setInterval(() => { r-=.1; const c=$(cId); if(c) c.textContent=Math.max(0,Math.ceil(r)); if(r<=0) { clearInterval(iv); P[prop]=0; if(b) b.classList.remove('cd'); } }, 100); }

    window.startMinigame = function(game) {
        state = ST.CDOWN; curGame = game; $('hud').style.display = 'none'; show('CDOWN'); setText('cdName', game.name); setText('cdTip', game.tip);
        let cnt = 3; setText('cdNum', '3'); const iv = setInterval(() => { cnt--; if (cnt > 0) setText('cdNum', cnt); else if (cnt === 0) setText('cdNum', 'GO!'); else { clearInterval(iv); hide('CDOWN'); beginGame(); } }, 900);
    }
    function buildArenaScenery() {
        for(let i=0; i<30; i++) {
            const ang = rnd(0, 6.28), dist = rnd(60, 100), x = Math.cos(ang)*dist, z = Math.sin(ang)*dist;
            const r = sMesh(new THREE.DodecahedronGeometry(rnd(2, 5)), mat(0x444444));
            r.position.set(x, 1, z); r.rotation.set(rnd(0,3), rnd(0,3), rnd(0,3)); addMesh(r);
        }
    }
    function buildArena(game) {
        buildArenaScenery();
        lobbyMeshes.forEach(o => scene.remove(o)); lobbyMeshes = []; gameMeshes.forEach(o => scene.remove(o)); gameMeshes = []; interacts = []; stars = []; pads = []; solidPlatforms = [];
        const gnd = sMesh(new THREE.CircleGeometry(120, 60), mat(0x111111)); gnd.rotation.x = -1.57; addMesh(gnd);
        if (game.id === "stars") {
            const r = 40; const ring = sMesh(new THREE.TorusGeometry(r, 1, 12, 64), mat(0xFFD700)); ring.rotation.x = 1.57; addMesh(ring);
            for(let i=0; i<30; i++) spawnStar();
        } else if (game.id === "sumo") {
            const r = 35; hillMesh = sMesh(new THREE.CylinderGeometry(r, r, 1, 64), mat(0xFF4444)); addMesh(hillMesh);
            hillMesh.userData.r = r;
        } else if (game.id === "hill") {
            const r = 15; hillMesh = sMesh(new THREE.CylinderGeometry(r, r, .5, 32), mat(0xFFFF00, .1)); hillMesh.position.y = .1; addMesh(hillMesh);
            hillMesh.userData.r = r;
        } else if (game.id === "pads") {
            const r = 45; for(let i=0; i<padCount; i++) {
                const a = (i/padCount)*6.28, px = Math.cos(a)*r, pz = Math.sin(a)*r;
                const p = sMesh(new THREE.BoxGeometry(6, .5, 6), mat(0x444444)); p.position.set(px, .25, pz); addMesh(p); pads.push(p);
            }
        } else if (game.id === "tag") {
            const r = 50; const ring = sMesh(new THREE.TorusGeometry(r, 1, 12, 64), mat(0xFF00FF)); ring.rotation.x = 1.57; addMesh(ring);
            P.isIt = true; setText("IND", "YOU ARE IT! TAG SOMEONE!"); show("IND");
        }
        player.position.set(0, 5, 0); bots.forEach((b, i) => b.mesh.position.set(Math.cos(i)*20, 5, Math.sin(i)*20));
    }
    function spawnStar() {
        const isGold = Math.random() < 0.2, col = isGold ? 0xFFD700 : 0xFFFFFF;
        const s = sMesh(new THREE.IcosahedronGeometry(isGold ? 1.5 : 1, 0), mat(col, .2));
        const a = Math.random()*6.28, d = Math.random()*38, x = Math.cos(a)*d, z = Math.sin(a)*d;
        s.position.set(x, 1.5, z); s.userData = { type: "star", val: isGold ? 30 : 10, bob: true, baseY: 1.5 }; addMesh(s); stars.push(s);
    }

    function beginGame() { buildArena(curGame);
        state = ST.GAME; gActive = true; gTimer = curGame.dur; show('GHUD'); show('SB'); P.score = 0; bots.forEach(b => b.score = 0);
        const iv = setInterval(() => { if (!gActive) { clearInterval(iv); return; } gTimer--; setText('gTime', Math.max(0, gTimer)); if (gTimer <= 0) { clearInterval(iv); endMinigame(); } }, 1000);
    }
    function endMinigame() { gActive = false; state = ST.RES; hide('GHUD'); hide('SB'); showResults(); }
    function showResults() {
        const sc = [{"name": 'YOU', "score": Math.floor(P.score), "emoji": curC().emoji}].concat(bots.map(b => ({ "name": b.name, "score": Math.floor(b.score), "emoji": b.emoji }))).sort((a, b) => b.score - a.score);
        const r = sc.findIndex(s => s.name === 'YOU') + 1; setText('resT', r === 1 ? 'VICTORY!' : 'NICE JOB!'); setText('resS', `#${r} — ${Math.floor(P.score)} PTS`);
        const p = $('resPod'); if (p) { p.innerHTML = ''; sc.slice(0, 5).forEach((e, i) => { const row = document.createElement('div'); row.className = `flex items-center justify-between p-5 bg-white/5 rounded-3xl border ${e.name === 'YOU' ? 'border-primary/40' : 'border-white/10'}`; row.innerHTML = `<div class="flex items-center gap-3 text-sm font-black italic tracking-tighter"><span class="w-4">${i + 1}</span><img src="${getGvEmoji(e.emoji)}" class="size-8"><span>${esc(e.name)}</span></div><span class="text-xs font-bold text-gray-500">${e.score} PTS</span>`; p.appendChild(row); }); }
        show('RES');
    }
    function backToLobby() { state = ST.LOBBY; hide('RES'); $('hud').style.display = 'flex'; spawnPlayer(); }

    function animate() {
        requestAnimationFrame(animate); const dt = Math.min(clk.getDelta(), .05), t = Date.now() * .001;
        if (P.buffTime > 0) P.buffTime -= dt;
        if (P.sprinting && joy.l.x**2 + joy.l.y**2 > 0.1) { P.stamina = Math.max(0, P.stamina - dt * 25); if (P.stamina <= 0) P.sprinting = false; } else { P.stamina = Math.min(100, P.stamina + dt * 15); }
        particles3d.forEach((p, i) => {
            p.position.x += p.userData.vx; p.position.y += p.userData.vy; p.position.z += p.userData.vz;
            p.userData.vy -= 0.02; p.userData.life -= 0.02;
            p.userData.m.opacity = p.userData.life;
            if (p.userData.life <= 0) { scene.remove(p); particles3d.splice(i, 1); }
        });
        scene.traverse(o => { if (o.userData.spin) o.rotation.y += dt * 2; if (o.userData.bob) o.position.y = (o.userData.baseY || 0) + Math.sin(t * 3) * 0.5; });
        if (state === ST.LOBBY) {
            const inp = joy.l, spd = SPD * 0.75 * ( (P.buffTime > 0 ? 1.4 : 1) * (P.sprinting ? 1.5 : 1)), mag = Math.sqrt(inp.x ** 2 + inp.y ** 2);
            if (mag > .1) { const ang = Math.atan2(inp.x, inp.y) + camAng; pVel.x += Math.sin(ang) * mag * spd * .12; pVel.z += Math.cos(ang) * mag * spd * .12; player.rotation.y = ang; }
            applyPhysics(player.position, pVel); if (Math.abs(joy.r.x) > .1) camAng -= joy.r.x * .035;
            const pd = d2(player.position, {x:0, z:0}); if(pd > 100) { player.position.x *= 100/pd; player.position.z *= 100/pd; }
            let bC = null, bD = Infinity; interacts.forEach(o => { const dd = d3(player.position, o.position); if (dd < (o.userData.r || 10) && dd < bD) { bD = dd; bC = o; } }); near = bC;
            const pr = $("PROMPT"); if (near && !document.querySelector(".overlay.show")) { $("prIcon").innerHTML = `<span class="material-symbols-outlined text-primary text-3xl">${near.userData.icon}</span>`; setText("prText", near.userData.text); pr.style.display = "flex"; } else pr.style.display = "none";
        } else if (state === ST.GAME) {
            const inp = joy.l, spd = SPD * .5 * ( (P.buffTime > 0 ? 1.4 : 1) * (P.sprinting ? 1.5 : 1)), mag = Math.sqrt(inp.x ** 2 + inp.y ** 2);
            if (mag > .1 && P.stunned <= 0) { const ang = Math.atan2(inp.x, inp.y) + camAng; pVel.x += Math.sin(ang) * mag * spd; pVel.z += Math.cos(ang) * mag * spd; player.rotation.y = ang; }
            applyPhysics(player.position, pVel); if (Math.abs(joy.r.x) > .1) camAng -= joy.r.x * .035;
            const pd = d2(player.position, {x:0, z:0}); if(pd > 100) { player.position.x *= 100/pd; player.position.z *= 100/pd; }
            if (curGame.id === "stars") {
                stars.forEach((s, i) => {
                    if (d3(player.position, s.position) < 3) { P.score += s.userData.val; scene.remove(s); stars.splice(i, 1); spawnStar(); notify("+" + s.userData.val, "ok"); }
                    bots.forEach(b => { if (d3(b.mesh.position, s.position) < 3) { b.score += s.userData.val; scene.remove(s); stars.splice(i, 1); spawnStar(); } });
                });
            } else if (curGame.id === "sumo") {
                const r = hillMesh.userData.r * (gTimer < 10 ? 0.5 : 1); hillMesh.scale.set(gTimer < 10 ? 0.5 : 1, 1, gTimer < 10 ? 0.5 : 1);
                if (d2(player.position, hillMesh.position) > r) pVel.y -= 0.05;
                bots.forEach(b => { if (d2(b.mesh.position, hillMesh.position) > r) b.vel.y -= 0.05; else b.score += dt * 10; });
                P.score += dt * 10;
            } else if (curGame.id === "hill") {
                if (d2(player.position, hillMesh.position) < hillMesh.userData.r) P.score += dt * 20;
                if (Math.floor(t) % 5 === 0 && !hillMesh.userData.pulsed) { hillMesh.userData.pulsed = true; flash("GHUD", 200); bots.forEach(b => { if (d2(b.mesh.position, hillMesh.position) < hillMesh.userData.r) { b.vel.y = 0.3; const d = d2(b.mesh.position, hillMesh.position); b.vel.x += (b.mesh.position.x/d)*1; b.vel.z += (b.mesh.position.z/d)*1; } }); }
                if (Math.floor(t) % 5 !== 0) hillMesh.userData.pulsed = false;
                bots.forEach(b => { if (d2(b.mesh.position, hillMesh.position) < hillMesh.userData.r) b.score += dt * 15; });
            } else if (curGame.id === "tag") {
                if (P.isIt) { P.score -= dt * 5; bots.forEach(b => { if (d3(player.position, b.mesh.position) < 3 && P.tagImmune <= 0) { P.isIt = false; b.isIt = true; P.tagImmune = 2; setText("IND", "RUN!"); notify("TAGGED " + b.name, "bad"); } }); }
                if (P.tagImmune > 0) P.tagImmune -= dt;
                bots.forEach(b => { if (b.isIt) { b.score -= dt * 5; if (d3(b.mesh.position, player.position) < 3) { b.isIt = false; P.isIt = true; setText("IND", "YOU ARE IT!"); notify("TAGGED BY " + b.name, "bad"); } } });
            } else if (curGame.id === "pads") {
                if (Math.sin(t) > 0) { musicOn = true; setText("IND", "DANCE!"); } else {
                    if (musicOn) { musicOn = false; setText("IND", "FREEZE!"); pads.forEach(p => p.material.color.set(0x44FF44)); setTimeout(() => { pads.forEach(p => {
                        let occupied = false; if (d2(player.position, p.position) < 3) occupied = true;
                        bots.forEach(b => { if (d2(b.mesh.position, p.position) < 3) occupied = true; });
                        if (!occupied) p.material.color.set(0xFF4444);
                    }); }, 2000); }
                }
            }
            bots.forEach(b => {
                if (b.stunned > 0) { b.stunned -= dt; } else {
                    let target = player.position;
                    if (curGame.id === "stars" && stars.length > 0) target = stars[0].position;
                    else if (curGame.id === "hill") target = hillMesh.position;
                    else if (curGame.id === "sumo") target = hillMesh.position;
                    else if (curGame.id === "tag") target = b.isIt ? player.position : { x: -player.position.x, z: -player.position.z };

                    const dx = target.x - b.mesh.position.x, dz = target.z - b.mesh.position.z, d = Math.sqrt(dx*dx+dz*dz)||1;
                    const s = SPD * 0.78; b.vel.x += (dx/d)*s*0.1; b.vel.z += (dz/d)*s*0.1;
                    b.mesh.rotation.y = Math.atan2(dx, dz);
                }
                applyBotPhysics(b);
            });
            updateScoreboard();
        }
        const tX = player.position.x + Math.sin(camAng) * 22, tZ = player.position.z + Math.cos(camAng) * 22, tY = player.position.y + 16;
        cam.position.x += (tX - cam.position.x) * .12; cam.position.y += (tY - cam.position.y) * .12; cam.position.z += (tZ - cam.position.z) * .12;
        cam.lookAt(player.position.x, player.position.y + 2.5, player.position.z); sun.position.set(player.position.x + 80, 120, player.position.z + 80); sun.target.position.copy(player.position); sun.target.updateMatrixWorld(); ren.render(scene, cam);
    }

    function updSet() { P.settings.shadows = $('sShadow').checked; P.settings.ai = $('sAI').value; P.settings.leftHand = $('sLeft').checked; P.settings.acc = $('sAcc').checked; P.settings.debug = $('sDebug').checked; saveData(); location.reload(); }
    function setPreset(p) { P.preset = p; P.settings.shadows = (p !== 'classic'); saveData(); location.reload(); }
    function startLoad() { let p = 0; const iv = setInterval(() => { p += rnd(16, 28); if (p > 100) p = 100; $('ldFill').style.width = p + '%'; if (p >= 100) { clearInterval(iv); setTimeout(() => { $('LD').classList.add('gone'); state = ST.LOBBY; }, 500); } }, 130); }

    loadData(); initThree(); buildLobby(); spawnPlayer(); spawnBots(5); initControls(); startLoad();
    window.DEBUG = {
        start: id => { const g = GAMES.find(x => x.id === id); if (g) startMinigame(g); },
        gotoLobby: () => backToLobby(),
        setGems: n => { P.gems = n; setText("hGems", n); saveData(); },
        setLv: n => { P.lv = n; setText("hLv", n); saveData(); }
    };
    animate();
</script>
</body>
