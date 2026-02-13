// ========== SAFE HELPERS ==========
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
const clamp=(v,lo,hi)=>Math.max(lo,Math.min(hi,v));
function notify(msg,type='inf'){const c=$('NOTIFS');if(!c)return;const n=document.createElement('div');n.className='noti '+type;n.textContent=msg;c.appendChild(n);setTimeout(()=>{n.style.opacity='0';setTimeout(()=>n.remove(),200);},2200);}
function flash(id,ms){const e=$(id);if(e){e.classList.add('on');setTimeout(()=>e.classList.remove('on'),ms);}}

// ========== DATA ==========
const CHARS=[
{id:'glitch',name:'Glitch',emoji:'😎',role:'Speed',color:0x5C6BC0,spd:90,pow:50,jmp:80,skill:'Blink',sType:'tele',sCD:5},
{id:'tank',name:'Harold',emoji:'🦣',role:'Tank',color:0x795548,spd:45,pow:95,jmp:40,skill:'Quake',sType:'stun',sCD:8},
{id:'sally',name:'Sally',emoji:'🐍',role:'Speed',color:0x26A69A,spd:95,pow:45,jmp:75,skill:'Dash',sType:'dash',sCD:4},
{id:'blob',name:'Blobby',emoji:'🟣',role:'Jump',color:0xEC407A,spd:65,pow:55,jmp:99,skill:'Bounce',sType:'jump',sCD:3},
{id:'santa',name:'Santa',emoji:'🎅',role:'All',color:0xE74C3C,spd:70,pow:70,jmp:70,skill:'Gift',sType:'buff',sCD:10}
];

const GAMES=[
{id:'stars',name:'⭐ Star Collector',tip:'Collect stars! Gold=30pts!',dur:50,type:'collect'},
{id:'sumo',name:'💪 Sumo Ring',tip:'Push enemies out of the ring!',dur:55,type:'sumo'},
{id:'hill',name:'👑 King of Hill',tip:'Stay on hill to score! Knocked off after 5s!',dur:50,type:'hill'},
{id:'tag',name:'🏷️ Tag Frenzy',tip:'GRAB to pass the tag! Don\'t be IT!',dur:45,type:'tag'},
{id:'pads',name:'🪑 Musical Pads',tip:'Stand on GREEN pad when music stops!',dur:70,type:'pads'}
];

const IS_DEC = new Date().getMonth() === 11;
if(IS_DEC){
  const ll=$('ldLogo'); if(ll)ll.textContent='🎄';
  const ls=$('ldSub'); if(ls)ls.textContent='HOLIDAY EDITION';
}
const EMOTES=['😄','🎄','🎅','⛄','🎁','❄️','🔥','💪'];

// ========== STATE ==========
const ST={LOAD:0,LOBBY:1,CDOWN:2,GAME:3,RES:4};
let state=ST.LOAD;
let P={gems:500,crowns:10,charId:'glitch',score:0,isIt:false,tagImmune:0,
skillCD:0,grabCD:0,stunned:0,stamina:100,sprinting:false,hillTime:0,lv:1,xp:0,buffTime:0};
let selChar='glitch';
let scene,cam,ren,clk,sun;
var player,bots=[],lobbyMeshes=[],gameMeshes=[],stars=[],pads=[];
let solidPlatforms=[]; // {mesh, radius, topY}
let hillMesh=null; // {mesh, radius, topY}
let interacts=[];
const joy={l:{x:0,y:0},r:{x:0,y:0}};
let camAng=0,pVel={x:0,y:0,z:0},grounded=true,near=null;
let curGame=null,gTimer=0,gActive=false,rGames=[],rIdx=0;
let musicOn=true,padCount=16,scoreT=0;
let particles3d=[];
let shakeAmt=0;

const G=.03,SPD=.13,JMP=.4,FRC=.86;

function getC(id){return CHARS.find(c=>c.id===id)||CHARS[0];}
function curC(){return getC(P.charId);}

// ========== THREE SETUP ==========
function initThree(){
scene=new THREE.Scene();
scene.background=new THREE.Color(0x1a2a4a);
scene.fog=new THREE.FogExp2(0x1a2a4a,.005);
cam=new THREE.PerspectiveCamera(55,innerWidth/innerHeight,.1,800);
ren=new THREE.WebGLRenderer({canvas:$('C'),antialias:true});
ren.setSize(innerWidth,innerHeight);
ren.setPixelRatio(Math.min(devicePixelRatio,2));
ren.shadowMap.enabled=true;
ren.shadowMap.type=THREE.PCFSoftShadowMap;
ren.toneMapping=THREE.ACESFilmicToneMapping;
ren.toneMappingExposure=1.2;
clk=new THREE.Clock();
// Lights
scene.add(new THREE.AmbientLight(0x8899bb,.5));
sun=new THREE.DirectionalLight(0xfff5e0,1.1);
sun.position.set(80,120,80);sun.castShadow=true;
const s=sun.shadow;s.mapSize.width=s.mapSize.height=2048;s.camera.near=20;s.camera.far=400;s.camera.left=s.camera.bottom=-120;s.camera.right=s.camera.top=120;
scene.add(sun);
scene.add(new THREE.HemisphereLight(0x6699cc,0x334455,.5));
}

function mat(c,r=.5){return new THREE.MeshStandardMaterial({color:c,roughness:r,metalness:.1});}

function makeChar(ch,isBot=false){
const g=new THREE.Group();
const col=ch.color;
// Body (cyl+spheres = capsule shape, NO CapsuleGeometry)
const bm=mat(col,.35);
const body=sMesh(new THREE.CylinderGeometry(.4,.44,.7,12),bm);
body.position.y=1;body.castShadow=true;g.add(body);
const top=sMesh(new THREE.SphereGeometry(.4,12,10),bm);
top.position.y=1.35;top.castShadow=true;g.add(top);
const bot=sMesh(new THREE.SphereGeometry(.44,12,10),bm);
bot.position.y=.65;bot.castShadow=true;g.add(bot);
// Head
const head=sMesh(new THREE.SphereGeometry(.36,16,14),mat(0xFFDFC4,.45));
head.position.y=1.85;head.castShadow=true;g.add(head);
// Eyes
[-1,1].forEach(s=>{
const eye=sMesh(new THREE.SphereGeometry(.07,8,6),mat(0x111111));
eye.position.set(s*.12,1.9,.3);g.add(eye);
});
// Hat
const hat=sMesh(new THREE.ConeGeometry(.28,.45,8),mat(0xE74C3C,.4));
hat.position.y=2.2;hat.rotation.z=.12;g.add(hat);
const pom=sMesh(new THREE.SphereGeometry(.07,8,6),mat(0xffffff));
pom.position.set(.07,2.42,0);g.add(pom);
// Bot indicator
if(isBot){
const ant=sMesh(new THREE.CylinderGeometry(.015,.015,.28,6),mat(0x444444));
ant.position.y=2.45;g.add(ant);
const ball=sMesh(new THREE.SphereGeometry(.05,8,6),mat(0xFF4444));
ball.position.y=2.55;g.add(ball);
}
return g;
}

// ========== LOBBY ==========

