#core/images.py
import torch
from diffusers import StableDiffusionPipeline
from datapizza.agents import Agent
from .config import *
from .story import *

def generate_ai_illustration(
    scene_text: str,
    character_desc: str,
    style_preset: str,
    prompt_agent: Agent,
    pipe: StableDiffusionPipeline,
    width: int = WIDTH,
    height: int = HEIGHT,
):
    custom_prompt = generate_image_prompt(
        prompt_agent=prompt_agent,
        scene_text=scene_text,
        character_desc=character_desc,
        style_preset=style_preset,
    )

    with torch.inference_mode():
        result = pipe(
            prompt=custom_prompt,
            negative_prompt=NEGATIVE,
            height=height,
            width=width,
            num_inference_steps=STEPS,
            guidance_scale=GUIDANCE,
        )
        image = result.images[0]

    return image, custom_prompt