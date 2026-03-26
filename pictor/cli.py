"""Simple CLI for pictor."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from .comfy_client import ComfyClient
from .prompts import LADYBIRD_STYLE, NEGATIVE_PROMPT, build_prompt
from .workflows import inject_prompt, list_workflows, load_workflow


def main():
    parser = argparse.ArgumentParser(description="pictor — illustration generator")
    parser.add_argument("prompt", help="Scene description or Latin phrase")
    parser.add_argument(
        "-w", "--workflow", default=None,
        help=f"Workflow template name. Available: {list_workflows()}"
    )
    parser.add_argument(
        "-u", "--url", default="https://spark-1.faun-rigel.ts.net:8188",
        help="ComfyUI server URL"
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output file path (default: auto-generated)"
    )
    parser.add_argument(
        "--raw", action="store_true",
        help="Use prompt as-is without adding Ladybird style"
    )
    parser.add_argument(
        "--list", action="store_true",
        help="List available workflows and exit"
    )
    args = parser.parse_args()

    if args.list:
        for name in list_workflows():
            print(f"  {name}")
        return

    workflows = list_workflows()
    if not workflows:
        print("No workflows found in workflows/ directory", file=sys.stderr)
        sys.exit(1)

    workflow_name = args.workflow or workflows[0]
    workflow = load_workflow(workflow_name)

    positive = args.prompt if args.raw else build_prompt(args.prompt)
    workflow = inject_prompt(workflow, positive=positive, negative=NEGATIVE_PROMPT)

    output_path = Path(args.output) if args.output else None

    client = ComfyClient(base_url=args.url)
    print(f"Submitting to {args.url} using workflow '{workflow_name}'...")
    result_path = client.generate(workflow, output_path=output_path)
    print(f"Done! Image saved to: {result_path}")


if __name__ == "__main__":
    main()
