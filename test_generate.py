#!/usr/bin/env python3
"""Quick test: generate one image via ComfyUI on spark-1."""

import sys
import random
from pathlib import Path
from pictor.workflows import load_workflow, inject_prompt
from pictor.prompts import LADYBIRD_STYLE, NEGATIVE_PROMPT, build_prompt
from pictor.comfy_client import ComfyClient

workflow_name = sys.argv[1] if len(sys.argv) > 1 else "sd15"
scene = sys.argv[2] if len(sys.argv) > 2 else "A friendly dog sleeping peacefully on marble steps in a sunlit Roman courtyard"

w = load_workflow(workflow_name)
positive = build_prompt(scene)

# Randomize seed
for node_id, node in w.items():
    if node.get("class_type") == "KSampler":
        node["inputs"]["seed"] = random.randint(0, 2**32)

w = inject_prompt(w, positive=positive, negative=NEGATIVE_PROMPT)

print(f"Workflow: {workflow_name}")
print(f"Prompt: {positive[:100]}...")

client = ComfyClient(base_url="https://spark-1.faun-rigel.ts.net:8188")
output_path = Path(f"output/{workflow_name}_test.png")
print("Submitting to ComfyUI...")
result = client.generate(w, output_path=output_path)
print(f"Done! Saved to: {result}")
