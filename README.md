# Japanese Story Generator

Generate Japanese stories using only words from your Anki vocabulary deck. Perfect for language learners who want reading practice with controlled vocabulary.

## Features

- ✅ **Vocabulary-constrained stories** - Generate stories using only words you know
- ✅ **OpenRouter API** - Access to multiple AI models (free tier available)
- ✅ **Strict/Flexible modes** - Control vocabulary usage
- ✅ **Conjugation verification** - Track vocabulary usage with multiple matching strategies
- ✅ **Compound word detection** - Handles compound nouns like 鍋料理
- ✅ **Kanji variant handling** - Matches 暖かい/温かい, 混ぜる/交ぜる correctly
- ✅ **Importable package** - Use in other Python projects
- ✅ **CLI tool** - Simple command-line interface

---

## Quick Start

### 1. Install

```bash
git clone <your-repo-url>
cd japanese-story-generator
uv sync
```

### 2. Set API Key

```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key"
```

Get a free key at: https://openrouter.ai/keys

### 3. Export Anki Deck

1. Open Anki → File → Export
2. Format: "Notes in Plain Text (.txt)"
3. ✅ Check "Include HTML and media references"
4. Save as `My_Japanese_Vocabulary.txt`

### 4. Generate Stories

```bash
uv run jp-story My_Japanese_Vocabulary.txt
```

---

## Usage Examples

### Basic Usage
```bash
uv run jp-story vocab.txt
```

### With Theme
```bash
uv run jp-story vocab.txt --theme "at school"
```

### Strict Vocabulary Mode
```bash
uv run jp-story vocab.txt --strict
```

### Verify Vocabulary Usage
```bash
uv run jp-story vocab.txt --verify
```

### Use Different Model
```bash
uv run jp-story vocab.txt --model "openai/gpt-4o-mini"
```

---

## Python Package Usage

```python
from japanese_story_generator import StoryGenerator, AnkiVocabParser

# Parse vocabulary
parser = AnkiVocabParser("My_Japanese_Vocabulary.txt")
vocab_words = parser.parse()

# Generate story
generator = StoryGenerator(api_key="your-key")
story = generator.generate(vocab_words, theme="daily life")
print(story)
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
├── docs/
│   ├── SETUP_GUIDE.md        # Installation guide
│   ├── MODEL_REFERENCE.md    # Available models
│   ├── TROUBLESHOOTING.md    # Common issues
│   ├── VOCABULARY_MODES.md   # Strict vs flexible
│   └── CONJUGATION_HANDLING_GUIDE.md
├── pyproject.toml
└── README.md
```

---

## CLI Options

| Option | Description | Default |
|--------|-------------|---------|
| `--theme TEXT` | Story theme | None |
| `--model MODEL` | OpenRouter model | `google/gemma-4-26b-a4b-it:free` |
| `--api-key KEY` | OpenRouter API key | `OPENROUTER_API_KEY` env var |
| `--output FILE` | Output file | `story.txt` |
| `--strict` | Use only provided vocabulary | False |
| `--max-length N` | Max story length (chars) | 500 |
| `--verify` | Show conjugation verification | False |
| `--show-vocab` | Display parsed vocabulary | False |

---

## Available Models

### Free Models
- `google/gemma-4-26b-a4b-it:free` (default)
- `google/gemma-2-9b-it:free`
- `meta-llama/llama-3.1-8b-instruct:free`
- `qwen/qwen-2-7b-instruct:free`

### Paid Models (Better Quality)
- `openai/gpt-4o-mini` (~$0.001/1K tokens)
- `openai/gpt-4o` (~$0.005/1K tokens)
- `anthropic/claude-3-haiku` (~$0.00025/1K tokens)

See [MODEL_REFERENCE.md](docs/MODEL_REFERENCE.md) for full list.

---

## Documentation

- **[SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Installation and usage
- **[MODEL_REFERENCE.md](docs/MODEL_REFERENCE.md)** - Available models
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues
- **[VOCABULARY_MODES.md](docs/VOCABULARY_MODES.md)** - Vocabulary constraints
- **[CONJUGATION_HANDLING_GUIDE.md](docs/CONJUGATION_HANDLING_GUIDE.md)** - Conjugation verification & vocabulary matching

---

## Violation-Based Learning

This package supports a violation-based learning approach where vocabulary violations become curriculum:

```python
from japanese_story_generator import StoryGenerator, ConjugationVerifier

# Generate story with current vocabulary
story = generator.generate(current_vocab, strict=True)

# Find violations (words not in vocabulary)
result = verifier.verify(story, current_vocab)
violations = result["violations"]

# Grade violations by difficulty (in learn-jp)
for v in violations:
    grade = grade_violation(v, current_level)
    if grade == "introduce_now":
        add_to_anki(v["surface"])
```

See [learn-jp/docs/VIOLATION_BASED_LEARNING.md](/home/arif/Projects/learn-jp/docs/VIOLATION_BASED_LEARNING.md) for the full approach.

---

## Development

```bash
# Install dev dependencies
uv sync

# Run tests
uv run pytest

# Run CLI
uv run jp-story --help
```

---

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

---

## License

MIT
