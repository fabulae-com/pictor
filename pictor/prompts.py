"""Style prompts and scene description generation.

Ported from the fabulae-old Rails app's Setting model defaults.
"""

# The Ladybird illustration style — used as suffix to scene descriptions
LADYBIRD_STYLE = (
    "Ladybird 1970s children's book illustration style, "
    "realistic proportions, vivid natural colours, bright balanced lighting, "
    "no yellow tint, no sepia, no vintage effect, no aged paper look, "
    "horizontal landscape format, "
    "classical Greco-Roman world aesthetic with period-accurate clothing, "
    "architecture, and surroundings."
)

# Negative prompt for SD/SDXL models (Flux ignores negative prompts)
NEGATIVE_PROMPT = (
    "text, watermark, signature, logo, words, letters, "
    "blurry, low quality, deformed, ugly, "
    "modern clothing, modern objects, technology, "
    "sepia, yellow tint, vintage filter, aged paper, "
    "anime, cartoon, 3d render, photorealistic"
)

# System prompt for LLM scene description (used by the agent, not ComfyUI)
SCENE_DESCRIPTION_SYSTEM_PROMPT = (
    "Write a concise, vivid scene description for a new illustration that "
    "helps a child understand the expression.\n"
    "Start by identifying the literal subject(s) and action(s) explicitly "
    "present in the expression text.\n"
    "Depict ONLY those subjects doing ONLY the action named in the expression. "
    "You may add setting, lighting, and mood details, but never introduce new "
    "characters, animals, or objects unless they are explicitly part of the expression.\n"
    "All scenes should feel anchored in a classical Greco-Roman world "
    "(clothing, architecture, props). No modern clothing, gadgets, or architecture.\n"
    "If the expression is a single noun (e.g., just 'canis' or 'luna'), focus "
    "entirely on that noun from a fresh visual angle — no extra people, animals, "
    "or props beyond what a background naturally requires.\n"
    "The new description must depict a different camera angle, action emphasis, "
    "or setting than the existing ones without altering the meaning of the "
    "expression itself.\n"
    "You may use up to two sentences (maximum 45 words) if the scene requires "
    "extra detail. Return only the description text without quotes."
)


def build_prompt(scene_description: str, style: str = LADYBIRD_STYLE) -> str:
    """Combine a scene description with a style prompt."""
    return f"{scene_description}. {style}"
