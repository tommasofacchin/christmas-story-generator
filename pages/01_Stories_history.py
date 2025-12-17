import json
from pathlib import Path
import streamlit as st
import base64

BASE_DIR = Path(__file__).resolve().parents[1]
OUT_DIR = BASE_DIR / "outputs"


st.set_page_config(
    page_title="Stories history",
    page_icon="📚",
    layout="wide",  
)
st.title("📚 Storybook history")


if not OUT_DIR.exists():
    st.info("No stories saved yet.")
    st.stop()

story_files = sorted(OUT_DIR.glob("*/story.json"), reverse=True)
options = []
records = []
for path in story_files:
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    records.append(data)
    
    title = data.get(
        "display_title",
        f"{data['name']} ({data['age']} y) – {path.stem}",
    )
    options.append(title)

if not options:
    st.info("No stories saved yet.")
    st.stop()

selected = st.selectbox("Select a storybook", options)

idx = options.index(selected)
data = records[idx]


st.subheader("Story info")
st.markdown(
    f"""
**Child:** {data['name']} ({data['age']} years old)  
**Themes:** {data.get('keywords', '')}
"""
)
st.divider()

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Character")
    st.write(data["character_desc"])

with col2:
    st.subheader("Full story")
    story_text = data["story"].replace("[SCENE_BREAK]", "\n")
    st.write(story_text)

st.divider()

slides_b64 = []
for img_path in data["image_paths"]:
    full_path = (BASE_DIR / img_path).resolve()
    with open(full_path, "rb") as f:
        b = f.read()
    slides_b64.append(base64.b64encode(b).decode())

name = data["name"]
scenes = data["scenes"]

html = f"""
<style>
  .container {{ max-width: 2400px; margin: 30px auto; padding: 0 20px; }}
  .title {{ text-align: center; font-size: 36px; font-weight: bold; margin-bottom: 40px;
            background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text;
            -webkit-text-fill-color: transparent; }}
  .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}
  .card {{ position: relative; border-radius: 12px; overflow: hidden;
           box-shadow: 0 8px 25px rgba(0,0,0,0.12); background: #fff; }}
  .card img {{ width: 100%; height: auto; display: block; }}
  .caption {{
      position: absolute;
      bottom: 0; left: 0; right: 0;
      padding: 12px 16px;
      color: #fff;
      font-weight: 800;
      font-size: 16px;
      line-height: 1.3;
      text-shadow:
        -2px -2px 0 rgba(0,0,0,0.8),
         2px -2px 0 rgba(0,0,0,0.8),
        -2px  2px 0 rgba(0,0,0,0.8),
         2px  2px 0 rgba(0,0,0,0.8);
  }}
  .counter {{
      position: absolute;
      bottom: 8px; right: 12px;
      font-size: 14px; font-weight: 900;
      color: #e6f5ff;
      text-shadow:
        -1px -1px 0 rgba(0,0,0,0.9),
         1px -1px 0 rgba(0,0,0,0.9),
        -1px  1px 0 rgba(0,0,0,0.9),
         1px  1px 0 rgba(0,0,0,0.9);
  }}
  @media (max-width: 1600px) {{ .grid {{ grid-template-columns: repeat(3, 1fr); }} .caption {{ font-size: 15px; }} }}
  @media (max-width: 1200px) {{ .grid {{ grid-template-columns: repeat(2, 1fr); }} .caption {{ font-size: 14px; }} }}
  @media (max-width: 700px)  {{ .grid {{ grid-template-columns: 1fr; }} .caption {{ font-size: 13px; }} }}
</style>

<div class="container">
  <div class="title">Personalized AI Story for {name}</div>
  <div class="grid">
    {''.join([f'''
      <div class="card">
        <img src="data:image/png;base64,{img}">
        <div class="caption">
          {scenes[i]}
          <div class="counter">{i+1}/{len(slides_b64)}</div>
        </div>
      </div>
    ''' for i, img in enumerate(slides_b64)])}
  </div>
</div>
"""

st.components.v1.html(html, height=3000, scrolling=True)
