"""ComfyUI API client.

Submits workflow JSON to a ComfyUI server, polls for completion,
and downloads the output image.
"""

from __future__ import annotations

import json
import time
import uuid
from pathlib import Path
from typing import Any

import httpx


class ComfyClient:
    """Thin client for the ComfyUI REST API."""

    def __init__(self, base_url: str = "http://127.0.0.1:8188", timeout: float = 300):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.client_id = uuid.uuid4().hex[:12]

    def queue_prompt(self, workflow: dict[str, Any]) -> str:
        """Submit a workflow and return the prompt_id."""
        payload = {"prompt": workflow, "client_id": self.client_id}
        with httpx.Client(timeout=30, verify=False) as http:
            r = http.post(f"{self.base_url}/prompt", json=payload)
            if r.status_code != 200:
                raise RuntimeError(f"ComfyUI error {r.status_code}: {r.text[:2000]}")
            return r.json()["prompt_id"]

    def poll_result(self, prompt_id: str, poll_interval: float = 1.0) -> dict:
        """Block until the prompt finishes, return the history entry."""
        deadline = time.monotonic() + self.timeout
        with httpx.Client(timeout=10, verify=False) as http:
            while time.monotonic() < deadline:
                r = http.get(f"{self.base_url}/history/{prompt_id}")
                r.raise_for_status()
                data = r.json()
                if prompt_id in data:
                    entry = data[prompt_id]
                    if entry.get("status", {}).get("completed", False):
                        return entry
                    status_msg = entry.get("status", {}).get("status_str", "")
                    if "error" in status_msg.lower():
                        raise RuntimeError(f"ComfyUI prompt failed: {status_msg}")
                time.sleep(poll_interval)
        raise TimeoutError(f"Prompt {prompt_id} did not complete within {self.timeout}s")

    def download_image(self, filename: str, subfolder: str = "", output_dir: str = "output") -> bytes:
        """Download a generated image from ComfyUI's output."""
        params = {"filename": filename, "subfolder": subfolder, "type": output_dir}
        with httpx.Client(timeout=30, verify=False) as http:
            r = http.get(f"{self.base_url}/view", params=params)
            r.raise_for_status()
            return r.content

    def generate(self, workflow: dict[str, Any], output_path: Path | None = None) -> Path:
        """Submit workflow, wait for result, save image. Returns path."""
        prompt_id = self.queue_prompt(workflow)
        result = self.poll_result(prompt_id)

        # Find the output image in the result
        outputs = result.get("outputs", {})
        for node_id, node_output in outputs.items():
            images = node_output.get("images", [])
            if images:
                img_info = images[0]
                image_data = self.download_image(
                    filename=img_info["filename"],
                    subfolder=img_info.get("subfolder", ""),
                    output_dir=img_info.get("type", "output"),
                )
                if output_path is None:
                    output_path = Path(f"output_{prompt_id}.png")
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_bytes(image_data)
                return output_path

        raise RuntimeError(f"No images found in prompt {prompt_id} output")
