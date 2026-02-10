import json

chars_data = [
    {"id": "glitch", "name": "Glitch", "emoji": "😎", "role": "Speed", "color": 0x5C6BC0, "spd": 90, "pow": 50, "jmp": 80, "skill": "Blink", "sType": "tele", "sCD": 5},
    {"id": "tank", "name": "Harold", "emoji": "🦣", "role": "Tank", "color": 0x795548, "spd": 45, "pow": 95, "jmp": 40, "skill": "Quake", "sType": "stun", "sCD": 8},
    {"id": "bear", "name": "Barry", "emoji": "🐻", "role": "Brawler", "color": 0x8D6E63, "spd": 60, "pow": 85, "jmp": 50, "skill": "Roar", "sType": "stun", "sCD": 7},
    {"id": "bunny", "name": "Bibi", "emoji": "🐰", "role": "Jumper", "color": 0xFF80AB, "spd": 85, "pow": 40, "jmp": 95, "skill": "Hop", "sType": "jump", "sCD": 3},
    {"id": "duck", "name": "Ducky", "emoji": "🦆", "role": "Scout", "color": 0xFFEB3B, "spd": 75, "pow": 50, "jmp": 70, "skill": "Dash", "sType": "dash", "sCD": 4},
    {"id": "ninja", "name": "Ninja", "emoji": "🥷", "role": "Stealth", "color": 0x212121, "spd": 85, "pow": 60, "jmp": 90, "skill": "Smoke", "sType": "smoke", "sCD": 6}
]

def get_emoji_url(e):
    return f"data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='50%' x='50%' dy='.35em' text-anchor='middle' font-size='80'>{e}</text></svg>"

