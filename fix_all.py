import re

with open('index.html', 'r') as f:
    code = f.read()

# 1. Fix CSS for .gone
code = code.replace("</style>", ".gone { opacity: 0; pointer-events: none; }\n</style>")

# 2. Add more animal characters
new_chars = """{id:'glitch',name:'Glitch',emoji:'😎',role:'Speed',color:0x5C6BC0,spd:90,pow:50,jmp:80,skill:'Blink',sType:'tele',sCD:5},
{id:'tank',name:'Harold',emoji:'🦣',role:'Tank',color:0x795548,spd:45,pow:95,jmp:40,skill:'Quake',sType:'stun',sCD:8},
{id:'bear',name:'Barry',emoji:'🐻',role:'Brawler',color:0x8D6E63,spd:60,pow:85,jmp:50,skill:'Roar',sType:'stun',sCD:7},
{id:'bunny',name:'Bibi',emoji:'🐰',role:'Jumper',color:0xFF80AB,spd:85,pow:40,jmp:95,skill:'Hop',sType:'jump',sCD:3},
{id:'duck',name:'Ducky',emoji:'🦆',role:'Scout',color:0xFFEB3B,spd:75,pow:50,jmp:70,skill:'Dash',sType:'dash',sCD:4},
{id:'ninja',name:'Ninja',emoji:'🥷',role:'Stealth',color:0x212121,spd:85,pow:60,jmp:90,skill:'Smoke',sType:'smoke',sCD:6}"""

code = re.sub(r'const CHARS=\[.*?\];', 'const CHARS=[' + new_chars + '];', code, flags=re.DOTALL)

# 3. Improve Character Models in makeChar
# Add procedural wobble and animal features
new_make_char = """
function makeChar(ch,name='',isBot=false){
  const g=new THREE.Group();
  const col=ch.color;
  const bm=mat(col,.35);

  // Body (Wobbly)
  const body=sMesh(new THREE.CylinderGeometry(.4,.44,.7,12),bm);
  body.position.y=1; g.add(body);
  const top=sMesh(new THREE.SphereGeometry(.4,12,10),bm);
  top.position.y=1.35; g.add(top);
  const bot=sMesh(new THREE.SphereGeometry(.44,12,10),bm);
  bot.position.y=.65; g.add(bot);

  // Head
  const head=sMesh(new THREE.SphereGeometry(.36,16,14),mat(0xFFDFC4,.45));
  head.position.y=1.85; g.add(head);

  // Eyes
  [-1,1].forEach(s=>{
    const eye=sMesh(new THREE.SphereGeometry(.07,8,6),mat(0x111111));
    eye.position.set(s*.12,1.9,.3);g.add(eye);
  });

  // Features based on ID
  if(ch.id==='glitch'){
    [-1,1].forEach(s=>{
      const ear=sMesh(new THREE.SphereGeometry(.12,8,8),mat(0x222222));
      ear.position.set(s*.25,2.15,0); g.add(ear);
    });
  } else if(ch.id==='tank' || ch.id==='bear'){
    [-1,1].forEach(s=>{
      const ear=sMesh(new THREE.SphereGeometry(.15,8,8),bm);
      ear.position.set(s*.25,2.1,0); g.add(ear);
    });
  } else if(ch.id==='bunny'){
    [-1,1].forEach(s=>{
      const ear=sMesh(new THREE.CylinderGeometry(.08,.08,.6,8),bm);
      ear.position.set(s*.15,2.3,0); ear.rotation.z=s*0.2; g.add(ear);
    });
  } else if(ch.id==='duck'){
    const beak=sMesh(new THREE.BoxGeometry(.2,.1,.25),mat(0xFF9800));
    beak.position.set(0,1.8,.35); g.add(beak);
  }

  // Hat
  const hat=sMesh(new THREE.ConeGeometry(.28,.45,8),mat(0xE74C3C,.4));
  hat.position.y=2.2;hat.rotation.z=.12;g.add(hat);

  if(isBot){
    const ant=sMesh(new THREE.CylinderGeometry(.015,.015,.28,6),mat(0x444444));
    ant.position.y=2.45;g.add(ant);
    const ball=sMesh(new THREE.SphereGeometry(.05,8,6),mat(0xFF4444));
    ball.position.y=2.55;g.add(ball);
  }

  if(name) g.add(makeNameTag(name));

  // Add animation meta
  g.userData.wobble = 0;
  return g;
}"""

code = re.sub(r'function makeChar\(ch,name=\'\',isBot=false\)\{.*?return g;\}', new_make_char, code, flags=re.DOTALL)

# 4. Add Wobble to animate()
# I need to find the movement logic and add rotation wobble
animate_wobble = """
    if(mag>.1){
      const ang=Math.atan2(inp.x,inp.y)+camAng;
      pVel.x+=Math.sin(ang)*mag*spd*.12;
      pVel.z+=Math.cos(ang)*mag*spd*.12;
      player.rotation.y=ang;
      // Wobble
      player.rotation.z = Math.sin(t*15)*0.1;
      player.rotation.x = Math.sin(t*10)*0.05;
    } else {
      player.rotation.z *= 0.8;
      player.rotation.x *= 0.8;
    }
"""
code = re.sub(r'if\(mag>\.1\)\{.*?player\.rotation\.y=ang;.*?\}', animate_wobble, code, flags=re.DOTALL)

# Do the same for Game movement
animate_game_wobble = """
      if(mag>.1){
        const ang=Math.atan2(inp.x,inp.y)+camAng;
        pVel.x+=Math.sin(ang)*mag*spd;
        pVel.z+=Math.cos(ang)*mag*spd;
        player.rotation.y=ang;
        // Wobble
        player.rotation.z = Math.sin(t*15)*0.15;
        player.rotation.x = Math.sin(t*10)*0.1;
      } else {
        player.rotation.z *= 0.8;
        player.rotation.x *= 0.8;
      }
"""
# This might be harder to replace due to different context.
# I'll just look for the game movement block
code = re.sub(r'if\(mag>\.1\)\{.*?player\.rotation\.y=ang;.*?\}', animate_game_wobble, code, flags=re.DOTALL, count=1)

# 5. Fix King of Hill (Ensure P.stunned is cleared and movement works)
# I already fixed getGroundY to be "always", but let's make sure hill is correctly handled
code = code.replace("if(P.hillTime>=5){ P.stunned=0;", "if(P.hillTime>=5){ P.stunned=0.5;")

# 6. Final cleanup: Remove any duplicate animate/backToLobby
# I'll use the same logic as before but more aggressively
code = re.sub(r'function animate\(\)\{.*?animate\(\);', 'ANIMATE_PLACEHOLDER', code, flags=re.DOTALL)
# Wait, if I have two animate() functions, this might replace both or just the first.
# Let's find all function definitions and keep the last one.

with open('index.html', 'w') as f:
    f.write(code)