function buildLobby(){
lobbyMeshes.forEach(o=>scene.remove(o)); lobbyMeshes=[];
gameMeshes.forEach(o=>scene.remove(o)); gameMeshes=[];
interacts=[];
solidPlatforms=[];
if(IS_DEC){
const gnd=sMesh(new THREE.CircleGeometry(110,60),mat(0xE8F4F8,.8));
gnd.rotation.x=-Math.PI/2;addMesh(gnd,true);
const plazaR=18,plazaH=3;
const plaza=sMesh(new THREE.CylinderGeometry(plazaR,plazaR+2,plazaH,32),mat(0x6D4C41,.5));
plaza.position.y=plazaH/2;addMesh(plaza,true);
solidPlatforms.push({mesh:plaza,radius:plazaR+2,topY:plazaH});
buildXmasTree(0,plazaH,0);
buildPortal(0,0,-42); buildMirror(42,0,0); buildArcade(-42,0,0);
for(let i=0;i<30;i++){ const a=(i/30)*Math.PI*2+rnd(-.2,.2),r=55+rnd(0,45); buildPine(Math.cos(a)*r,Math.sin(a)*r); }
for(let i=0;i<8;i++){ const a=rnd(0,Math.PI*2),r=30+rnd(0,35); buildSnowman(Math.cos(a)*r,Math.sin(a)*r); }
for(let i=0;i<15;i++){ const a=rnd(0,Math.PI*2),r=24+rnd(0,50); buildPresent(Math.cos(a)*r,Math.sin(a)*r); }
for(let i=0;i<6;i++){ const a=(i/6)*Math.PI*2,r=30; buildLamp(Math.cos(a)*r,Math.sin(a)*r); }
}else{
const gnd=sMesh(new THREE.CircleGeometry(110,60),mat(0x388E3C));
gnd.rotation.x=-Math.PI/2;addMesh(gnd,true);
const plazaR=20,plazaH=1.5;
const plaza=sMesh(new THREE.CylinderGeometry(plazaR,plazaR,plazaH,32),mat(0xCFD8DC));
plaza.position.y=plazaH/2;addMesh(plaza,true);
solidPlatforms.push({mesh:plaza,radius:plazaR,topY:plazaH});
// Fountain
const f=new THREE.Group(); f.position.set(0,plazaH,0);
const fBase=sMesh(new THREE.CylinderGeometry(5,5,0.8,24),mat(0x90A4AE)); fBase.position.y=0.4; f.add(fBase);
const fMid=sMesh(new THREE.CylinderGeometry(1,1,3,16),mat(0x90A4AE)); fMid.position.y=2; f.add(fMid);
const fTop=sMesh(new THREE.CylinderGeometry(3,3,0.4,16),mat(0x90A4AE)); fTop.position.y=3.5; f.add(fTop);
const water=sMesh(new THREE.SphereGeometry(2.5,16,12,0,Math.PI*2,0,Math.PI/2),mat(0x29B6F6,.6));
water.position.y=3.5; f.add(water);
const lt=new THREE.PointLight(0x29B6F6,2,25); lt.position.y=5; f.add(lt);
addMesh(f,true);
buildPortal(0,0,-45); buildMirror(45,0,0); buildArcade(-45,0,0);
for(let i=0;i<40;i++){
const a=(i/40)*Math.PI*2+rnd(-.1,.1), r=45+rnd(0,55);
const x=Math.cos(a)*r, z=Math.sin(a)*r;
if(Math.random()>0.4){
const h=rnd(6,15);
const tree=new THREE.Group(); tree.position.set(x,0,z);
const tr=sMesh(new THREE.CylinderGeometry(.4,.6,h*.3,8),mat(0x5D4037)); tr.position.y=h*.15; tree.add(tr);
const leaf=sMesh(new THREE.ConeGeometry(rnd(3,5),h*.8,8),mat(0x2E7D32)); leaf.position.y=h*.5; tree.add(leaf);
addMesh(tree,true);
} else {
const rock=sMesh(new THREE.DodecahedronGeometry(rnd(2,4)),mat(0x9E9E9E));
rock.position.set(x,1,z); rock.rotation.set(rnd(0,6),rnd(0,6),rnd(0,6)); addMesh(rock,true);
}
}
}
}


function buildXmasTree(x,y,z){
const g=new THREE.Group();g.position.set(x,y,z);
const trunk=sMesh(new THREE.CylinderGeometry(1,1.5,3,10),mat(0x5D4037,.8));
trunk.position.y=1.5;trunk.castShadow=true;g.add(trunk);
for(let i=0;i<4;i++){
const layer=sMesh(new THREE.ConeGeometry(5.5-i*1,4.5,12),mat(0x2E7D32,.7));
layer.position.y=4.5+i*3;layer.castShadow=true;g.add(layer);
}
const star=sMesh(new THREE.OctahedronGeometry(1),mat(0xFFD700,.2));
star.position.y=18;star.userData.spin=true;g.add(star);
// Ornaments
for(let i=0;i<35;i++){
const orb=sMesh(new THREE.SphereGeometry(.3,10,8),mat([0xFF0000,0x0000FF,0xFFD700,0xFF69B4][i%4],.3));
const a=rnd(0,Math.PI*2),r=rnd(.8,4.5-i/10),h=4.5+rnd(0,10);
orb.position.set(Math.cos(a)*r,h,Math.sin(a)*r);g.add(orb);
}
scene.add(g);lobbyMeshes.push(g);
}

function buildPortal(x,y,z){
const g=new THREE.Group();g.position.set(x,y,z);
for(let i=0;i<3;i++){
const step=sMesh(new THREE.CylinderGeometry(8-i,8.5-i,.6,14),mat(0xE0E0E0,.3));
step.position.y=.3+i*.6;step.castShadow=true;g.add(step);
}
const ring=sMesh(new THREE.TorusGeometry(3,.6,10,20),mat(0x9C27B0,.3));
ring.position.y=5;ring.userData.spin=true;g.add(ring);
const orb=sMesh(new THREE.SphereGeometry(1.6,14,12),mat(0x00E5FF,.2));
orb.position.y=5;orb.userData.bob=true;orb.userData.baseY=5;g.add(orb);
g.userData={interact:true,type:'portal',text:'Enter Portal',icon:'🌀',r:12};
scene.add(g);lobbyMeshes.push(g);interacts.push(g);
}

function buildMirror(x,y,z){
const g=new THREE.Group();g.position.set(x,y,z);
const frame=sMesh(new THREE.BoxGeometry(5,7,.7),mat(0xFFD700,.2));
frame.position.y=4;frame.castShadow=true;g.add(frame);
const mirror=sMesh(new THREE.BoxGeometry(4.2,6,.15),new THREE.MeshStandardMaterial({color:0xE8EAF6,metalness:.95,roughness:.05}));
mirror.position.set(0,4,.45);g.add(mirror);
g.rotation.y=-Math.PI/2;
g.userData={interact:true,type:'char',text:'Choose Runner',icon:'🎭',r:10};
scene.add(g);lobbyMeshes.push(g);interacts.push(g);
}

function buildArcade(x,y,z){
const g=new THREE.Group();g.position.set(x,y,z);
const body=sMesh(new THREE.BoxGeometry(5,6.5,3),mat(0x1A237E,.5));
body.position.y=3.25;body.castShadow=true;g.add(body);
const screen=sMesh(new THREE.BoxGeometry(3.5,2.5,.15),mat(0x00E676,.3));
screen.position.set(0,4.5,1.6);g.add(screen);
g.rotation.y=Math.PI/2;
g.userData={interact:true,type:'arcade',text:'Practice',icon:'🕹️',r:10};
scene.add(g);lobbyMeshes.push(g);interacts.push(g);
}

function buildPine(x,z){
const g=new THREE.Group();g.position.set(x,0,z);
const h=rnd(7,13);
const trunk=sMesh(new THREE.CylinderGeometry(.4,.65,h*.3,8),mat(0x5D4037,.85));
trunk.position.y=h*.15;trunk.castShadow=true;g.add(trunk);
for(let i=0;i<3;i++){
const cone=sMesh(new THREE.ConeGeometry(2.5-i*.5,h*.22,10),mat(0x2E7D32,.7));
cone.position.y=h*.3+i*h*.18;cone.castShadow=true;g.add(cone);
}
const snow=sMesh(new THREE.ConeGeometry(1.2,.5,10),mat(0xFFFFFF,.8));
snow.position.y=h*.3+2*h*.18+.3;g.add(snow);
scene.add(g);lobbyMeshes.push(g);
}

function buildSnowman(x,z){
  const g=new THREE.Group();g.position.set(x,0,z);
  const sm=mat(0xFFFFFF,.75);
  const snowmanParts = [
    { radius: 1.2, segs: 14, rings: 12, y: 1.2 },
    { radius: 0.9, segs: 12, rings: 10, y: 2.8 },
    { radius: 0.65, segs: 10, rings: 8, y: 4.0 },
  ];
  snowmanParts.forEach(({ radius, segs, rings, y }) => {
    const sphere = sMesh(new THREE.SphereGeometry(radius, segs, rings), sm);
    sphere.position.set(0, y, 0);
    g.add(sphere);
  });
  const nose = sMesh(new THREE.ConeGeometry(.08,.45,6),mat(0xFF6600));
  nose.position.set(0,4,.65);nose.rotation.x=Math.PI/2;g.add(nose);
  scene.add(g);lobbyMeshes.push(g);
}

