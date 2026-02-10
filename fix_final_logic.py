import re

with open('index.html', 'r') as f:
    code = f.read()

# 1. Add addLobbyDeco definition
add_lobby_deco_fn = """
function addLobbyDeco(){
  // Balloons
  for(let i=0; i<15; i++){
    const a=rnd(0,6.2), r=rnd(15,45), h=10+rnd(0,10);
    const g=new THREE.Group(); g.position.set(Math.cos(a)*r, h, Math.sin(a)*r);
    const b=sMesh(new THREE.SphereGeometry(0.7,12,10), mat(Math.random()*0xffffff, 0.3)); g.add(b);
    const s=sMesh(new THREE.CylinderGeometry(0.02,0.02,15), mat(0xcccccc)); s.position.y=-7.5; g.add(s);
    g.userData={bob:true, baseY:h}; addMesh(g,true);
  }
}
"""
# Insert after makeChar
code = code.replace("if(name) g.add(makeNameTag(name)); return g;\\n}", "if(name) g.add(makeNameTag(name)); return g;\\n}\\n" + add_lobby_deco_fn)

# 2. Update Tag/Sumo obstacles to be solid
code = code.replace("const p=sMesh(new THREE.BoxGeometry(6,12,6),mat(0x006064)); p.position.set(x,6,z); addMesh(p);",
                    "const p=sMesh(new THREE.BoxGeometry(6,12,6),mat(0x006064)); p.position.set(x,6,z); addMesh(p); solidPlatforms.push({mesh:p,radius:4,topY:12});")

code = code.replace("const p=sMesh(new THREE.DodecahedronGeometry(rnd(3,5)),mat(0x5D4037)); p.position.set(Math.cos(a)*r,2,Math.sin(a)*r); p.rotation.set(rnd(0,6),rnd(0,6),rnd(0,6)); addMesh(p);",
                    "const p=sMesh(new THREE.DodecahedronGeometry(rnd(3,5)),mat(0x5D4037)); p.position.set(Math.cos(a)*r,2,Math.sin(a)*r); p.rotation.set(rnd(0,6),rnd(0,6),rnd(0,6)); addMesh(p); solidPlatforms.push({mesh:p,radius:4,topY:4});")

# 3. Handle YOU'RE IT string escaping properly
code = code.replace("YOU\\'RE IT!", "YOU\\\\\\'RE IT!") # wait, this is getting confusing.

with open('index.html', 'w') as f:
    f.write(code)