js_code = r"""
    const $ = id => document.getElementById(id);
    const getGvEmoji = e => `data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='50%' x='50%' dy='.35em' text-anchor='middle' font-size='80'>${e}</text></svg>`;
    const sMesh = (g, m) => { const e = new THREE.Mesh(g, m); e.castShadow = e.receiveShadow = true; return e; };
    const addMesh = (m, isL = false) => { scene.add(m); (isL ? lobbyMeshes : gameMeshes).push(m); };
    const show = id => { const e=$(id); if(e) e.classList.add('show'); };
    const hide = id => { const e=$(id); if(e) e.classList.remove('show'); };
    const setText = (id, t) => { const e=$(id); if(e) e.textContent=t; };
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

    const CHARS = REPLACE_CHARS;
    const GAMES = [
        { id: 'stars', name: '⭐ STAR COLLECTOR', tip: 'COLLECT STARS! GOLD = 30 PTS!', dur: 50, type: 'collect' },
        { id: 'sumo', name: '💪 SUMO RING', tip: 'PUSH ENEMIES OUT OF THE RING!', dur: 55, type: 'sumo' },
        { id: 'hill', name: '👑 KING OF HILL', tip: 'STAY ON HILL! PULSE EVERY 5S!', dur: 50, type: 'hill' },
        { id: 'tag', name: '🏷️ TAG FRENZY', tip: "GRAB TO PASS THE TAG! DON'T BE IT!", dur: 45, type: 'tag' },
        { id: 'pads', name: '🪑 MUSICAL PADS', tip: 'STAND ON GREEN PAD WHEN MUSIC STOPS!', dur: 70, type: 'pads' }
    ];

    const month = new Date().getMonth();
    const IS_DEC = month === 11, IS_OCT = month === 9, IS_SPRING = month >= 2 && month <= 4;
    const EMOTES = ['😄', '🤣', '😎', '🥷', '🔥', '👑', '💪', '🌟'];
    const ST = { LOAD: 0, LOBBY: 1, CDOWN: 2, GAME: 3, RES: 4 };
    let state = ST.LOAD;

    let P = { gems: 500, crowns: 10, charId: 'glitch', score: 0, isIt: false, tagImmune: 0, skillCD: 0, grabCD: 0, stunned: 0, stamina: 100, sprinting: false, hillTime: 0, lv: 1, xp: 0, buffTime: 0, friends: [], invited: [], preset: 'hd', settings: { shadows: true, ai: 'medium', leftHand: false, acc: false, debug: false } };

    function saveData() { localStorage.setItem('RR_DATA', JSON.stringify({ gems: P.gems, crowns: P.crowns, lv: P.lv, xp: P.xp, charId: P.charId, friends: P.friends, invited: P.invited, preset: P.preset, settings: P.settings })); }
    function loadData() {
        const d = localStorage.getItem('RR_DATA');
        if (d) {
            try {
                const j = JSON.parse(d);
                if (j.settings) Object.assign(P.settings, j.settings);
                if (j.friends) P.friends = j.friends;
                if (j.invited) P.invited = j.invited;
                ['gems', 'crowns', 'lv', 'xp', 'charId', 'preset'].forEach(k => { if (j[k] !== undefined) P[k] = j[k]; });
            } catch (e) {}
        }
        setText('hGems', P.gems); setText('hLv', P.lv); setText('hName', curC().name.toUpperCase());
        const cur = curC(), av = $('hAvatar'); if (av) { av.style.backgroundImage = `url('${getGvEmoji(cur.emoji)}')`; }
        document.documentElement.style.fontSize = P.settings.acc ? "18px" : "16px";
        applyLayout();
        const sS = $('sShadow'), sL = $('sLeft'), sA = $('sAcc'), sD = $('sDebug'), sAi = $('sAI'), sG = $('sGraph');
        if (sS) sS.checked = P.settings.shadows; if (sL) sL.checked = P.settings.leftHand; if (sA) sA.checked = P.settings.acc; if (sD) sD.checked = P.settings.debug; if (sAi) sAi.value = P.settings.ai; if (sG) sG.value = P.preset;
    }

    function applyLayout() {
        const jL = $('joyL'), jR = $('joyR'), bt = $('BTNS'), side = $('SIDE');
        if (P.settings.leftHand) {
            if (jL) { jL.style.left = 'auto'; jL.style.right = '18px'; }
            if (jR) { jR.style.right = 'auto'; jR.style.left = '18px'; }
            if (bt) { bt.style.right = 'auto'; bt.style.left = '18px'; }
        } else {
            if (jL) { jL.style.right = 'auto'; jL.style.left = '18px'; }
            if (jR) { jR.style.left = 'auto'; jR.style.right = '18px'; }
            if (bt) { bt.style.left = 'auto'; bt.style.right = '18px'; }
        }
    }

    let selChar = 'glitch', scene, cam, ren, clk, sun, camAng = 0, pVel = { x: 0, y: 0, z: 0 }, grounded = true, near = null, curGame = null, gTimer = 0, gActive = false, rGames = [], rIdx = 0, musicOn = true, padCount = 16, scoreT = 0, shakeAmt = 0;
    const BOT_NAMES = ['ZIPPY', 'BOUNCER', 'SPARKY', 'GLIMMER', 'TURBO', 'RIFTY', 'ECHO', 'NOVA', 'PIXEL', 'GLITCHY', 'TANKER', 'FROSTY', 'SHADOW', 'BLAZE', 'BOLT', 'AURA', 'RUSTY', 'COMET', 'PULSE', 'ZEN'];
    var player, bots = [], lobbyMeshes = [], gameMeshes = [], stars = [], pads = [], solidPlatforms = [], hillMesh = null, interacts = [], particles3d = [];
    const G = .025, SPD = .12, JMP = .38, FRC = .86;
    const joy = { l: { x: 0, y: 0 }, r: { x: 0, y: 0 } };

    function getC(id) { return CHARS.find(c => c.id === id) || CHARS[0]; }
    function curC() { return getC(P.charId); }

    function initThree() {
        scene = new THREE.Scene();
        let skyCol = 0x1a2a4a; if (P.preset === 'deluxe') skyCol = 0xFFB74D; else if (IS_DEC) skyCol = 0x0a1a2a; else if (IS_OCT) skyCol = 0x0d0208; else if (IS_SPRING) skyCol = 0x81D4FA;
        scene.background = new THREE.Color(skyCol); scene.fog = new THREE.FogExp2(skyCol, P.preset === 'deluxe' ? .008 : .005);
        cam = new THREE.PerspectiveCamera(55, innerWidth / innerHeight, .1, 800);
        ren = new THREE.WebGLRenderer({ canvas: $('C'), antialias: true }); ren.setSize(innerWidth, innerHeight); ren.setPixelRatio(Math.min(devicePixelRatio, 2));
        ren.shadowMap.enabled = P.settings.shadows; ren.shadowMap.type = THREE.PCFSoftShadowMap;
        ren.toneMapping = THREE.ACESFilmicToneMapping; ren.toneMappingExposure = P.preset === 'deluxe' ? 1.6 : 1.2;
        clk = new THREE.Clock();
        scene.add(new THREE.AmbientLight(0xFFE0B2, P.preset === 'deluxe' ? 1.0 : 0.5));
        sun = new THREE.DirectionalLight(0xfff5e0, P.preset === 'deluxe' ? 1.8 : 1.1); sun.position.set(80, 120, 80);
        if (P.settings.shadows) { sun.castShadow = true; sun.shadow.mapSize.width = sun.shadow.mapSize.height = 2048; }
        scene.add(sun); scene.add(new THREE.HemisphereLight(0x6699cc, 0x334455, .5));
    }

    function mat(c, r = .5) { if (P.preset === 'classic') return new THREE.MeshLambertMaterial({ color: c }); return new THREE.MeshStandardMaterial({ color: c, roughness: r, metalness: (P.preset === 'deluxe' ? 0.2 : 0.1) }); }

    function makeNameTag(name) {
        const canvas = document.createElement('canvas'); canvas.width = 256; canvas.height = 64; const ctx = canvas.getContext('2d');
        ctx.fillStyle = 'rgba(0,0,0,0.6)'; ctx.roundRect(0, 0, 256, 64, 32); ctx.fill();
        ctx.font = 'black 34px Spline Sans, sans-serif'; ctx.fillStyle = '#f2f20d'; ctx.textAlign = 'center'; ctx.fillText(name, 128, 44);
        const tex = new THREE.CanvasTexture(canvas); const sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true }));
        sprite.scale.set(3, 0.75, 1); sprite.position.y = 3.2; return sprite;
    }

    function makeChar(ch, name = '', isBot = false) {
        const g = new THREE.Group(), col = ch.color, bm = mat(col, .3);
        const body = sMesh(new THREE.CylinderGeometry(.4, .44, .7, 12), bm); body.position.y = 1; g.add(body);
        const top = sMesh(new THREE.SphereGeometry(.4, 12, 10), bm); top.position.y = 1.35; g.add(top);
        const bot = sMesh(new THREE.SphereGeometry(.44, 12, 10), bm); bot.position.y = .65; g.add(bot);
        const head = sMesh(new THREE.SphereGeometry(.36, 16, 14), mat(0xFFDFC4, .45)); head.position.y = 1.85; g.add(head);
        [-1, 1].forEach(s => { const eye = sMesh(new THREE.SphereGeometry(.07, 8, 6), mat(0x111111)); eye.position.set(s * .12, 1.9, .3); g.add(eye); });
        if (ch.id === 'glitch') { [-1, 1].forEach(s => { const e = sMesh(new THREE.SphereGeometry(.12, 8, 8), mat(0x222222)); e.position.set(s * .25, 2.15, 0); g.add(e); }); }
        else if (ch.id === 'tank' || ch.id === 'bear') { [-1, 1].forEach(s => { const e = sMesh(new THREE.SphereGeometry(.15, 8, 8), bm); e.position.set(s * .25, 2.1, 0); g.add(e); }); }
        else if (ch.id === 'bunny') { [-1, 1].forEach(s => { const e = sMesh(new THREE.CylinderGeometry(.08, .08, .6, 8), bm); e.position.set(s * .15, 2.3, 0); e.rotation.z = s * .2; g.add(e); }); }
        else if (ch.id === 'duck') { const b = sMesh(new THREE.BoxGeometry(.2, .1, .25), mat(0xFF9800)); b.position.set(0, 1.8, .35); g.add(b); }
        const t = sMesh(new THREE.SphereGeometry(.15, 8, 8), bm); t.position.set(0, .8, -.45); g.add(t);
        const h = sMesh(new THREE.ConeGeometry(.28, .45, 8), mat(0xE74C3C, .4)); h.position.y = 2.2; h.rotation.z = .12; g.add(h);
        if (isBot) { const a = sMesh(new THREE.CylinderGeometry(.015, .015, .28, 6), mat(0x444444)); a.position.y = 2.45; g.add(a); const bl = sMesh(new THREE.SphereGeometry(.05, 8, 6), mat(0xFF4444)); bl.position.y = 2.55; g.add(bl); }
        if (name) g.add(makeNameTag(name)); return g;
    }

    function buildLobby() {
        lobbyMeshes.forEach(o => scene.remove(o)); lobbyMeshes = []; gameMeshes.forEach(o => scene.remove(o)); gameMeshes = []; interacts = []; stars = []; pads = []; solidPlatforms = [];
        if (IS_DEC) buildDecLobby(); else if (IS_OCT) buildOctLobby(); else if (IS_SPRING) buildSpringLobby(); else buildDefaultLobby();
        buildBanners();
    }
    function buildBanners() { for (let i = 0; i < 8; i++) { const a = i / 8 * 6.28, r = 40, g = new THREE.Group(); g.position.set(Math.cos(a) * r, 10, Math.sin(a) * r); const p = sMesh(new THREE.CylinderGeometry(.1, .1, 10), mat(0x333333)); p.position.y = -5; g.add(p); const f = sMesh(new THREE.BoxGeometry(3, 2, .1), mat(Math.random() * 0xffffff)); f.position.set(1.5, 0, 0); g.add(f); addMesh(g, true); } }
    function addLobbyDeco() { for (let i = 0; i < 15; i++) { const a = rnd(0, 6.2), r = rnd(15, 45), h = 10 + rnd(0, 10), g = new THREE.Group(); g.position.set(Math.cos(a) * r, h, Math.sin(a) * r); const b = sMesh(new THREE.SphereGeometry(0.7, 12, 10), mat(Math.random() * 0xffffff, 0.3)); g.add(b); const s = sMesh(new THREE.CylinderGeometry(0.02, 0.02, 15), mat(0xcccccc)); s.position.y = -7.5; g.add(s); g.userData = { bob: true, baseY: h }; addMesh(g, true); } }
    function buildDecLobby() { const g = sMesh(new THREE.CircleGeometry(110, 60), mat(0xE8F4F8, .8)); g.rotation.x = -1.57; addMesh(g, true); const pR = 18, pH = 3, pl = sMesh(new THREE.CylinderGeometry(pR, pR + 2, pH, 32), mat(0x6D4C41, .5)); pl.position.y = pH / 2; addMesh(pl, true); solidPlatforms.push({ mesh: pl, radius: pR + 2, topY: pH }); buildXmasTree(0, pH, 0); buildPortal(0, 0, -42); buildMirror(42, 0, 0); buildArcade(-42, 0, 0); buildSocial(0, 0, 42); }
    function buildOctLobby() { const g = sMesh(new THREE.CircleGeometry(110, 60), mat(0x1a0a00)); g.rotation.x = -1.57; addMesh(g, true); const pR = 20, pH = 1.5, pl = sMesh(new THREE.CylinderGeometry(pR, pR, pH, 32), mat(0x3e2723)); pl.position.y = pH / 2; addMesh(pl, true); solidPlatforms.push({ mesh: pl, radius: pR, topY: pH }); const p = new THREE.Group(); p.position.set(0, pH, 0); const b = sMesh(new THREE.SphereGeometry(4, 16, 12), mat(0xff6d00, .2)); b.scale.y = 0.8; b.position.y = 3; p.add(b); const s = sMesh(new THREE.CylinderGeometry(0.3, 0.5, 1.5, 8), mat(0x1b5e20)); s.position.y = 6; p.add(s); p.add(new THREE.PointLight(0xffab40, 3, 30)); addMesh(p, true); buildPortal(0, 0, -45); buildMirror(45, 0, 0); buildArcade(-45, 0, 0); buildSocial(0, 0, 45); }
    function buildSpringLobby() { const g = sMesh(new THREE.CircleGeometry(110, 60), mat(0x66bb6a)); g.rotation.x = -1.57; addMesh(g, true); const pR = 20, pH = 1.5, pl = sMesh(new THREE.CylinderGeometry(pR, pR, pH, 32), mat(0xfff176)); pl.position.y = pH / 2; addMesh(pl, true); solidPlatforms.push({ mesh: pl, radius: pR, topY: pH }); buildPortal(0, 0, -45); buildMirror(45, 0, 0); buildArcade(-45,0, 0); buildSocial(0, 0, 45); }
    function buildDefaultLobby() { const g = sMesh(new THREE.CircleGeometry(110, 60), mat(0x388E3C)); g.rotation.x = -1.57; addMesh(g, true); const pR = 20, pH = 1.5, pl = sMesh(new THREE.CylinderGeometry(pR, pR, pH, 32), mat(0xCFD8DC)); pl.position.y = pH / 2; addMesh(pl, true); solidPlatforms.push({ mesh: pl, radius: pR, topY: pH }); const f = new THREE.Group(); f.position.set(0, pH, 0); f.add(sMesh(new THREE.CylinderGeometry(5, 5, 0.8, 24), mat(0x90A4AE))); const m = sMesh(new THREE.CylinderGeometry(1, 1, 3, 16), mat(0x90A4AE)); m.position.y = 1.5; f.add(m); const w = sMesh(new THREE.SphereGeometry(2.5, 16, 12, 0, 6.28, 0, 1.57), mat(0x29B6F6, .6)); w.position.y = 3; f.add(w); f.add(new THREE.PointLight(0x29B6F6, 2, 25)); addMesh(f, true); addLobbyDeco(); buildPortal(0, 0, -45); buildMirror(45, 0, 0); buildArcade(-45, 0, 0); buildSocial(0, 0, 45); }
    function buildXmasTree(x, y, z) { const g = new THREE.Group(); g.position.set(x, y, z); g.add(sMesh(new THREE.CylinderGeometry(1, 1.5, 3, 10), mat(0x5D4037, .8))); g.children[0].position.y = 1.5; for (let i = 0; i < 4; i++) { const l = sMesh(new THREE.ConeGeometry(5.5 - i, 4.5, 12), mat(0x2E7D32, .7)); l.position.y = 4.5 + i * 3; g.add(l); } const s = sMesh(new THREE.OctahedronGeometry(1), mat(0xFFD700, .2)); s.position.y = 18; s.userData.spin = true; g.add(s); scene.add(g); lobbyMeshes.push(g); }
    function buildSocial(x, y, z) { const g = new THREE.Group(); g.position.set(x, 0, z); g.add(sMesh(new THREE.CylinderGeometry(4, 4.5, 1, 24), mat(0x27ae60))); const t = sMesh(new THREE.TorusGeometry(3.5, 0.3, 12, 32), mat(0x2ecc71)); t.rotation.x = 1.57; t.position.y = 0.5; g.add(t); const i = sMesh(new THREE.IcosahedronGeometry(1.5, 0), mat(0xffffff, .2)); i.position.y = 4.5; i.userData.spin = true; i.userData.bob = true; i.userData.baseY = 4.5; g.add(i); g.add(new THREE.PointLight(0x2ecc71, 2, 15)); g.userData = { type: 'social', icon: '👥', text: 'FRIENDS' }; addMesh(g, true); interacts.push(g); }
    function buildPortal(x, y, z) { const g = new THREE.Group(); g.position.set(x, y, z); for (let i = 0; i < 3; i++) { const s = sMesh(new THREE.CylinderGeometry(8 - i, 8.5 - i, .6, 14), mat(0xE0E0E0, .3)); s.position.y = .3 + i * .6; g.add(s); } const r = sMesh(new THREE.TorusGeometry(3, .6, 10, 20), mat(0x9C27B0, .3)); r.position.y = 5; r.userData.spin = true; g.add(r); const o = sMesh(new THREE.SphereGeometry(1.6, 14, 12), mat(0x00E5FF, .2)); o.position.y = 5; o.userData.bob = true; o.userData.baseY = 5; g.add(o); g.userData = { type: 'portal', text: 'ENTER PORTAL', icon: '🌀', r: 12 }; addMesh(g, true); interacts.push(g); }
    function buildMirror(x, y, z) { const g = new THREE.Group(); g.position.set(x, y, z); g.add(sMesh(new THREE.BoxGeometry(5, 7, .7), mat(0xFFD700, .2))); g.children[0].position.y = 4; const m = sMesh(new THREE.BoxGeometry(4.2, 6, .15), new THREE.MeshStandardMaterial({ color: 0xE8EAF6, metalness: .95, roughness: .05 })); m.position.set(0, 4, .45); g.add(m); g.rotation.y = -1.57; g.userData = { type: 'char', text: 'CHOOSE RUNNER', icon: '🎭', r: 10 }; addMesh(g, true); interacts.push(g); }
    function buildArcade(x, y, z) { const g = new THREE.Group(); g.position.set(x, y, z); g.add(sMesh(new THREE.BoxGeometry(5, 6.5, 3), mat(0x1A237E, .5))); g.children[0].position.y = 3.25; const s = sMesh(new THREE.BoxGeometry(3.5, 2.5, .15), mat(0x00E676, .3)); s.position.set(0, 4.5, 1.6); g.add(s); g.rotation.y = 1.57; g.userData = { type: 'arcade', text: 'PRACTICE', icon: '🕹️', r: 10 }; addMesh(g, true); interacts.push(g); }

    function spawnPlayer() { if (player) scene.remove(player); player = makeChar(curC(), 'YOU'); player.position.set(0, 3.5, 22); scene.add(player); if (P.charId === 'ninja') player.traverse(o => { if (o.isMesh) { o.material = o.material.clone(); o.material.transparent = true; o.material.opacity = 0.5; } }); }
    function spawnBots(n) { bots.forEach(b => scene.remove(b.mesh)); bots = []; const pool = CHARS.filter(c => c.id !== P.charId); const names = [...P.invited]; while (names.length < n) { const rn = BOT_NAMES[Math.floor(Math.random() * BOT_NAMES.length)]; if (!names.includes(rn)) names.push(rn); } for (let i = 0; i < n; i++) { const ch = pool[i % pool.length], name = names[i], mesh = makeChar(ch, name, true); mesh.position.set(Math.cos((i + 1) / (n + 1) * 6.28) * (22 + rnd(0, 10)), 10, Math.sin((i + 1) / (n + 1) * 6.28) * (22 + rnd(0, 10))); bots.push({ mesh, ch, name, emoji: ch.emoji, color: ch.color, score: 0, isIt: false, tagImmune: 0, stunned: 0, vel: { x: 0, y: 0, z: 0 }, grounded: false, eliminated: false, hillTime: 0, target: null, aiTimer: 0, skillCD: 0, mem: { bad: [] } }); scene.add(mesh); } }

    function getGroundY(pos) { let gy = 0; solidPlatforms.forEach(sp => { if (d2(pos, sp.mesh.position) < sp.radius) gy = Math.max(gy, sp.topY); }); if (hillMesh && d2(pos, hillMesh.mesh.position) < hillMesh.radius) gy = Math.max(gy, hillMesh.topY); return gy; }
    function applyPhysics(pos, vel) { if (!grounded) vel.y -= G; pos.x += vel.x; pos.y += vel.y; pos.z += vel.z; const gy = getGroundY(pos); if (pos.y <= gy) { pos.y = gy; vel.y = 0; grounded = true; } else grounded = false; vel.x *= FRC; vel.z *= FRC; }
    function applyBotPhysics(b) { if (!b.grounded) b.vel.y -= G; b.mesh.position.x += b.vel.x; b.mesh.position.y += b.vel.y; b.mesh.position.z += b.vel.z; const gy = getGroundY(b.mesh.position); if (b.mesh.position.y <= gy) { b.mesh.position.y = gy; b.vel.y = 0; b.grounded = true; } else b.grounded = false; b.vel.x *= FRC; b.vel.z *= FRC; }

    function initControls() {
        mkJoy('joyL', 'knobL', 'l'); mkJoy('joyR', 'knobR', 'r');
        const tap = (id, fn) => { const e=$(id); if (!e) return; e.addEventListener('touchstart', ev => { ev.preventDefault(); ev.stopPropagation(); fn(); }, { passive: false }); e.addEventListener('click', ev => { ev.preventDefault(); fn(); }); };
        tap('prGo', doInteract); tap('bJump', doJump); tap('bGrab', doGrab); tap('bSkill', doSkill);
        const emPop = $('emPop'), emGrid = $('emoteGrid'); if (emGrid) EMOTES.forEach(e => { const b = document.createElement('button'); b.className = 'size-11 rounded-xl bg-white/5 hover:bg-white/10 flex items-center justify-center transition-all active:scale-90 shadow-lg'; b.innerHTML = `<img src="${getGvEmoji(e)}" class="size-7">`; b.onclick = () => { showEmoji(player, e); emPop.classList.add('hidden'); }; emGrid.appendChild(b); });
        tap('bEmote', () => emPop.classList.toggle('hidden'));
        const sp = $('bSprint'); if (sp) { const on = () => { P.sprinting = true; sp.classList.add('bg-primary'); }; const off = () => { P.sprinting = false; sp.classList.remove('bg-primary'); }; sp.addEventListener('touchstart', ev => { ev.preventDefault(); on(); }, { passive: false }); sp.addEventListener('touchend', off); sp.addEventListener('mousedown', on); sp.addEventListener('mouseup', off); }
    }
    function mkJoy(aId, kId, key) {
        const a = $(aId), k = $(kId); if (!a || !k) return; let tid = null, cx = 0, cy = 0;
        const upd = (x, y) => { let dx = x - cx, dy = y - cy, d = Math.sqrt(dx * dx + dy * dy), r = 50; if (d > r) { dx *= r / d; dy *= r / d; } k.style.transform = `translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`; joy[key] = { x: dx / r, y: dy / r }; };
        a.addEventListener('touchstart', ev => { ev.preventDefault(); const t = ev.changedTouches[0]; tid = t.identifier; const r = a.getBoundingClientRect(); cx = r.left + r.width / 2; cy = r.top + r.height / 2; upd(t.clientX, t.clientY); }, { passive: false });
        a.addEventListener('touchmove', ev => { ev.preventDefault(); for (let t of ev.changedTouches) if (t.identifier === tid) upd(t.clientX, t.clientY); }, { passive: false });
        a.addEventListener('touchend', ev => { for (let t of ev.changedTouches) if (t.identifier === tid) { tid = null; k.style.transform = 'translate(-50%,-50%)'; joy[key] = { x: 0, y: 0 }; } }, { passive: false });
        a.addEventListener('mousedown', ev => { const r = a.getBoundingClientRect(); cx = r.left + r.width / 2; cy = r.top + r.height / 2; upd(ev.clientX, ev.clientY); const mv = e => upd(e.clientX, e.clientY), up = () => { document.removeEventListener('mousemove', mv); document.removeEventListener('mouseup', up); k.style.transform = 'translate(-50%,-50%)'; joy[key] = { x: 0, y: 0 }; }; document.addEventListener('mousemove', mv); document.addEventListener('mouseup', up); });
    }

    function doInteract() { if (!near) return; const t = near.userData.type; if (t === 'portal') { show('oPortal'); loadModes(); } else if (t === 'char') { show('oChar'); loadChars(); } else if (t === 'arcade') { show('oArcade'); loadArcade(); } else if (t === 'social') { show('oSocial'); loadSocial(); } $('PROMPT')?.classList.remove('show'); }
    function loadSocial() {
        const el = $('socialList'); if (!el) return; el.innerHTML = ''; if (P.friends.length === 0) { el.innerHTML = '<div class="py-12 text-center text-gray-500 font-bold uppercase tracking-widest text-[10px]">No friends yet.<br>Add bots after a game!</div>'; return; }
        P.friends.forEach(name => { const isInv = P.invited.includes(name); const row = document.createElement('div'); row.className = 'flex items-center justify-between p-5 bg-white/5 rounded-3xl border border-white/5 mb-3'; row.innerHTML = `<div class="flex items-center gap-3"><div class="size-11 rounded-full bg-white/10 flex items-center justify-center"><img src="${getGvEmoji('🤖')}" class="size-7"></div><span class="font-black italic tracking-tighter text-sm">${name}</span></div><button class="px-5 py-2.5 rounded-full text-[10px] font-black tracking-widest transition-all ${isInv ? 'bg-primary text-black' : 'bg-white/10 text-white'}" onclick="toggleInvite('${name}', this)">${isInv ? 'INVITED' : 'INVITE'}</button>`; el.appendChild(row); });
    }
    function toggleInvite(name, btn) { const idx = P.invited.indexOf(name); if (idx > -1) { P.invited.splice(idx, 1); btn.textContent = 'INVITE'; btn.className = 'px-5 py-2.5 rounded-full text-[10px] font-black tracking-widest transition-all bg-white/10 text-white'; } else { if (P.invited.length >= 8) { notify('MAX 8 INVITED!', 'bad'); return; } P.invited.push(name); btn.textContent = 'INVITED'; btn.className = 'px-5 py-2.5 rounded-full text-[10px] font-black tracking-widest transition-all bg-primary text-black'; } saveData(); }
    function loadModes() {
        const el = $('modeList'); if (!el) return; el.innerHTML = '<div class="space-y-4 pt-4"></div>'; const ml = el.firstChild;
        [{ name: 'QUICK PLAY', desc: 'One random rift', cnt: 1, icon: '⚡' }, { name: 'PARTY MODE', desc: 'Three random rifts', cnt: 3, icon: '🎉' }].forEach(m => {
            const c = document.createElement('div'); c.className = 'group p-6 bg-white/5 rounded-[2rem] border-2 border-transparent hover:border-primary transition-all cursor-pointer flex items-center gap-5';
            c.innerHTML = `<div class="size-16 rounded-2xl bg-white/5 flex items-center justify-center border border-white/10 shadow-lg"><img src="${getGvEmoji(m.icon)}" class="size-10"></div><div class="flex-1"><h4 class="font-black italic text-lg leading-none mb-1 group-hover:text-primary transition-colors tracking-tighter">${m.name}</h4><p class="text-[10px] text-gray-500 font-bold uppercase tracking-widest">${m.desc}</p></div><span class="material-symbols-outlined text-gray-700 group-hover:text-primary">arrow_forward_ios</span>`;
            c.onclick = () => { hide('oPortal'); rGames = shuffle(GAMES).slice(0, m.cnt); rIdx = 0; setTimeout(() => startMinigame(rGames[0]), 300); }; ml.appendChild(c);
        });
    }
    function loadChars() { const el = $('charList'); if (!el) return; el.innerHTML = ''; CHARS.forEach(c => { const isSel = c.id === selChar, item = document.createElement('div'); item.className = 'group relative flex flex-col items-center gap-2'; item.innerHTML = `${isSel ? '<div class="absolute -top-1 -right-1 z-10 bg-primary text-black rounded-full p-1 shadow-lg shadow-primary/20"><span class="material-symbols-outlined text-xs font-black block">check</span></div>' : ''}<button class="w-full aspect-square bg-white/5 rounded-2xl border-2 ${isSel ? 'border-primary shadow-[0_0_20px_rgba(242,242,13,0.15)]' : 'border-transparent hover:border-white/10'} transition-all flex items-center justify-center relative overflow-hidden">${isSel ? '<div class="absolute inset-0 bg-primary/5"></div>' : ''}<div class="w-full h-full bg-center bg-contain bg-no-repeat transform scale-75" style="background-image: url('${getGvEmoji(c.emoji)}');"></div></button><span class="text-[9px] font-black ${isSel ? 'text-primary' : 'text-gray-500 group-hover:text-white'} transition-colors uppercase tracking-widest">${c.name}</span>`; item.onclick = () => { selChar = c.id; loadChars(); }; el.appendChild(item); }); updateCharDetail(getC(selChar)); }
    function updateCharDetail(c) {
        const el = $('charDetail'); if (!el) return;
        const stats = [['POWER', 'fitness_center', c.pow], ['SPEED', 'bolt', c.spd], ['JUMP', 'stat_2', c.jmp]];
        el.innerHTML = `<h2 class="text-white text-5xl font-black italic tracking-tighter leading-none mb-1">${c.name.toUpperCase()}</h2><p class="text-primary text-[10px] font-black tracking-[0.4em] uppercase mb-10">${c.role}</p><div class="grid grid-cols-3 w-full gap-3 mb-10">${stats.map(s => `<div class="flex flex-col items-center gap-2 p-4 rounded-3xl bg-white/5 border border-white/5"><div class="size-11 rounded-full bg-white/5 flex items-center justify-center text-gray-400 mb-1"><span class="material-symbols-outlined filled text-xl tracking-tighter">${s[1]}</span></div><div class="text-center"><p class="text-[8px] font-black text-gray-500 uppercase tracking-widest">${s[0]}</p><div class="h-1 w-12 bg-white/5 rounded-full mt-1.5 overflow-hidden"><div class="h-full bg-primary rounded-full shadow-[0_0_8px_#f2f20d]" style="width:${s[2]}%"></div></div></div></div>`).join('')}</div><div class="w-full bg-white/5 border border-white/10 rounded-3xl p-5 flex items-center justify-between gap-4"><div class="flex items-center gap-4"><div class="size-12 rounded-2xl bg-primary/10 flex items-center justify-center border border-primary/20"><img src="${getGvEmoji(c.emoji)}" class="size-8"></div><div class="flex flex-col"><span class="text-[9px] text-gray-500 font-black uppercase tracking-[0.2em]">Ability</span><span class="text-white font-black italic text-xl tracking-tighter uppercase">${c.skill}</span></div></div></div>`;
        $('btnPlayAs').onclick = () => { if (P.charId !== selChar) { P.charId = selChar; saveData(); spawnPlayer(); loadData(); } hide('oChar'); };
    }
    function loadArcade() {
        const el = $('modeList'); if (!el) return; el.innerHTML = '<div class="grid grid-cols-2 gap-3 pt-4"></div>'; const ml = el.firstChild;
        GAMES.forEach(g => { const c = document.createElement('div'); c.className = 'p-5 bg-white/5 rounded-3xl border border-white/5 hover:border-primary/30 transition-all cursor-pointer text-center group'; c.innerHTML = `<div class="size-16 mx-auto mb-3 bg-white/5 rounded-2xl flex items-center justify-center group-hover:scale-110 transition-transform"><img src="${getGvEmoji(g.name.split(' ')[0])}" class="size-10"></div><div class="font-black italic text-[10px] tracking-widest uppercase">${g.name}</div>`; c.onclick = () => { hide('oArcade'); curGame = g; setTimeout(() => startMinigame(g), 300); }; ml.appendChild(c); });
    }

    function doJump() { if (P.stunned > 0 || !grounded) return; pVel.y = JMP * (curC().jmp / 80); grounded = false; mkParts(player.position.x, .3, player.position.z, 0xFFFFFF, 15); }
    function doPush() { if (P.grabCD > 0) return; P.grabCD = 0.8; const targets = bots.filter(b => !b.eliminated); let p = false; targets.forEach(b => { if (d3(player.position, b.mesh.position) < 4.5) { const dx = b.mesh.position.x - player.position.x, dz = b.mesh.position.z - player.position.z, m = Math.sqrt(dx * dx + dz * dz) || 1; b.vel.x += (dx / m) * 0.65; b.vel.z += (dz / m) * 0.65; b.vel.y = 0.28; b.stunned = 1.2; p = true; } }); if (p) { flash('bGrab', 200); mkParts(player.position.x, 1.5, player.position.z, 0xffffff, 15); } }
    function doGrab() { doPush(); }
    function doSkill() {
        if (P.skillCD > 0 || P.stunned > 0) return; if (state !== ST.GAME && state !== ST.LOBBY) return; const c = curC(); P.skillCD = c.sCD; cooldown('bSkill', 'cdSkill', c.sCD, 'skillCD'); const f = new THREE.Vector3(0, 0, -1).applyAxisAngle(new THREE.Vector3(0, 1, 0), player.rotation.y);
        switch (c.sType) {
            case 'tele': mkParts(player.position.x, 1.5, player.position.z, 0x00FFFF, 20); player.position.add(f.multiplyScalar(10)); mkParts(player.position.x, 1.5, player.position.z, 0x00FFFF, 30); break;
            case 'dash': pVel.x += f.x * 1.3; pVel.z += f.z * 1.3; flash('SPEED', 500); mkParts(player.position.x, 1, player.position.z, 0x4ECDC4, 25); break;
            case 'jump': pVel.y = .75; grounded = false; mkParts(player.position.x, .3, player.position.z, 0xFF69B4, 25); break;
            case 'stun': bots.forEach(b => { if (d3(player.position, b.mesh.position) < 12) { b.stunned = 2.5; b.vel.y = .22; mkParts(b.mesh.position.x, 1.5, b.mesh.position.z, 0xFFD700, 20); showEmoji(b.mesh, '💫'); } }); shakeAmt = .8; break;
            case 'smoke': mkParts(player.position.x, 1.5, player.position.z, 0x333333, 50); bots.forEach(b => { if (d3(player.position, b.mesh.position) < 10) { b.stunned = 2; showEmoji(b.mesh, '❓'); } }); player.visible = false; setTimeout(() => player.visible = true, 3000); break;
            case 'buff': P.buffTime = 5; notify('POWER UP!', 'ok'); flash('SPEED', 5000); mkParts(player.position.x, 2, player.position.z, 0xFF0000, 30); break;
        }
        notify(c.skill.toUpperCase() + '!', 'inf'); showEmoji(player, c.emoji);
    }
    function cooldown(bId, cId, dur, prop) { const b = $(bId); if (b) b.classList.add('cd'); let r = dur; const iv = setInterval(() => { r -= .1; const c = $(cId); if (c) c.textContent = Math.max(0, Math.ceil(r)); if (r <= 0) { clearInterval(iv); P[prop] = 0; if (b) b.classList.remove('cd'); } }, 100); }

    function startMinigame(game) {
        state = ST.CDOWN; curGame = game; scoreT = 0; musicOn = true; padCount = 16; hillMesh = null; $('hud').style.display = 'none'; $('MM')?.classList.remove('show'); $('PROMPT')?.classList.remove('show'); $('SIDE').style.display = 'flex';
        const gb = $('bGrab'); if (gb) gb.classList.toggle('hidden', game.type === 'collect' || game.type === 'pads'); lobbyMeshes.forEach(o => o.visible = false); player.visible = false; bots.forEach(b => b.mesh.visible = false); solidPlatforms = []; buildArena(game);
        setText('cdName', game.name); setText('cdTip', game.tip); show('CDOWN');
        let cnt = 3; setText('cdNum', '3'); $('cdNum').className = 'cd-num';
        const iv = setInterval(() => { cnt--; if (cnt > 0) setText('cdNum', cnt); else if (cnt === 0) { setText('cdNum', 'GO!'); $('cdNum').className = 'cd-num cd-go'; } else { clearInterval(iv); hide('CDOWN'); beginGame(); } }, 900);
    }
    function beginGame() {
        state = ST.GAME; gActive = true; gTimer = curGame.dur; show('GHUD'); setText('gTitle', curGame.name); show('SB'); $('BTNS').style.display = 'flex';
        P.score = 0; P.isIt = false; P.tagImmune = 0; P.stamina = 100; P.hillTime = 0; P.sprinting = false;
        bots.forEach(b => { b.score = 0; b.isIt = false; b.tagImmune = 0; b.eliminated = false; b.mesh.visible = true; b.stunned = 0; b.hillTime = 0; b.aiTimer = 0; b.skillCD = rnd(3, 6); });
        if (curGame.type === 'tag') { const it = bots[Math.floor(Math.random() * bots.length)]; it.isIt = true; it.tagImmune = 4; updInd(); }
        if (curGame.type === 'pads') { resetPads(); updInd(); }
        const tEl = $('gTime'); const iv = setInterval(() => { if (!gActive) { clearInterval(iv); return; } gTimer--; if (tEl) { tEl.textContent = Math.max(0, gTimer); tEl.className = 'g-time'; if (gTimer <= 10) tEl.classList.add('danger'); else if (gTimer <= 20) tEl.classList.add('warn'); } if (curGame?.type === 'pads' && gTimer % 11 === 0 && gTimer > 0 && gTimer < curGame.dur) { musicOn = !musicOn; if (!musicOn) { padCount = Math.max(2, padCount - 2); notify('🎵 STOP!', 'inf'); setTimeout(() => checkPads(), 1200); } else { notify('🎵 DANCE!', 'inf'); resetPads(); } updInd(); } if (gTimer <= 0) { clearInterval(iv); endMinigame(); } }, 1000);
    }

    function buildArena(game) {
        lobbyMeshes.forEach(o => scene.remove(o)); lobbyMeshes = []; gameMeshes.forEach(o => scene.remove(o)); gameMeshes = []; stars = []; pads = []; hillMesh = null; solidPlatforms = [];
        const bgMap = { collect: 0x0D47A1, sumo: 0x3E2723, hill: 0xBF360C, tag: 0x01579B, pads: 0x4A148C }; scene.background = new THREE.Color(bgMap[game.type] || 0x1a2a4a); scene.fog = new THREE.FogExp2(bgMap[game.type] || 0x1a2a4a, .004);
        const R = game.type === 'sumo' ? 50 : 85; const gnd = sMesh(new THREE.CircleGeometry(R, 60), mat({ collect: 0x2E7D32, sumo: 0x5D4037, hill: 0xBF360C, tag: 0x006064, pads: 0x4A148C }[game.type] || 0x2E7D32, .8)); gnd.rotation.x = -1.57; addMesh(gnd, false);
        const bor = sMesh(new THREE.TorusGeometry(R, 1.5, 10, 60), mat(0xFFD700, .4)); bor.rotation.x = 1.57; bor.position.y = .75; addMesh(bor, false);
        if (game.type === 'collect') { for (let i = 0; i < 55; i++) spawnStar(); for (let i = 0; i < 5; i++) { const a = i / 5 * 6.28, r = 40, x = Math.cos(a) * r, z = Math.sin(a) * r, p = sMesh(new THREE.CylinderGeometry(8, 8, 4, 16), mat(0x1B5E20)); p.position.set(x, 2, z); addMesh(p, false); solidPlatforms.push({ mesh: p, radius: 8, topY: 4 }); } }
        if (game.type === 'hill') { const hm = sMesh(new THREE.CylinderGeometry(16, 20, 10, 32), mat(0xFFD700, .35)); hm.position.y = 4; scene.add(hm); gameMeshes.push(hm); hillMesh = { mesh: hm, radius: 15.5, topY: 9 }; const cr = sMesh(new THREE.ConeGeometry(3, 4, 5), mat(0xFFD700, .2)); cr.position.y = 11; cr.userData.spin = true; cr.userData.bob = true; cr.userData.baseY = 11; scene.add(cr); gameMeshes.push(cr); for (let i = 0; i < 4; i++) { const a = i / 4 * 6.28, r = 40, x = Math.cos(a) * r, z = Math.sin(a) * r, p = sMesh(new THREE.CylinderGeometry(8, 8, 4, 16), mat(0xBF360C)); p.position.set(x, 2, z); addMesh(p); solidPlatforms.push({ mesh: p, radius: 8, topY: 4 }); } }
        if (game.type === 'pads') { const sz = 4, sp = 12, off = -(sz - 1) * sp / 2; for (let x = 0; x < sz; x++) for (let z = 0; z < sz; z++) { const p = sMesh(new THREE.CylinderGeometry(6, 6.5, 1.5, 16), mat(0x9C27B0, .35)); p.position.set(off + x * sp, .6, off + z * sp); p.userData = { active: true, idx: x * sz + z }; scene.add(p); gameMeshes.push(p); pads.push(p); solidPlatforms.push({ mesh: p, radius: 6, topY: 1.35 }); } }
        if (game.type === 'tag') { for (let i = 0; i < 8; i++) { const a = i / 8 * 6.28, r = 30, x = Math.cos(a) * r, z = Math.sin(a) * r, p = sMesh(new THREE.BoxGeometry(6, 12, 6), mat(0x006064)); p.position.set(x, 6, z); addMesh(p); solidPlatforms.push({ mesh: p, radius: 4, topY: 12 }); } }
        if (game.type === 'sumo') { for (let i = 0; i < 6; i++) { const a = i / 6 * 6.28 + rnd(-.3, .3), r = 12 + rnd(0, 10), p = sMesh(new THREE.DodecahedronGeometry(rnd(3, 5)), mat(0x5D4037)); p.position.set(Math.cos(a) * r, 2, Math.sin(a) * r); p.rotation.set(rnd(0, 6), rnd(0, 6), rnd(0, 6)); addMesh(p); solidPlatforms.push({ mesh: p, radius: 4, topY: 4 }); } }
        player.visible = true; player.position.set(0, 10, 28); pVel = { x: 0, y: 0, z: 0 }; grounded = false;
        bots.forEach((b, i) => { b.mesh.visible = true; b.eliminated = false; b.mesh.position.set(Math.cos((i + 1) / (bots.length + 1) * 6.28) * (22 + rnd(0, 10)), 10, Math.sin((i + 1) / (bots.length + 1) * 6.28) * (22 + rnd(0, 10))); b.vel = { x: 0, y: 0, z: 0 }; b.stunned = 0; b.grounded = false; });
    }
    function spawnStar() {
        const g = Math.random() < .12; const v = g ? 30 : 10; const sh = new THREE.Shape(); for (let i = 0; i < 10; i++) { const r = i % 2 === 0 ? .8 : .38, a = i / 10 * 6.28 - 1.57; if (i === 0) sh.moveTo(Math.cos(a) * r, Math.sin(a) * r); else sh.lineTo(Math.cos(a) * r, Math.sin(a) * r); } sh.closePath();
        const m = g ? new THREE.MeshStandardMaterial({ color: 0xFFD700, metalness: 0.8, roughness: 0.2 }) : mat(0xFFFFFF, 0.3);
        const s = sMesh(new THREE.ExtrudeGeometry(sh, { depth: .35, bevelEnabled: false }), m); if (g) s.scale.setScalar(1.5); s.position.set(Math.cos(rnd(0, 6.28)) * rnd(10, 60), 2.5, Math.sin(rnd(0, 6.28)) * rnd(10, 60)); s.rotation.x = 1.57; s.userData = { val: v, off: rnd(0, 6.28) }; scene.add(s); gameMeshes.push(s); stars.push(s);
    }

    function runBotAI(dt) {
        const bSpd = SPD * .78 * (curGame?.type === 'pads' ? .6 : 1) * (curGame?.type === 'sumo' ? .7 : 1) * (P.settings.ai === 'hard' ? 1.2 : P.settings.ai === 'easy' ? 0.7 : 1);
        bots.forEach((b, idx) => {
            if (b.eliminated) { b.mesh.visible = true; return; } if (b.stunned > 0) { b.stunned -= dt; return; } if (b.tagImmune > 0) b.tagImmune -= dt;
            if (!b.skillCD) b.skillCD = rnd(5, 10); b.skillCD -= dt;
            if (b.skillCD <= 0 && !b.stunned && state === ST.GAME) {
                const dP = d3(b.mesh.position, player.position); let trig = false;
                if (['stun', 'smoke'].includes(b.ch.sType) && dP < 8) trig = true; else if (['dash', 'tele', 'jump'].includes(b.ch.sType) && b.target && d3(b.mesh.position, b.target) > 15) trig = true; else if (b.ch.sType === 'buff' && Math.random() < .3) trig = true;
                if (trig) {
                    b.skillCD = b.ch.sCD + rnd(2, 5); const f = new THREE.Vector3(0, 0, -1).applyAxisAngle(new THREE.Vector3(0, 1, 0), b.mesh.rotation.y);
                    switch (b.ch.sType) {
                        case 'tele': b.mesh.position.add(f.multiplyScalar(8)); break;
                        case 'dash': b.vel.x += f.x * 0.8; b.vel.z += f.z * 0.8; break;
                        case 'jump': b.vel.y = 0.3; b.grounded = false; break;
                        case 'stun': if (dP < 10) { P.stunned = 2; flash('STUMBLE', 500); showEmoji(player, '💫'); } bots.forEach(o => { if (o !== b && d3(b.mesh.position, o.mesh.position) < 10) { o.stunned = 2; showEmoji(o.mesh, '💫'); } }); break;
                        case 'smoke': if (dP < 10) { P.stunned = 1.5; showEmoji(player, '❓'); } bots.forEach(o => { if (o !== b && d3(b.mesh.position, o.mesh.position) < 10) { o.stunned = 1.5; showEmoji(o.mesh, '❓'); } }); b.mesh.visible = false; setTimeout(() => b.mesh.visible = true, 2000); break;
                        case 'buff': b.score += 20; showEmoji(b.mesh, '🎁'); break;
                    }
                    showEmoji(b.mesh, b.ch.emoji);
                }
            }
            if (state === ST.LOBBY && d2(b.mesh.position, { x: 0, z: 0 }) < 10) { if (b.grounded && Math.random() < 0.05) { b.vel.y = 0.25; b.grounded = false; } }
            if (b.mesh.position.y < -5) { b.mem.bad.push({ x: b.mesh.position.x, z: b.mesh.position.z }); if (b.mem.bad.length > 10) b.mem.bad.shift(); b.mesh.position.set(0, 5, 0); b.vel.set(0, 0, 0); }
            b.aiTimer -= dt;
            if (b.aiTimer <= 0) {
                b.aiTimer = rnd(.3, 1);
                if (curGame?.type === 'collect') { let bS = null, bD = Infinity; stars.forEach(s => { if (!s.userData.taken) { const dd = d3(b.mesh.position, s.position); if (dd < bD) { bD = dd; bS = s; } } }); if (bS) b.target = { x: bS.position.x, z: bS.position.z }; }
                else if (curGame?.type === 'hill') { b.target = { x: rnd(-5, 5), z: rnd(-5, 5) }; }
                else if (curGame?.type === 'tag') { if (b.isIt) { let bS = null, bD = Infinity; if (!P.isIt && P.tagImmune <= 0) { const dd = d2(b.mesh.position, player.position); if (dd < bD) { bD = dd; bS = player.position; } } bots.forEach(o => { if (o !== b && !o.isIt && !o.eliminated && o.tagImmune <= 0) { const dd = d2(b.mesh.position, o.mesh.position); if (dd < bD) { bD = dd; bS = o.mesh.position; } } }); if (bS) b.target = { x: bS.x, z: bS.z }; } else { const it = bots.find(o => o.isIt) || (P.isIt ? player : null); if (it) { const p = it.position || it.mesh?.position; if (p) { const dx = b.mesh.position.x - p.x, dz = b.mesh.position.z - p.z, dd = Math.sqrt(dx * dx + dz * dz); if (dd > .1) b.target = { x: b.mesh.position.x + (dx / dd) * 22, z: b.mesh.position.z + (dz / dd) * 22 }; } } } }
                else if (curGame?.type === 'pads' && !musicOn) { const ac = pads.filter(p => p.userData.active); if (ac.length > 0) b.target = { x: ac[idx % ac.length].position.x, z: ac[idx % ac.length].position.z }; }
                else if (curGame?.type === 'sumo') { if (Math.random() > .4) { b.target = { x: player.position.x, z: player.position.z }; } else { const o = bots.filter(x => x !== b && !x.eliminated); if (o.length) b.target = { x: o[Math.floor(Math.random() * o.length)].mesh.position.x, z: o[Math.floor(Math.random() * o.length)].mesh.position.z }; } }
                else b.target = { x: rnd(-35, 35), z: rnd(-35, 35) };
            }
            if (b.target) { let tx = b.target.x, tz = b.target.z; b.mem.bad.forEach(s => { if (d2(b.mesh.position, s) < 8) { const dx = b.mesh.position.x - s.x, dz = b.mesh.position.z - s.z, d = Math.sqrt(dx * dx + dz * dz) || 1; tx += (dx / d) * 15; tz += (dz / d) * 15; } }); const dx = tx - b.mesh.position.x, dz = tz - b.mesh.position.z, dd = Math.sqrt(dx * dx + dz * dz); if (dd > 1.2) { b.mesh.position.x += (dx / dd) * bSpd; b.mesh.position.z += (dz / dd) * bSpd; b.mesh.rotation.y = Math.atan2(dx, dz); } }
            applyBotPhysics(b);
            const bd = d2(b.mesh.position, { x: 0, z: 0 }), sR = (curGame?.type === 'sumo' ? 28 : 70); if (bd > sR) { if (curGame?.type === 'sumo') { b.score = Math.max(0, b.score - 50); b.mesh.position.set(Math.cos(rnd(0, 6.28)) * 15, 0, Math.sin(rnd(0, 6.28)) * 15); } else { b.mesh.position.x *= sR / bd; b.mesh.position.z *= sR / bd; } }
            stars.forEach(s => { if (!s.userData.taken && d3(b.mesh.position, s.position) < 3) { s.userData.taken = true; scene.remove(s); b.score += s.userData.val; if (state === ST.GAME && curGame?.type === 'collect') setTimeout(() => spawnStar(), 4000); } });
            if (curGame?.type === 'tag' && b.isIt && b.tagImmune <= 0) {
                if (!P.isIt && P.tagImmune <= 0 && d3(b.mesh.position, player.position) < 3) { b.isIt = false; P.isIt = true; P.tagImmune = 3; notify("YOU'RE IT! -50", 'bad'); P.score = Math.max(0, P.score - 50); b.score += 100; updInd(); }
                bots.forEach(o => { if (o !== b && !o.isIt && !o.eliminated && o.tagImmune <= 0 && d3(b.mesh.position, o.mesh.position) < 3) { b.isIt = false; o.isIt = true; o.tagImmune = 3; b.score += 100; o.score = Math.max(0, o.score - 50); updInd(); } });
            }
            if (curGame?.type === 'hill' && hillMesh) { const hd = d2(b.mesh.position, { x: 0, z: 0 }); if (hd < hillMesh.radius && b.mesh.position.y >= hillMesh.topY - .5) { b.hillTime = (b.hillTime || 0) + dt; if (b.hillTime >= 1) { b.score += 1; b.hillTime -= 1; } if (b.hillTime >= 5) { b.vel.x += Math.cos(rnd(0, 6.28)) * .5; b.vel.z += Math.sin(rnd(0, 6.28)) * .5; b.vel.y = .25; b.hillTime = 0; } } else b.hillTime = 0; }
        });
    }

    function updateMinigame(dt) {
        if (!gActive) return; if (P.tagImmune > 0) P.tagImmune -= dt; if (!P.sprinting && P.stamina < 100) P.stamina = Math.min(100, P.stamina + 22 * dt); scoreT += dt; if (P.buffTime > 0) P.buffTime -= dt;
        const t = Date.now() * .001; gameMeshes.forEach(o => { if (o.userData.bob) o.position.y = (o.userData.baseY || 4) + Math.sin(t * 2) * .5; if (curGame?.type === 'hill' && o.geometry.type === 'ConeGeometry') o.scale.setScalar(1 + Math.sin(t * 5) * 0.1); if (o.userData.spin) o.rotation.y += dt; });
        stars.forEach(s => { if (!s.userData.taken) { s.position.y = 2.5 + Math.sin(t * 3 + s.userData.off) * .5; s.rotation.z += dt * 5; if (d3(player.position, s.position) < 3) { s.userData.taken = true; scene.remove(s); P.score += s.userData.val; mkParts(s.position.x, s.position.y, s.position.z, 0xFFD700, 18); if (state === ST.GAME && curGame?.type === 'collect') setTimeout(() => spawnStar(), 4000); } } });
        if (curGame?.type === 'hill' && hillMesh) { const hd = d2(player.position, { x: 0, z: 0 }); if (hd < hillMesh.radius && player.position.y >= hillMesh.topY - .5) { P.hillTime += dt; if (P.hillTime >= 1) { P.score += 1; P.hillTime -= 1; } if (P.hillTime >= 5) { P.stunned = 0.5; pVel.x += Math.cos(rnd(0, 6.28)) * .6; pVel.z += Math.sin(rnd(0, 6.28)) * .6; pVel.y = .3; P.hillTime = 0; notify('KNOCKED OFF!', 'inf'); mkParts(player.position.x, 1.5, player.position.z, 0xFFD700, 20); } } else P.hillTime = 0; }
        if (curGame?.type === 'sumo') { const pd = d2(player.position, { x: 0, z: 0 }), sR = 40; if (gTimer < curGame.dur - 10) { const sh = 1 - (curGame.dur - 10 - gTimer) / 100, cR = Math.max(15, 40 * sh); if (gameMeshes[0]) gameMeshes[0].scale.set(cR / 40, 1, cR / 40); if (gameMeshes[1]) gameMeshes[1].scale.set(cR / 40, 1, cR / 40); if (pd > cR) { P.score = Math.max(0, P.score - 50); player.position.set(0, 0, 0); flash('STUMBLE', 350); } bots.forEach(b => { if (!b.eliminated && d2(b.mesh.position, { x: 0, z: 0 }) > cR) { b.score = Math.max(0, b.score - 50); b.mesh.position.set(0, 0, 0); } }); } }
        if (curGame?.type === 'tag') { const pd = d2(player.position, { x: 0, z: 0 }); if (pd > 70) { player.position.x *= 70 / pd; player.position.z *= 70 / pd; } if (P.isIt && P.tagImmune <= 0) { bots.forEach(b => { if (!b.isIt && !b.eliminated && b.tagImmune <= 0 && d3(player.position, b.mesh.position) < 3) { P.isIt = false; b.isIt = true; b.tagImmune = 3; P.tagImmune = 2; notify('TAGGED ' + b.name + '!', 'ok'); P.score += 100; b.score = Math.max(0, b.score - 50); updInd(); } }); } }
        if (curGame?.type === 'pads' && musicOn) { const pd = d2(player.position, { x: 0, z: 0 }); if (pd > 70) { player.position.x *= 70 / pd; player.position.z *= 70 / pd; } }
        if (curGame?.type === 'collect') { const pd = d2(player.position, { x: 0, z: 0 }); if (pd > 70) { player.position.x *= 70 / pd; player.position.z *= 70 / pd; } }
        runBotAI(dt); updateSB(); updateMM();
    }

    function getAllScores() { return [{"name": 'YOU', "score": Math.floor(P.score), "emoji": curC().emoji, "color": curC().color, "isPlayer": true, "isIt": P.isIt}, ...bots.map(b => ({ "name": b.name, "score": Math.floor(b.score), "emoji": b.emoji, "color": b.color, "isPlayer": false, "isIt": b.isIt, "eliminated": b.eliminated }))].sort((a, b) => b.score - a.score); }
    function updateSB() { const b = $('sbBody'); if (!b) return; b.innerHTML = ''; getAllScores().slice(0, 10).forEach((e, i) => { const d = document.createElement('div'); d.className = `flex justify-between items-center text-[10px] ${e.isPlayer ? 'text-primary font-black' : 'text-white/70 font-bold'}`; d.innerHTML = `<span>${i + 1}. ${e.name}</span><span>${e.score}</span>`; b.appendChild(d); }); }
    function updateMM() { const mm = $('MM'); if (!mm) return; mm.classList.add('show'); mm.querySelectorAll('.mm-dot').forEach(d => d.remove()); bots.forEach(b => { if (b.eliminated) return; const dx = b.mesh.position.x - player.position.x, dz = b.mesh.position.z - player.position.z; if (Math.abs(dx) < 60 && Math.abs(dz) < 60) { const d = document.createElement('div'); d.className = 'absolute size-1.5 rounded-full bg-red-500 border border-white'; d.style.left = (50 + dx * .65) + '%'; d.style.top = (50 + dz * .65) + '%'; mm.appendChild(d); } }); }
    function endMinigame() { gActive = false; state = ST.RES; hide('GHUD'); hide('SB'); hide('IND'); $('BTNS').style.display = 'none'; showResults(); }
    function addFriend(name, btn) { if (!P.friends.includes(name)) { P.friends.push(name); saveData(); } btn.textContent = 'FRIENDS ✅'; btn.classList.add('bg-white/10', 'text-gray-500'); btn.classList.remove('bg-primary', 'text-black'); btn.disabled = true; }
    function showResults() {
        const sc = getAllScores(), r = sc.findIndex(s => s.isPlayer) + 1, won = r === 1; setText('resT', won ? 'VICTORY!' : 'NICE WORK!'); setText('resS', `#${r} — ${Math.floor(P.score)} PTS`);
        const p = $('resPod'); if (p) { p.innerHTML = ''; sc.slice(0, 5).forEach((e, i) => { const isF = P.friends.includes(e.name), row = document.createElement('div'); row.className = `flex items-center justify-between p-5 bg-white/5 rounded-3xl border border-white/10 ${e.isPlayer ? 'border-primary/40 bg-primary/5' : ''}`; row.innerHTML = `<div class="flex items-center gap-3 text-sm font-black italic tracking-tighter"><span class="${i == 0 ? 'text-primary' : 'text-gray-600'} w-4">${i + 1}</span><img src="${getGvEmoji(e.emoji)}" class="size-8"><span>${e.name}</span></div><div class="flex items-center gap-3"><span class="text-xs font-bold text-gray-500">${e.score} PTS</span>${e.isPlayer ? '' : `<button class="px-4 py-2 rounded-full text-[9px] font-black tracking-widest ${isF ? 'bg-white/10 text-gray-600' : 'bg-primary text-black'}" onclick="addFriend('${e.name}', this)">${isF ? 'FRIENDS' : 'ADD'}</button>`}</div>`; p.appendChild(row); }); }
        const shards = won ? 180 : 50 + r * 15; P.gems += shards; setText('hGems', P.gems); const rr = $('resRew'); if (rr) rr.innerHTML = `<div class="bg-primary/20 border-2 border-primary px-8 py-4 rounded-[2rem] flex items-center gap-3 shadow-2xl shadow-primary/10"><span class="text-3xl font-bold">💎</span><span class="text-primary font-black text-2xl tracking-tighter">+${shards}</span></div>`;
        show('RES'); if (won) for (let i = 0; i < 50; i++) setTimeout(() => { const c = document.createElement('div'); c.className = 'fixed text-2xl pointer-events-none z-[600] animate-bounce'; c.textContent = '🎉'; c.style.left = rnd(0, 100) + 'vw'; c.style.top = '-50px'; c.style.animation = `snow ${rnd(3, 5)}s linear forwards`; $('PARTS')?.appendChild(c); setTimeout(() => c.remove(), 5000); }, i * 40);
        const nx = $('resNext'); if (nx) { nx.textContent = (rGames && rGames.length > 0 && rIdx < rGames.length - 1) ? 'NEXT RIFT' : 'PLAY AGAIN'; nx.onclick = () => { hide('RES'); if (rGames && rGames.length > 0 && rIdx < rGames.length - 1) { rIdx++; setTimeout(() => startMinigame(rGames[rIdx]), 400); } else backToLobby(); }; }
    }
    function backToLobby() {
        state = ST.LOBBY; curGame = null; rGames = []; rIdx = 0; hillMesh = null; hide('RES'); $('hud').style.display = 'flex'; hide('IND'); $('SIDE').style.display = 'none'; $('bGrab')?.classList.remove('hidden'); scene.background = new THREE.Color(0x1a2a4a); scene.fog = new THREE.FogExp2(0x1a2a4a, .005);
        buildLobby(); spawnPlayer(); pVel = { x: 0, y: 0, z: 0 }; bots.forEach((b, i) => { b.mesh.visible = true; b.eliminated = false; b.mesh.position.set(Math.cos((i + 1) / (bots.length + 1) * 6.28) * 24, 0, Math.sin((i + 1) / (bots.length + 1) * 6.28) * 24); });
    }
    function mkParts(x, y, z, col, n) { for (let i = 0; i < n; i++) { const m = new THREE.MeshBasicMaterial({ color: col, transparent: true, opacity: .9 }), p = sMesh(new THREE.SphereGeometry(.15, 8, 6), m); p.position.set(x, y, z); p.userData = { vx: rnd(-.5, .5), vy: rnd(.2, .55), vz: rnd(-.5, .5), life: 1, m }; scene.add(p); particles3d.push(p); } }
    function showEmoji(parent, text) {
        const canvas = document.createElement('canvas'); canvas.width = 128; canvas.height = 128; const ctx = canvas.getContext('2d'); ctx.font = '80px serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(text, 64, 64);
        const tex = new THREE.CanvasTexture(canvas), sprite = new THREE.Sprite(new THREE.SpriteMaterial({ map: tex, transparent: true })); sprite.position.y = 3.2; sprite.scale.set(2, 2, 2); parent.add(sprite); let start = Date.now(); const ani = () => { let age = (Date.now() - start) / 2000; if (age >= 1) { parent.remove(sprite); return; } sprite.position.y = 3.2 + age * 1.5; sprite.material.opacity = 1 - age; requestAnimationFrame(ani); }; ani();
    }
    function animate() {
        requestAnimationFrame(animate); const dt = Math.min(clk.getDelta(), .05), t = Date.now() * .001;
        if (P.settings.debug) { const fEl = $("fps"); if (fEl) { fEl.style.display = "block"; fEl.textContent = "FPS: " + Math.round(1 / dt); } }
        if (P.grabCD > 0) P.grabCD -= dt; if (P.skillCD > 0) P.skillCD -= dt;
        if (state === ST.LOBBY) {
            const c = curC(), inp = joy.l, sprint = P.sprinting ? 1.4 : 1, spd = SPD * (c.spd / 80) * sprint * 0.75, mag = Math.sqrt(inp.x ** 2 + inp.y ** 2);
            if (mag > .1) { const ang = Math.atan2(inp.x, inp.y) + camAng; pVel.x += Math.sin(ang) * mag * spd * .12; pVel.z += Math.cos(ang) * mag * spd * .12; player.rotation.y = ang; player.rotation.z = Math.sin(t * 15) * 0.1; player.rotation.x = Math.sin(t * 10) * 0.05; } else { player.rotation.z *= 0.8; player.rotation.x *= 0.8; }
            applyPhysics(player.position, pVel); const pd = d2(player.position, { x: 0, z: 0 }); if (pd > 100) { player.position.x *= 100 / pd; player.position.z *= 100 / pd; } if (Math.abs(joy.r.x) > .1) camAng -= joy.r.x * .035;
            let bC = null, bD = Infinity; interacts.forEach(o => { const dd = d3(player.position, o.position); if (dd < (o.userData.r || 10) && dd < bD) { bD = dd; bC = o; } }); near = bC; const pr = $('PROMPT'); if (near && !document.querySelector('.overlay.show')) { $('prIcon').innerHTML = `<img src="${getGvEmoji(near.userData.icon)}" class="size-8">`; setText('prText', near.userData.text); pr?.classList.add('flex'); pr?.classList.remove('hidden'); } else { pr?.classList.add('hidden'); pr?.classList.remove('flex'); }
            updateMM(); lobbyMeshes.forEach(o => { if (o.userData?.spin) o.rotation.y += dt; if (o.userData?.bob) o.position.y = (o.userData.baseY || 4) + Math.sin(t * 2) * .4; });
            bots.forEach(b => { if (Math.random() < .01 || !b.target) b.target = { x: rnd(-40, 40), z: rnd(-40, 40) }; const dx = b.target.x - b.mesh.position.x, dz = b.target.z - b.mesh.position.z, dd = Math.sqrt(dx * dx + dz * dz); if (dd > 1.5) { b.mesh.position.x += (dx / dd) * .05; b.mesh.position.z += (dz / dd) * .05; b.mesh.rotation.y = Math.atan2(dx, dz); } applyBotPhysics(b); });
        } else if (state === ST.GAME) {
            if (gActive && P.stunned <= 0) {
                const c = curC(), inp = joy.l, sprint = (P.sprinting && P.stamina > 0 ? 1.4 : 1) * (P.buffTime > 0 ? 1.3 : 1); if (P.sprinting && P.stamina > 0) P.stamina = Math.max(0, P.stamina - dt * 30);
                const spd = SPD * (c.spd / 80) * sprint * .42 * (curGame?.type === 'pads' ? !musicOn ? 0.15 : 0.7 : 1), mag = Math.sqrt(inp.x ** 2 + inp.y ** 2);
                if (mag > .1) { const ang = Math.atan2(inp.x, inp.y) + camAng; pVel.x += Math.sin(ang) * mag * spd; pVel.z += Math.cos(ang) * mag * spd; player.rotation.y = ang; player.rotation.z = Math.sin(t * 15) * 0.15; player.rotation.x = Math.sin(t * 10) * 0.1; } else { player.rotation.z *= 0.8; player.rotation.x *= 0.8; }
                if (Math.abs(joy.r.x) > .1) camAng -= joy.r.x * .035; if (P.sprinting && mag > .3) flash('SPEED', 80);
            } else if (P.stunned > 0) P.stunned -= dt;
            applyPhysics(player.position, pVel); updateMinigame(dt);
        }
        for (let i = particles3d.length - 1; i >= 0; i--) { const p = particles3d[i]; p.position.x += p.userData.vx; p.position.y += p.userData.vy; p.position.z += p.userData.vz; p.userData.vy -= .025; p.userData.life -= dt * 4; if (p.userData.m) p.userData.m.opacity = p.userData.life; if (p.userData.life <= 0) { scene.remove(p); particles3d.splice(i, 1); } }
        const tX = player.position.x + Math.sin(camAng) * 22, tZ = player.position.z + Math.cos(camAng) * 22, tY = player.position.y + 16;
        cam.position.x += (tX - cam.position.x) * .12; cam.position.y += (tY - cam.position.y) * .12; cam.position.z += (tZ - cam.position.z) * .12; if (shakeAmt > 0) { cam.position.x += rnd(-shakeAmt, shakeAmt); cam.position.y += rnd(-shakeAmt, shakeAmt); shakeAmt *= .8; if (shakeAmt < .01) shakeAmt = 0; }
        cam.lookAt(player.position.x, player.position.y + 2.5, player.position.z); if (sun) { sun.position.set(player.position.x + 80, 120, player.position.z + 80); sun.target.position.copy(player.position); sun.target.updateMatrixWorld(); } ren.render(scene, cam);
    }

    function updSet() {
        const s = P.settings, oS = s.shadows, oP = P.preset, oA = s.acc;
        s.shadows = $('sShadow').checked; s.ai = $('sAI').value; s.leftHand = $('sLeft').checked; s.acc = $('sAcc').checked; s.debug = $('sDebug').checked; P.preset = $('sGraph')?.value || P.preset;
        saveData(); if (s.acc !== oA) document.documentElement.style.fontSize = s.acc ? "18px" : "16px";
        applyLayout(); if (s.shadows !== oS || P.preset !== oP) if (confirm("Reload to apply graphics?")) location.reload();
    }
    function setPreset(p) { P.preset = p; P.settings.shadows = (p !== 'classic'); const sg = $('sGraph'), ss = $('sShadow'); if (sg) sg.value = p; if (ss) ss.checked = P.settings.shadows; saveData(); location.reload(); }
    function startLoad() {
        let p = 0; const iv = setInterval(() => { p += rnd(16, 28); if (p > 100) p = 100; const f = $('ldFill'); if (f) f.style.width = p + '%'; if (p >= 100) { clearInterval(iv); setTimeout(() => { $('LD')?.classList.add('gone'); state = ST.LOBBY; }, 500); } }, 130);
    }
    function updInd() { const ind = $('IND'); if (!ind) return; if (curGame?.type === 'pads') { ind.textContent = musicOn ? '🎵 DANCE!' : '⛔ STOP! ON GREEN!'; ind.style.color = musicOn ? '#fff' : '#f00'; ind.style.display = 'block'; } else if (curGame?.type === 'tag') { ind.textContent = P.isIt ? "⚠️ YOU'RE IT! TAG SOMEONE!" : '✅ SAFE'; ind.style.color = P.isIt ? '#f00' : '#fff'; ind.style.display = 'block'; } else ind.style.display = 'none'; }
    function resetPads() { pads.forEach(p => { p.material.color.setHex(0x9C27B0); p.userData.active = true; }); }
    function checkPads() {
        const w = new Set(); pads.forEach(p => { let c = 0; if (d2(player.position, p.position) < 6 && player.position.y >= .5) { w.add('player'); c++; } bots.forEach(b => { if (d2(b.mesh.position, p.position) < 6 && b.mesh.position.y >= .5) { w.add(b.name); c++; } }); if (c > 0) p.material.color.setHex(0x44FF44); else { p.userData.active = false; p.material.color.setHex(0x333333); } });
        if (w.has('player')) { P.score += 25; notify('SAFE! +25', 'ok'); } else { P.score = Math.max(0, P.score - 40); flash('STUMBLE', 350); notify('NO PAD! -40', 'bad'); }
        bots.forEach(b => { if (!b.eliminated) { if (w.has(b.name)) b.score += 25; else b.score = Math.max(0, b.score - 40); } }); setTimeout(() => { musicOn = true; resetPads(); updInd(); }, 2000);
    }

    loadData(); initThree(); buildLobby(); spawnPlayer(); spawnBots(5); initControls(); startLoad();
    window.DEBUG = { gotoLobby: () => backToLobby(), start: id => { let g = (typeof id === "number") ? GAMES[id] : GAMES.find(x => x.id === id); if (g) startMinigame(g); }, setGems: n => { P.gems = n; setText('hGems', n); }, setLv: n => { P.lv = n; setText('hLv', n); } };
    animate();
"""

