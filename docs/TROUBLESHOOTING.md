# Troubleshooting Guide

## Error: "Insufficient credits" or "credit balance is too low"

**What happened:** Your Anthropic account doesn't have enough credits to make API calls.

**Solutions:**

### Option 1: Add credits to your Anthropic account
1. Go to: https://console.anthropic.com/settings/billing
2. Add credits ($5 minimum)
3. Try running the script again

### Option 2: Use local LLM instead (FREE)
```bash
# Install dependencies
uv pip install torch transformers accelerate

# Run with local model (no API needed)
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py My_Japanese_Vocabulary.txt --mode local
```

**Recommended local models:**
- `rinna/japanese-gpt2-medium` (default, fastest, ~500MB)
- `rinna/japanese-gpt-1b` (better quality, ~2.6GB, recommended)

**Example with better model:**
```bash
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py My_Japanese_Vocabulary.txt \
  --mode local \
  --model rinna/japanese-gpt-1b
```

---

## Error: "Invalid API key" or "Authentication failed"

**Problem:** Your API key is incorrect or expired.

**Solution:**
1. Get a new API key: https://console.anthropic.com/settings/keys
2. Update your `anthropic-api-key.txt` file:
   ```bash
   echo "sk-ant-your-new-key-here" > anthropic-api-key.txt
   ```
3. Make sure the key starts with `sk-ant-`

---

## Error: "Module not found: anthropic"

**Solution with UV:**
```bash
uv run --with anthropic python japanese_story_gen.py My_Japanese_Vocabulary.txt
```

**Or install it:**
```bash
uv pip install anthropic
# or
pip install --user anthropic
```

---

## Error: "Module not found: torch" (when using local mode)

**Solution:**
```bash
uv pip install torch transformers accelerate

# Or use UV's --with flag:
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt --mode local
```

---

## Local mode is very slow

**Reasons:**
- Running on CPU (not GPU)
- Large model size

**Solutions:**

### 1. Use smaller model:
```bash
python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/japanese-gpt2-medium  # Smallest/fastest
```

### 2. Use GPU (if you have NVIDIA GPU):
```bash
# Install CUDA-enabled PyTorch
pip install torch --index-url https://download.pytorch.org/whl/cu118
```

### 3. Use Claude API instead:
- Much faster (~5 seconds vs 2+ minutes)
- Better quality stories
- Only ~$0.01 per story

---

## Stories contain words I don't know

**Issue:** The model is introducing new vocabulary.

**Why:** 
- Local models (especially smaller ones) struggle with strict constraints
- GPT-2 Medium is old (2020) and small (336M parameters)

**Solutions:**

### 1. Use Claude API (best constraint adherence):
```bash
# Add credits first, then:
python japanese_story_gen.py vocab.txt
```

### 2. Use larger local model:
```bash
python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/japanese-gpt-1b  # 4x larger, better quality
```

### 3. Build your vocabulary more:
- Add more words to your Anki deck
- Re-export and generate again

---

## "CUDA out of memory" error

**Problem:** Model is too large for your GPU.

**Solutions:**

### 1. Use smaller model:
```bash
python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/japanese-gpt2-medium
```

### 2. Use CPU instead (slower but works):
```bash
# PyTorch will automatically fall back to CPU
# Just be patient - it will take 2-5 minutes
```

### 3. Use Claude API (no GPU needed):
```bash
python japanese_story_gen.py vocab.txt
```

---

## Can't find my API key file

**Make sure:**
1. The file is named exactly `anthropic-api-key.txt`
2. It's in the same directory as `japanese_story_gen.py`
3. It contains just your API key (no extra spaces or newlines)

**Check:**
```bash
# See if file exists
ls -la anthropic-api-key.txt

# View contents (be careful - this shows your key!)
cat anthropic-api-key.txt
```

**Or specify a different location:**
```bash
python japanese_story_gen.py vocab.txt \
  --api-key-file /path/to/my-key.txt
```

---

## Rate limit exceeded

**Problem:** You're making too many requests too quickly.

**Solution:** 
Wait a minute and try again. Anthropic has rate limits to prevent abuse.

---

## Connection error / Network issues

**Possible causes:**
- No internet connection
- Firewall blocking requests
- Anthropic API is down (rare)

**Solutions:**
1. Check your internet connection
2. Try again in a few minutes
3. Use local mode (doesn't need internet):
   ```bash
   python japanese_story_gen.py vocab.txt --mode local
   ```

---

## Comparison: Claude API vs Local LLM

| Feature | Claude API | Local LLM |
|---------|-----------|-----------|
| **Cost** | ~$0.01/story | Free |
| **Speed** | ~5 seconds | 2-10 minutes (CPU) |
| **Quality** | ⭐⭐⭐⭐⭐ | ⭐⭐ to ⭐⭐⭐ |
| **Constraint adherence** | Excellent | Fair to Good |
| **Internet needed** | Yes | No (after download) |
| **Setup difficulty** | Easy | Medium |
| **RAM needed** | None | 2-16GB |

**Recommendation:**
- **For best results:** Use Claude API
- **For offline/free:** Use local with `rinna/japanese-gpt-1b`
- **For fastest local:** Use `rinna/japanese-gpt2-medium`

---

## Still having issues?

1. Make sure you're using the latest version of the script
2. Check that your Anki export file is valid:
   ```bash
   python demo.py My_Japanese_Vocabulary.txt
   ```
3. Try the simplest command first:
   ```bash
   python japanese_story_gen.py vocab.txt --show-vocab
   ```

If the demo works but story generation doesn't, the issue is with the LLM setup (API key or local model installation).
