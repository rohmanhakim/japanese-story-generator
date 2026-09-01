# Troubleshooting Guide

## Error: "API key required"

**What happened:** No API key was found.

**Solutions:**

### Option 1: Set environment variable
```bash
export OPENROUTER_API_KEY="sk-or-v1-your-key"
```

### Option 2: Use CLI flag
```bash
uv run jp-story vocab.txt --api-key "sk-or-v1-your-key"
```

### Option 3: Get API key
1. Visit: https://openrouter.ai/keys
2. Create account and get key
3. Set as above

---

## Error: "Rate limit exceeded"

**What happened:** Free model rate limit reached.

**Solutions:**

1. **Wait and retry** - Rate limits reset after 1-2 minutes

2. **Use different model**
   ```bash
   uv run jp-story vocab.txt --model "openai/gpt-4o-mini"
   ```

3. **Add your own API key** to bypass shared rate limits
   - Go to: https://openrouter.ai/settings/integrations
   - Add your own provider API key

---

## Error: "Invalid model" or "Model not found"

**What happened:** The model doesn't exist or isn't available for free.

**Solution:**
```bash
# Check available models
# Visit: https://openrouter.ai/models

# Use default (free) model
uv run jp-story vocab.txt

# Or specify a valid model
uv run jp-story vocab.txt --model "openai/gpt-4o-mini"
```

---

## Error: "Invalid API key"

**What happened:** API key is incorrect.

**Solution:**
1. Get correct key: https://openrouter.ai/keys
2. Update your key:
   ```bash
   export OPENROUTER_API_KEY="sk-or-v1-correct-key"
   ```

---

## Error: "Could not connect to OpenRouter"

**What happened:** Network connection issue.

**Solutions:**
1. Check internet connection
2. Check firewall settings
3. Try again later (OpenRouter may be temporarily down)

---

## Error: "Insufficient credits"

**What happened:** Your account doesn't have enough credits for paid models.

**Solutions:**
1. Add credits: https://openrouter.ai/credits
2. Use free model: `--model "google/gemma-4-26b-a4b-it:free"`
3. Use different provider

---

## Import Errors

### "Cannot import name 'ConjugationVerifier'"

```bash
# Reinstall package
uv sync
```

### "ModuleNotFoundError: No module named 'japanese_story_generator'"

```bash
# Make sure you're in the project directory
cd japanese-story-generator

# Reinstall
uv sync
```

---

## Story Generation Issues

### Stories contain words not in vocabulary

**Cause:** Model may add some words outside vocabulary for natural flow.

**Solutions:**
1. Use strict mode:
   ```bash
   uv run jp-story vocab.txt --strict
   ```

2. Use better model:
   ```bash
   uv run jp-story vocab.txt --model "openai/gpt-4o"
   ```

3. Add more vocabulary to your Anki deck

### Stories are too short/long

**Adjust max length:**
```bash
uv run jp-story vocab.txt --max-length 300  # Shorter
uv run jp-story vocab.txt --max-length 1000 # Longer
```

### Stories are repetitive

**Cause:** Vocabulary list may be too small or similar.

**Solutions:**
1. Add more diverse vocabulary
2. Use theme option:
   ```bash
   uv run jp-story vocab.txt --theme "cooking at home"
   ```

---

## Anki Export Issues

### "Found 0 words"

**Cause:** Anki export format doesn't match expected format.

**Solution:**
1. Re-export from Anki:
   - File → Export
   - Format: "Notes in Plain Text (.txt)"
   - ✅ Check "Include HTML and media references"

2. Check file format:
   ```bash
   head -5 My_Japanese_Vocabulary.txt
   ```
   Should show: `word[TAB]"html content"`

---

## Performance Issues

### Slow generation with free models

**Cause:** Free models may be slower due to shared resources.

**Solutions:**
1. Use faster model:
   ```bash
   uv run jp-story vocab.txt --model "qwen/qwen-2-7b-instruct:free"
   ```

2. Use paid model:
   ```bash
   uv run jp-story vocab.txt --model "openai/gpt-4o-mini"
   ```

---

## Still having issues?

1. Check the error message carefully
2. Verify your setup:
   ```bash
   uv run jp-story --help
   ```

3. Test with minimal command:
   ```bash
   uv run jp-story vocab.txt --show-vocab
   ```

4. Open an issue with:
   - Full error message
   - Command you ran
   - Your operating system
   - Python version (`python --version`)