js_code = js_code.replace("REPLACE_CHARS", json.dumps(chars_data))

final_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1,maximum-scale=1,user-scalable=no">
<title>RIFT RUCKUS - Party Animal Edition</title>
<link href="https://fonts.googleapis.com/css2?family=Spline+Sans:wght@300;400;500;600;700;800&display=swap" rel="stylesheet"/>
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:wght,FILL@100..700,0..1&display=swap" rel="stylesheet"/>
<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
<script>
    tailwind.config = {{
        darkMode: "class",
        theme: {{
            extend: {{
                colors: {{
                    "primary": "#f2f20d",
                    "background-dark": "#121212",
                    "card-dark": "#1e1e1e",
                }},
                fontFamily: {{
                    "display": ["Spline Sans", "sans-serif"]
                }}
            }},
        }},
    }}
</script>
<style>
    * {{ margin: 0; padding: 0; box-sizing: border-box; touch-action: none; -webkit-user-select: none; user-select: none; }}
    html, body {{ overflow: hidden; height: 100%; width: 100%; font-family: 'Spline Sans', sans-serif; background: #000; }}
    canvas {{ display: block; width: 100vw; height: 100vh; position: fixed; top: 0; left: 0; }}
    .vignette {{ position: fixed; top: 0; left: 0; right: 0; bottom: 0; pointer-events: none; z-index: 50; background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.5) 100%); }}
    .gone {{ opacity: 0 !important; pointer-events: none !important; }}

    .joy-area {{ position: fixed; bottom: 25px; width: 120px; height: 120px; z-index: 200; }}
    .joy-ring {{ position: absolute; width: 100%; height: 100%; border-radius: 50%; background: rgba(255,255,255,0.05); border: 2px solid rgba(255,255,255,0.1); }}
    .joy-knob {{ position: absolute; width: 50px; height: 50px; border-radius: 50%; background: white; box-shadow: 0 4px 15px rgba(0,0,0,0.5); top: 50%; left: 50%; transform: translate(-50%,-50%); pointer-events: none; }}

    .btn {{ width: 64px; height: 64px; border-radius: 50%; border: none; font-size: 28px; cursor: pointer; position: relative; box-shadow: 0 4px 15px rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; transition: transform 0.1s; }}
    .btn:active {{ transform: scale(0.9); }}
    .btn-cd {{ position: absolute; inset: 0; border-radius: 50%; background: rgba(0,0,0,0.7); display: none; align-items: center; justify-content: center; font-size: 16px; font-weight: 800; color: white; }}
    .btn.cd .btn-cd {{ display: flex; }}

    .overlay {{ position: fixed; inset: 0; background: rgba(0,0,0,0.85); z-index: 500; display: none; align-items: center; justify-content: center; padding: 20px; backdrop-filter: blur(5px); }}
    .overlay.show {{ display: flex; }}

    .scrollbar-hide::-webkit-scrollbar {{ display: none; }}
    .g-emoji {{ background-position: center; background-repeat: no-repeat; background-size: contain; display: inline-block; }}

    #fps {{ position: fixed; top: 10px; right: 10px; color: #f2f20d; font-weight: 800; font-size: 12px; z-index: 1000; background: rgba(0,0,0,0.5); padding: 4px 8px; border-radius: 8px; }}
