# Pictor

**The painter.** Image generation pipeline for [fabulae.com](https://fabulae.com).

Takes a Latin phrase, generates a scene description via LLM, and produces a Ladybird-style illustration. Designed to work with ComfyUI + style LoRA for local generation, with API fallbacks (Gemini, GPT Image).

## Pipeline

```
Latin phrase → Scene description (LLM) → Illustration (ComfyUI / API)
```

## Features (planned)

- Latin phrase → scene description generation
- ComfyUI API integration with custom style LoRA
- Character reference sheets for consistency across collections
- Batch generation mode
- API fallbacks: Gemini (free), GPT Image 1.5

## Stack

Python

## Part of

[fabulae.com](https://fabulae.com) — free, open-source Latin Comprehensible Input materials for children.

## License

MIT
