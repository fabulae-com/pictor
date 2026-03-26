#!/usr/bin/env python3
"""Compare IPAdapter settings: different refs, weights, style_boost."""

import json, random
from pathlib import Path
from pictor.comfy_client import ComfyClient
from pictor.workflows import load_workflow, inject_prompt
from pictor.prompts import NEGATIVE_PROMPT

SCENE = (
    "A large brown dog curled up asleep on sun-warmed marble steps, "
    "head resting on its front paws, in the shade of a columned Roman portico. "
    "Ladybird 1970s children's book illustration, gouache painting, "
    "visible brushstrokes, soft warm colours, hand-painted texture."
)

client = ComfyClient(base_url="https://spark-1.faun-rigel.ts.net:8188", timeout=600)
seed = random.randint(0, 2**32)
print(f"Seed: {seed}\n")

variants = [
    # (name, ref_image, weight, style_boost)
    ("ref01_w08_sb10", "ladybird_ref/ref_01.jpg", 0.8, 1.0),
    ("ref01_w10_sb15", "ladybird_ref/ref_01.jpg", 1.0, 1.5),
    ("ref01_w10_sb20", "ladybird_ref/ref_01.jpg", 1.0, 2.0),
    ("ref07_w10_sb15", "ladybird_ref/ref_07.jpg", 1.0, 1.5),
    ("ref03_w10_sb15", "ladybird_ref/ref_03.jpg", 1.0, 1.5),
]

for name, ref, weight, style_boost in variants:
    print(f"=== {name} (ref={ref}, w={weight}, sb={style_boost}) ===")
    
    w = load_workflow("sdxl-ipadapter")
    w["4"]["inputs"]["image"] = ref
    w["5"]["inputs"]["weight"] = weight
    w["5"]["inputs"]["style_boost"] = style_boost
    w["9"]["inputs"]["seed"] = seed
    w = inject_prompt(w, positive=SCENE, negative=NEGATIVE_PROMPT)
    
    output_path = Path(f"output/ipa_{name}.png")
    try:
        result = client.generate(w, output_path=output_path)
        print(f"  Done: {result}")
    except Exception as e:
        print(f"  FAILED: {e}")

print("\nAll done!")