</style>
</head>
<body class="text-white">
<div class="vignette"></div>
<div id="fps" style="display:none;"></div>
<div id="NOTIFS" class="fixed top-24 left-1/2 -translate-x-1/2 z-[1000] flex flex-col gap-2 pointer-events-none"></div>
<div id="PARTS" class="fixed inset-0 pointer-events-none z-[400]"></div>

<!-- HUD -->
<div id="hud" class="fixed top-0 left-0 right-0 p-4 z-[100] pointer-events-none flex items-start justify-between">
    <div class="flex items-center gap-3 bg-black/50 backdrop-blur-md p-2 pr-6 rounded-full border border-white/10 pointer-events-auto cursor-pointer shadow-xl hover:scale-105 transition-transform" onclick="show('oChar')">
        <div class="size-12 rounded-full bg-gradient-to-br from-primary to-yellow-600 border-2 border-white/20 g-emoji shadow-lg" id="hAvatar"></div>
        <div class="flex flex-col justify-center">
            <span class="text-white font-black text-sm italic tracking-tighter" id="hName">RUNNER</span>
            <span class="text-primary font-black text-[10px] tracking-[0.2em] uppercase">Level <span id="hLv">1</span></span>
        </div>
    </div>

    <div class="flex gap-2 pointer-events-auto">
        <div class="bg-black/50 backdrop-blur-md px-4 py-2 rounded-2xl border border-white/10 flex items-center gap-2 shadow-xl">
            <span class="text-lg">💎</span>
            <span class="text-white font-black text-sm" id="hGems">0</span>
        </div>
        <button class="bg-black/50 backdrop-blur-md size-12 rounded-full border border-white/10 flex items-center justify-center text-white hover:text-primary transition-colors shadow-xl" onclick="show('oSettings')">
            <span class="material-symbols-outlined text-2xl">settings</span>
        </button>
    </div>
