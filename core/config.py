#core/config.py
from pathlib import Path
import os

OUT_DIR = Path("outputs")
OUT_DIR.mkdir(exist_ok=True)


STEPS = 10
GUIDANCE = 7.5
WIDTH = 576
HEIGHT = 768
MIN_SCENES = 10
MAX_SCENES = 15
MAX_WORDS = 200


STYLE_PRESET = (
    "cozy warm children's storybook illustration, highly detailed watercolor and gouache on soft textured paper, "
    "clean black ink outlines with subtle pencil linework, smooth shading, "
    "soft warm golden hour lighting, gentle fireplace and candlelight glow, "
    "rich amber, honey, and soft orange color palette, muted cool tones only in the distant background, "
    "Scandinavian hygge atmosphere, comfortable, peaceful, whimsical, friendly mood, "
    "hand-painted 2D illustration, slightly soft edges, slight vignette around the image borders, "
    "no motion blur, no grain, no noise, "
    "NOT realistic, NOT photorealistic, NOT 3D render, NOT CGI, NOT cold blue lighting"
)


NEGATIVE = (
    "photorealistic, realistic, photograph, photo, hyperrealistic, high detail skin, skin pores, "
    "dslr, film grain, bokeh, depth of field, lens flare, studio lighting, flash, hdr, "
    "3d render, cgi, octane render, unreal engine, sharp focus, ultra-detailed, "
    "cold colors, blue tones, gray, dark, gloomy, harsh lighting, "
    "text, letters, watermark, logo, signature, low quality, blurry, deformed, ugly"
)


THEME_POOL = [
    # winter & weather
    "snow", "blizzard", "snowstorm", "first snowfall", "frozen lake",
    "icicles", "snowy forest", "mountain village",

    # transport & travel
    "train", "night train", "toy train", "sleigh ride", "flying sleigh",
    "hot air balloon", "Christmas cruise",

    # classic Christmas symbols
    "Christmas tree", "Christmas market", "Christmas lights", "wreaths",
    "stockings by the fireplace", "nativity scene", "advent calendar",

    # characters & creatures
    "friendly monster", "talking snowman", "tiny dragon", "polar bear",
    "penguins", "wise old owl", "magic fox", "reindeer", "baby reindeer",
    "elves", "toy soldier", "gingerbread man",

    # Santa & workshop
    "Santa's workshop", "Santa's office", "busy elves", "gift wrapping room",
    "reindeer stables", "lost present", "letter to Santa",

    # cozy / hygge vibes
    "hot chocolate", "cozy fireplace", "warm blanket", "fluffy socks",
    "marshmallows", "gingerbread cookies", "cinnamon rolls",
    "family dinner", "board games night",

    # places & settings
    "gingerbread house", "enchanted forest", "hidden attic",
    "snowy lighthouse", "ice castle", "tiny mountain cabin",
    "secret library", "frozen waterfall",

    # sky & magic
    "aurora borealis", "shooting star", "full moon", "starry night sky",
    "magic sled", "time-traveling snow globe", "magic bell",
    "talking Christmas ornament",

    # emotions & themes
    "friendship", "kindness", "sharing gifts", "forgiveness",
    "finding courage", "helping a stranger", "missing someone at Christmas",
    "first Christmas away from home",

    # activities
    "snowball fight", "building a snowman", "ice skating", "sledding",
    "decorating the tree", "baking cookies", "carol singing",

    # misc cozy details
    "snowman", "mistletoe", "twinkling fairy lights",
    "handmade gifts", "secret wish", "lost mitten",
]
