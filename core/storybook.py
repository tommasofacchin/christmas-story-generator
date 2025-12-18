#core/storybook.py
import base64
import json
from io import BytesIO
from pathlib import Path
from datapizza.agents import Agent
from diffusers import StableDiffusionPipeline

from .config import *
from .clients import *
from .story import *
from .images import *
from .export import *



def generate_storybook(
    story_agent: Agent,
    prompt_agent: Agent,
    pipe: StableDiffusionPipeline,
    name: str,
    age: int,
    keywords: str,
    story_id: str,
):
    clean_keywords = sanitize_keywords(keywords)

    character_desc = generate_character_desc(prompt_agent, name, age, clean_keywords)
    story = generate_story(story_agent, name, age, clean_keywords)

    scenes = [s.strip() for s in story.split("[SCENE_BREAK]") if s.strip()]
    scenes = [s.replace("[SCENE_BREAK]", "").strip() for s in scenes]

    MAX_CHARS_PER_SCENE = 300
    normalized_scenes = []
    for s in scenes:
        if len(s) <= MAX_CHARS_PER_SCENE:
            normalized_scenes.append(s)
        else:
            parts = [p.strip() for p in s.split(".") if p.strip()]
            chunk = ""
            for p in parts:
                candidate = (chunk + " " + p + ".").strip()
                if len(candidate) > MAX_CHARS_PER_SCENE and chunk:
                    normalized_scenes.append(chunk)
                    chunk = p + "."
                else:
                    chunk = candidate
            if chunk:
                normalized_scenes.append(chunk)

    scenes = normalized_scenes[:15]
    if len(scenes) == 0:
        raise ValueError("No scenes generated. Check [SCENE_BREAK] formatting.")

    story_out_dir = Path(OUT_DIR) / story_id
    story_out_dir.mkdir(parents=True, exist_ok=True)

    slides_b64 = []
    prompts_used = []
    image_paths = []

    for i, scene in enumerate(scenes, 1):
        img, pr = generate_ai_illustration(
            scene_text=scene,
            character_desc=character_desc,
            style_preset=STYLE_PRESET,
            prompt_agent=prompt_agent,
            pipe=pipe,
        )
        prompts_used.append(pr)

        img_path = story_out_dir / f"{i:02d}.png"
        img.save(img_path)
        #image_paths.append(str(img_path))
        image_paths.append(img_path.as_posix())

        buf = BytesIO()
        img.save(buf, format="PNG")
        slides_b64.append(base64.b64encode(buf.getvalue()).decode())


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


    pdf_path = story_out_dir / f"{name}_christmas_storybook.pdf"
    export_storybook_pdf(
        pdf_path=str(pdf_path),
        title=f"{name}'s AI Christmas Storybook",
        scenes=scenes,
        image_paths=image_paths,
    )

    story_record = {
        "id": story_id,
        "display_title": f"{name} ({age}): {keywords} - {story_id}",
        "name": name,
        "age": age,
        "keywords": keywords,
        "character_desc": character_desc,
        "story": story,
        "scenes": scenes,
        "image_paths": image_paths,
    }

    story_json_path = story_out_dir / "story.json"
    story_json_path.write_text(
        json.dumps(story_record, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )


    return {
        "character_desc": character_desc,
        "story": story,
        "scenes": scenes,
        "image_paths": image_paths,
        "html": html,
        "prompts_used": prompts_used,
    }