</div>

<div class="overlay" id="oChar">
    <div class="relative flex h-full max-h-[90vh] w-full flex-col overflow-hidden max-w-md mx-auto bg-[#121212] shadow-2xl rounded-[2.5rem] border border-white/10 text-white">
        <header class="flex items-center justify-between p-6 pt-8 pb-4 shrink-0">
            <button class="text-white hover:text-primary transition-colors flex items-center justify-center size-12 rounded-full bg-white/5" onclick="hide('oChar')">
                <span class="material-symbols-outlined text-2xl">arrow_back</span>
            </button>
            <h1 class="text-2xl font-black italic tracking-tighter">SELECT RUNNER</h1>
            <div class="size-12"></div>
        </header>
        <main class="flex-1 flex flex-col px-6 pb-24 overflow-y-auto scrollbar-hide">
            <div class="grid grid-cols-3 gap-3 mb-8" id="charList"></div>
            <div id="charDetail" class="flex flex-col items-center"></div>
        </main>
        <div class="absolute bottom-0 left-0 right-0 p-6 bg-gradient-to-t from-[#121212] via-[#121212]/95 to-transparent">
            <button id="btnPlayAs" class="w-full bg-primary hover:scale-[1.02] active:scale-95 transition-all text-black font-black text-xl py-5 rounded-full shadow-[0_8px_25px_rgba(242,242,13,0.3)]">SELECT RUNNER</button>
        </div>
    </div>