function buildPresent(x,z){
const g=new THREE.Group();g.position.set(x,0,z);
const s=rnd(.5,1);
const col=[0xFF0000,0x00FF00,0x0000FF,0xFF69B4][Math.floor(Math.random()*4)];
const box=sMesh(new THREE.BoxGeometry(s,s,s),mat(col,.4));
box.position.y=s/2;box.castShadow=true;g.add(box);
const rb=sMesh(new THREE.BoxGeometry(s*1.05,s*.1,s*1.05),mat(0xFFD700,.3));
rb.position.y=s/2;g.add(rb);
const bow=sMesh(new THREE.SphereGeometry(s*.2,8,6),mat(0xFFD700,.3));
bow.position.y=s+s*.1;g.add(bow);
scene.add(g);lobbyMeshes.push(g);
}

function buildLamp(x,z){
const g=new THREE.Group();g.position.set(x,0,z);
const pole=sMesh(new THREE.CylinderGeometry(.12,.18,5,8),mat(0x333333,.4));
pole.position.y=2.5;pole.castShadow=true;g.add(pole);
const lamp=sMesh(new THREE.SphereGeometry(.4,10,8),mat(0xFFE4B5,.25));
lamp.position.y=5.3;g.add(lamp);
const lt=new THREE.PointLight(0xFFE4B5,1.2,16);
lt.position.y=5.3;g.add(lt);
scene.add(g);lobbyMeshes.push(g);
}

// ========== PLAYER & BOTS ==========
function spawnPlayer(){
player=makeChar(curC(),false);
player.position.set(0,3.5,22);
scene.add(player);
}

function spawnBots(n){
bots.forEach(b=>scene.remove(b.mesh));bots=[];
const pool=CHARS.filter(c=>c.id!==P.charId);
for(let i=0;i<n;i++){
const ch=pool[i%pool.length];
const mesh=makeChar(ch,true);
const a=((i+1)/(n+1))*Math.PI*2,r=24+rnd(0,10);
mesh.position.set(Math.cos(a)*r,0,Math.sin(a)*r);
bots.push({
mesh,ch,name:ch.name,emoji:ch.emoji,color:ch.color,
score:0,isIt:false,tagImmune:0,stunned:0,
vel:{x:0,y:0,z:0},grounded:true,eliminated:false,
hillTime:0,target:null,aiTimer:0
});
scene.add(mesh);
}
}

// ========== GROUND / PHYSICS ==========
// THE key fix: ONE function determines ground height, no bouncing ever
function getGroundY(pos){
let gy=0;
// Lobby solids
if(state===ST.LOBBY){
solidPlatforms.forEach(sp=>{
const d=d2(pos,sp.mesh.position);
if(d<sp.radius) gy=Math.max(gy,sp.topY);
});
}
// Game hill
if(hillMesh){
const hd=d2(pos,hillMesh.mesh.position);
if(hd<hillMesh.radius) gy=Math.max(gy,hillMesh.topY);
}
return gy;
}

function applyPhysics(pos,vel){
// Gravity
if(!grounded) vel.y-=G;
// Move
pos.x+=vel.x;
pos.y+=vel.y;
pos.z+=vel.z;
// Ground
const gy=getGroundY(pos);
if(pos.y<=gy){
pos.y=gy;
vel.y=0;
grounded=true;
}else{
grounded=false;
}
// Friction
vel.x*=FRC;
vel.z*=FRC;
}

function applyBotPhysics(b){
if(!b.grounded) b.vel.y-=G;
b.mesh.position.x+=b.vel.x;
b.mesh.position.y+=b.vel.y;
b.mesh.position.z+=b.vel.z;
const gy=getGroundY(b.mesh.position);
if(b.mesh.position.y<=gy){
b.mesh.position.y=gy;
b.vel.y=0;
b.grounded=true;
}else b.grounded=false;
b.vel.x*=FRC;
b.vel.z*=FRC;
}

// ========== CONTROLS ==========
function initControls(){
mkJoy('joyL','knobL','l');
mkJoy('joyR','knobR','r');
const tap=(id,fn)=>{const e=$(id);if(!e)return;e.addEventListener('touchstart',ev=>{ev.preventDefault();ev.stopPropagation();fn();},{passive:false});e.addEventListener('click',ev=>{ev.preventDefault();fn();});};
tap('prGo',doInteract);
tap('bJump',doJump);
tap('bGrab',doGrab);
tap('bSkill',doSkill);
tap('bEmote',()=>$('emPop')?.classList.toggle('show'));
// Sprint hold
const sp=$('bSprint');
if(sp){
sp.addEventListener('touchstart',ev=>{ev.preventDefault();P.sprinting=true;sp.classList.add('on');},{passive:false});
sp.addEventListener('touchend',()=>{P.sprinting=false;sp.classList.remove('on');});
sp.addEventListener('touchcancel',()=>{P.sprinting=false;sp.classList.remove('on');});
}
// Emotes
const ep=$('emPop');
EMOTES.forEach(e=>{const b=document.createElement('button');b.textContent=e;b.onclick=()=>{notify(e);$('emPop')?.classList.remove('show');};ep?.appendChild(b);});
// Modal close
document.querySelectorAll('.overlay').forEach(o=>{o.addEventListener('click',ev=>{if(ev.target===o)o.classList.remove('show');});});
// Results
tap('resNext',()=>{hide('RES');if(rGames.length>0&&rIdx<rGames.length-1){rIdx++;setTimeout(()=>startMinigame(rGames[rIdx]),400);}else backToLobby();});
tap('resAgain',()=>{hide('RES');if(curGame)setTimeout(()=>startMinigame(curGame),300);else backToLobby();});
window.addEventListener('resize',()=>{cam.aspect=innerWidth/innerHeight;cam.updateProjectionMatrix();ren.setSize(innerWidth,innerHeight);});
}

function mkJoy(cId,kId,side){
const c=$(cId),k=$(kId);if(!c||!k)return;
const max=45;let cx=0,cy=0,tid=null;
c.addEventListener('touchstart',ev=>{ev.preventDefault();const t=ev.changedTouches[0];tid=t.identifier;const r=c.getBoundingClientRect();cx=r.left+r.width/2;cy=r.top+r.height/2;upd(t.clientX,t.clientY);},{passive:false});
c.addEventListener('touchmove',ev=>{ev.preventDefault();for(const t of ev.changedTouches)if(t.identifier===tid)upd(t.clientX,t.clientY);},{passive:false});
c.addEventListener('touchend',reset);c.addEventListener('touchcancel',reset);
function upd(tx,ty){let dx=tx-cx,dy=ty-cy;const d=Math.sqrt(dx*dx+dy*dy);if(d>max){dx=dx/d*max;dy=dy/d*max;}k.style.transform=`translate(calc(-50% + ${dx}px),calc(-50% + ${dy}px))`;joy[side]={x:dx/max,y:dy/max};}
function reset(){tid=null;joy[side]={x:0,y:0};k.style.transform='translate(-50%,-50%)';}
}

// ========== ACTIONS ==========
function doJump(){
if(P.stunned>0||!grounded)return;
pVel.y=JMP*(curC().jmp/80);
grounded=false;
mkParts(player.position.x,.3,player.position.z,0xFFFFFF,12);
}


