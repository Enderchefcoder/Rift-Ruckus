import re

with open('index.html', 'r') as f:
    content = f.read()

# Fix buildLobby's June block
old_lobby_june = r"""\}else\{
const gnd=sMesh\(new THREE\.CircleGeometry\(110,60\),mat\(0x2d5a27,\.9\)\);
gnd\.rotation\.x=-Math\.PI/2;addMesh\(gnd\);
const plazaR=20,plazaH=2;
const plaza=sMesh\(new THREE\.CylinderGeometry\(plazaR,plazaR,plazaH,32\),mat\(0x3e4a59,\.4\)\);
plaza\.position\.y=plazaH/2;addMesh\(plaza\);
solidPlatforms\.push\(\{mesh:plaza,radius:plazaR,topY:plazaH\}\);
// Fountain
const f=new THREE\.Group\(\); f\.position\.set\(0,plazaH,0\);
const fBase=sMesh\(new THREE\.CylinderGeometry\(5,5,1\.2,24\),mat\(0x7f8c8d\)\); fBase\.position\.y=0\.6; f\.add\(fBase\);
const fMid=sMesh\(new THREE\.CylinderGeometry\(1\.5,1\.5,4,16\),mat\(0x7f8c8d\)\); fMid\.position\.y=2\.5; f\.add\(fMid\);
const fTop=sMesh\(new THREE\.CylinderGeometry\(3\.5,3\.5,0\.6,16\),mat\(0x7f8c8d\)\); fTop\.position\.y=4\.5; f\.add\(fTop\);
const water=sMesh\(new THREE\.SphereGeometry\(3,16,12,0,Math\.PI\*2,0,Math\.PI/2\),mat\(0x00D4FF,\.4\)\);
water\.position\.y=4\.5; f\.add\(water\);
const lt=new THREE\.PointLight\(0x00D4FF,2,30\); lt\.position\.y=6; f\.add\(lt\);
addMesh\(f\);
buildPortal\(0,0,-45\); buildMirror\(45,0,0\); buildArcade\(-45,0,0\);
for\(let i=0;i<40;i\)\{
const a=\(i/40\)\*Math\.PI\*2, r=50\+rnd\(0,50\);
const x=Math\.cos\(a\)\*r, z=Math\.sin\(a\)\*r;
const spike=sMesh\(new THREE\.ConeGeometry\(rnd\(1,3\),rnd\(10,25\),4\),mat\(0x0f3460\)\);
spike\.position\.set\(x,spike\.geometry\.parameters\.height/2,z\); addMesh\(spike\);
\}
\}"""

new_lobby_june = r"""}else{
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
}"""

content = re.sub(old_lobby_june, new_lobby_june, content)

# Fix buildArenaScenery and buildArena
old_arena = r"""function buildArenaScenery\(\)\{
const R=120;
for\(let i=0;i<15;i\)\{
const a=\(i/15\)\*Math\.PI\*2\+rnd\(-.2,.2\), r=R\+rnd\(0,60\);
const x=Math\.cos\(a\)\*r, z=Math\.sin\(a\)\*r;
if\(IS_DEC\)\{
const g=new THREE\.Group\(\); g\.position\.set\(x,0,z\);
const h=rnd\(10,25\);
const trunk=sMesh\(new THREE\.CylinderGeometry\(\.8,1\.2,h\*\.3,8\),mat\(0x5D4037\)\);
trunk\.position\.y=h\*\.15; g\.add\(trunk\);
for\(let j=0;j<3;j\)\{
const cone=sMesh\(new THREE\.ConeGeometry\(5-j,h\*\.4,10\),mat\(0x2E7D32\)\);
cone\.position\.y=h\*\.3\+j\*h\*\.25; g\.add\(cone\);
\}
addMesh\(g\);
\}else\{
const g=new THREE\.Group\(\); g\.position\.set\(x,0,z\);
const h=rnd\(20,40\);
const pillar=sMesh\(new THREE\.CylinderGeometry\(3,5,h,6\),mat\(0x333344\)\);
pillar\.position\.y=h/2; g\.add\(pillar\);
const crystal=sMesh\(new THREE\.OctahedronGeometry\(5\),mat\(0x00FFFF,\.1\)\);
crystal\.position\.y=h\+6; crystal\.userData\.spin=true; g\.add\(crystal\);
const light=new THREE\.PointLight\(0x00FFFF,1,30\); light\.position\.y=h\+6; g\.add\(light\);
addMesh\(g\);
\}
\}
\}

// ========== ARENA BUILDER ==========
function buildArena\(game\)\{
buildArenaScenery\(\);
gameMeshes\.forEach\(o=>scene\.remove\(o\)\);gameMeshes=\[\];stars=\[\];pads=\[\];hillMesh=null;solidPlatforms=\[\];
const bgMap=\{collect:0x0D47A1,sumo:0x3E2723,hill:0xBF360C,tag:0x01579B,pads:0x4A148C\};
scene\.background=new THREE\.Color\(bgMap\[game\.type\]\|\|0x1a2a4a\);
scene\.fog=new THREE\.FogExp2\(bgMap\[game\.type\]\|\|0x1a2a4a,\.005\);
const R=game\.type==='sumo'\?35:75;
// Ground
const gnd=sMesh\(new THREE\.CircleGeometry\(R,50\),mat\(\{collect:0x1B5E20,sumo:0x5D4037,hill:0xBF360C,tag:0x006064,pads:0x4A148C\}\[game\.type\]\|\|0x1B5E20,\.7\)\);
gnd\.rotation\.x=-Math\.PI/2;gnd\.receiveShadow=true;scene\.add\(gnd\);gameMeshes\.push\(gnd\);
// Border
const bor=sMesh\(new THREE\.TorusGeometry\(R,1\.2,10,50\),mat\(0xFFD700,\.25\)\);
bor\.rotation\.x=Math\.PI/2;bor\.position\.y=\.6;scene\.add\(bor\);gameMeshes\.push\(bor\);"""

new_arena = r"""function buildArenaScenery(){
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
bor.rotation.x=Math.PI/2;bor.position.y=.75;addMesh(bor,false);"""

content = re.sub(old_arena, new_arena, content)

# Fix Hill scale
content = re.sub(r"const mesh=sMesh\(new THREE\.CylinderGeometry\(12,14,8,28\),mat\(0xFFD700,\.35\)\);",
                 r"const mesh=sMesh(new THREE.CylinderGeometry(16,20,10,32),mat(0xFFD700,.35));", content)

# Fix Stars scale
content = re.sub(r"const s=sMesh\(new THREE\.IcosahedronGeometry\(\.8,1\),mat\(isG\?0xFFD700:0xFFFFFF\)\);",
                 r"const s=sMesh(new THREE.IcosahedronGeometry(1.5,1),mat(isG?0xFFD700:0xFFFFFF));", content)

# Fix Pads scale
content = re.sub(r"const pad=sMesh\(new THREE\.CylinderGeometry\(4,4\.3,1\.2,16\),mat\(0x9C27B0,\.35\)\);",
                 r"const pad=sMesh(new THREE.CylinderGeometry(6,6.5,1.5,16),mat(0x9C27B0,.35));", content)

with open('index.html', 'w') as f:
    f.write(content)