</div>

<div class="overlay" id="oSettings">
    <div class="relative flex h-full max-h-[85vh] w-full flex-col overflow-hidden max-w-md mx-auto bg-[#121212] shadow-2xl rounded-[2.5rem] border border-white/10 text-white">
        <header class="flex items-center justify-between p-6 pt-8 pb-4 shrink-0">
            <button class="text-white hover:text-primary transition-colors flex items-center justify-center size-12 rounded-full bg-white/5" onclick="hide('oSettings')">
                <span class="material-symbols-outlined text-2xl">close</span>
            </button>
            <h1 class="text-2xl font-black italic tracking-tighter">SETTINGS</h1>
            <div class="size-12"></div>
        </header>
        <main class="flex-1 px-6 pb-8 overflow-y-auto scrollbar-hide space-y-6">
            <div class="space-y-3">
                <label class="text-[10px] font-black text-gray-500 uppercase tracking-[0.2em]">Graphics Mode</label>
                <div class="grid grid-cols-3 gap-2">
                    <button class="py-3 rounded-2xl bg-white/5 border border-white/5 text-xs font-black hover:border-primary/50" onclick="setPreset('classic')">CLASSIC</button>
                    <button class="py-3 rounded-2xl bg-white/5 border border-white/5 text-xs font-black hover:border-primary/50" onclick="setPreset('hd')">HD</button>
                    <button class="py-3 rounded-2xl bg-white/5 border border-white/5 text-xs font-black hover:border-primary/50" onclick="setPreset('deluxe')">DELUXE</button>
                </div>
                <select id="sGraph" onchange="updSet()" class="hidden"><option value="classic">Classic</option><option value="hd">HD</option><option value="deluxe">Deluxe</option></select>
            </div>
            <div class="space-y-3">
                <div class="flex items-center justify-between p-5 bg-white/5 rounded-3xl border border-white/5">
                    <div><p class="font-black text-sm tracking-tight">Shadows</p><p class="text-[10px] text-gray-500 font-bold uppercase">Real-time lighting</p></div>
                    <input type="checkbox" id="sShadow" onchange="updSet()" class="w-7 h-7 rounded-lg bg-black border-white/10 text-primary focus:ring-primary">
                </div>
                <div class="flex items-center justify-between p-5 bg-white/5 rounded-3xl border border-white/5">
                    <div><p class="font-black text-sm tracking-tight">Left-Hand Mode</p><p class="text-[10px] text-gray-500 font-bold uppercase">Swap controls</p></div>
                    <input type="checkbox" id="sLeft" onchange="updSet()" class="w-7 h-7 rounded-lg bg-black border-white/10 text-primary focus:ring-primary">
                </div>
                <div class="flex items-center justify-between p-5 bg-white/5 rounded-3xl border border-white/5">
                    <div><p class="font-black text-sm tracking-tight">Accessibility</p><p class="text-[10px] text-gray-500 font-bold uppercase">Larger UI text</p></div>
                    <input type="checkbox" id="sAcc" onchange="updSet()" class="w-7 h-7 rounded-lg bg-black border-white/10 text-primary focus:ring-primary">
                </div>
                <div class="flex items-center justify-between p-5 bg-white/5 rounded-3xl border border-white/5">
                    <div><p class="font-black text-sm tracking-tight">Debug Info</p><p class="text-[10px] text-gray-500 font-bold uppercase">Show FPS Counter</p></div>
                    <input type="checkbox" id="sDebug" onchange="updSet()" class="w-7 h-7 rounded-lg bg-black border-white/10 text-primary focus:ring-primary">
                </div>
            </div>
            <div class="space-y-3">
                <label class="text-[10px] font-black text-gray-500 uppercase tracking-[0.2em]">Bot Difficulty</label>
                <select id="sAI" onchange="updSet()" class="w-full p-5 bg-white/5 border border-white/10 rounded-3xl font-black text-white focus:ring-primary outline-none uppercase text-sm">
                    <option value="easy">Easy</option><option value="medium">Medium</option><option value="hard">Hard</option>
                </select>
            </div>
        </main>
    </div>