function doGrab(){
if(P.grabCD>0||P.stunned>0||state!==ST.GAME)return;
P.grabCD=.5;cooldown('bGrab','cdGrab',.5,'grabCD');
const fwd=new THREE.Vector3(0,0,-1).applyAxisAngle(new THREE.Vector3(0,1,0),player.rotation.y);
const hit=player.position.clone().add(fwd.multiplyScalar(2));
bots.forEach(b=>{
if(b.eliminated||d3(hit,b.mesh.position)>3.2)return;
const dx=b.mesh.position.x-player.position.x,dz=b.mesh.position.z-player.position.z,dd=Math.sqrt(dx*dx+dz*dz);
if(dd>.05){b.vel.x+=(dx/dd)*(curC().pow/100)*.55;b.vel.z+=(dz/dd)*(curC().pow/100)*.55;b.vel.y=.15;}
b.stunned=.45;
mkParts(b.mesh.position.x,1.5,b.mesh.position.z,0xFF6B6B,16);
shakeAmt=.3;
if(curGame?.type==='tag'&&P.isIt&&b.tagImmune<=0){
P.isIt=false;b.isIt=true;b.tagImmune=3;P.tagImmune=2;
notify('Tagged '+b.name+'! +100','ok'); P.score+=100; b.score=Math.max(0,b.score-50);
updInd();
}
});
}



function doSkill(){
if(P.skillCD>0||P.stunned>0)return;
if(state!==ST.GAME&&state!==ST.LOBBY)return;
const c=curC();
P.skillCD=c.sCD;cooldown('bSkill','cdSkill',c.sCD,'skillCD');
const fwd=new THREE.Vector3(0,0,-1).applyAxisAngle(new THREE.Vector3(0,1,0),player.rotation.y);
switch(c.sType){
case'tele':
  mkParts(player.position.x,1.5,player.position.z,0x00FFFF,20);
  player.position.add(fwd.clone().multiplyScalar(10));
  mkParts(player.position.x,1.5,player.position.z,0x00FFFF,30);
  break;
case'dash':
  pVel.x+=fwd.x*1.2;pVel.z+=fwd.z*1.2;
  flash('SPEED',500);
  mkParts(player.position.x,1,player.position.z,0x4ECDC4,25);
  break;
case'jump':
  pVel.y=.7;grounded=false;
  mkParts(player.position.x,.3,player.position.z,0xFF69B4,25);
  break;
case'stun':
  bots.forEach(b=>{if(d3(player.position,b.mesh.position)<12){b.stunned=2.5;b.vel.y=.2;mkParts(b.mesh.position.x,1.5,b.mesh.position.z,0xFFD700,20);showEmoji(b.mesh,'💫');}});
  shakeAmt=.8;
  const ring=sMesh(new THREE.TorusGeometry(1,.2,8,32),mat(0xFFD700,.1));
  ring.position.copy(player.position); ring.rotation.x=Math.PI/2;
  scene.add(ring);
  let rStart=Date.now();
  const rAni=()=>{
    let age=(Date.now()-rStart)/600;
    if(age>=1){scene.remove(ring);return;}
    ring.scale.set(1+age*15, 1+age*15, 1);
    ring.material.opacity=1-age;
    requestAnimationFrame(rAni);
  };
  rAni();
  break;
case'buff':
  P.buffTime=5;
  notify('POWER UP!','ok');
  flash('SPEED',5000);
  mkParts(player.position.x,2,player.position.z,0xFF0000,30);
  break;
}
notify(c.skill+'!','inf');
showEmoji(player, c.emoji);
}

function cooldown(btnId,cdId,dur,prop){
const btn=$(btnId);if(btn)btn.classList.add('cd');
let rem=dur;
const iv=setInterval(()=>{
rem-=.1;const cd=$(cdId);if(cd)cd.textContent=Math.max(0,Math.ceil(rem));
if(rem<=0){clearInterval(iv);P[prop]=0;if(btn)btn.classList.remove('cd');}
},100);
}

function doInteract(){
if(!near)return;
const t=near.userData.type;
if(t==='portal'){show('oPortal');loadModes();}
else if(t==='char'){show('oChar');loadChars();}
else if(t==='arcade'){show('oArcade');loadArcade();}
$('PROMPT')?.classList.remove('show');
}

// ========== UI LOADERS ==========
function loadModes(){
const el=$('modeList');if(!el)return;
el.innerHTML='<div class="ml" id="mList"></div>';
const ml=$('mList');
[{name:'⚡ Quick',desc:'1 random game',cnt:1},{name:'🎉 Party',desc:'3 games',cnt:3}].forEach(m=>{
const c=document.createElement('div');c.className='mc';
c.innerHTML=`<span class="mc-icon">${m.name.split(' ')[0]}</span><div class="mc-info"><h4>${m.name}</h4><p>${m.desc}</p></div>`;
c.onclick=()=>{hide('oPortal');rGames=shuffle(GAMES).slice(0,m.cnt);rIdx=0;setTimeout(()=>startMinigame(rGames[0]),300);};
ml.appendChild(c);
});
}

function loadChars(){
const grid=$('charGrid');if(!grid)return;
grid.innerHTML='';
CHARS.forEach(c=>{
const card=document.createElement('div');
card.className='cc'+(c.id===selChar?' sel':'');
card.innerHTML=`<div class="cc-av" style="background:#${c.color.toString(16).padStart(6,'0')}">${c.emoji}</div><div class="cc-n">${c.name}</div><div class="cc-r">${c.role}</div>`;
card.onclick=()=>{selChar=c.id;loadChars();previewChar(c);};
grid.appendChild(card);
});
previewChar(getC(selChar));
}

function previewChar(c){
const el=$('charPrev');if(!el)return;
el.innerHTML=`<div class="cp-top"><div class="cp-av" style="background:#${c.color.toString(16).padStart(6,'0')}">${c.emoji}</div><div><div class="cp-name">${c.name}</div><div class="cp-role">${c.role}</div></div></div>
<div class="stats"><div class="stat">⚡<div class="stat-track"><div class="stat-fill" style="width:${c.spd}%;background:#4ecdc4"></div></div></div><div class="stat">💪<div class="stat-track"><div class="stat-fill" style="width:${c.pow}%;background:#ff6b6b"></div></div></div><div class="stat">🦘<div class="stat-track"><div class="stat-fill" style="width:${c.jmp}%;background:#f1c40f"></div></div></div></div>
<div class="ab"><h5>⚡ ${c.skill} (${c.sCD}s)</h5><p>Special ability</p></div>
<button class="sel-btn" id="selBtn">Play as ${c.name}</button>`;
$('selBtn').onclick=()=>{P.charId=c.id;updatePlayerMesh();hide('oChar');notify('Playing as '+c.name+'!','ok');};
}

function updatePlayerMesh(){
const pos=player.position.clone(),rot=player.rotation.y;
scene.remove(player);
player=makeChar(curC(),false);
player.position.copy(pos);player.rotation.y=rot;
scene.add(player);
setText('hAvatar',curC().emoji);
setText('lblSkill',curC().skill);
}

function loadArcade(){
const grid=$('arcGrid');if(!grid)return;
grid.innerHTML='';
GAMES.forEach(g=>{
const card=document.createElement('div');card.className='ac';
card.innerHTML=`<div class="ac-icon">${g.name.split(' ')[0]}</div><div class="ac-name">${g.name.substring(g.name.indexOf(' ')+1)}</div>`;
card.onclick=()=>{hide('oArcade');curGame=g;setTimeout(()=>startMinigame(g),300);};
grid.appendChild(card);
});
}

function updInd(){
const el=$('IND');if(!el)return;
if(curGame?.type==='tag'){
el.textContent=P.isIt?'🏷️ YOU ARE IT!':'🏷️ IT: '+(bots.find(b=>b.isIt)?.name||'?');
el.classList.add('show');
}else if(curGame?.type==='pads'){
el.textContent=musicOn?'🎵 Running...':'⚠️ FIND GREEN PAD!';
el.classList.add('show');
}else el.classList.remove('show');
}

// ========== SNOW ==========
function startSnow(){
setInterval(()=>{
if(state===ST.LOAD)return;
const f=document.createElement('div');f.className='snow';
f.textContent=['❄','❅','❆'][Math.floor(Math.random()*3)];
f.style.left=rnd(0,100)+'vw';f.style.fontSize=rnd(10,22)+'px';
f.style.animationDuration=rnd(5,9)+'s';
$('PARTS')?.appendChild(f);
setTimeout(()=>f.remove(),9000);
},220);
}

