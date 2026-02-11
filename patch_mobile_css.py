import re

new_css = """    @media (max-width: 640px) {
        #hud { padding: 0.5rem; justify-content: space-between; align-items: flex-start; }
        #hud > div:first-child { transform: scale(0.9); transform-origin: left top; flex-shrink: 0; }
        #hLeft .w-24 { width: 10rem !important; height: 0.75rem !important; }
        #hName { font-size: 1.8rem !important; }
        #hud > div:last-child { transform: scale(0.85); transform-origin: right top; flex-shrink: 0; gap: 0.4rem !important; }
        #social-btn, #hud button { width: 3.5rem !important; height: 3.5rem !important; }

        .joy-area { width: 100px; height: 100px; bottom: 20px; left: 10px; }
        .joy-knob { width: 40px; height: 40px; }

        #BTNS { bottom: 10px; right: 5px; scale: 1; transform: none; gap: 0.4rem; display: flex !important; flex-direction: column; align-items: flex-end; }
        #BTNS > div { gap: 0.4rem; display: flex; }
        #bGrab, #bSkill { width: 52px !important; height: 52px !important; border-radius: 1rem !important; font-size: 1.5rem !important; flex-shrink: 0; }
        #bJump { width: 80px !important; height: 80px !important; border-radius: 1.5rem !important; font-size: 2.2rem !important; flex-shrink: 0; }

        #PROMPT { scale: 0.7; bottom: 110px; }
        #SB { scale: 0.6; left: 5px; top: 70px; }
        .overlay > div { scale: 1; transform: scale(0.95); width: 95% !important; max-height: 90% !important; }
        #socialList { padding: 1rem !important; }
    }"""

with open('index.html', 'r') as f:
    content = f.read()

pattern = re.compile(r'    @media \(max-width: 640px\) \{.*?    \}', re.DOTALL)
new_content = pattern.sub(new_css, content)

with open('index.html', 'w') as f:
    f.write(new_content)