</div>

<div class="overlay" id="oPortal">
    <div class="relative flex h-full max-h-[70vh] w-full flex-col overflow-hidden max-w-md mx-auto bg-[#121212] shadow-2xl rounded-[2.5rem] border border-white/10 text-white">
        <header class="flex items-center justify-between p-6 pt-8 pb-4 shrink-0">
            <button class="text-white hover:text-primary transition-colors flex items-center justify-center size-12 rounded-full bg-white/5" onclick="hide('oPortal')">
                <span class="material-symbols-outlined text-2xl">close</span>
            </button>
            <h1 class="text-2xl font-black italic tracking-tighter">SELECT MODE</h1>
            <div class="size-12"></div>
        </header>
        <main class="flex-1 px-6 pb-8 overflow-y-auto scrollbar-hide" id="modeList"></main>
    </div>
</div>

<div class="overlay" id="oSocial">
    <div class="relative flex h-full max-h-[80vh] w-full flex-col overflow-hidden max-w-md mx-auto bg-[#121212] shadow-2xl rounded-[2.5rem] border border-white/10 text-white">
        <header class="flex items-center justify-between p-6 pt-8 pb-4 shrink-0">
            <button class="text-white hover:text-primary transition-colors flex items-center justify-center size-12 rounded-full bg-white/5" onclick="hide('oSocial')">
                <span class="material-symbols-outlined text-2xl">close</span>
            </button>
            <h1 class="text-2xl font-black italic tracking-tighter">FRIENDS</h1>
            <div class="size-12"></div>
        </header>
        <main class="flex-1 px-6 pb-8 overflow-y-auto scrollbar-hide" id="socialList"></main>
    </div>
