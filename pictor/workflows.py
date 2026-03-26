"""Workflow template loading and parameter injection."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

WORKFLOW_DIR = Path(__file__).parent.parent / "workflows"


def list_workflows() -> list[str]:
    """Return names of available workflow templates."""
    return sorted(p.stem for p in WORKFLOW_DIR.glob("*.json"))


def load_workflow(name: str) -> dict[str, Any]:
    """Load a workflow template by name."""
    path = WORKFLOW_DIR / f"{name}.json"
    if not path.exists():
        available = list_workflows()
        raise FileNotFoundError(
            f"Workflow '{name}' not found. Available: {available}"
        )
    return json.loads(path.read_text())


def inject_prompt(workflow: dict[str, Any], positive: str, negative: str = "") -> dict[str, Any]:
    """Inject positive/negative prompts into a workflow.

    Looks for nodes with class_type CLIPTextEncode and replaces
    the text input. Convention: the node with 'positive' in its
    _meta.title gets the positive prompt, 'negative' gets negative.
    If no _meta match, uses the first two CLIPTextEncode nodes.
    """
    clip_nodes = []
    for node_id, node in workflow.items():
        if node.get("class_type") == "CLIPTextEncode":
            clip_nodes.append((node_id, node))

    if not clip_nodes:
        raise ValueError("No CLIPTextEncode nodes found in workflow")

    positive_set = False
    negative_set = False

    for node_id, node in clip_nodes:
        title = node.get("_meta", {}).get("title", "").lower()
        if "positive" in title and not positive_set:
            node["inputs"]["text"] = positive
            positive_set = True
        elif "negative" in title and not negative_set:
            node["inputs"]["text"] = negative
            negative_set = True

    # Fallback: first = positive, second = negative
    if not positive_set and clip_nodes:
        clip_nodes[0][1]["inputs"]["text"] = positive
        positive_set = True
    if not negative_set and len(clip_nodes) > 1:
        clip_nodes[1][1]["inputs"]["text"] = negative

    return workflow
