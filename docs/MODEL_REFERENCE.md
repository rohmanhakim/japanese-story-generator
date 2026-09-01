# Available Models Reference

This project uses OpenRouter API for story generation. Free models are available with rate limits.

---

## Free Models (with `:free` suffix)

### Google Models

| Model | Quality | Speed | Notes |
|-------|---------|-------|-------|
| `google/gemma-4-26b-a4b-it:free` | ⭐⭐⭐⭐ | Fast | **Default** - Good balance |
| `google/gemma-2-9b-it:free` | ⭐⭐⭐ | Fast | Smaller, faster |
| `google/gemma-2-27b-it:free` | ⭐⭐⭐⭐ | Medium | Larger, better quality |

### Meta Models

| Model | Quality | Speed | Notes |
|-------|---------|-------|-------|
| `meta-llama/llama-3.1-8b-instruct:free` | ⭐⭐⭐⭐ | Fast | Good general purpose |
| `meta-llama/llama-3.1-70b-instruct:free` | ⭐⭐⭐⭐⭐ | Medium | High quality |

### Other Models

| Model | Quality | Speed | Notes |
|-------|---------|-------|-------|
| `qwen/qwen-2-7b-instruct:free` | ⭐⭐⭐ | Fast | Good for Japanese |
| `microsoft/phi-3-mini-128k-instruct:free` | ⭐⭐⭐ | Fast | Small but capable |

---

## Paid Models (Better Quality, No Rate Limits)

| Model | Cost | Quality | Notes |
|-------|------|---------|-------|
| `openai/gpt-4o-mini` | ~$0.001/1K tokens | ⭐⭐⭐⭐⭐ | Excellent, affordable |
| `openai/gpt-4o` | ~$0.005/1K tokens | ⭐⭐⭐⭐⭐ | Best quality |
| `anthropic/claude-3-haiku` | ~$0.00025/1K tokens | ⭐⭐⭐⭐ | Fast, cheap |
| `anthropic/claude-3.5-sonnet` | ~$0.003/1K tokens | ⭐⭐⭐⭐⭐ | High quality |

---

## Model Selection Guide

### For Testing/Trying Out
```bash
# Use free model
uv run jp-story vocab.txt --model "google/gemma-4-26b-a4b-it:free"
```

### For Regular Use (Best Balance)
```bash
# Use affordable paid model
uv run jp-story vocab.txt --model "openai/gpt-4o-mini"
```

### For Best Quality
```bash
# Use premium model
uv run jp-story vocab.txt --model "openai/gpt-4o"
```

---

## Free Model Rate Limits

Free models have strict rate limits:
- **Requests:** ~1-5 per minute
- **Tokens:** Limited per day
- **Availability:** May be temporarily unavailable

**Workarounds:**
1. Wait between requests
2. Use your own API key (add at provider settings)
3. Switch to paid model

---

## Japanese Language Support

All models support Japanese, but some are better than others:

| Model | Japanese Quality | Notes |
|-------|------------------|-------|
| Google Gemma | ⭐⭐⭐⭐ | Good Japanese training |
| Meta Llama | ⭐⭐⭐ | Decent, improving |
| Qwen | ⭐⭐⭐⭐ | Strong multilingual |
| GPT-4o | ⭐⭐⭐⭐⭐ | Excellent |
| Claude | ⭐⭐⭐⭐⭐ | Excellent |

---

## Setting Your Model

### Via CLI
```bash
uv run jp-story vocab.txt --model "model-name:free"
```

### Via Environment Variable
```bash
export OPENROUTER_MODEL="model-name:free"
```

### In Code
```python
from japanese_story_generator import StoryGenerator

generator = StoryGenerator(
    api_key="your-key",
    model="model-name:free"
)
```

---

## Finding Available Models

Visit: https://openrouter.ai/models

Filter by:
- **Free** - Models with `:free` suffix
- **Japanese** - Models with good Japanese support
- **Chat** - Instruction-tuned models

---

## Recommended Setup

1. **Get free API key:** https://openrouter.ai/keys
2. **Use default model:** `google/gemma-4-26b-a4b-it:free`
3. **If rate limited:** Wait or use `openai/gpt-4o-mini` (requires credits)

---

## Quick Reference

```bash
# List models in help
uv run jp-story --help

# Use specific model
uv run jp-story vocab.txt --model "google/gemma-4-26b-a4b-it:free"

# Use paid model (no rate limits)
uv run jp-story vocab.txt --model "openai/gpt-4o-mini"
```
