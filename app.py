#app.py
import streamlit as st
import streamlit.components.v1 as components
import uuid
import json
import random
from pathlib import Path
from core import build_clients, build_pipeline, generate_storybook
from core.config import THEME_POOL


# Configure basic page settings
st.set_page_config(
    page_title="Christmas Story Generator",
    page_icon="🎄",
    layout="wide",
)

# ---- Sidebar: API configuration ----
st.sidebar.header("Configuration")

# GROQ API key for Datapizza OpenAI client
groq_api_key = st.sidebar.text_input(
    "GROQ API key",
    type="password",
    help="API key used by the Datapizza OpenAI client (Groq backend).",
)

if groq_api_key:
    st.session_state["groq_api_key"] = groq_api_key

api_key = st.session_state.get("groq_api_key")

# Optional Hugging Face token (for SD weights if needed)
hf_token = st.sidebar.text_input(
    "Hugging Face token (optional)",
    type="password",
    help="Optional token for loading Stable Diffusion models from Hugging Face.",
)

st.sidebar.markdown(
    "A GPU is recommended for faster image generation, "
    "but the app can also run on CPU (slower)."
)

# ---- Main UI ----
st.title("🎄 Christmas Storybook Generator")

st.markdown(
    "Generate a short Christmas story with custom illustrations, optimized for children."
)

# Basic form: child information and themes
st.header("Story settings")

col1, col2 = st.columns(2)

with col1:
    child_name = st.text_input("Child name", value="Tommaso")

with col2:
    child_age = st.number_input(
        "Child age",
        min_value=1,
        max_value=120,
        value=8,
        step=1,
    )


if "keywords_text" not in st.session_state:
    st.session_state["keywords_text"] = "train, snow, friendly monster, hot chocolate"

themes_col, button_col = st.columns([3, 1])

with button_col:
    st.write("")
    st.write("")
    if st.button("🎲 Random themes"):
        random_themes = ", ".join(random.sample(THEME_POOL, 3))
        st.session_state["keywords_text"] = random_themes  

with themes_col:
    keywords = st.text_area(
        "Themes / keywords",
        value=st.session_state["keywords_text"],
        help="Write a few words that describe the mood, characters or objects you want in the story.",
        key="keywords_text",
    )

keywords = st.session_state["keywords_text"]


generate_btn = st.button("Generate Christmas storybook 🎁")

# ---- Generation logic ----
if generate_btn:
    if not groq_api_key:
        st.error("Please provide your GROQ API key in the sidebar before generating.")
    elif not keywords.strip():
        st.error("Please provide at least one theme or keyword.")
    else:
        story_id = str(uuid.uuid4())[:8]

        # 1) Build LLM agents
        with st.spinner("Building LLM agents (story + prompt writer)..."):
            story_agent, prompt_agent = build_clients(groq_api_key)

        # 2) Build diffusion pipeline
        with st.spinner("Loading image generation pipeline (this may take a while)..."):
            pipe = build_pipeline(hf_token or None)

        # 3) Generate story, scenes and images (+ HTML grid)
        with st.spinner("Generating story and illustrations..."):
            result = generate_storybook(
                story_agent=story_agent,
                prompt_agent=prompt_agent,
                pipe=pipe,
                name=child_name,
                age=int(child_age),
                keywords=keywords,
                story_id=story_id, 
            )

        st.success("Storybook generated successfully!")

        # Title: Name (age): theme - id
        display_title = f"{child_name} ({int(child_age)}): {keywords} - {story_id}"
        

        # ---- Story info ----
        st.subheader("Story info")
        st.markdown(
            f"""
**Child:** {child_name} ({int(child_age)} years old)  
**Themes:** {keywords}
"""
        )
        st.divider()

        col1, col2 = st.columns([1, 2])

        with col1:
            st.subheader("Character")
            st.write(result["character_desc"])

        with col2:
            st.subheader("Full story")
            story_text = result["story"].replace("[SCENE_BREAK]", "\n")
            st.write(story_text)

        st.divider()

        import base64
        BASE_DIR = Path(__file__).resolve().parent

        slides_b64 = []
        for img_path in result["image_paths"]:
            full_path = (BASE_DIR / img_path).resolve()
            with open(full_path, "rb") as f:
                b = f.read()
            slides_b64.append(base64.b64encode(b).decode())

        name = child_name
        scenes = result["scenes"]

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

        components.html(html, height=3000, scrolling=True)


