import sys
import re

with open('index.html', 'r') as f:
    content = f.read()

# 1. Characters Enhancement
chars_patch = """
function makeChar(ch,isBot=false){
const g=new THREE.Group();
const col=ch.color;
const bm=mat(col,.35);
const body=sMesh(new THREE.CylinderGeometry(.4,.44,.7,12),bm);
body.position.y=1;body.castShadow=true;g.add(body);
const top=sMesh(new THREE.SphereGeometry(.4,12,10),bm);
top.position.y=1.35;top.castShadow=true;g.add(top);
const bot=sMesh(new THREE.SphereGeometry(.44,12,10),bm);
bot.position.y=.65;bot.castShadow=true;g.add(bot);
const head=sMesh(new THREE.SphereGeometry(.36,16,14),mat(0xFFDFC4,.45));
head.position.y=1.85;head.castShadow=true;g.add(head);
[-1,1].forEach(s=>{
  const eye=sMesh(new THREE.SphereGeometry(.07,8,6),mat(0x111111));
  eye.position.set(s*.12,1.9,.3);g.add(eye);
});

// Character specific details
if(ch.id==='glitch'){ // Panda style
  [-1,1].forEach(s=>{
    const ear=sMesh(new THREE.SphereGeometry(.12,8,8),mat(0x222222));
    ear.position.set(s*.25,2.15,0); g.add(ear);
    const patch=sMesh(new THREE.SphereGeometry(.1,8,8),mat(0x222222));
    patch.position.set(s*.12,1.9,.28); patch.scale.z=0.1; g.add(patch);
  });
} else if(ch.id==='tank'){ // Harold / Shiba style
  [-1,1].forEach(s=>{
    const ear=sMesh(new THREE.ConeGeometry(.15,.3,4),mat(col));
    ear.position.set(s*.22,2.15,0); ear.rotation.z=-s*0.3; g.add(ear);
  });
} else if(ch.id==='santa'){ // Piggy style
  const snout=sMesh(new THREE.CylinderGeometry(.12,.12,.1,12),mat(0xFFA07A));
  snout.position.set(0,1.82,.35); snout.rotation.x=Math.PI/2; g.add(snout);
}

const hat=sMesh(new THREE.ConeGeometry(.28,.45,8),mat(0xE74C3C,.4));
hat.position.y=2.2;hat.rotation.z=.12;g.add(hat);
if(isBot){
  const ant=sMesh(new THREE.CylinderGeometry(.015,.015,.28,6),mat(0x444444));
  ant.position.y=2.45;g.add(ant);
  const ball=sMesh(new THREE.SphereGeometry(.05,8,6),mat(0xFF4444));
  ball.position.y=2.55;g.add(ball);
}
return g;
}
"""

# Replace makeChar
content = re.sub(r'function makeChar\(ch,isBot=false\)\{.*?return g;.*?\}', chars_patch, content, flags=re.DOTALL)

# 2. Deluxe HD Environment
# Update buildLobby for better colors in Deluxe mode
lobby_patch = """
if(IS_DEC){
  // ... (keep original IS_DEC)
}else{
  const gndCol = P.preset === 'deluxe' ? 0x76FF03 : 0x388E3C;
  const gnd=sMesh(new THREE.CircleGeometry(110,60),mat(gndCol));
  gnd.rotation.x=-Math.PI/2;addMesh(gnd,true);
  const plazaR=20,plazaH=1.5;
  const plazaCol = P.preset === 'deluxe' ? 0xFFEB3B : 0xCFD8DC;
  const plaza=sMesh(new THREE.CylinderGeometry(plazaR,plazaR,plazaH,32),mat(plazaCol));
  plaza.position.y=plazaH/2;addMesh(plaza,true);
  solidPlatforms.push({mesh:plaza,radius:plazaR,topY:plazaH});

  if(P.preset === 'deluxe'){
    // Colorful path
    for(let i=0; i<12; i++){
      const a = (i/12)*Math.PI*2;
      const pad = sMesh(new THREE.BoxGeometry(4,0.2,4), mat([0xFF4081, 0x00E5FF, 0x76FF03, 0xFFEA00][i%4]));
      pad.position.set(Math.cos(a)*15, 1.55, Math.sin(a)*15);
      addMesh(pad, true);
    }
  }

  const f=new THREE.Group(); f.position.set(0,plazaH,0);
  // ... (rest of fountain)
"""
# This part is harder to replace with a simple sub, I'll use a more targeted approach.

# Update initThree for Deluxe colors
three_patch = """
function initThree(){
scene=new THREE.Scene();
const skyCol = P.preset === 'deluxe' ? 0xFFB74D : (IS_DEC ? 0x0a1a2a : 0x1a2a4a);
scene.background=new THREE.Color(skyCol);
scene.fog=new THREE.FogExp2(skyCol, P.preset === 'deluxe' ? .008 : .005);
cam=new THREE.PerspectiveCamera(55,innerWidth/innerHeight,.1,800);
ren=new THREE.WebGLRenderer({canvas:$('C'),antialias:true});
ren.setSize(innerWidth,innerHeight);
ren.setPixelRatio(Math.min(devicePixelRatio, 2));
ren.shadowMap.enabled = P.settings.shadows;
ren.shadowMap.type = THREE.PCFSoftShadowMap; // Safer than VSM in headless
ren.toneMapping = THREE.ACESFilmicToneMapping;
ren.toneMappingExposure = P.preset === 'deluxe' ? 1.6 : 1.2;
clk=new THREE.Clock();
const ambInt = P.preset === 'deluxe' ? 1.0 : 0.5;
scene.add(new THREE.AmbientLight(0xFFE0B2, ambInt));
sun=new THREE.DirectionalLight(0xfff5e0, P.preset === 'deluxe' ? 1.8 : 1.1);
sun.position.set(80,120,80);
if(P.settings.shadows){
  sun.castShadow=true;
  const s=sun.shadow; s.mapSize.width=s.mapSize.height=(P.preset === 'deluxe' ? 2048 : 2048);
  s.camera.near=20; s.camera.far=400; s.camera.left=s.camera.bottom=-120; s.camera.right=s.camera.top=120;
}
scene.add(sun);
scene.add(new THREE.HemisphereLight(0x6699cc,0x334455,.5));
}
"""
content = re.sub(r'function initThree\(\)\{.*?\}', three_patch, content, flags=re.DOTALL)

# Re-apply the speed balance just in case
content = content.replace('SPD*(c.spd/80)*sprint*0.8', 'SPD*(c.spd/80)*sprint*0.75')

with open('index.html', 'w') as f:
    f.write(content)
