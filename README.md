# Japanese Story Generator from Anki Vocabulary

Generate Japanese stories using only words from your Anki vocabulary deck.

## Features

- ✅ Generate stories using your known vocabulary
- ✅ Two modes: Claude API (best quality) or Local LLM (free)
- ✅ Flexible or strict vocabulary constraints
- ✅ Token-optimized (50% savings)
- ✅ Multiple model support (Rinna, Llama, Gemma)

## Quick Start

### 1. Install UV
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. Clone and Setup
```bash
git clone <your-repo-url>
cd japanese-story-generator
uv sync  # Installs all dependencies
```

### 3. Add Your API Key (if using Claude)
```bash
echo "sk-ant-your-api-key-here" > anthropic-api-key.txt
```

### 4. Export Your Anki Deck
1. Anki → File → Export → Notes in Plain Text (.txt)
2. ✅ Check "Include HTML and media references"
3. Save as `My_Japanese_Vocabulary.txt`

### 5. Generate!
```bash
# With Claude API
uv run python japanese_story_gen.py My_Japanese_Vocabulary.txt

# With local model (free)
uv run python japanese_story_gen.py My_Japanese_Vocabulary.txt --mode local
```

## Documentation

- **[SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** - Full setup instructions
- **[MODEL_REFERENCE.md](docs/MODEL_REFERENCE.md)** - Model selection guide
- **[TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)** - Common issues
- **[VOCABULARY_MODES.md](docs/VOCABULARY_MODES.md)** - Vocabulary constraints

---

## Project Structure

```
japanese-story-generator/
├── pyproject.toml              # ✅ COMMIT - Dependencies
├── .python-version             # ✅ COMMIT - Python version  
├── .gitignore                  # ✅ COMMIT - Ignore rules
│
├── japanese_story_gen.py       # ✅ COMMIT - Main script
├── demo.py                     # ✅ COMMIT - Test script
├── docs/
│   ├── reports/
│   │   ├── *.md                # ✅ COMMIT - Experimentation reports
│   │   └── story*.txt          # ✅ COMMIT - Experiment outputs
│   └── *.md                    # ✅ COMMIT - Documentations
│
├── scripts/
│   └── *.sh                    # ✅ COMMIT - Helper scripts
│
├── .venv/                      # ❌ IGNORE - Virtual env
├── anthropic-api-key.txt       # ❌ IGNORE - SECRET!
├── My_Japanese_Vocabulary.txt  # ❌ IGNORE - Personal data
└── story.txt                   # ❌ IGNORE - Output
```

## Contributing

### Adding Dependencies:
```bash
uv add package-name          # Adds to pyproject.toml
git add pyproject.toml       # Commit the change
git commit -m "Add package-name dependency"
```

### Never Commit:
- API keys
- Personal vocabulary files
- Generated stories
- Virtual environments

## Troubleshooting

See [TROUBLESHOOTING.md](docs/TROUBLESHOOTING.md)

Quick fixes:
```bash
# Module not found
uv sync

# API key issues
cat anthropic-api-key.txt  # Check it exists and has your key

# Use local mode instead
uv run python japanese_story_gen.py vocab.txt --mode local
```

## License

MIT
