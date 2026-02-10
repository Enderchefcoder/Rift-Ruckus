import re

with open('index.html', 'r') as f:
    content = f.read()

full_js = """
const $=id=>document.getElementById(id);
const sMesh=(g,m)=>{const e=new THREE.Mesh(g,m);e.castShadow=e.receiveShadow=true;return e;};
const addMesh=(m,isLobby=false)=>{scene.add(m);(isLobby?lobbyMeshes:gameMeshes).push(m);};
const show=id=>{const e=$(id);if(e)e.classList.add('show');};
const hide=id=>{const e=$(id);if(e)e.classList.remove('show');};
const setText=(id,t)=>{const e=$(id);if(e)e.textContent=t;};
const rnd=(a,b)=>a+Math.random()*(b-a);
const shuffle=a=>[...a].sort(()=>Math.random()-.5);
const d2=(a,b)=>Math.sqrt((a.x-b.x)**2+(a.z-b.z)**2);
const d3=(a,b)=>Math.sqrt((a.x-b.x)**2+((a.y||0)-(b.y||0))**2+(a.z-b.z)**2);
const getGvEmoji = e => `data:image/svg+xml;utf8,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='50%' x='50%' dy='.35em' text-anchor='middle' font-size='80'>${e}</text></svg>`;
const clamp=(v,lo,hi)=>Math.max(lo,Math.min(hi,v));
function notify(msg,type='inf'){const c=$('NOTIFS');if(!c)return;const n=document.createElement('div');n.className='noti '+type;n.textContent=msg;c.appendChild(n);setTimeout(()=>{n.style.opacity='0';setTimeout(()=>n.remove(),200);},2200);}
function flash(id,ms){const e=$(id);if(e){e.classList.add('on');setTimeout(()=>e.classList.remove('on'),ms);}}

const CHARS=[
{id:'glitch',name:'Glitch',emoji:'😎',role:'Speed',color:0x5C6BC0,spd:90,pow:50,jmp:80,skill:'Blink',sType:'tele',sCD:5},
{id:'tank',name:'Harold',emoji:'🦣',role:'Tank',color:0x795548,spd:45,pow:95,jmp:40,skill:'Quake',sType:'stun',sCD:8},
{id:'bear',name:'Barry',emoji:'🐻',role:'Brawler',color:0x8D6E63,spd:60,pow:85,jmp:50,skill:'Roar',sType:'stun',sCD:7},
{id:'bunny',name:'Bibi',emoji:'🐰',role:'Jumper',color:0xFF80AB,spd:85,pow:40,jmp:95,skill:'Hop',sType:'jump',sCD:3},
{id:'duck',name:'Ducky',emoji:'🦆',role:'Scout',color:0xFFEB3B,spd:75,pow:50,jmp:70,skill:'Dash',sType:'dash',sCD:4},
{id:'ninja',name:'Ninja',emoji:'🥷',role:'Stealth',color:0x212121,spd:85,pow:60,jmp:90,skill:'Smoke',sType:'smoke',sCD:6}
];

const GAMES=[
{id:'stars',name:'⭐ Star Collector',tip:'Collect stars! Gold=30pts!',dur:50,type:'collect'},
{id:'sumo',name:'💪 Sumo Ring',tip:'Push enemies out of the ring!',dur:55,type:'sumo'},
{id:'hill',name:'👑 King of Hill',tip:'Stay on hill to score! Knocked off after 5s!',dur:50,type:'hill'},
{id:'tag',name:'🏷️ Tag Frenzy',tip:\"GRAB to pass the tag! Don't be IT!\",dur:45,type:'tag'},
{id:'pads',name:'🪑 Musical Pads',tip:'Stand on GREEN pad when music stops!',dur:70,type:'pads'}
];

const month = new Date().getMonth();
const IS_DEC = month === 11, IS_OCT = month === 9, IS_SPRING = month >= 2 && month <= 4;
const EMOTES=['😄','🤣','😎','🥷','🔥','👑','💪','🌟'];
const ST={LOAD:0,LOBBY:1,CDOWN:2,GAME:3,RES:4};
let state=ST.LOAD;
let P={gems:500,crowns:10,charId:'glitch',score:0,isIt:false,tagImmune:0,skillCD:0,grabCD:0,stunned:0,stamina:100,sprinting:false,hillTime:0,lv:1,xp:0,buffTime:0,friends:[],invited:[],preset:'hd',settings:{shadows:true,ai:'medium',leftHand:false,acc:false,debug:false}};

function saveData(){ localStorage.setItem('RR_DATA', JSON.stringify({gems:P.gems, crowns:P.crowns, lv:P.lv, xp:P.xp, charId:P.charId, friends:P.friends, invited:P.invited, preset:P.preset, settings:P.settings})); }
function loadData(){
  const d = localStorage.getItem('RR_DATA');
  if(d){
    try {
        const j = JSON.parse(d);
        if(j.settings) Object.assign(P.settings, j.settings);
        if(j.friends) P.friends = j.friends;
        if(j.invited) P.invited = j.invited;
        ['gems','crowns','lv','xp','charId','preset'].forEach(k=> { if(j[k]!==undefined) P[k]=j[k]; });
    } catch(e) {}
  }
  setText('hGems', P.gems); setText('hLv', P.lv);
  const cur = curC(), av = $('hAvatar'); if(av){ av.textContent = ''; av.style.backgroundImage = `url('${getGvEmoji(cur.emoji)}')`; av.classList.add('g-emoji'); }
  document.documentElement.style.fontSize = P.settings.acc ? "18px" : "16px";
  const jL=$('joyL'), jR=$('joyR'), bt=$('BTNS');
  if(P.settings.leftHand){ if(jL){jL.style.left='auto';jL.style.right='18px';} if(jR){jR.style.right='auto';jR.style.left='18px';} if(bt){bt.style.right='auto';bt.style.left='14px';} }
  else { if(jL){jL.style.right='auto';jL.style.left='18px';} if(jR){jR.style.left='auto';jR.style.right='18px';} if(bt){bt.left='auto';bt.style.right='14px';} }
  const sS=$('sShadow'), sL=$('sLeft'), sA=$('sAcc'), sD=$('sDebug'), sAi=$('sAI'), sG=$('sGraph');
  if(sS) sS.checked = P.settings.shadows; if(sL) sL.checked = P.settings.leftHand; if(sA) sA.checked = P.settings.acc; if(sD) sD.checked = P.settings.debug; if(sAi) sAi.value = P.settings.ai; if(sG) sG.value = P.preset;
}

let selChar='glitch', scene, cam, ren, clk, sun, camAng=0, pVel={x:0,y:0,z:0}, grounded=true, near=null, curGame=null, gTimer=0, gActive=false, rGames=[], rIdx=0, musicOn=true, padCount=16, scoreT=0, shakeAmt=0;
const BOT_NAMES=['Zippy','Bouncer','Sparky','Glimmer','Turbo','RiftRunner','Echo','Nova','Pixel','Glitchy','Tanker','Frosty','Shadow','Blaze','Bolt','Aura','Rusty','Comet','Pulse','Zen'];
var player, bots=[], lobbyMeshes=[], gameMeshes=[], stars=[], pads=[], solidPlatforms=[], hillMesh=null, interacts=[], particles3d=[];
const G=.03, SPD=.13, JMP=.4, FRC=.86;
const joy={l:{x:0,y:0},r:{x:0,y:0}};

function getC(id){return CHARS.find(c=>c.id===id)||CHARS[0];}
function curC(){return getC(P.charId);}

function initThree(){
  scene=new THREE.Scene();
  let skyCol = 0x1a2a4a; if(P.preset === 'deluxe') skyCol = 0xFFB74D; else if(IS_DEC) skyCol = 0x0a1a2a; else if(IS_OCT) skyCol = 0x0d0208; else if(IS_SPRING) skyCol = 0x81D4FA;
  scene.background=new THREE.Color(skyCol); scene.fog=new THREE.FogExp2(skyCol, P.preset === 'deluxe' ? .008 : .005);
  cam=new THREE.PerspectiveCamera(55,innerWidth/innerHeight,.1,800);
  ren=new THREE.WebGLRenderer({canvas:$('C'),antialias:true}); ren.setSize(innerWidth,innerHeight); ren.setPixelRatio(Math.min(devicePixelRatio, 2));
  ren.shadowMap.enabled = P.settings.shadows; ren.shadowMap.type = THREE.PCFSoftShadowMap;
  ren.toneMapping = THREE.ACESFilmicToneMapping; ren.toneMappingExposure = P.preset === 'deluxe' ? 1.6 : 1.2;
  clk=new THREE.Clock();
  scene.add(new THREE.AmbientLight(0xFFE0B2, P.preset === 'deluxe' ? 1.0 : 0.5));
  sun=new THREE.DirectionalLight(0xfff5e0, P.preset === 'deluxe' ? 1.8 : 1.1); sun.position.set(80,120,80);
  if(P.settings.shadows){ sun.castShadow=true; sun.shadow.mapSize.width=sun.shadow.mapSize.height=2048; }
  scene.add(sun); scene.add(new THREE.HemisphereLight(0x6699cc,0x334455,.5));
}
function mat(c,r=.5){ if(P.preset === 'classic') return new THREE.MeshLambertMaterial({color:c}); return new THREE.MeshStandardMaterial({color:c, roughness:r, metalness: (P.preset === 'deluxe' ? 0.2 : 0.1)}); }

function makeNameTag(name){
  const canvas = document.createElement('canvas'); canvas.width = 256; canvas.height = 64; const ctx = canvas.getContext('2d');
  ctx.fillStyle = 'rgba(0,0,0,0.5)'; ctx.roundRect(0, 0, 256, 64, 32); ctx.fill();
  ctx.font = 'bold 32px Spline Sans, sans-serif'; ctx.fillStyle = 'white'; ctx.textAlign = 'center'; ctx.fillText(name, 128, 44);
  const tex = new THREE.CanvasTexture(canvas); const sprite = new THREE.Sprite(new THREE.SpriteMaterial({map: tex, transparent: true}));
  sprite.scale.set(4, 1, 1); sprite.position.y = 2.8; return sprite;
}

function makeChar(ch,name='',isBot=false){
  const g=new THREE.Group(), col=ch.color, bm=mat(col,.35);
  const body=sMesh(new THREE.CylinderGeometry(.4,.44,.7,12),bm); body.position.y=1; g.add(body);
  const top=sMesh(new THREE.SphereGeometry(.4,12,10),bm); top.position.y=1.35; g.add(top);
  const bot=sMesh(new THREE.SphereGeometry(.44,12,10),bm); bot.position.y=.65; g.add(bot);
  const head=sMesh(new THREE.SphereGeometry(.36,16,14),mat(0xFFDFC4,.45)); head.position.y=1.85; g.add(head);
  [-1,1].forEach(s=>{ const eye=sMesh(new THREE.SphereGeometry(.07,8,6),mat(0x111111)); eye.position.set(s*.12,1.9,.3); g.add(eye); });
  if(ch.id==='glitch'){ [-1,1].forEach(s=>{ const e=sMesh(new THREE.SphereGeometry(.12,8,8),mat(0x222222)); e.position.set(s*.25,2.15,0); g.add(e); }); }
  else if(ch.id==='tank'||ch.id==='bear'){ [-1,1].forEach(s=>{ const e=sMesh(new THREE.SphereGeometry(.15,8,8),bm); e.position.set(s*.25,2.1,0); g.add(e); }); }
  else if(ch.id==='bunny'){ [-1,1].forEach(s=>{ const e=sMesh(new THREE.CylinderGeometry(.08,.08,.6,8),bm); e.position.set(s*.15,2.3,0); e.rotation.z=s*.2; g.add(e); }); }
  else if(ch.id==='duck'){ const beak=sMesh(new THREE.BoxGeometry(.2,.1,.25),mat(0xFF9800)); beak.position.set(0,1.8,.35); g.add(beak); }
  const tail=sMesh(new THREE.SphereGeometry(.15,8,8),bm); tail.position.set(0,.8,-.45); g.add(tail);
  const hat=sMesh(new THREE.ConeGeometry(.28,.45,8),mat(0xE74C3C,.4)); hat.position.y=2.2; hat.rotation.z=.12; g.add(hat);
  if(isBot){ const ant=sMesh(new THREE.CylinderGeometry(.015,.015,.28,6),mat(0x444444)); ant.position.y=2.45; g.add(ant); const ball=sMesh(new THREE.SphereGeometry(.05,8,6),mat(0xFF4444)); ball.position.y=2.55; g.add(ball); }
  if(name) g.add(makeNameTag(name)); return g;
}

function buildLobby(){
  lobbyMeshes.forEach(o=>scene.remove(o)); lobbyMeshes=[]; gameMeshes.forEach(o=>scene.remove(o)); gameMeshes=[]; interacts=[]; stars=[]; pads=[]; solidPlatforms=[];
  if(IS_DEC) buildDecLobby(); else if(IS_OCT) buildOctLobby(); else if(IS_SPRING) buildSpringLobby(); else buildDefaultLobby();
  buildBanners();
}
function buildBanners(){
  for(let i=0; i<8; i++){ const a=(i/8)*Math.PI*2, r=40, g=new THREE.Group(); g.position.set(Math.cos(a)*r, 10, Math.sin(a)*r); const pole=sMesh(new THREE.CylinderGeometry(.1,.1,10), mat(0x333333)); pole.position.y=-5; g.add(pole); const flag=sMesh(new THREE.BoxGeometry(3,2,.1), mat(Math.random()*0xffffff)); flag.position.set(1.5,0,0); g.add(flag); addMesh(g,true); }
}
function buildDecLobby(){
  const gnd=sMesh(new THREE.CircleGeometry(110,60),mat(0xE8F4F8,.8)); gnd.rotation.x=-Math.PI/2; addMesh(gnd,true);
  const pR=18,pH=3, pl=sMesh(new THREE.CylinderGeometry(pR,pR+2,pH,32),mat(0x6D4C41,.5)); pl.position.y=pH/2; addMesh(pl,true); solidPlatforms.push({mesh:pl,radius:pR+2,topY:pH});
  buildXmasTree(0,pH,0); buildPortal(0,0,-42); buildMirror(42,0,0); buildArcade(-42,0,0); buildSocial(0,0,42);
}
function buildOctLobby(){
  const gnd=sMesh(new THREE.CircleGeometry(110,60),mat(0x1a0a00)); gnd.rotation.x=-Math.PI/2; addMesh(gnd,true);
  const pR=20,pH=1.5, pl=sMesh(new THREE.CylinderGeometry(pR,pR,pH,32),mat(0x3e2723)); pl.position.y=pH/2; addMesh(pl,true); solidPlatforms.push({mesh:pl,radius:pR,topY:pH});
  const p=new THREE.Group(); p.position.set(0,pH,0); const b=sMesh(new THREE.SphereGeometry(4,16,12),mat(0xff6d00,.2)); b.scale.y=0.8; b.position.y=3; p.add(b); const s=sMesh(new THREE.CylinderGeometry(0.3,0.5,1.5,8),mat(0x1b5e20)); s.position.y=6; p.add(s); p.add(new THREE.PointLight(0xffab40,3,30)); addMesh(p,true);
  buildPortal(0,0,-45); buildMirror(45,0,0); buildArcade(-45,0,0); buildSocial(0,0,45);
}
function buildSpringLobby(){
  const gnd=sMesh(new THREE.CircleGeometry(110,60),mat(0x66bb6a)); gnd.rotation.x=-Math.PI/2; addMesh(gnd,true);
  const pR=20,pH=1.5, pl=sMesh(new THREE.CylinderGeometry(pR,pR,pH,32),mat(0xfff176)); pl.position.y=pH/2; addMesh(pl,true); solidPlatforms.push({mesh:pl,radius:pR,topY:pH});
  buildPortal(0,0,-45); buildMirror(45,0,0); buildArcade(-45,0,0); buildSocial(0,0,45);
}
function buildDefaultLobby(){
  const gnd=sMesh(new THREE.CircleGeometry(110,60),mat(0x388E3C)); gnd.rotation.x=-Math.PI/2; addMesh(gnd,true);
  const pR=20,pH=1.5, pl=sMesh(new THREE.CylinderGeometry(pR,pR,pH,32),mat(0xCFD8DC)); pl.position.y=pH/2; addMesh(pl,true); solidPlatforms.push({mesh:pl,radius:pR,topY:pH});
  const f=new THREE.Group(); f.position.set(0,pH,0); f.add(sMesh(new THREE.CylinderGeometry(5,5,0.8,24),mat(0x90A4AE))); f.add(sMesh(new THREE.CylinderGeometry(1,1,3,16),mat(0x90A4AE))); f.children[1].position.y=2; const w=sMesh(new THREE.SphereGeometry(2.5,16,12,0,Math.PI*2,0,Math.PI/2),mat(0x29B6F6,.6)); w.position.y=3.5; f.add(w); f.add(new THREE.PointLight(0x29B6F6,2,25)); addMesh(f,true);
  addLobbyDeco(); buildPortal(0,0,-45); buildMirror(45,0,0); buildArcade(-45,0,0); buildSocial(0,0,45);
}

function buildXmasTree(x,y,z){
  const g=new THREE.Group(); g.position.set(x,y,z); g.add(sMesh(new THREE.CylinderGeometry(1,1.5,3,10),mat(0x5D4037,.8))); g.children[0].position.y=1.5;
  for(let i=0;i<4;i++){ const l=sMesh(new THREE.ConeGeometry(5.5-i,4.5,12),mat(0x2E7D32,.7)); l.position.y=4.5+i*3; g.add(l); }
  const s=sMesh(new THREE.OctahedronGeometry(1),mat(0xFFD700,.2)); s.position.y=18; s.userData.spin=true; g.add(s); scene.add(g); lobbyMeshes.push(g);
}
function buildSocial(x,y,z){
  const g=new THREE.Group(); g.position.set(x,0,z); g.add(sMesh(new THREE.CylinderGeometry(4,4.5,1,24),mat(0x27ae60))); g.add(sMesh(new THREE.TorusGeometry(3.5,0.3,12,32),mat(0x2ecc71))); g.children[1].rotation.x=Math.PI/2; g.children[1].position.y=0.5;
  const i=sMesh(new THREE.IcosahedronGeometry(1.5,0),mat(0xffffff,.2)); i.position.y=4.5; i.userData.spin=true; i.userData.bob=true; i.userData.baseY=4.5; g.add(i); g.add(new THREE.PointLight(0x2ecc71,2,15)); g.userData={type:'social',icon:'👥',text:'Friends'}; addMesh(g,true); interacts.push(g);
}
function buildPortal(x,y,z){
  const g=new THREE.Group(); g.position.set(x,y,z); for(let i=0;i<3;i++){ const s=sMesh(new THREE.CylinderGeometry(8-i,8.5-i,.6,14),mat(0xE0E0E0,.3)); s.position.y=.3+i*.6; g.add(s); }
  const r=sMesh(new THREE.TorusGeometry(3,.6,10,20),mat(0x9C27B0,.3)); r.position.y=5; r.userData.spin=true; g.add(r); const o=sMesh(new THREE.SphereGeometry(1.6,14,12),mat(0x00E5FF,.2)); o.position.y=5; o.userData.bob=true; o.userData.baseY=5; g.add(o);
  g.userData={type:'portal',text:'Enter Portal',icon:'🌀',r:12}; addMesh(g,true); interacts.push(g);
}
function buildMirror(x,y,z){
  const g=new THREE.Group(); g.position.set(x,y,z); g.add(sMesh(new THREE.BoxGeometry(5,7,.7),mat(0xFFD700,.2))); g.children[0].position.y=4;
  const m=sMesh(new THREE.BoxGeometry(4.2,6,.15),new THREE.MeshStandardMaterial({color:0xE8EAF6,metalness:.95,roughness:.05})); m.position.set(0,4,.45); g.add(m); g.rotation.y=-Math.PI/2; g.userData={type:'char',text:'Choose Runner',icon:'🎭',r:10}; addMesh(g,true); interacts.push(g);
}
function buildArcade(x,y,z){
  const g=new THREE.Group(); g.position.set(x,y,z); g.add(sMesh(new THREE.BoxGeometry(5,6.5,3),mat(0x1A237E,.5))); g.children[0].position.y=3.25;
  const s=sMesh(new THREE.BoxGeometry(3.5,2.5,.15),mat(0x00E676,.3)); s.position.set(0,4.5,1.6); g.add(s); g.rotation.y=Math.PI/2; g.userData={type:'arcade',text:'Practice',icon:'🕹️',r:10}; addMesh(g,true); interacts.push(g);
}

function spawnPlayer(){
  if(player) scene.remove(player); player = makeChar(curC(), 'YOU'); player.position.set(0,3.5,22); scene.add(player);
  if(P.charId === 'ninja') player.traverse(o=>{ if(o.isMesh){ o.material=o.material.clone(); o.material.transparent=true; o.material.opacity=0.5; } });
}
function spawnBots(n){
  bots.forEach(b=>scene.remove(b.mesh)); bots=[]; const pool=CHARS.filter(c=>c.id!==P.charId); const names=[...P.invited];
  while(names.length<n){ const rn=BOT_NAMES[Math.floor(Math.random()*BOT_NAMES.length)]; if(!names.includes(rn)) names.push(rn); }
  for(let i=0;i<n;i++){
    const ch=pool[i%pool.length], name=names[i], mesh=makeChar(ch,name,true); mesh.position.set(Math.cos((i+1)/(n+1)*Math.PI*2)*(24+rnd(0,10)),10,Math.sin((i+1)/(n+1)*Math.PI*2)*(24+rnd(0,10)));
    bots.push({mesh, ch, name, emoji:ch.emoji, color:ch.color, score:0, isIt:false, tagImmune:0, stunned:0, vel:{x:0,y:0,z:0}, grounded:false, eliminated:false, hillTime:0, target:null, aiTimer:0, skillCD:0, mem:{bad:[]}}); scene.add(mesh);
  }
}

function getGroundY(pos){
  let gy=0; solidPlatforms.forEach(sp=>{ if(d2(pos,sp.mesh.position)<sp.radius) gy=Math.max(gy,sp.topY); });
  if(hillMesh && d2(pos,hillMesh.mesh.position)<hillMesh.radius) gy=Math.max(gy,hillMesh.topY); return gy;
}
function applyPhysics(pos,vel){
  if(!grounded) vel.y-=G; pos.x+=vel.x; pos.y+=vel.y; pos.z+=vel.z; const gy=getGroundY(pos);
  if(pos.y<=gy){ pos.y=gy; vel.y=0; grounded=true; } else grounded=false; vel.x*=FRC; vel.z*=FRC;
}
function applyBotPhysics(b){
  if(!b.grounded) b.vel.y-=G; b.mesh.position.x+=b.vel.x; b.mesh.position.y+=b.vel.y; b.mesh.position.z+=b.vel.z; const gy=getGroundY(b.mesh.position);
  if(b.mesh.position.y<=gy){ b.mesh.position.y=gy; b.vel.y=0; b.grounded=true; } else b.grounded=false; b.vel.x*=FRC; b.vel.z*=FRC;
}

function initControls(){
  mkJoy('joyL','knobL','l'); mkJoy('joyR','knobR','r');
  const tap=(id,fn)=>{const e=$(id);if(!e)return;e.addEventListener('touchstart',ev=>{ev.preventDefault();ev.stopPropagation();fn();},{passive:false});e.addEventListener('click',ev=>{ev.preventDefault();fn();});};
  tap('prGo',doInteract); tap('bJump',doJump); tap('bGrab',doGrab); tap('bSkill',doSkill);
  const emPop=$('emPop'), emGrid=$('emoteGrid'); if(emGrid) EMOTES.forEach(e=>{ const b=document.createElement('button'); b.className='size-10 rounded-xl bg-white/5 hover:bg-white/10 flex items-center justify-center g-emoji transition-all active:scale-90'; b.style.backgroundImage=`url('${getGvEmoji(e)}')`; b.onclick=()=>{showEmoji(player,e);emPop.classList.add('hidden');}; emGrid.appendChild(b); });
  tap('bEmote',()=>emPop.classList.toggle('hidden'));
  const sp=$('bSprint'); if(sp){ sp.addEventListener('touchstart',ev=>{ev.preventDefault();P.sprinting=true;sp.classList.add('on');},{passive:false}); sp.addEventListener('touchend',()=>{P.sprinting=false;sp.classList.remove('on');}); sp.addEventListener('mousedown',()=>{P.sprinting=true;sp.classList.add('on');}); sp.addEventListener('mouseup',()=>{P.sprinting=false;sp.classList.remove('on');}); }
}
function mkJoy(aId,kId,key){
  const a=$(aId), k=$(kId); if(!a||!k)return; let tid=null,cx=0,cy=0;
  const upd=(x,y)=>{ let dx=x-cx,dy=y-cy,d=Math.sqrt(dx*dx+dy*dy),r=50; if(d>r){dx*=r/d;dy*=r/d;} k.style.transform=`translate(calc(-50% + ${dx}px), calc(-50% + ${dy}px))`; joy[key]={x:dx/r,y:dy/r}; };
  a.addEventListener('touchstart',ev=>{ev.preventDefault();const t=ev.changedTouches[0];tid=t.identifier;const r=a.getBoundingClientRect();cx=r.left+r.width/2;cy=r.top+r.height/2;upd(t.clientX,t.clientY);},{passive:false});
  a.addEventListener('touchmove',ev=>{ev.preventDefault();for(let t of ev.changedTouches)if(t.identifier===tid)upd(t.clientX,t.clientY);},{passive:false});
  a.addEventListener('touchend',ev=>{for(let t of ev.changedTouches)if(t.identifier===tid){tid=null;k.style.transform='translate(-50%,-50%)';joy[key]={x:0,y:0};}},{passive:false});
  a.addEventListener('mousedown',ev=>{const r=a.getBoundingClientRect();cx=r.left+r.width/2;cy=r.top+r.height/2;upd(ev.clientX,ev.clientY);const mv=e=>upd(e.clientX,e.clientY),up=()=>{document.removeEventListener('mousemove',mv);document.removeEventListener('mouseup',up);k.style.transform='translate(-50%,-50%)';joy[key]={x:0,y:0};};document.addEventListener('mousemove',mv);document.addEventListener('mouseup',up);});
}

function doInteract(){ if(!near)return; const t=near.userData.type; if(t==='portal'){show('oPortal');loadModes();} else if(t==='char'){show('oChar');loadChars();} else if(t==='arcade'){show('oArcade');loadArcade();} else if(t==='social'){show('oSocial');loadSocial();} $('PROMPT')?.classList.remove('show'); }
function loadSocial(){
  const el=$('socialList'); if(!el)return; el.innerHTML=''; if(P.friends.length===0){el.innerHTML='<div class="py-12 text-center text-gray-500 font-medium">No friends yet.<br>Add bots after a game!</div>';return;}
  P.friends.forEach(name=>{ const isInv=P.invited.includes(name); const row=document.createElement('div'); row.className='flex items-center justify-between p-4 bg-card-dark rounded-2xl border border-white/5 mb-3'; row.innerHTML=`<div class="flex items-center gap-3"><div class="size-10 rounded-full bg-white/5 flex items-center justify-center g-emoji" style="background-image:url('${getGvEmoji('🤖')}')"></div><span class="font-bold">${name}</span></div><button class="px-4 py-2 rounded-full text-xs font-bold transition-all ${isInv?'bg-primary text-black':'bg-white/10 text-white'}" onclick="toggleInvite('${name}', this)">${isInv?'Invited ✅':'Invite'}</button>`; el.appendChild(row); });
}
function toggleInvite(name, btn){ const idx=P.invited.indexOf(name); if(idx>-1){P.invited.splice(idx,1);btn.textContent='Invite';btn.classList.remove('bg-primary','text-black');btn.classList.add('bg-white/10','text-white');} else {if(P.invited.length>=8){notify('Max 8 invited bots!','bad');return;} P.invited.push(name);btn.textContent='Invited ✅';btn.classList.add('bg-primary','text-black');btn.classList.remove('bg-white/10','text-white');} saveData(); }
function loadModes(){
  const el=$('modeList'); if(!el)return; el.innerHTML='<div class="space-y-4 pt-4"></div>'; const ml=el.firstChild;
  [{name:'⚡ Quick Play',desc:'One random rift',cnt:1,icon:'⚡'},{name:'🎉 Party Mode',desc:'Three random rifts',cnt:3,icon:'🎉'}].forEach(m=>{ const c=document.createElement('div'); c.className='group p-5 bg-card-dark rounded-3xl border-2 border-transparent hover:border-primary/40 transition-all cursor-pointer flex items-center gap-4'; c.innerHTML=`<div class="size-14 rounded-2xl bg-white/5 flex items-center justify-center text-3xl g-emoji" style="background-image:url('${getGvEmoji(m.icon)}')"></div><div class="flex-1"><h4 class="font-black text-lg leading-none mb-1 group-hover:text-primary transition-colors">${m.name}</h4><p class="text-xs text-gray-500 font-medium">${m.desc}</p></div><span class="material-symbols-outlined text-gray-600 group-hover:text-primary">arrow_forward_ios</span>`; c.onclick=()=>{hide('oPortal');rGames=shuffle(GAMES).slice(0,m.cnt);rIdx=0;setTimeout(()=>startMinigame(rGames[0]),300);}; ml.appendChild(c); });
}
function loadChars(){
  const el=$('charList'); if(!el)return; el.innerHTML=''; CHARS.forEach(c=>{ const isSel=c.id===selChar, item=document.createElement('div'); item.className='group relative flex flex-col items-center gap-2'; item.innerHTML=`${isSel?'<div class="absolute -top-2 -right-2 z-10 bg-primary text-black rounded-full p-1 shadow-lg shadow-primary/20"><span class="material-symbols-outlined text-sm font-bold block">check</span></div>':''}<button class="w-full aspect-square bg-card-dark rounded-xl border-2 ${isSel?'border-primary shadow-[0_0_15px_rgba(242,242,13,0.1)]':'border-transparent hover:border-white/10'} transition-all flex items-center justify-center relative overflow-hidden">${isSel?'<div class="absolute inset-0 bg-primary/5"></div>':''}<div class="w-full h-full bg-center bg-contain bg-no-repeat transform scale-75 g-emoji" style="background-image:url('${getGvEmoji(c.emoji)}');"></div></button><span class="text-xs font-bold ${isSel?'text-primary':'text-gray-500 group-hover:text-white'} transition-colors">${c.name}</span>`; item.onclick=()=>{selChar=c.id;loadChars();}; el.appendChild(item); });
  updateCharDetail(getC(selChar));
}
function updateCharDetail(c){
  const el=$('charDetail'); if(!el)return;
  el.innerHTML=`<h2 class="text-white text-[2.5rem] font-black italic tracking-tighter leading-none mb-1">${c.name.toUpperCase()}</h2><p class="text-primary text-sm font-black tracking-widest uppercase mb-8">${c.role}</p><div class="grid grid-cols-3 w-full gap-4 mb-8"><div class="flex flex-col items-center gap-2 p-4 rounded-2xl bg-card-dark border ${c.pow>70?'border-primary/30':'border-white/5'} relative overflow-hidden group"><div class="size-10 rounded-full ${c.pow>70?'bg-primary text-black':'bg-white/10 text-gray-400'} flex items-center justify-center mb-1"><span class="material-symbols-outlined filled text-xl">fitness_center</span></div><div class="text-center"><p class="text-[10px] font-bold ${c.pow>70?'text-primary':'text-gray-500'} uppercase">Power</p><div class="h-1 w-12 bg-gray-800 rounded-full mt-1 overflow-hidden"><div class="h-full bg-current rounded-full" style="width:${c.pow}%;color:${c.pow>70?'#f2f20d':'#666'}"></div></div></div></div><div class="flex flex-col items-center gap-2 p-4 rounded-2xl bg-card-dark border ${c.spd>70?'border-primary/30':'border-white/5'} relative overflow-hidden"><div class="size-10 rounded-full ${c.spd>70?'bg-primary text-black':'bg-white/10 text-gray-400'} flex items-center justify-center mb-1"><span class="material-symbols-outlined filled text-xl">bolt</span></div><div class="text-center"><p class="text-[10px] font-bold ${c.spd>70?'text-primary':'text-gray-500'} uppercase">Speed</p><div class="h-1 w-12 bg-gray-800 rounded-full mt-1 overflow-hidden"><div class="h-full bg-current rounded-full" style="width:${c.spd}%;color:${c.spd>70?'#f2f20d':'#666'}"></div></div></div></div><div class="flex flex-col items-center gap-2 p-4 rounded-2xl bg-card-dark border ${c.jmp>70?'border-primary/30':'border-white/5'} relative overflow-hidden"><div class="size-10 rounded-full ${c.jmp>70?'bg-primary text-black':'bg-white/10 text-gray-400'} flex items-center justify-center mb-1"><span class="material-symbols-outlined filled text-xl">stat_2</span></div><div class="text-center"><p class="text-[10px] font-bold ${c.jmp>70?'text-primary':'text-gray-500'} uppercase">Jump</p><div class="h-1 w-12 bg-gray-800 rounded-full mt-1 overflow-hidden"><div class="h-full bg-current rounded-full" style="width:${c.jmp}%;color:${c.jmp>70?'#f2f20d':'#666'}"></div></div></div></div></div><div class="w-full bg-card-dark border border-white/5 rounded-2xl p-4 flex items-center justify-between gap-4"><div class="flex items-center gap-3"><div class="size-10 rounded-full bg-primary/10 text-primary flex items-center justify-center shrink-0 border border-primary/20 g-emoji" style="background-image:url('${getGvEmoji(c.emoji)}')"></div><div class="flex flex-col"><span class="text-[10px] text-gray-500 font-bold uppercase tracking-wider">Special Skill</span><span class="text-white font-black text-lg">${c.skill}</span></div></div></div>`;
  $('btnPlayAs').onclick=()=>{ if(P.charId!==selChar){P.charId=selChar;saveData();spawnPlayer();loadData();} hide('oChar'); };
}
function loadArcade(){
  const el=$('modeList'); if(!el)return; el.innerHTML='<div class="grid grid-cols-2 gap-3 pt-4"></div>'; const ml=el.firstChild;
  GAMES.forEach(g=>{ const c=document.createElement('div'); c.className='p-4 bg-card-dark rounded-2xl border border-white/5 hover:border-primary/30 transition-all cursor-pointer text-center'; c.innerHTML=`<div class="text-3xl mb-2 g-emoji size-12 mx-auto" style="background-image:url('${getGvEmoji(g.name.split(' ')[0])}')"></div><div class="font-bold text-xs">${g.name}</div>`; c.onclick=()=>{hide('oArcade');curGame=g;setTimeout(()=>startMinigame(g),300);}; ml.appendChild(c); });
}

function doJump(){ if(P.stunned>0||!grounded)return; pVel.y=JMP*(curC().jmp/80); grounded=false; mkParts(player.position.x,.3,player.position.z,0xFFFFFF,12); }
function doPush(){
  if(P.grabCD>0)return; P.grabCD=0.8; const targets=bots.filter(b=>!b.eliminated); let pushed=false;
  targets.forEach(b=>{ if(d3(player.position,b.mesh.position)<4.5){ const dx=b.mesh.position.x-player.position.x,dz=b.mesh.position.z-player.position.z,mag=Math.sqrt(dx*dx+dz*dz)||1; b.vel.x+=(dx/mag)*0.6; b.vel.z+=(dz/mag)*0.6; b.vel.y=0.25; b.stunned=1.2; pushed=true; } });
  if(pushed){flash('bGrab',200);mkParts(player.position.x,1.5,player.position.z,0xffffff,10);}
}
function doGrab(){ doPush(); }
function doSkill(){
  if(P.skillCD>0||P.stunned>0)return; if(state!==ST.GAME&&state!==ST.LOBBY)return;
  const c=curC(); P.skillCD=c.sCD; cooldown('bSkill','cdSkill',c.sCD,'skillCD'); const fwd=new THREE.Vector3(0,0,-1).applyAxisAngle(new THREE.Vector3(0,1,0),player.rotation.y);
  switch(c.sType){
    case 'tele': mkParts(player.position.x,1.5,player.position.z,0x00FFFF,20); player.position.add(fwd.multiplyScalar(10)); mkParts(player.position.x,1.5,player.position.z,0x00FFFF,30); break;
    case 'dash': pVel.x+=fwd.x*1.2; pVel.z+=fwd.z*1.2; flash('SPEED',500); mkParts(player.position.x,1,player.position.z,0x4ECDC4,25); break;
    case 'jump': pVel.y=.7; grounded=false; mkParts(player.position.x,.3,player.position.z,0xFF69B4,25); break;
    case 'stun': bots.forEach(b=>{if(d3(player.position,b.mesh.position)<12){b.stunned=2.5;b.vel.y=.2;mkParts(b.mesh.position.x,1.5,b.mesh.position.z,0xFFD700,20);showEmoji(b.mesh,'💫');}}); shakeAmt=.8; break;
    case 'smoke': mkParts(player.position.x,1.5,player.position.z,0x333333,50); bots.forEach(b=>{if(d3(player.position,b.mesh.position)<10){b.stunned=2;showEmoji(b.mesh,'❓');}}); player.visible=false; setTimeout(()=>player.visible=true,3000); break;
    case 'buff': P.buffTime=5; notify('POWER UP!','ok'); flash('SPEED',5000); mkParts(player.position.x,2,player.position.z,0xFF0000,30); break;
  }
  notify(c.skill+'!','inf'); showEmoji(player,c.emoji);
}
function cooldown(bId,cId,dur,prop){ const b=$(bId); if(b)b.classList.add('cd'); let r=dur; const iv=setInterval(()=>{r-=.1; const c=$(cId); if(c)c.textContent=Math.max(0,Math.ceil(r)); if(r<=0){clearInterval(iv);P[prop]=0;if(b)b.classList.remove('cd');}},100); }

function startMinigame(game){
  state=ST.CDOWN; curGame=game; scoreT=0; musicOn=true; padCount=16; hillMesh=null;
  $('hud').style.display='none'; $('MM')?.classList.remove('show'); $('PROMPT')?.classList.remove('show'); $('SIDE').style.display='flex';
  const gb=$('bGrab'); if(gb)gb.classList.toggle('hidden',game.type==='collect'||game.type==='pads');
  lobbyMeshes.forEach(o=>o.visible=false); player.visible=false; bots.forEach(b=>b.mesh.visible=false);
  solidPlatforms=[]; buildArena(game);
  setText('cdName',game.name); setText('cdTip',game.tip); show('CDOWN');
  let cnt=3; setText('cdNum','3'); $('cdNum').className='cd-num';
  const iv=setInterval(()=>{ cnt--; if(cnt>0)setText('cdNum',cnt); else if(cnt===0){setText('cdNum','GO!');$('cdNum').className='cd-num cd-go';} else {clearInterval(iv);hide('CDOWN');beginGame();} },900);
}
function beginGame(){
  state=ST.GAME; gActive=true; gTimer=curGame.dur; show('GHUD'); setText('gTitle',curGame.name); show('SB'); $('BTNS').style.display='flex';
  P.score=0; P.isIt=false; P.tagImmune=0; P.stamina=100; P.hillTime=0; P.sprinting=false;
  bots.forEach(b=>{b.score=0;b.isIt=false;b.tagImmune=0;b.eliminated=false;b.mesh.visible=true;b.stunned=0;b.hillTime=0;b.aiTimer=0;b.skillCD=rnd(3,6);});
  if(curGame.type==='tag'){ const it=bots[Math.floor(Math.random()*bots.length)]; it.isIt=true; it.tagImmune=4; updInd(); }
  if(curGame.type==='pads'){ resetPads(); updInd(); }
  const tEl=$('gTime');
  const iv=setInterval(()=>{
    if(!gActive){clearInterval(iv);return;} gTimer--;
    if(tEl){tEl.textContent=Math.max(0,gTimer);tEl.className='g-time';if(gTimer<=10)tEl.classList.add('danger');else if(gTimer<=20)tEl.classList.add('warn');}
    if(curGame?.type==='pads'&&gTimer%11===0&&gTimer>0&&gTimer<curGame.dur){ musicOn=!musicOn; if(!musicOn){padCount=Math.max(2,padCount-2);notify('🎵 MUSIC STOPPED!','inf');setTimeout(()=>checkPads(),1200);} else {notify('🎵 Playing!','inf');resetPads();} updInd(); }
    if(gTimer<=0){clearInterval(iv);endMinigame();}
  },1000);
}

function buildArena(game){
  lobbyMeshes.forEach(o=>scene.remove(o)); lobbyMeshes=[]; gameMeshes.forEach(o=>scene.remove(o)); gameMeshes=[]; stars=[]; pads=[]; hillMesh=null; solidPlatforms=[];
  const bgMap={collect:0x0D47A1,sumo:0x3E2723,hill:0xBF360C,tag:0x01579B,pads:0x4A148C};
  scene.background=new THREE.Color(bgMap[game.type]||0x1a2a4a); scene.fog=new THREE.FogExp2(bgMap[game.type]||0x1a2a4a,.004);
  const R=game.type==='sumo'?50:85;
  const gnd=sMesh(new THREE.CircleGeometry(R,60),mat({collect:0x2E7D32,sumo:0x5D4037,hill:0xBF360C,tag:0x006064,pads:0x4A148C}[game.type]||0x2E7D32,.8)); gnd.rotation.x=-Math.PI/2; addMesh(gnd,false);
  const bor=sMesh(new THREE.TorusGeometry(R,1.5,10,60),mat(0xFFD700,.4)); bor.rotation.x=Math.PI/2; bor.position.y=.75; addMesh(bor,false);
  if(game.type==='collect'){ for(let i=0;i<55;i++)spawnStar(); }
  if(game.type==='hill'){ const hm=sMesh(new THREE.CylinderGeometry(16,20,10,32),mat(0xFFD700,.35)); hm.position.y=4; scene.add(hm); gameMeshes.push(hm); hillMesh={mesh:hm,radius:15.5,topY:9}; const cr=sMesh(new THREE.ConeGeometry(3,4,5),mat(0xFFD700,.2)); cr.position.y=11; cr.userData.spin=true; cr.userData.bob=true; cr.userData.baseY=11; scene.add(cr); gameMeshes.push(cr); }
  if(game.type==='pads'){ const sz=4,sp=12,off=-(sz-1)*sp/2; for(let x=0;x<sz;x++)for(let z=0;z<sz;z++){ const p=sMesh(new THREE.CylinderGeometry(6,6.5,1.5,16),mat(0x9C27B0,.35)); p.position.set(off+x*sp,.6,off+z*sp); p.userData={active:true,idx:x*sz+z}; scene.add(p); gameMeshes.push(p); pads.push(p); solidPlatforms.push({mesh:p,radius:6,topY:1.35}); } }
  player.visible=true; player.position.set(0,10,28); pVel={x:0,y:0,z:0}; grounded=false;
  bots.forEach((b,i)=>{ b.mesh.visible=true; b.eliminated=false; b.mesh.position.set(Math.cos((i+1)/(bots.length+1)*Math.PI*2)*(22+rnd(0,10)),10,Math.sin((i+1)/(bots.length+1)*Math.PI*2)*(22+rnd(0,10))); b.vel={x:0,y:0,z:0}; b.stunned=0; b.grounded=false; });
}
function spawnStar(){
  const gold=Math.random()<.12; const val=gold?30:10; const shape=new THREE.Shape(); for(let i=0;i<10;i++){const r=i%2===0?.8:.38,a=(i/10)*Math.PI*2-Math.PI/2;if(i===0)shape.moveTo(Math.cos(a)*r,Math.sin(a)*r);else shape.lineTo(Math.cos(a)*r,Math.sin(a)*r);} shape.closePath();
  const m=gold?new THREE.MeshStandardMaterial({color:0xFFD700,metalness:0.8,roughness:0.2}):mat(0xFFFFFF,0.3);
  const s=sMesh(new THREE.ExtrudeGeometry(shape,{depth:.35,bevelEnabled:false}),m); if(gold)s.scale.setScalar(1.5); s.position.set(Math.cos(rnd(0,6.2))*rnd(10,60),2.5,Math.sin(rnd(0,6.2))*rnd(10,60)); s.rotation.x=Math.PI/2; s.userData={val,off:rnd(0,6.2)}; scene.add(s); gameMeshes.push(s); stars.push(s);
}

function runBotAI(dt){
  const spd_base=SPD*.78*(curGame?.type==='pads'?.6:1)*(curGame?.type==='sumo'?.7:1)*(P.settings.ai==='hard'?1.2:P.settings.ai==='easy'?0.7:1);
  bots.forEach((b,idx)=>{
    if(b.eliminated){b.mesh.visible=true;return;} if(b.stunned>0){b.stunned-=dt;return;} if(b.tagImmune>0)b.tagImmune-=dt;
    if(!b.skillCD) b.skillCD=rnd(5,10); b.skillCD-=dt;
    if(b.skillCD<=0&&!b.stunned&&state===ST.GAME){
      const dP=d3(b.mesh.position,player.position); let trig=false;
      if(['stun','smoke'].includes(b.ch.sType)&&dP<8)trig=true; else if(['dash','tele','jump'].includes(b.ch.sType)&&b.target&&d3(b.mesh.position,b.target)>15)trig=true; else if(b.ch.sType==='buff'&&Math.random()<.3)trig=true;
      if(trig){
        b.skillCD=b.ch.sCD+rnd(2,5); const fwd=new THREE.Vector3(0,0,-1).applyAxisAngle(new THREE.Vector3(0,1,0),b.mesh.rotation.y);
        switch(b.ch.sType){
          case 'tele': b.mesh.position.add(fwd.multiplyScalar(8)); break;
          case 'dash': b.vel.x+=fwd.x*0.8; b.vel.z+=fwd.z*0.8; break;
          case 'jump': b.vel.y=0.3; b.grounded=false; break;
          case 'stun': if(dP<10){P.stunned=2;flash('STUMBLE',500);showEmoji(player,'💫');} bots.forEach(o=>{if(o!==b&&d3(b.mesh.position,o.mesh.position)<10){o.stunned=2;showEmoji(o.mesh,'💫');}}); break;
          case 'smoke': if(dP<10){P.stunned=1.5;showEmoji(player,'❓');} bots.forEach(o=>{if(o!==b&&d3(b.mesh.position,o.mesh.position)<10){o.stunned=1.5;showEmoji(o.mesh,'❓');}}); b.mesh.visible=false; setTimeout(()=>b.mesh.visible=true,2000); break;
          case 'buff': b.score+=20; showEmoji(b.mesh,'🎁'); break;
        }
        showEmoji(b.mesh,b.ch.emoji);
      }
    }
    if(state===ST.LOBBY && d2(b.mesh.position,{x:0,z:0})<10){ if(b.grounded&&Math.random()<.05){b.vel.y=0.25;b.grounded=false;} }
    if(b.mesh.position.y<-5){b.mem.bad.push({x:b.mesh.position.x,z:b.mesh.position.z});if(b.mem.bad.length>10)b.mem.bad.shift();b.mesh.position.set(0,5,0);b.vel.set(0,0,0);}
    b.aiTimer-=dt;
    if(b.aiTimer<=0){
      b.aiTimer=rnd(.3,1);
      if(curGame?.type==='collect'){ let bS=null,bD=Infinity; stars.forEach(s=>{if(!s.userData.taken){const dd=d3(b.mesh.position,s.position);if(dd<bD){bD=dd;bS=s;}}}); if(bS)b.target={x:bS.position.x,z:bS.position.z}; }
      else if(curGame?.type==='hill'){ b.target={x:rnd(-5,5),z:rnd(-5,5)}; }
      else if(curGame?.type==='tag'){
        if(b.isIt){ let bS=null,bD=Infinity; if(!P.isIt&&P.tagImmune<=0){const dd=d2(b.mesh.position,player.position);if(dd<bD){bD=dd;bS=player.position;}} bots.forEach(o=>{if(o!==b&&!o.isIt&&!o.eliminated&&o.tagImmune<=0){const dd=d2(b.mesh.position,o.mesh.position);if(dd<bD){bD=dd;bS=o.mesh.position;}}}); if(bS)b.target={x:bS.x,z:bS.z}; }
        else { const it=bots.find(o=>o.isIt)||(P.isIt?player:null); if(it){const pos=it.position||it.mesh?.position;if(pos){const dx=b.mesh.position.x-pos.x,dz=b.mesh.position.z-pos.z,dd=Math.sqrt(dx*dx+dz*dz);if(dd>.1)b.target={x:b.mesh.position.x+(dx/dd)*22,z:b.mesh.position.z+(dz/dd)*22};}} }
      }
      else if(curGame?.type==='pads'&&!musicOn){ const ac=pads.filter(p=>p.userData.active); if(ac.length>0){const pad=ac[idx%ac.length];b.target={x:pad.position.x,z:pad.position.z};} }
      else if(curGame?.type==='sumo'){ if(Math.random()>.4){b.target={x:player.position.x,z:player.position.z};} else{const o=bots.filter(x=>x!==b&&!x.eliminated);if(o.length){const t=o[Math.floor(Math.random()*o.length)];b.target={x:t.mesh.position.x,z:t.mesh.position.z};}} }
      else b.target={x:rnd(-35,35),z:rnd(-35,35)};
    }
    if(b.target){
      let tx=b.target.x, tz=b.target.z; b.mem.bad.forEach(s=>{if(d2(b.mesh.position,s)<8){const dx=b.mesh.position.x-s.x,dz=b.mesh.position.z-s.z,d=Math.sqrt(dx*dx+dz*dz)||1;tx+=(dx/d)*15;tz+=(dz/d)*15;}});
      const dx=tx-b.mesh.position.x,dz=tz-b.mesh.position.z,dd=Math.sqrt(dx*dx+dz*dz);
      if(dd>1.2){ const s=spd_base*(b.ch.spd/80); b.mesh.position.x+=(dx/dd)*s; b.mesh.position.z+=(dz/dd)*s; b.mesh.rotation.y=Math.atan2(dx,dz); }
    }
    applyBotPhysics(b);
    const bd=d2(b.mesh.position,{x:0,z:0}), sR=(curGame?.type==='sumo'?28:70); if(bd>sR){ if(curGame?.type==='sumo'){b.score=Math.max(0,b.score-50);const a=rnd(0,6.2);b.mesh.position.set(Math.cos(a)*15,0,Math.sin(a)*15);} else {b.mesh.position.x*=sR/bd;b.mesh.position.z*=sR/bd;} }
    stars.forEach(s=>{ if(!s.userData.taken&&d3(b.mesh.position,s.position)<3){ s.userData.taken=true; scene.remove(s); b.score+=s.userData.val; if(state===ST.GAME&&curGame?.type==='collect') setTimeout(()=>spawnStar(),4000); } });
    if(curGame?.type==='tag'&&b.isIt&&b.tagImmune<=0){
      if(!P.isIt&&P.tagImmune<=0&&d3(b.mesh.position,player.position)<3){ b.isIt=false; P.isIt=true; P.tagImmune=3; notify('⚠️ YOU\\\'RE IT! -50','bad'); P.score=Math.max(0,P.score-50); b.score+=100; updInd(); }
      bots.forEach(o=>{ if(o!==b&&!o.isIt&&!o.eliminated&&o.tagImmune<=0&&d3(b.mesh.position,o.mesh.position)<3){ b.isIt=false; o.isIt=true; o.tagImmune=3; b.score+=100; o.score=Math.max(0,o.score-50); updInd(); } });
    }
    if(curGame?.type==='hill'&&hillMesh){
      const hd=d2(b.mesh.position,{x:0,z:0}); if(hd<hillMesh.radius&&b.mesh.position.y>=hillMesh.topY-.5){ b.hillTime=(b.hillTime||0)+dt; if(b.hillTime>=1){b.score+=1;b.hillTime-=1;} if(b.hillTime>=5){const a=rnd(0,6.2);b.vel.x+=Math.cos(a)*.5;b.vel.z+=Math.sin(a)*.5;b.vel.y=.25;b.hillTime=0;} } else b.hillTime=0;
    }
  });
}

function updateMinigame(dt){
  if(!gActive)return; if(P.tagImmune>0)P.tagImmune-=dt; if(!P.sprinting&&P.stamina<100)P.stamina=Math.min(100,P.stamina+22*dt); scoreT+=dt; if(P.buffTime>0)P.buffTime-=dt;
  const t=Date.now()*.001; gameMeshes.forEach(o=>{ if(o.userData.bob)o.position.y=(o.userData.baseY||4)+Math.sin(t*2)*.5; if(curGame?.type==='hill'&&o.geometry.type==='ConeGeometry') o.scale.setScalar(1+Math.sin(t*5)*0.1); if(o.userData.spin)o.rotation.y+=dt; });
  stars.forEach(s=>{ if(!s.userData.taken){ s.position.y=2.5+Math.sin(t*3+s.userData.off)*.5; s.rotation.z+=dt*5; if(d3(player.position,s.position)<3){ s.userData.taken=true; scene.remove(s); P.score+=s.userData.val; mkParts(s.position.x,s.position.y,s.position.z,0xFFD700,18); if(state===ST.GAME&&curGame?.type==='collect') setTimeout(()=>spawnStar(),4000); } } });
  if(curGame?.type==='hill'&&hillMesh){ const hd=d2(player.position,{x:0,z:0}); if(hd<hillMesh.radius&&player.position.y>=hillMesh.topY-.5){ P.hillTime+=dt; if(P.hillTime>=1){P.score+=1;P.hillTime-=1;} if(P.hillTime>=5){P.stunned=0.5;const a=rnd(0,6.2);pVel.x+=Math.cos(a)*.6;pVel.z+=Math.sin(a)*.6;pVel.y=.3;P.hillTime=0;notify('Knocked off!','inf');mkParts(player.position.x,1.5,player.position.z,0xFFD700,20);} } else P.hillTime=0; }
  if(curGame?.type==='sumo'){ const pd=d2(player.position,{x:0,z:0}), sR=40; if(gTimer<curGame.dur-10){ const sh=1-(curGame.dur-10-gTimer)/100, cR=Math.max(15,40*sh); if(gameMeshes[0])gameMeshes[0].scale.set(cR/40,1,cR/40); if(gameMeshes[1])gameMeshes[1].scale.set(cR/40,1,cR/40); if(pd>cR){P.score=Math.max(0,P.score-50);player.position.set(0,0,0);flash('STUMBLE',350);} bots.forEach(b=>{if(!b.eliminated&&d2(b.mesh.position,{x:0,z:0})>cR){b.score=Math.max(0,b.score-50);b.mesh.position.set(0,0,0);}}); } }
  if(curGame?.type==='tag'){ const pd=d2(player.position,{x:0,z:0}); if(pd>70){player.position.x*=70/pd;player.position.z*=70/pd;} if(P.isIt&&P.tagImmune<=0){bots.forEach(b=>{if(!b.isIt&&!b.eliminated&&b.tagImmune<=0&&d3(player.position,b.mesh.position)<3){P.isIt=false;b.isIt=true;b.tagImmune=3;P.tagImmune=2;notify('Tagged '+b.name+'! +100','ok');P.score+=100;b.score=Math.max(0,b.score-50);updInd();}});}}
  if(curGame?.type==='pads'&&musicOn){ const pd=d2(player.position,{x:0,z:0}); if(pd>70){player.position.x*=70/pd;player.position.z*=70/pd;} }
  if(curGame?.type==='collect'){ const pd=d2(player.position,{x:0,z:0}); if(pd>70){player.position.x*=70/pd;player.position.z*=70/pd;} }
  runBotAI(dt); updateSB(); updateMM();
}

function getAllScores(){ return[{name:'You',score:Math.floor(P.score),emoji:curC().emoji,color:curC().color,isPlayer:true,isIt:P.isIt},...bots.map(b=>({name:b.name,score:Math.floor(b.score),emoji:b.emoji,color:b.color,isPlayer:false,isIt:b.isIt,eliminated:b.eliminated}))].sort((a,b)=>b.score-a.score); }
function updateSB(){ const b=$('sbBody'); if(!b)return; b.innerHTML=''; getAllScores().slice(0,10).forEach((e,i)=>{ const d=document.createElement('div'); d.className='sb-r'+(e.isPlayer?' me':'')+(i===0?' top':''); d.innerHTML=`<span class="sb-rk">${i+1}</span><span class="sb-nm">${e.emoji} ${e.name}${e.isIt?' 🏷️':''}</span><span class="sb-sc">${e.score}</span>`; b.appendChild(d); }); }
function updateMM(){ const mm=$('MM'); if(!mm)return; mm.classList.add('show'); mm.querySelectorAll('.mm-dot').forEach(d=>d.remove()); bots.forEach(b=>{ if(b.eliminated)return; const dx=b.mesh.position.x-player.position.x,dz=b.mesh.position.z-player.position.z; if(Math.abs(dx)<60&&Math.abs(dz)<60){ const d=document.createElement('div'); d.className='mm-dot bot'+(b.isIt?' it':''); d.style.left=(50+dx*.65)+'px'; d.style.top=(50+dz*.65)+'px'; mm.appendChild(d); } }); }
function endMinigame(){ gActive=false; state=ST.RES; hide('GHUD'); hide('SB'); hide('IND'); $('BTNS').style.display='none'; showResults(); }
function addFriend(name, btn){ if(!P.friends.includes(name)){P.friends.push(name);saveData();} btn.textContent='FRIENDS ✅'; btn.classList.add('bg-white/10','text-gray-500'); btn.classList.remove('bg-primary','text-black'); btn.disabled=true; }
function showResults(){
  const sc=getAllScores(), r=sc.findIndex(s=>s.isPlayer)+1, won=r===1; setText('resT',won?'VICTORY!':'NICE WORK!'); setText('resS',`#${r} — ${Math.floor(P.score)} pts`);
  const p=$('resPod'); if(p){ p.innerHTML=''; sc.slice(0,5).forEach((e,i)=>{ const isF=P.friends.includes(e.name), row=document.createElement('div'); row.className=`flex items-center justify-between p-4 rounded-2xl border ${e.isPlayer?'bg-primary/10 border-primary/40':'bg-card-dark border-white/5'}`; row.innerHTML=`<div class="flex items-center gap-3"><span class="font-black italic text-lg ${i==0?'text-primary':'text-gray-500'} w-4">${i+1}</span><div class="size-10 rounded-full bg-white/5 flex items-center justify-center g-emoji" style="background-image:url('${getGvEmoji(e.emoji)}')"></div><div class="flex flex-col"><span class="font-bold text-sm ${e.isPlayer?'text-primary':'text-white'}">${e.name}</span><span class="text-[10px] font-bold text-gray-500 uppercase tracking-widest">${e.score} pts</span></div></div>${e.isPlayer?'<span class="text-[10px] font-black text-primary uppercase">YOU</span>':`<button class="px-3 py-1.5 rounded-full text-[10px] font-black transition-all ${isF?'bg-white/10 text-gray-500':'bg-primary text-black shadow-lg shadow-primary/20'}" onclick="addFriend('${e.name}', this)">${isF?'FRIENDS ✅':'ADD FRIEND'}</button>`}`; p.appendChild(row); }); }
  const shards=won?180:50+r*15; P.gems+=shards; setText('hGems',P.gems); const rr=$('resRew'); if(rr) rr.innerHTML=`<div class="bg-primary/20 border border-primary/30 px-6 py-3 rounded-2xl flex items-center gap-3"><span class="text-2xl g-emoji size-8" style="background-image:url('${getGvEmoji('💎')}')"></span><span class="text-primary font-black text-xl">+${shards}</span></div>`;
  show('RES'); if(won)for(let i=0;i<50;i++)setTimeout(()=>{const c=document.createElement('div');c.className='snow';c.textContent=(IS_DEC?['🎉','🎊','⭐','🎄','🎅']:['🎉','🎊','⭐','💎','🏆'])[Math.floor(Math.random()*5)];c.style.left=rnd(0,100)+'vw';c.style.fontSize='24px';c.style.animationDuration=rnd(3,5)+'s';$('PARTS')?.appendChild(c);setTimeout(()=>c.remove(),5000);},i*40);
  const nx=$('resNext'); if(nx){ nx.textContent=(rGames && rGames.length>0&&rIdx<rGames.length-1)?'NEXT RIFT':'PLAY AGAIN'; nx.onclick=()=>{hide('RES');if(rGames && rGames.length>0&&rIdx<rGames.length-1){rIdx++;setTimeout(()=>startMinigame(rGames[rIdx]),400);}else backToLobby();}; }
}
function backToLobby(){
  state=ST.LOBBY; curGame=null; rGames=[]; rIdx=0; hillMesh=null; hide('RES'); $('hud').style.display='flex'; hide('IND'); $('SIDE').style.display='none'; $('bGrab')?.classList.remove('hidden'); scene.background=new THREE.Color(0x1a2a4a); scene.fog=new THREE.FogExp2(0x1a2a4a,.005);
  buildLobby(); player.visible=true; player.position.set(0,3.5,22); pVel={x:0,y:0,z:0}; bots.forEach((b,i)=>{b.mesh.visible=true;b.eliminated=false;b.mesh.position.set(Math.cos((i+1)/(bots.length+1)*6.28)*24,0,Math.sin((i+1)/(bots.length+1)*6.28)*24);});
}
function mkParts(x,y,z,col,n){ for(let i=0;i<n;i++){ const m=new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:.9}), p=sMesh(new THREE.SphereGeometry(.15,8,6),m); p.position.set(x,y,z); p.userData={vx:rnd(-.5,.5),vy:rnd(.2,.55),vz:rnd(-.5,.5),life:1,m}; scene.add(p); particles3d.push(p); } }
function showEmoji(parent, text){
  const canvas=document.createElement('canvas'); canvas.width=128; canvas.height=128; const ctx=canvas.getContext('2d'); ctx.font='80px serif'; ctx.textAlign='center'; ctx.textBaseline='middle'; ctx.fillText(text, 64, 64);
  const tex=new THREE.CanvasTexture(canvas), sprite=new THREE.Sprite(new THREE.SpriteMaterial({map:tex,transparent:true})); sprite.position.y=3.2; sprite.scale.set(2,2,2); parent.add(sprite); let start=Date.now(); const ani=()=>{ let age=(Date.now()-start)/2000; if(age>=1){parent.remove(sprite);return;} sprite.position.y=3.2+age*1.5; sprite.material.opacity=1-age; requestAnimationFrame(ani); }; ani();
}
function animate(){
  requestAnimationFrame(animate); const dt=Math.min(clk.getDelta(),.05), t=Date.now()*.001;
  if(P.settings.debug){ const fEl=$("fps"); if(fEl){fEl.style.display="block";fEl.textContent="FPS: "+Math.round(1/dt);} }
  if(P.grabCD>0)P.grabCD-=dt; if(P.skillCD>0)P.skillCD-=dt;
  if(state===ST.LOBBY){
    const c=curC(), inp=joy.l, sprint=P.sprinting?1.4:1, spd=SPD*(c.spd/80)*sprint*0.75, mag=Math.sqrt(inp.x**2+inp.y**2);
    if(mag>.1){ const ang=Math.atan2(inp.x,inp.y)+camAng; pVel.x+=Math.sin(ang)*mag*spd*.12; pVel.z+=Math.cos(ang)*mag*spd*.12; player.rotation.y=ang; player.rotation.z=Math.sin(t*15)*0.1; player.rotation.x=Math.sin(t*10)*0.05; } else { player.rotation.z*=0.8; player.rotation.x*=0.8; }
    applyPhysics(player.position,pVel); const pd=d2(player.position,{x:0,z:0}); if(pd>100){player.position.x*=100/pd;player.position.z*=100/pd;} if(Math.abs(joy.r.x)>.1)camAng-=joy.r.x*.035;
    let bC=null, bD=Infinity; interacts.forEach(o=>{const dd=d3(player.position,o.position);if(dd<(o.userData.r||10)&&dd<bD){bD=dd;bC=o;}}); near=bC; const pr=$('PROMPT'); if(near&&!document.querySelector('.overlay.show')){$('prIcon').style.backgroundImage=`url('${getGvEmoji(near.userData.icon)}')`;setText('prText',near.userData.text);pr?.classList.add('show');}else pr?.classList.remove('show');
    updateMM(); lobbyMeshes.forEach(o=>{if(o.userData?.spin)o.rotation.y+=dt;if(o.userData?.bob)o.position.y=(o.userData.baseY||4)+Math.sin(t*2)*.4;});
    bots.forEach(b=>{ if(Math.random()<.01||!b.target)b.target={x:rnd(-40,40),z:rnd(-40,40)}; const dx=b.target.x-b.mesh.position.x,dz=b.target.z-b.mesh.position.z,dd=Math.sqrt(dx*dx+dz*dz); if(dd>1.5){b.mesh.position.x+=(dx/dd)*.05;b.mesh.position.z+=(dz/dd)*.05;b.mesh.rotation.y=Math.atan2(dx,dz);} applyBotPhysics(b); });
  }else if(state===ST.GAME){
    if(gActive&&P.stunned<=0){
      const c=curC(), inp=joy.l, sprint=(P.sprinting&&P.stamina>0?1.4:1)*(P.buffTime>0?1.3:1); if(P.sprinting&&P.stamina>0)P.stamina=Math.max(0,P.stamina-dt*30);
      const spd=SPD*(c.spd/80)*sprint*.42*(curGame?.type==='pads'?!musicOn?0.15:0.7:1), mag=Math.sqrt(inp.x**2+inp.y**2);
      if(mag>.1){ const ang=Math.atan2(inp.x,inp.y)+camAng; pVel.x+=Math.sin(ang)*mag*spd; pVel.z+=Math.cos(ang)*mag*spd; player.rotation.y=ang; player.rotation.z=Math.sin(t*15)*0.15; player.rotation.x=Math.sin(t*10)*0.1; } else { player.rotation.z*=0.8; player.rotation.x*=0.8; }
      if(Math.abs(joy.r.x)>.1)camAng-=joy.r.x*.035; if(P.sprinting&&mag>.3)flash('SPEED',80);
    }else if(P.stunned>0)P.stunned-=dt;
    applyPhysics(player.position,pVel); updateMinigame(dt);
  }
  for(let i=particles3d.length-1;i>=0;i--){ const p=particles3d[i]; p.position.x+=p.userData.vx;p.position.y+=p.userData.vy;p.position.z+=p.userData.vz; p.userData.vy-=.025;p.userData.life-=dt*4; if(p.userData.m)p.userData.m.opacity=p.userData.life; if(p.userData.life<=0){scene.remove(p);particles3d.splice(i,1);} }
  const tX=player.position.x+Math.sin(camAng)*22, tZ=player.position.z+Math.cos(camAng)*22, tY=player.position.y+16;
  cam.position.x+=(tX-cam.position.x)*.12; cam.position.y+=(tY-cam.position.y)*.12; cam.position.z+=(tZ-cam.position.z)*.12; if(shakeAmt>0){cam.position.x+=rnd(-shakeAmt,shakeAmt);cam.position.y+=rnd(-shakeAmt,shakeAmt);shakeAmt*=.8;if(shakeAmt<.01)shakeAmt=0;}
  cam.lookAt(player.position.x,player.position.y+2.5,player.position.z); if(sun){sun.position.set(player.position.x+80,120,player.position.z+80);sun.target.position.copy(player.position);sun.target.updateMatrixWorld();} ren.render(scene,cam);
}

function updSet(){
  const s=P.settings, oS=s.shadows, oP=P.preset, oA=s.acc;
  s.shadows=$('sShadow').checked; s.ai=$('sAI').value; s.leftHand=$('sLeft').checked; s.acc=$('sAcc').checked; s.debug=$('sDebug').checked; P.preset=$('sGraph')?.value||P.preset;
  saveData(); if(s.acc!==oA) document.documentElement.style.fontSize=s.acc?"18px":"16px";
  const jL=$('joyL'), jR=$('joyR'), bt=$('BTNS');
  if(s.leftHand){ if(jL){jL.style.left='auto';jL.style.right='18px';} if(jR){jR.style.right='auto';jR.style.left='18px';} if(bt){bt.style.right='auto';bt.style.left='14px';} }
  else { if(jL){jL.style.right='auto';jL.style.left='18px';} if(jR){jR.style.left='auto';jR.style.right='18px';} if(bt){bt.left='auto';bt.style.right='14px';} }
  if(s.shadows!==oS||P.preset!==oP) if(confirm("Reload to apply graphics?")) location.reload();
}
function setPreset(p){ P.preset=p; P.settings.shadows=(p!=='classic'); const sg=$('sGraph'), ss=$('sShadow'); if(sg)sg.value=p; if(ss)ss.checked=P.settings.shadows; saveData(); location.reload(); }
function startLoad(){
  let p=0; const iv=setInterval(()=>{ p+=rnd(16,28);if(p>100)p=100; const f=$('ldFill');if(f)f.style.width=p+'%'; if(p>=100){clearInterval(iv);setTimeout(()=>{$('LD')?.classList.add('gone');state=ST.LOBBY;},500);} },130);
}
function updInd(){ const ind=$('IND'); if(!ind)return; if(curGame?.type==='pads'){ ind.textContent=musicOn?'🎵 DANCE!':'⛔ STOP! ON GREEN!'; ind.style.color=musicOn?'#fff':'#f00'; ind.style.display='block'; }else if(curGame?.type==='tag'){ ind.textContent=P.isIt?'⚠️ YOU ARE IT! TAG SOMEONE!':'✅ SAFE'; ind.style.color=P.isIt?'#f00':'#fff'; ind.style.display='block'; }else ind.style.display='none'; }
function resetPads(){ pads.forEach(p=>{ p.material.color.setHex(0x9C27B0); p.userData.active=true; }); }
function checkPads(){
  const w=new Set(); pads.forEach(p=>{ let c=0; if(d2(player.position,p.position)<6&&player.position.y>=.5){w.add('player');c++;} bots.forEach(b=>{if(d2(b.mesh.position,p.position)<6&&b.mesh.position.y>=.5){w.add(b.name);c++;}}); if(c>0)p.material.color.setHex(0x44FF44); else {p.userData.active=false;p.material.color.setHex(0x333333);} });
  if(w.has('player')) {P.score+=25;notify('Safe! +25','ok');} else {P.score=Math.max(0,P.score-40);flash('STUMBLE',350);notify('No pad! -40','bad');}
  bots.forEach(b=>{if(!b.eliminated){if(w.has(b.name))b.score+=25;else b.score=Math.max(0,b.score-40);}}); setTimeout(()=>{musicOn=true;resetPads();updInd();},2000);
}

loadData(); initThree(); buildLobby(); spawnPlayer(); spawnBots(5); initControls(); startLoad();
window.DEBUG={gotoLobby:()=>backToLobby(),start:id=>{let g=(typeof id==="number")?GAMES[id]:GAMES.find(x=>x.id===id);if(g)startMinigame(g);},setGems:n=>{P.gems=n;setText('hGems',n);},setLv:n=>{P.lv=n;setText('hLv',n);}};
animate();
"""

code = re.sub(r'<script>.*?</script>', '<script>' + full_js + '</script>', content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(code)
