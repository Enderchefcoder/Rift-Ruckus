import re

with open('index.html', 'r') as f:
    code = f.read()

# 1. Add Tail to characters
tail_logic = """
  // Tail
  const tail=sMesh(new THREE.SphereGeometry(.15,8,8),bm);
  tail.position.set(0,.8,-.45); g.add(tail);
"""
code = code.replace("hat.position.y=2.2; hat.rotation.z=.12;g.add(hat);", "hat.position.y=2.2; hat.rotation.z=.12;g.add(hat);\n" + tail_logic)

# 2. Add Banners to lobby
banner_func = """
function buildBanners(){
  for(let i=0; i<8; i++){
    const a=(i/8)*Math.PI*2; const r=40;
    const g=new THREE.Group(); g.position.set(Math.cos(a)*r, 10, Math.sin(a)*r);
    const pole=sMesh(new THREE.CylinderGeometry(.1,.1,10), mat(0x333333)); pole.position.y=-5; g.add(pole);
    const flag=sMesh(new THREE.BoxGeometry(3,2,.1), mat(Math.random()*0xffffff)); flag.position.set(1.5,0,0); g.add(flag);
    addMesh(g,true);
  }
}
"""
code = code.replace("function buildLobby(){", banner_func + "\nfunction buildLobby(){")
code = code.replace("buildDefaultLobby();", "buildDefaultLobby(); buildBanners();")

with open('index.html', 'w') as f:
    f.write(code)