// ========== LOADING ==========
function startLoad(){
let p=0;
const iv=setInterval(()=>{
p+=rnd(16,28);if(p>100)p=100;
const fill=$('ldFill');if(fill)fill.style.width=p+'%';
if(p>=100){clearInterval(iv);setTimeout(()=>{$('LD')?.classList.add('gone');state=ST.LOBBY;},500);}
},130);
}

// ========== MINIGAME START ==========
function startMinigame(game){
state=ST.CDOWN;curGame=game;scoreT=0;musicOn=true;padCount=16;hillMesh=null;
$('hud').style.display='none';
$('MM')?.classList.remove('show');
$('PROMPT')?.classList.remove('show');
$('SIDE').style.display='flex';
// Hide grab for non-applicable
const gb=$('bGrab');if(gb)gb.classList.toggle('hidden',game.type==='collect'||game.type==='pads');
lobbyMeshes.forEach(o=>o.visible=false);
player.visible=false;bots.forEach(b=>b.mesh.visible=false);
solidPlatforms=[];
buildArena(game);
// Countdown
setText('cdName',game.name);setText('cdTip',game.tip);
show('CDOWN');
let cnt=3;setText('cdNum','3');$('cdNum').className='cd-num';
const iv=setInterval(()=>{
cnt--;
if(cnt>0)setText('cdNum',cnt);
else if(cnt===0){setText('cdNum','GO!');$('cdNum').className='cd-num cd-go';}
else{clearInterval(iv);hide('CDOWN');beginGame();}
},900);
}


function beginGame(){
state=ST.GAME;gActive=true;gTimer=curGame.dur;
show('GHUD');setText('gTitle',curGame.name);
show('SB');
$('BTNS').style.display='flex';
const tip=$('gTip');if(tip){tip.textContent='💡 '+curGame.tip;tip.classList.add('show');setTimeout(()=>tip.classList.remove('show'),3500);}
P.score=0;P.isIt=false;P.tagImmune=0;P.stamina=100;P.hillTime=0;P.sprinting=false;
bots.forEach(b=>{b.score=0;b.isIt=false;b.tagImmune=0;b.eliminated=false;b.mesh.visible=true;b.stunned=0;b.hillTime=0;b.aiTimer=0;});
if(curGame.type==='tag'){
const it=bots[Math.floor(Math.random()*bots.length)];
it.isIt=true;it.tagImmune=4;
updInd();
}
if(curGame.type==='pads'){resetPads();updInd();}
updateSB();
const tEl=$('gTime');
const iv=setInterval(()=>{
if(!gActive){clearInterval(iv);return;}
gTimer--;
if(tEl){tEl.textContent=Math.max(0,gTimer);tEl.className='g-time';if(gTimer<=10)tEl.classList.add('danger');else if(gTimer<=20)tEl.classList.add('warn');}
if(curGame?.type==='pads'&&gTimer%11===0&&gTimer>0&&gTimer<curGame.dur){
musicOn=!musicOn;
if(!musicOn){padCount=Math.max(2,padCount-2);notify('🎵 MUSIC STOPPED!','inf');setTimeout(()=>checkPads(),1200);}
else{notify('🎵 Playing!','inf');resetPads();}
updInd();
}
if(gTimer<=0){clearInterval(iv);endMinigame();}
},1000);
}


function showEmoji(parent, text){
const canvas = document.createElement('canvas');
canvas.width = 128; canvas.height = 128;
const ctx = canvas.getContext('2d');
ctx.font = '80px serif'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
ctx.fillText(text, 64, 64);
const tex = new THREE.CanvasTexture(canvas);
const smat = new THREE.SpriteMaterial({map: tex, transparent: true});
const sprite = new THREE.Sprite(smat);
sprite.position.y = 3.2; sprite.scale.set(2, 2, 2);
parent.add(sprite);
let start = Date.now();
const ani = () => {
  let age = (Date.now() - start) / 2000;
  if(age >= 1) { parent.remove(sprite); return; }
  sprite.position.y = 3.2 + age * 1.5;
  sprite.material.opacity = 1 - age;
  requestAnimationFrame(ani);
};
ani();
}

function buildArenaScenery(){
const R=120;
for(let i=0;i<20;i++){
const a=(i/20)*Math.PI*2+rnd(-.2,.2), r=R+rnd(0,60);
const x=Math.cos(a)*r, z=Math.sin(a)*r;
const g=new THREE.Group(); g.position.set(x,0,z);
if(Math.random()>0.5){
const h=rnd(8,20);
const tr=sMesh(new THREE.CylinderGeometry(.5,.8,h*.2,8),mat(0x5D4037)); tr.position.y=h*.1; g.add(tr);
for(let j=0;j<3;j++){
const leaf=sMesh(new THREE.ConeGeometry(5-j,h*.4,10),mat(0x2E7D32));
leaf.position.y=h*.3+j*h*.25; g.add(leaf);
}
} else {
const s=rnd(3,7);
const rock=sMesh(new THREE.DodecahedronGeometry(s),mat(0x757575));
rock.position.y=s*.6; rock.rotation.set(rnd(0,6),rnd(0,6),rnd(0,6)); g.add(rock);
}
addMesh(g,false);
}
}

// ========== ARENA BUILDER ==========
function buildArena(game){
lobbyMeshes.forEach(o=>scene.remove(o)); lobbyMeshes=[];
gameMeshes.forEach(o=>scene.remove(o)); gameMeshes=[];
stars=[];pads=[];hillMesh=null;solidPlatforms=[];
const bgMap={collect:0x0D47A1,sumo:0x3E2723,hill:0xBF360C,tag:0x01579B,pads:0x4A148C};
scene.background=new THREE.Color(bgMap[game.type]||0x1a2a4a);
scene.fog=new THREE.FogExp2(bgMap[game.type]||0x1a2a4a,.004);
buildArenaScenery();
const R=game.type==='sumo'?50:85;
// Ground
const gnd=sMesh(new THREE.CircleGeometry(R,60),mat({collect:0x2E7D32,sumo:0x5D4037,hill:0xBF360C,tag:0x006064,pads:0x4A148C}[game.type]||0x2E7D32,.8));
gnd.rotation.x=-Math.PI/2;gnd.receiveShadow=true;addMesh(gnd,false);
// Border
const bor=sMesh(new THREE.TorusGeometry(R,1.5,10,60),mat(0xFFD700,.4));
bor.rotation.x=Math.PI/2;bor.position.y=.75;addMesh(bor,false);
// Game-specific
if(game.type==='collect')for(let i=0;i<55;i++)spawnStar();
if(game.type==='hill'){
buildHill();
for(let i=0;i<4;i++){ const a=(i/4)*Math.PI*2, r=40, x=Math.cos(a)*r, z=Math.sin(a)*r; const p=sMesh(new THREE.CylinderGeometry(8,8,4,16),mat(0xBF360C)); p.position.set(x,2,z); addMesh(p); solidPlatforms.push({mesh:p,radius:8,topY:4}); }
}
if(game.type==='pads')buildPadGrid();
if(game.type==='tag'){
for(let i=0;i<8;i++){ const a=(i/8)*Math.PI*2, r=30, x=Math.cos(a)*r, z=Math.sin(a)*r; const p=sMesh(new THREE.BoxGeometry(6,12,6),mat(0x006064)); p.position.set(x,6,z); addMesh(p); solidPlatforms.push({mesh:p,radius:4,topY:12}); }
}
if(game.type==='sumo'){
for(let i=0;i<6;i++){ const a=(i/6)*Math.PI*2+rnd(-.3,.3),r=12+rnd(0,10); const p=sMesh(new THREE.DodecahedronGeometry(rnd(3,5)),mat(0x5D4037)); p.position.set(Math.cos(a)*r,2,Math.sin(a)*r); p.rotation.set(rnd(0,6),rnd(0,6),rnd(0,6)); addMesh(p); solidPlatforms.push({mesh:p,radius:4,topY:4}); }
}
// Players
player.visible=true;player.position.set(0,0,28);pVel={x:0,y:0,z:0};grounded=true;
bots.forEach((b,i)=>{
b.mesh.visible=true;b.eliminated=false;
const a=((i+1)/(bots.length+1))*Math.PI*2,r=22+rnd(0,10);
b.mesh.position.set(Math.cos(a)*r,0,Math.sin(a)*r);
b.vel={x:0,y:0,z:0};b.stunned=0;b.grounded=true;
});
}

