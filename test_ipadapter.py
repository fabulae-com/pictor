#!/usr/bin/env python3
"""Test SDXL + IPAdapter style transfer with Ladybird reference images."""

import json, random, sys, copy
from pathlib import Path
from pictor.comfy_client import ComfyClient
from pictor.workflows import load_workflow, inject_prompt
from pictor.prompts import NEGATIVE_PROMPT

# Scene description following fabulae-old rules for "canis dormit"
SCENE = (
    "A large brown dog curled up asleep on sun-warmed marble steps, "
    "head resting on its front paws, in the shade of a columned Roman portico. "
    "Ladybird 1970s children's book illustration style, "
    "realistic proportions, vivid natural colours, bright balanced lighting, "
    "horizontal landscape format, "
    "classical Greco-Roman world aesthetic."
)

# Reference images to test (in ComfyUI input/ladybird_ref/)
REFS = [
    "ladybird_ref/ref_01.jpg",
    "ladybird_ref/ref_03.jpg",
    "ladybird_ref/ref_05.jpg",
    "ladybird_ref/ref_08.jpg",
]

# IPAdapter weight variants
WEIGHTS = [0.6, 0.8, 1.0]

client = ComfyClient(base_url="https://spark-1.faun-rigel.ts.net:8188", timeout=600)
seed = random.randint(0, 2**32)

# Quick mode: just test one ref at different weights
ref = sys.argv[1] if len(sys.argv) > 1 else REFS[0]
print(f"Using reference: {ref}")
print(f"Seed: {seed}\n")

for weight in WEIGHTS:
    name = f"ipa_w{weight:.1f}"
    print(f"=== {name} (weight={weight}) ===")
    
    w = load_workflow("sdxl-ipadapter")
    
    # Set reference image
    w["4"]["inputs"]["image"] = ref
    
    # Set IPAdapter weight
    w["5"]["inputs"]["weight"] = weight
    w["5"]["inputs"]["weight_style"] = weight
    
    # Set seed
    w["9"]["inputs"]["seed"] = seed
    
    # Inject prompts
    w = inject_prompt(w, positive=SCENE, negative=NEGATIVE_PROMPT)
    
    output_path = Path(f"output/ipa_{name}.png")
    print("Submitting...")
    try:
        result = client.generate(w, output_path=output_path)
        print(f"Done: {result}")
    except Exception as e:
        print(f"FAILED: {e}")
        # Print more detail
        import traceback
        traceback.print_exc()

print("\nAll done!")
