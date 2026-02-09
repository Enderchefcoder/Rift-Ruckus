import re

with open('index.html', 'r') as f:
    content = f.read()

# Add more variety to lobby deco
deco_js = """
function addLobbyDeco(){
  // Balloons
  for(let i=0; i<12; i++){
    const a=(i/12)*Math.PI*2; const r=rnd(15,35);
    const b=sMesh(new THREE.SphereGeometry(.7,12,12), mat(Math.random()*0xffffff, .3));
    b.position.set(Math.cos(a)*r, 10+rnd(0,5), Math.sin(a)*r);
    b.userData={bob:true, baseY:b.position.y}; addMesh(b,true);
    const st=sMesh(new THREE.CylinderGeometry(.02,.02,15), mat(0xcccccc));
    st.position.set(b.position.x, b.position.y-7.5, b.position.z); addMesh(st,true);
  }
  // Bushes & Flowers
  for(let i=0; i<30; i++){
    const a=rnd(0, Math.PI*2); const r=rnd(10, 40);
    const x=Math.cos(a)*r, z=Math.sin(a)*r;
    if(d2({x,z}, {x:0,z:0}) < 18) continue; // Don't block plaza
    const b=sMesh(new THREE.SphereGeometry(rnd(.8, 1.5), 8, 8), mat(0x2E7D32, .8));
    b.position.set(x, 0.5, z); addMesh(b, true);
    if(Math.random() > 0.5){
      const f=sMesh(new THREE.SphereGeometry(.2, 8, 8), mat(Math.random()*0xffffff, .2));
      f.position.set(x+rnd(-.5,.5), 1.2, z+rnd(-.5,.5)); addMesh(f, true);
    }
  }
}
"""

content = re.sub(r'function addLobbyDeco\(\)\{.*?\}', deco_js, content, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(content)