function buildHill(){
const mesh=sMesh(new THREE.CylinderGeometry(16,20,10,32),mat(0xFFD700,.35));
mesh.position.y=4;mesh.castShadow=true;mesh.receiveShadow=true;
scene.add(mesh);gameMeshes.push(mesh);
hillMesh={mesh,radius:14,topY:8};
const crown=sMesh(new THREE.ConeGeometry(3,4,5),mat(0xFFD700,.2));
crown.position.y=11;crown.userData.spin=true;crown.userData.bob=true;crown.userData.baseY=11;
scene.add(crown);gameMeshes.push(crown);
}

function buildPadGrid(){
const sz=4,sp=12,off=-(sz-1)*sp/2;
for(let x=0;x<sz;x++){
for(let z=0;z<sz;z++){
const pad=sMesh(new THREE.CylinderGeometry(6,6.5,1.5,16),mat(0x9C27B0,.35));
pad.position.set(off+x*sp,.6,off+z*sp);
pad.userData={active:true,idx:x*sz+z};
scene.add(pad);gameMeshes.push(pad);pads.push(pad);
}
}
}

function resetPads(){
pads.forEach(p=>{p.userData.active=true;p.material.color.setHex(0x9C27B0);p.position.y=.6;});
const toOff=pads.length-padCount;
const sh=shuffle([...pads]);
for(let i=0;i<toOff;i++){sh[i].userData.active=false;sh[i].material.color.setHex(0x333333);sh[i].position.y=-.5;}
pads.filter(p=>p.userData.active).forEach(p=>p.material.color.setHex(0x00FF00));
}


function checkPads(){
const activePads = pads.filter(p=>p.userData.active);
const participants = [
{id:'player', pos:player.position, obj:P, name:'You'},
...bots.filter(b=>!b.eliminated).map(b=>({id:b.name, pos:b.mesh.position, obj:b, name:b.name}))
];
const winners = new Set();
const padOccupant = new Map();
participants.forEach(p => {
  let bestPad = null, bestD = 5;
  activePads.forEach(pad => {
    const d = d2(p.pos, pad.position);
    if(d < bestD) { bestPad = pad; bestD = d; }
  });
  if(bestPad) {
    if(!padOccupant.has(bestPad) || padOccupant.get(bestPad).dist > bestD) {
      padOccupant.set(bestPad, {p, dist: bestD});
    }
  }
});
padOccupant.forEach((v, pad) => {
  winners.add(v.p.id);
  pad.material.color.setHex(0x4444FF);
});
if(winners.has('player')){ P.score+=25; notify('Safe! +25','ok'); }
else { P.score=Math.max(0,P.score-40); flash('STUMBLE',350); notify('No pad! -40','bad'); }
bots.forEach(b => {
  if(b.eliminated) return;
  if(winners.has(b.name)) b.score+=25;
  else b.score=Math.max(0,b.score-40);
});
setTimeout(()=>{musicOn=true;resetPads();updInd();},2000);
}


function spawnStar(){
const gold=Math.random()<.12;
const val=gold?30:10;
const shape=new THREE.Shape();
for(let i=0;i<10;i++){const r=i%2===0?.8:.38,a=(i/10)*Math.PI*2-Math.PI/2;if(i===0)shape.moveTo(Math.cos(a)*r,Math.sin(a)*r);else shape.lineTo(Math.cos(a)*r,Math.sin(a)*r);}
shape.closePath();
const mesh=sMesh(new THREE.ExtrudeGeometry(shape,{depth:.35,bevelEnabled:false}),mat(gold?0xFFD700:0xFFFF00,.3));
if(gold)mesh.scale.setScalar(1.5);
const a=rnd(0,Math.PI*2),r=rnd(10,60);
mesh.position.set(Math.cos(a)*r,2.5,Math.sin(a)*r);
mesh.rotation.x=Math.PI/2;
mesh.userData={val,off:rnd(0,Math.PI*2)};
scene.add(mesh);gameMeshes.push(mesh);stars.push(mesh);
}

// ========== BOT AI ==========

function runBotAI(dt){
const spd_base=SPD*.7*(curGame?.type==='pads'?.6:1)*(curGame?.type==='sumo'?.7:1);
bots.forEach((b,idx)=>{
if(b.eliminated){b.mesh.visible=true;return;}
if(b.stunned>0){b.stunned-=dt;return;}
if(b.tagImmune>0)b.tagImmune-=dt;
b.aiTimer-=dt;
if(b.aiTimer<=0){
b.aiTimer=rnd(.3,1);
if(curGame?.type==='collect'){
let best=null,bestD=Infinity;
stars.forEach(s=>{if(!s.userData.taken){const dd=d3(b.mesh.position,s.position);if(dd<bestD){bestD=dd;best=s;}}});
if(best)b.target={x:best.position.x,z:best.position.z};
}else if(curGame?.type==='hill'){
b.target={x:rnd(-5,5),z:rnd(-5,5)};
}else if(curGame?.type==='tag'){
if(b.isIt){
let best=null,bestD=Infinity;
if(!P.isIt&&P.tagImmune<=0){const dd=d2(b.mesh.position,player.position);if(dd<bestD){bestD=dd;best=player.position;}}
bots.forEach(o=>{if(o!==b&&!o.isIt&&!o.eliminated&&o.tagImmune<=0){const dd=d2(b.mesh.position,o.mesh.position);if(dd<bestD){bestD=dd;best=o.mesh.position;}}});
if(best)b.target={x:best.x,z:best.z};
}else{
const it=bots.find(o=>o.isIt)||(P.isIt?player:null);
if(it){
const pos=it.position||it.mesh?.position;
if(pos){const dx=b.mesh.position.x-pos.x,dz=b.mesh.position.z-pos.z,dd=Math.sqrt(dx*dx+dz*dz);
if(dd>.1)b.target={x:b.mesh.position.x+(dx/dd)*22,z:b.mesh.position.z+(dz/dd)*22};}
}
}
}else if(curGame?.type==='pads'&&!musicOn){
const active=pads.filter(p=>p.userData.active);
if(active.length>0){const pad=active[idx%active.length];b.target={x:pad.position.x,z:pad.position.z};}
}else if(curGame?.type==='sumo'){
if(Math.random()>.4){b.target={x:player.position.x,z:player.position.z};}
else{const o=bots.filter(x=>x!==b&&!x.eliminated);if(o.length){const t=o[Math.floor(Math.random()*o.length)];b.target={x:t.mesh.position.x,z:t.mesh.position.z};}}
}else b.target={x:rnd(-35,35),z:rnd(-35,35)};
}
if(b.target){
const dx=b.target.x-b.mesh.position.x,dz=b.target.z-b.mesh.position.z,dd=Math.sqrt(dx*dx+dz*dz);
if(dd>1.2){
const s=spd_base*(b.ch.spd/80);
b.mesh.position.x+=(dx/dd)*s;
b.mesh.position.z+=(dz/dd)*s;
b.mesh.rotation.y=Math.atan2(dx,dz);
}
}
if(state===ST.GAME && !b.isIt && Math.random() < 0.02) {
  const targets = [player, ...bots.filter(o=>o!==b)];
  targets.forEach(t => {
    const tPos = t.position || t.mesh.position;
    if(d3(b.mesh.position, tPos) < 4) {
      const dx=tPos.x-b.mesh.position.x, dz=tPos.z-b.mesh.position.z, dd=Math.sqrt(dx*dx+dz*dz);
      if(t === player) { pVel.x+=(dx/dd)*0.4; pVel.z+=(dz/dd)*0.4; pVel.y=0.15; P.stunned=0.4; flash('STUMBLE', 300); }
      else { t.vel.x+=(dx/dd)*0.4; t.vel.z+=(dz/dd)*0.4; t.vel.y=0.15; t.stunned=0.4; }
      mkParts(tPos.x, 1.5, tPos.z, 0xFFFFFF, 10);
    }
  });
}
applyBotPhysics(b);
const bd=d2(b.mesh.position,{x:0,z:0});
const sumoR = (curGame?.type==='sumo'?28:70);
if(bd>sumoR){
if(curGame?.type==='sumo'){b.score=Math.max(0,b.score-50);const a=rnd(0,Math.PI*2);b.mesh.position.set(Math.cos(a)*15,0,Math.sin(a)*15);}
else{b.mesh.position.x*=sumoR/bd;b.mesh.position.z*=sumoR/bd;}
}
stars.forEach(s=>{
if(!s.userData.taken&&d3(b.mesh.position,s.position)<3){
s.userData.taken=true;scene.remove(s);b.score+=s.userData.val;
setTimeout(()=>spawnStar(),4000);
}
});
if(curGame?.type==='tag'&&b.isIt&&b.tagImmune<=0){
if(!P.isIt&&P.tagImmune<=0&&d3(b.mesh.position,player.position)<3){
b.isIt=false;P.isIt=true;P.tagImmune=3;
notify('⚠️ YOU\'RE IT! -50','bad'); P.score=Math.max(0,P.score-50); b.score+=100; updInd();
}
bots.forEach(o=>{
if(o!==b&&!o.isIt&&!o.eliminated&&o.tagImmune<=0&&d3(b.mesh.position,o.mesh.position)<3){
b.isIt=false;o.isIt=true;o.tagImmune=3;b.score+=100;o.score=Math.max(0,o.score-50);updInd();
}
});
}
if(curGame?.type==='hill'&&hillMesh){
const hd=d2(b.mesh.position,{x:0,z:0});
if(hd<hillMesh.radius&&b.mesh.position.y>=hillMesh.topY-.5){
b.hillTime=(b.hillTime||0)+dt;
if(b.hillTime>=1){b.score+=1;b.hillTime-=1;}
if(b.hillTime>=5){ const a=rnd(0,Math.PI*2); b.vel.x+=Math.cos(a)*.5; b.vel.z+=Math.sin(a)*.5; b.vel.y=.25; b.hillTime=0; }
}else b.hillTime=0;
}
});
}



