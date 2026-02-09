import sys

with open('index.html', 'r') as f:
    code = f.read()

bot_names_arr = "const BOT_NAMES=['Zippy','Bouncer','Sparky','Glimmer','Turbo','RiftRunner','Echo','Nova','Pixel','Glitchy','Tanker','Frosty','Shadow','Blaze','Bolt','Aura','Rusty','Comet','Pulse','Zen'];"

# Insert BOT_NAMES
code = code.replace("var player,bots=[],", bot_names_arr + "\\nvar player,bots=[],")

# Update spawnBots
new_spawn_bots = """
function spawnBots(n){
  bots.forEach(b=>scene.remove(b.mesh)); bots=[];
  const pool=CHARS.filter(c=>c.id!==P.charId);

  // Use invited friends if they exist
  const names = [...P.invited];
  while(names.length < n){
    const rn = BOT_NAMES[Math.floor(Math.random()*BOT_NAMES.length)];
    if(!names.includes(rn)) names.push(rn);
  }
  // Shuffle pool to get random chars for bots
  const botChars = [];
  for(let i=0; i<n; i++) botChars.push(pool[Math.floor(Math.random()*pool.length)]);

  for(let i=0; i<n; i++){
    const ch=botChars[i];
    const name=names[i];
    const mesh=makeChar(ch,true);
    const a=((i+1)/(n+1))*Math.PI*2,r=24+rnd(0,10);
    mesh.position.set(Math.cos(a)*r,0,Math.sin(a)*r);
    bots.push({
      mesh, ch, name, emoji:ch.emoji, color:ch.color,
      score:0, isIt:false, tagImmune:0, stunned:0,
      vel:{x:0,y:0,z:0}, grounded:true, eliminated:false,
      hillTime:0, target:null, aiTimer:0,
      mem: { bad: [] }
    });
    scene.add(mesh);
  }
}
"""

import re
code = re.sub(r'function spawnBots\(n\)\{.*?\}', new_spawn_bots, code, flags=re.DOTALL)

with open('index.html', 'w') as f:
    f.write(code)
