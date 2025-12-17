#core/story.py
from datapizza.agents import Agent
from .config import *


def generate_story(story_agent: Agent, name: str, age: int, keywords: str) -> str:
    prompt = f"""
You are writing a story split into scenes.

TASK:
Write a Christmas story for {name}, age {age}.
Themes: {keywords}

HARD CONSTRAINTS (ALL MUST BE RESPECTED):
- Total length: at most {MAX_WORDS} words.
- Write BETWEEN {MIN_SCENES} and {MAX_SCENES} scenes.
- EACH SCENE MUST BE 1–2 short sentences.
- AFTER EACH SCENE, WRITE THE TOKEN: [SCENE_BREAK]
- Do NOT number the scenes.
- Do NOT add titles.
- Do NOT repeat the entire story inside a single scene.
- Output ONLY the scenes with [SCENE_BREAK] separators.
""".strip()

    resp = story_agent.run(prompt)
    return resp.text.strip()


def generate_image_prompt(prompt_agent: Agent, scene_text: str, character_desc: str, style_preset: str) -> str:
    prompt = f"""
Create ONE Stable Diffusion prompt.

Scene:
\"\"\"{scene_text}\"\"\"

Character constraints (MUST be fully and explicitly included in the final prompt, without changing them):
{character_desc}

Style (MUST be included exactly as is, without removing parts):
{style_preset}

Hard rules:
- Warm golden/amber/orange tones (NO cold colors, NO blues, NO grays).
- The prompt MUST explicitly restate the full character description above, unchanged.
- Soft lighting: fireplace, candlelight, warm glow, gentle shadows.
- 2D illustration storybook style, watercolor, ink outline, flat colors.
- Hygge, comfortable, peaceful atmosphere.
- NO photorealistic, NO photograph.
- No text/letters/logos.
- Under 70 words.

Output ONLY the prompt.
""".strip()

    resp = prompt_agent.run(prompt)
    return resp.text.strip()



def generate_character_desc(prompt_agent: Agent, name: str, age: int, keywords: str) -> str:
    prompt = f"""
You are creating a highly detailed visual description of a recurring character
for a cozy, warm Christmas storybook, optimized for Stable Diffusion prompts.

Given:
- Name: {name}
- Exact numeric age: {age} years old
- Themes/keywords: {keywords}

TASK:
Describe ONLY how the character LOOKS, as if you were giving instructions to an illustrator.
The character's apparent age MUST CLEARLY match a {age}-year-old human, in both face and body proportions.

HARD CONSTRAINTS:
- ONE sentence, maximum 45 words.
- Third person only (no "I" or "you").
- The character must clearly look like a {age}-year-old (no baby, no teenager, no adult if {age} is a child).
- Do NOT contradict the given age visually (no adult height or facial structure for a child).
- Include, in this order if possible:
 1) apparent age range and body type,
 2) skin tone and face details (eye color, hair color, hairstyle),
 3) distinctive facial features (freckles, glasses, beard, dimples, etc.),
 4) upper body clothing (type, color, winter style),
 5) lower body clothing (pants/skirt, color),
 6) shoes/boots (type, color),
 7) 1–2 small accessories (scarf, hat, gloves, bag).

STYLE REQUIREMENTS:
- Warm, friendly, winter/Christmas outfit (scarves, hats, sweaters, coats, etc.).
- No background, no actions, no personality, no props other than clothing/accessories.
- Do NOT mention camera, lighting, art style, or environment (those come from another prompt).
- Do NOT explicitly mention the name or the numeric age in the sentence.

Output ONLY the final description sentence, nothing else.
""".strip()

    resp = prompt_agent.run(prompt)
    return resp.text.strip()