function updateMinigame(dt){
if(!gActive)return;
if(P.tagImmune>0)P.tagImmune-=dt;
if(!P.sprinting&&P.stamina<100)P.stamina=Math.min(100,P.stamina+22*dt);
scoreT+=dt;
if(P.buffTime>0)P.buffTime-=dt;
const t=Date.now()*.001;
gameMeshes.forEach(o=>{
if(o.userData.bob)o.position.y=(o.userData.baseY||4)+Math.sin(t*2)*.5;
if(curGame?.type==='hill' && o.geometry.type==='ConeGeometry') o.scale.setScalar(1+Math.sin(t*5)*0.1);
if(o.userData.spin)o.rotation.y+=dt;
});
stars.forEach(s=>{
if(!s.userData.taken){
s.position.y=2.5+Math.sin(t*3+s.userData.off)*.5;
s.rotation.z+=dt*5;
if(d3(player.position,s.position)<3){
s.userData.taken=true;scene.remove(s);
P.score+=s.userData.val;
mkParts(s.position.x,s.position.y,s.position.z,0xFFD700,18);
setTimeout(()=>spawnStar(),4000);
}
}
});
if(curGame?.type==='hill'&&hillMesh){
const hd=d2(player.position,{x:0,z:0});
if(hd<hillMesh.radius&&player.position.y>=hillMesh.topY-.5){
P.hillTime+=dt;
if(P.hillTime>=1){P.score+=1;P.hillTime-=1;}
if(P.hillTime>=5){
const a=rnd(0,Math.PI*2); pVel.x+=Math.cos(a)*.6; pVel.z+=Math.sin(a)*.6; pVel.y=.3;
P.hillTime=0; notify('Knocked off!','inf'); mkParts(player.position.x,1.5,player.position.z,0xFFD700,20);
}
}else P.hillTime=0;
}
if(curGame?.type==='sumo'){
if(scoreT>=1){ if(!P.isIt)P.score+=1; bots.forEach(b=>{if(!b.isIt&&!b.eliminated)b.score+=1;}); scoreT=0; }
const pd=d2(player.position,{x:0,z:0});
const sumoR = (curGame?.type==='sumo'?28:70);
if(pd>sumoR){P.score=Math.max(0,P.score-50);player.position.set(0,0,0);flash('STUMBLE',350);}
if(gTimer < curGame.dur - 10) {
  const shrink = 1 - (curGame.dur - 10 - gTimer) / 100;
  const currentR = Math.max(15, 40 * shrink);
  if(gameMeshes[0]) gameMeshes[0].scale.set(currentR/40, 1, currentR/40);
  if(gameMeshes[1]) gameMeshes[1].scale.set(currentR/40, 1, currentR/40);
  if(pd > currentR) { P.score=Math.max(0,P.score-50); player.position.set(0,0,0); flash('STUMBLE',350); }
  bots.forEach(b => { if(!b.eliminated && d2(b.mesh.position,{x:0,z:0}) > currentR) { b.score=Math.max(0,b.score-50); b.mesh.position.set(0,0,0); } });
}
}
if(curGame?.type==='tag'){
const pd=d2(player.position,{x:0,z:0});
if(pd>70){player.position.x*=70/pd;player.position.z*=70/pd;}
if(P.isIt&&P.tagImmune<=0){
bots.forEach(b=>{
if(!b.isIt&&!b.eliminated&&b.tagImmune<=0&&d3(player.position,b.mesh.position)<3){
P.isIt=false;b.isIt=true;b.tagImmune=3;P.tagImmune=2;
notify('Tagged '+b.name+'! +100','ok'); P.score+=100; b.score=Math.max(0,b.score-50);updInd();
}
});
}
}
if(curGame?.type==='pads'){
  if(musicOn){
    const pd=d2(player.position,{x:0,z:0});
    if(pd>70){player.position.x*=70/pd;player.position.z*=70/pd;}
  }
}
if(curGame?.type==='collect'){
  const pd=d2(player.position,{x:0,z:0});
  if(pd>70){player.position.x*=70/pd;player.position.z*=70/pd;}
}
runBotAI(dt);
updateSB();
updateMM();
}


function getAllScores(){
return[{name:'You',score:Math.floor(P.score),emoji:curC().emoji,color:curC().color,isPlayer:true,isIt:P.isIt},
...bots.map(b=>({name:b.name,score:Math.floor(b.score),emoji:b.emoji,color:b.color,isPlayer:false,isIt:b.isIt,eliminated:b.eliminated}))
].sort((a,b)=>b.score-a.score);
}

function updateSB(){
const body=$('sbBody');if(!body)return;
body.innerHTML='';
getAllScores().slice(0,10).forEach((e,i)=>{
const d=document.createElement('div');
d.className='sb-r'+(e.isPlayer?' me':'')+(i===0?' top':'');
d.innerHTML=`<span class="sb-rk">${i+1}</span><span class="sb-nm">${e.emoji} ${e.name}${e.isIt?' 🏷️':''}</span><span class="sb-sc">${e.score}</span>`;
body.appendChild(d);
});
}

function updateMM(){
const mm=$('MM');if(!mm)return;
mm.classList.add('show');
mm.querySelectorAll('.mm-dot').forEach(d=>d.remove());
bots.forEach(b=>{
if(b.eliminated)return;
const dx=b.mesh.position.x-player.position.x,dz=b.mesh.position.z-player.position.z;
if(Math.abs(dx)<60&&Math.abs(dz)<60){
const dot=document.createElement('div');
dot.className='mm-dot bot'+(b.isIt?' it':'');
dot.style.left=(50+dx*.65)+'px';
dot.style.top=(50+dz*.65)+'px';
mm.appendChild(dot);
}
});
}

function endMinigame(){
gActive=false;state=ST.RES;
hide('GHUD');hide('SB');hide('IND');
$('BTNS').style.display='none';
showResults();
}

