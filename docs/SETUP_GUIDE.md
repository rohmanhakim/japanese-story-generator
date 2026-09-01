# Quick Setup Guide

## Prerequisites

Install UV (if you haven't already):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Quick Start

### 1. Clone and Install

```bash
git clone <your-repo-url>
cd japanese-story-generator
uv sync
```

### 2. Set API Key

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-api-key"
```

Get your API key at: https://openrouter.ai/keys

### 3. Export Anki Deck

1. Open Anki → File → Export
2. Select "Notes in Plain Text (.txt)"
3. ✅ Check "Include HTML and media references"
4. Save as `My_Japanese_Vocabulary.txt`

### 4. Generate Stories

```bash
uv run jp-story My_Japanese_Vocabulary.txt
```

---

## Package Structure

```
japanese-story-generator/
├── japanese_story_generator/
│   ├── __init__.py           # Package exports
│   ├── anki_parser.py        # AnkiVocabParser class
│   ├── story_generator.py    # StoryGenerator class
│   ├── openrouter.py         # OpenRouterClient class
│   └── verifier.py           # ConjugationVerifier class
├── scripts/
│   └── generate.py           # CLI entry point
├── pyproject.toml
└── README.md
```

---

## Usage as CLI

```bash
# Basic usage
uv run jp-story My_Japanese_Vocabulary.txt

# With theme
uv run jp-story My_Japanese_Vocabulary.txt --theme "at school"

# Strict vocabulary mode
uv run jp-story My_Japanese_Vocabulary.txt --strict

# Verify conjugations
uv run jp-story My_Japanese_Vocabulary.txt --verify

# Show vocabulary list
uv run jp-story My_Japanese_Vocabulary.txt --show-vocab

# Use different model
uv run jp-story My_Japanese_Vocabulary.txt --model "openai/gpt-4o-mini"
```

---

## Usage as Python Package

```python
from japanese_story_generator import StoryGenerator, AnkiVocabParser

# Parse vocabulary
parser = AnkiVocabParser("My_Japanese_Vocabulary.txt")
vocab_words = parser.parse()
print(f"Found {len(vocab_words)} words")

# Generate story
generator = StoryGenerator(api_key="your-api-key")
story = generator.generate(vocab_words, theme="daily life")
print(story)
```

---

## API Reference

### AnkiVocabParser

```python
from japanese_story_generator import AnkiVocabParser

parser = AnkiVocabParser("My_Japanese_Vocabulary.txt")

# Get list of words
words = parser.parse()  # ["食べる", "飲む", "水", ...]

# Get words with readings
words_with_readings = parser.parse_with_readings()
# [{"kanji": "食べる", "reading": "たべる"}, ...]
```

### StoryGenerator

```python
from japanese_story_generator import StoryGenerator

generator = StoryGenerator(api_key="your-key")

# Generate story
story = generator.generate(
    vocab_words=["食べる", "飲む", "水"],
    theme="daily life",
    max_length=500,
    strict_vocab=True
)

# Generate with comprehension questions
result = generator.generate_with_questions(
    vocab_words=["食べる", "飲む", "水"],
    level="n5"
)
# {"story": "...", "questions": "...", "vocab_used": [...]}
```

### ConjugationVerifier

```python
from japanese_story_generator import ConjugationVerifier

verifier = ConjugationVerifier()
result = verifier.verify("私は学校に行きます", ["行く", "学校"])

print(result["conjugations"])  # Words found in vocabulary
print(result["violations"])    # Words not in vocabulary
```

---

## CLI Options

| Option | Description |
|--------|-------------|
| `--theme TEXT` | Story theme |
| `--model MODEL` | OpenRouter model (default: google/gemma-4-26b-a4b-it:free) |
| `--api-key KEY` | OpenRouter API key |
| `--output FILE` | Output file (default: story.txt) |
| `--strict` | Use only provided vocabulary |
| `--max-length N` | Max story length in characters (default: 500) |
| `--verify` | Show conjugation verification |
| `--show-vocab` | Display parsed vocabulary |

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `OPENROUTER_API_KEY` | Your OpenRouter API key |

---

## Troubleshooting

### "API key required"
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key"
# Or use --api-key flag
```

### "Rate limit exceeded"
- Wait a few minutes and retry
- Use a different model: `--model "openai/gpt-4o-mini"`
- Add your own API key: https://openrouter.ai/settings/integrations

### "Invalid model"
- Check available models: https://openrouter.ai/models
- Free models use `:free` suffix

See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for more issues.

---

## Next Steps

- [MODEL_REFERENCE.md](MODEL_REFERENCE.md) - Available models
- [VOCABULARY_MODES.md](VOCABULARY_MODES.md) - Vocabulary constraint options
- [CONJUGATION_HANDLING_GUIDE.md](CONJUGATION_HANDLING_GUIDE.md) - Conjugation verification
