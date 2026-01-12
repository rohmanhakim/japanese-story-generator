# Quick Setup Guide

## Prerequisites

Install UV (if you haven't already):
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Or on Windows: powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

---

## Setup Methods

Choose the method that fits your workflow:

### Method 1: UV Quick Run (Easiest - No Setup!)

**Best for:** Trying it out, one-off usage

```bash
# Just run - UV handles everything!
uv run --with torch --with transformers --with accelerate --with anthropic \
  python japanese_story_gen.py My_Japanese_Vocabulary.txt
```

**What UV does automatically:**
- ✅ Creates temporary environment
- ✅ Installs all dependencies
- ✅ Runs your script
- ✅ Cleans up after

**No installation, no activation, no hassle!**

---

### Method 2: UV Project (Recommended for Regular Use)

**Best for:** Using this regularly, customization

#### One-time setup:

```bash
# 1. Create UV project
uv init japanese-story-generator
cd japanese-story-generator

# 2. Add dependencies
uv add torch transformers accelerate anthropic

# 3. Copy your files
cp /path/to/japanese_story_gen.py .
cp /path/to/demo.py .
cp /path/to/My_Japanese_Vocabulary.txt .

# 4. Create API key file
echo "sk-ant-your-api-key-here" > anthropic-api-key.txt
```

#### Daily usage:

```bash
# Test vocabulary parsing
uv run python demo.py My_Japanese_Vocabulary.txt

# Generate story with Claude API
uv run python japanese_story_gen.py My_Japanese_Vocabulary.txt

# Generate with local model
uv run python japanese_story_gen.py My_Japanese_Vocabulary.txt \
  --mode local \
  --model rinna/gemma-2-baku-2b

# With theme
uv run python japanese_story_gen.py My_Japanese_Vocabulary.txt \
  --theme "冬の寒い日に料理を作りました"
```

**No need to activate/deactivate environments!**

---

### Method 3: Traditional pip + venv (If You Prefer)

**Best for:** People comfortable with traditional Python workflows

```bash
# 1. Create virtual environment
python3 -m venv venv

# 2. Activate it
source venv/bin/activate  # Linux/Mac
# OR
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install torch transformers accelerate anthropic

# 4. Run your script
python japanese_story_gen.py My_Japanese_Vocabulary.txt

# 5. When done
deactivate
```

---

## Quick Comparison

| Method | Setup Time | Daily Usage | Best For |
|--------|------------|-------------|----------|
| **UV Quick Run** | 0 seconds | Simple command | Trying it out |
| **UV Project** | 2 minutes | Simple command | Regular use ⭐ |
| **pip + venv** | 2 minutes | Activate → Run → Deactivate | Traditional workflow |

---

## Common UV Commands

### Run with specific model:
```bash
uv run python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/gemma-2-baku-2b
```

### Show vocabulary before generating:
```bash
uv run python japanese_story_gen.py vocab.txt --show-vocab
```

### Use Claude API (with key file):
```bash
# Make sure anthropic-api-key.txt exists in current directory
uv run python japanese_story_gen.py vocab.txt
```

### Test vocabulary parsing:
```bash
uv run python demo.py My_Japanese_Vocabulary.txt
```

---

## Troubleshooting UV Issues

### "ModuleNotFoundError: No module named 'torch'"

**Problem:** You're running `python3` directly instead of using `uv run`

**Solution:**
```bash
# DON'T do this:
python3 japanese_story_gen.py vocab.txt

# DO this:
uv run python japanese_story_gen.py vocab.txt

# OR if you used "uv add torch", activate the environment:
source .venv/bin/activate
python japanese_story_gen.py vocab.txt
```

---

### "uv: command not found"

**Solution:** Install UV first
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh

# Restart your terminal or:
source ~/.bashrc  # or ~/.zshrc
```

---

### Dependencies not found even with "uv run --with"

**Solution:** Make sure you list ALL dependencies:
```bash
uv run --with torch --with transformers --with accelerate --with anthropic \
  python japanese_story_gen.py vocab.txt
```

---

## UV Project Structure (Method 2)

After setup, your directory should look like:

```
japanese-story-generator/
├── .venv/                      # Virtual environment (auto-created)
├── pyproject.toml              # UV project config (auto-created)
├── japanese_story_gen.py       # Main script
├── demo.py                     # Vocabulary parser demo
├── anthropic-api-key.txt       # Your API key (gitignored)
├── My_Japanese_Vocabulary.txt  # Your vocab export
├── story.txt                   # Generated stories (gitignored)
└── .gitignore                  # Git ignore file
```

---

## API Key Setup (All Methods)

### Create the API key file:
```bash
echo "sk-ant-your-actual-api-key-here" > anthropic-api-key.txt
```

### Or create manually:
1. Create file: `anthropic-api-key.txt`
2. Paste your API key (just the key, nothing else)
3. Save

### Get your API key:
Visit: https://console.anthropic.com/settings/keys

---

## First Run Examples

### Test everything works:
```bash
# 1. Parse vocabulary (no API needed)
uv run python demo.py My_Japanese_Vocabulary.txt

# 2. Generate with Claude API (needs credits)
uv run python japanese_story_gen.py My_Japanese_Vocabulary.txt

# 3. Generate with local model (free, no API)
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py My_Japanese_Vocabulary.txt \
  --mode local \
  --model rinna/gemma-2-baku-2b
```

---

## Migration from pip to UV

If you already have a pip-based setup:

```bash
# 1. Create UV project
uv init japanese-story-generator
cd japanese-story-generator

# 2. Copy your files
cp ../path/to/*.py .
cp ../path/to/*.txt .

# 3. Add dependencies (UV reads requirements.txt automatically!)
uv add torch transformers accelerate anthropic

# 4. Run with UV
uv run python japanese_story_gen.py vocab.txt

# 5. (Optional) Delete old venv
rm -rf ../old-project/venv
```

---

## Tips for Best Experience

### 1. **Use UV Project for regular use:**
```bash
# Setup once
uv init my-project && cd my-project
uv add torch transformers accelerate anthropic

# Use daily
uv run python script.py
```

### 2. **Create shell alias for convenience:**
```bash
# Add to ~/.bashrc or ~/.zshrc
alias jpstory='uv run python japanese_story_gen.py'

# Then just:
jpstory My_Japanese_Vocabulary.txt --theme "冬の日"
```

### 3. **Pin your dependencies:**
```bash
# In pyproject.toml, UV automatically tracks versions
# This ensures reproducible environments
```

### 4. **Keep API key secure:**
```bash
# Always add to .gitignore
echo "anthropic-api-key.txt" >> .gitignore

# Check it's ignored:
git status  # Should not show the key file
```

---

## Next Steps

After setup, see:
- **README.md** - Full documentation
- **VOCABULARY_MODES.md** - Strict vs flexible vocabulary modes
- **MODEL_REFERENCE.md** - Which model to use
- **TROUBLESHOOTING.md** - Common issues

---

## Quick Reference Card

```bash
# Parse vocabulary (test)
uv run python demo.py vocab.txt

# Generate story (Claude API)
uv run python japanese_story_gen.py vocab.txt

# Generate story (local model)
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt --mode local

# With theme
uv run python japanese_story_gen.py vocab.txt --theme "テーマ"

# Strict vocabulary mode
uv run python japanese_story_gen.py vocab.txt --strict-vocab

# Show vocabulary list
uv run python japanese_story_gen.py vocab.txt --show-vocab
```

---

## Summary

**Recommended workflow:**
1. Install UV (`curl -LsSf https://astral.sh/uv/install.sh | sh`)
2. Use `uv run` for everything (no setup needed)
3. Or create a UV project for regular use
4. Never worry about virtual environments again