function showResults(){
const scores=getAllScores();
const rank=scores.findIndex(s=>s.isPlayer)+1;
const won=rank===1;
setText('resT',won?'🎉 VICTORY!':rank<=3?'🥈 Nice!':'Try Again');
setText('resS',`#${rank} — ${P.score} pts`);
const pod=$('resPod');if(pod){
pod.innerHTML='';
const order=[scores[1],scores[0],scores[2]],places=[2,1,3];
order.forEach((e,i)=>{
if(!e)return;
const d=document.createElement('div');d.className='pod-s';
d.innerHTML=`<div class="pod-av" style="background:#${e.color.toString(16).padStart(6,'0')}">${e.emoji}</div><div class="pod-n">${e.name}</div><div class="pod-p">${e.score}</div><div class="pod-b">${places[i]}</div>`;
pod.appendChild(d);
});
}
const shards=won?180:50+rank*15;
P.gems+=shards;
setText('hGems',P.gems);
const rr=$('resRew');if(rr)rr.innerHTML=`<div class="rew-c">💎 +${shards}</div>`;
show('RES');
if(won)for(let i=0;i<50;i++)setTimeout(()=>{
const c=document.createElement('div');c.className='snow';c.textContent=(IS_DEC?['🎉','🎊','⭐','🎄','🎅']:['🎉','🎊','⭐','💎','🏆'])[Math.floor(Math.random()*5)];c.style.left=rnd(0,100)+'vw';c.style.fontSize='24px';c.style.animationDuration=rnd(3,5)+'s';$('PARTS')?.appendChild(c);setTimeout(()=>c.remove(),5000);
},i*40);
const next=$('resNext');if(next)next.textContent=rGames.length>0&&rIdx<rGames.length-1?'Next Game':'Continue';
}

function backToLobby(){
state=ST.LOBBY;curGame=null;rGames=[];rIdx=0;hillMesh=null;
hide('RES');
$('hud').style.display='block';
hide('IND');
$('SIDE').style.display='none';
$('bGrab')?.classList.remove('hidden');
scene.background=new THREE.Color(0x1a2a4a);
scene.fog=new THREE.FogExp2(0x1a2a4a,.005);
buildLobby();
player.visible=true;player.position.set(0,3.5,22);pVel={x:0,y:0,z:0};
bots.forEach((b,i)=>{b.mesh.visible=true;b.eliminated=false;const a=((i+1)/(bots.length+1))*Math.PI*2;b.mesh.position.set(Math.cos(a)*24,0,Math.sin(a)*24);});
}

// ========== PARTICLES ==========
function mkParts(x,y,z,col,n){
for(let i=0;i<n;i++){
const m=new THREE.MeshBasicMaterial({color:col,transparent:true,opacity:.9});
const p=sMesh(new THREE.SphereGeometry(.15,8,6),m);
p.position.set(x,y,z);
p.userData={vx:rnd(-.5,.5),vy:rnd(.2,.55),vz:rnd(-.5,.5),life:1,m};
scene.add(p);particles3d.push(p);
}
}

// ========== MAIN LOOP ==========
function animate(){
requestAnimationFrame(animate);
const dt=Math.min(clk.getDelta(),.05);
const t=Date.now()*.001;
if(state===ST.LOBBY){
// Player movement - smooth, no bounce
const c=curC();
const inp=joy.l;
const sprint=P.sprinting?1.4:1;
const spd=SPD*(c.spd/80)*sprint;
const mag=Math.sqrt(inp.x**2+inp.y**2);
if(mag>.1){
const ang=Math.atan2(inp.x,inp.y)+camAng;
pVel.x+=Math.sin(ang)*mag*spd*.12;
pVel.z+=Math.cos(ang)*mag*spd*.12;
player.rotation.y=ang;
}
applyPhysics(player.position,pVel);
// Boundary
const pd=d2(player.position,{x:0,z:0});
if(pd>100){player.position.x*=100/pd;player.position.z*=100/pd;}
// Camera
if(Math.abs(joy.r.x)>.1)camAng-=joy.r.x*.035;
// Interact check
let closest=null,closestD=Infinity;
interacts.forEach(o=>{const dd=d3(player.position,o.position);if(dd<(o.userData.r||10)&&dd<closestD){closestD=dd;closest=o;}});
near=closest;
const prompt=$('PROMPT');
if(near && !document.querySelector('.overlay.show')){
setText('prIcon',near.userData.icon);setText('prText',near.userData.text);
prompt?.classList.add('show');
}else prompt?.classList.remove('show');
// Minimap
updateMM();
// Animate lobby
lobbyMeshes.forEach(o=>{if(o.userData?.spin)o.rotation.y+=dt;if(o.userData?.bob)o.position.y=(o.userData.baseY||4)+Math.sin(t*2)*.4;});
bots.forEach((b,i)=>{
if(Math.random()<.01||!b.target)b.target={x:rnd(-40,40),z:rnd(-40,40)};
const dx=b.target.x-b.mesh.position.x,dz=b.target.z-b.mesh.position.z,dd=Math.sqrt(dx*dx+dz*dz);
if(dd>1.5){b.mesh.position.x+=(dx/dd)*.05;b.mesh.position.z+=(dz/dd)*.05;b.mesh.rotation.y=Math.atan2(dx,dz);}
});
}else if(state===ST.GAME){
// Game player movement
if(gActive&&P.stunned<=0){
const c=curC();
const inp=joy.l;
const sprint=(P.sprinting&&P.stamina>0?1.4:1)*(P.buffTime>0?1.3:1);
if(P.sprinting&&P.stamina>0)P.stamina=Math.max(0,P.stamina-dt*30);
const spd=SPD*(c.spd/80)*sprint*.55*(curGame?.type==='pads'?!musicOn?0.15:0.7:1);
const mag=Math.sqrt(inp.x**2+inp.y**2);
if(mag>.1){
const ang=Math.atan2(inp.x,inp.y)+camAng;
pVel.x+=Math.sin(ang)*mag*spd;
pVel.z+=Math.cos(ang)*mag*spd;
player.rotation.y=ang;
}
if(Math.abs(joy.r.x)>.1)camAng-=joy.r.x*.035;
if(P.sprinting&&mag>.3)flash('SPEED',80);
}else if(P.stunned>0)P.stunned-=dt;
applyPhysics(player.position,pVel);
updateMinigame(dt);
}
// Particles
for(let i=particles3d.length-1;i>=0;i--){
const p=particles3d[i];
p.position.x+=p.userData.vx;p.position.y+=p.userData.vy;p.position.z+=p.userData.vz;
p.userData.vy-=.025;p.userData.life-=dt*4;
if(p.userData.m)p.userData.m.opacity=p.userData.life;
if(p.userData.life<=0){scene.remove(p);particles3d.splice(i,1);}
}
// Camera
const tX=player.position.x+Math.sin(camAng)*22;
const tZ=player.position.z+Math.cos(camAng)*22;
const tY=player.position.y+16;
cam.position.x+=(tX-cam.position.x)*.12;
cam.position.y+=(tY-cam.position.y)*.12;
cam.position.z+=(tZ-cam.position.z)*.12;
if(shakeAmt>0){cam.position.x+=rnd(-shakeAmt,shakeAmt);cam.position.y+=rnd(-shakeAmt,shakeAmt);shakeAmt*=.8;if(shakeAmt<.01)shakeAmt=0;}
cam.lookAt(player.position.x,player.position.y+2.5,player.position.z);
if(sun){sun.position.set(player.position.x+80,120,player.position.z+80);sun.target.position.copy(player.position);sun.target.updateMatrixWorld();}
ren.render(scene,cam);
}

// ========== INIT ==========
initThree();
buildLobby();
spawnPlayer();
spawnBots(5);
initControls();
if(IS_DEC) startSnow();
startLoad();

// ========== DEBUG SYSTEM ==========
window.DEBUG = {
  gotoLobby: () => backToLobby(),
  start: (id) => {
    let g; if(typeof id === "number") g = GAMES[id]; else g = GAMES.find(x => x.id === id);
    if(g) startMinigame(g);
    else console.error("Game not found:", id);
  },
  show: (id) => show(id),
  setGems: (n) => { P.gems = n; setText('hGems', n); },
  setLv: (n) => { P.lv = n; setText('hLv', n); }
};

animate();