</div>

<div class="overlay" id="RES">
    <div class="relative flex h-full max-h-[95vh] w-full flex-col overflow-hidden max-w-md mx-auto bg-[#121212] shadow-2xl rounded-[2.5rem] border border-white/10 text-white">
        <div class="flex-1 overflow-y-auto scrollbar-hide px-6 pt-12 pb-32">
            <div class="text-center mb-8">
                <h2 class="text-5xl font-black italic tracking-tighter text-primary mb-2" id="resT">VICTORY!</h2>
                <p class="text-xl font-bold text-gray-500 uppercase tracking-widest" id="resS">#1 - 1500 PTS</p>
            </div>
            <div id="resPod" class="space-y-3 mb-8"></div>
            <div id="resRew" class="flex justify-center mb-4"></div>
        </div>
        <div class="absolute bottom-0 left-0 right-0 p-8 bg-gradient-to-t from-[#121212] via-[#121212]/95 to-transparent flex gap-4">
            <button onclick="backToLobby()" class="flex-1 bg-white/10 hover:bg-white/20 py-5 rounded-full font-black uppercase text-sm tracking-widest transition-all">Lobby</button>
            <button id="resNext" class="flex-[2] bg-primary text-black py-5 rounded-full font-black uppercase text-sm tracking-widest shadow-lg shadow-primary/20 transition-all">Next Rift</button>
        </div>
    </div>
</div>

<div class="ld fixed inset-0 bg-[#121212] z-[1000] flex flex-col items-center justify-center transition-all duration-700" id="LD">
    <div class="ld-logo text-7xl mb-6 animate-bounce" id="ldLogo">🌀</div>
    <div class="ld-title text-5xl font-black italic tracking-tighter text-white mb-1">RIFT RUCKUS</div>
    <div class="ld-sub text-primary text-[10px] font-black tracking-[0.4em] uppercase mb-10" id="ldSub">RIFT EDITION</div>
    <div class="w-64 h-2 bg-white/5 rounded-full overflow-hidden border border-white/10 p-0.5">
        <div class="ld-fill h-full bg-primary rounded-full transition-all duration-300 shadow-[0_0_10px_#f2f20d]" id="ldFill" style="width:0%"></div>
    </div>
</div>

<canvas id="C"></canvas>

<div id="GHUD" class="fixed top-6 left-1/2 -translate-x-1/2 bg-black/60 backdrop-blur-xl px-8 py-3 rounded-3xl border border-white/10 hidden z-[150] shadow-2xl">
    <div class="flex flex-col items-center">
        <div class="text-white font-black italic text-sm tracking-tight uppercase leading-tight" id="gTitle">GAME</div>
        <div class="text-primary font-black text-3xl tabular-nums" id="gTime">00</div>
    </div>
</div>

<div id="IND" class="fixed top-32 left-1/2 -translate-x-1/2 bg-black/70 backdrop-blur-md px-6 py-2 rounded-full border border-white/20 text-white font-black text-xs tracking-[0.2em] hidden z-[150] uppercase"></div>

<div id="SB" class="fixed top-24 left-4 bg-black/50 backdrop-blur-lg p-4 rounded-[2rem] border border-white/10 hidden z-[90] min-w-[160px] shadow-2xl">
    <div class="text-[9px] font-black text-gray-500 uppercase tracking-widest mb-3 border-b border-white/10 pb-2">Leaderboard</div>
    <div id="sbBody" class="space-y-1.5"></div>
</div>

<div id="MM" class="fixed bottom-32 left-4 size-28 bg-black/50 backdrop-blur-md border border-white/10 rounded-[2rem] hidden z-90 overflow-hidden shadow-2xl">
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 size-2.5 bg-primary rounded-full shadow-[0_0_10px_#f2f20d] border-2 border-white z-10"></div>
</div>

<div class="joy-area" id="joyL"><div class="joy-ring"></div><div class="joy-knob" id="knobL"></div></div>
<div class="joy-area" id="joyR"><div class="joy-ring"></div><div class="joy-knob" id="knobR"></div></div>

<div id="BTNS" class="fixed bottom-32 right-4 flex gap-3 z-[200]">
    <button class="btn btn-jump bg-gradient-to-br from-blue-500 to-blue-700" id="bJump">🦘<div class="btn-cd" id="cdJump"></div></button>
    <button class="btn btn-grab bg-gradient-to-br from-red-500 to-red-700" id="bGrab">🤜<div class="btn-cd" id="cdGrab"></div></button>
    <button class="btn btn-skill bg-gradient-to-br from-purple-500 to-purple-800 shadow-purple-500/20" id="bSkill">✨<div class="btn-cd" id="cdSkill"></div></button>
</div>

<div id="SIDE" class="fixed bottom-[240px] right-6 flex flex-col gap-4 z-[200]" style="display:none">
    <button class="size-12 rounded-full bg-white/10 backdrop-blur-md border border-white/10 flex items-center justify-center text-xl shadow-xl active:scale-90 transition-all" id="bEmote">🎭</button>
    <button class="size-12 rounded-full bg-white/10 backdrop-blur-md border border-white/10 flex items-center justify-center text-xl shadow-xl active:scale-90 transition-all" id="bSprint">⚡</button>
</div>

<div class="fixed bottom-[320px] right-6 bg-black/80 backdrop-blur-xl border border-white/10 p-2 rounded-3xl hidden z-[250] shadow-2xl" id="emPop">
    <div class="grid grid-cols-4 gap-2" id="emoteGrid"></div>
</div>

<div id="PROMPT" class="fixed bottom-64 left-1/2 -translate-x-1/2 bg-black/90 backdrop-blur-2xl border-2 border-white/10 px-8 py-5 rounded-[2.5rem] hidden items-center gap-6 z-[150] shadow-2xl min-w-[300px]">
    <div class="size-14 rounded-2xl bg-primary/20 flex items-center justify-center shadow-inner" id="prIcon"></div>
    <div class="flex-1 flex flex-col">
        <span class="text-[10px] text-primary font-black tracking-widest uppercase">Action Available</span>
        <span class="text-white font-black text-lg tracking-tight uppercase" id="prText">INTERACT</span>
    </div>
    <button id="prGo" class="bg-primary text-black font-black text-sm px-8 py-3 rounded-full shadow-lg shadow-primary/30 active:scale-95 transition-all">GO</button>
</div>

<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>
<script>
""" + js_code + r"""
</script>
</body>
</html>
"""

with open('index.html', 'w') as f:
    f.write(final_html)
