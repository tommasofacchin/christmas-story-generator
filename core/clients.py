#core/clients.py
from datapizza.clients.openai import OpenAIClient
from datapizza.agents import Agent
from datapizza.tools import tool
from .config import *


@tool
def sanitize_keywords(keywords: str) -> str:
    replacements = {
        "gun": "snowball blaster",
        "guns": "snowball blasters",
        "weapon": "magic snow wand",
        "weapons": "magic snow wands",
        "knife": "carving knife for gingerbread",
        "knives": "carving knives for gingerbread",
        "sword": "candy cane sword",
        "swords": "candy cane swords",
        "war": "snowball tournament",
        "battle": "snowball battle",
        "battles": "snowball battles",
        "fight": "playful snowball fight",
        "fights": "playful snowball fights",
        "fighting": "playing with snowballs",
        "monster": "friendly monster",
        "monsters": "friendly monsters",
        "demon": "grumpy snow spirit",
        "demons": "grumpy snow spirits",
        "ghost": "shy winter ghost",
        "ghosts": "shy winter ghosts",
        "zombie": "sleepy snowwalker",
        "zombies": "sleepy snowwalkers",
        "blood": "red cranberry sauce",
        "gore": "messy frosting",
        "killing": "defeating in a snowball game",
        "kill": "defeat in a snowball game",
        "alcohol": "hot chocolate",
        "beer": "gingerbread soda",
        "wine": "sparkling cranberry juice",
        "vodka": "extra-strong hot chocolate",
        "whisky": "spiced apple cider",
        "whiskey": "spiced apple cider",
        "rum": "vanilla sugar syrup",
        "drugs": "magic Christmas candies",
        "drug": "magic Christmas candy",
        "smoke": "chimney smoke from cozy houses",
        "smoking": "chimney smoke from cozy houses",
        "death": "the end of winter",
        "dead": "fast asleep after a long snow day",
    }
    out = keywords
    for k, v in replacements.items():
        out = out.replace(k, v).replace(k.title(), v)
    return out


def build_clients(groq_api_key: str):
    client = OpenAIClient(
        api_key=groq_api_key,
        base_url="https://api.groq.com/openai/v1",
        model="llama-3.3-70b-versatile",
    )

    story_agent = Agent(
        name="christmas_story_writer",
        client=client,
        system_prompt=(
            "You write short Christmas stories with a magical, warm, cozy tone. "
            "You strictly follow formatting rules given by the user."
        ),
        tools=[sanitize_keywords],
    )

    prompt_agent = Agent(
        name="sd_prompt_writer",
        client=client,
        system_prompt=(
            "You create Stable Diffusion prompts for 2D children storybook illustrations. "
            "You follow constraints exactly and you output only the final prompt."
        ),
    )

    return story_agent, prompt_agent