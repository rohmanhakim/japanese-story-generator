# Available Models Quick Reference

## Rinna Models (Verified Working - January 2025)

### 1. rinna/japanese-gpt2-medium ⚡
- **Size:** 336M parameters (~500MB download)
- **Year:** 2020
- **Speed:** Very fast (10-30 seconds on CPU)
- **Quality:** ⭐⭐ Basic
- **RAM needed:** 2GB
- **Best for:** Testing, quick results, low-end hardware

```bash
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/japanese-gpt2-medium
```

---

### 2. rinna/japanese-gpt-1b - GOOD BALANCE
- **Size:** 1.3B parameters (~2.6GB download)
- **Year:** 2021
- **Speed:** Medium (1-2 minutes on CPU)
- **Quality:** ⭐⭐⭐ Good
- **RAM needed:** 4-6GB
- **Best for:** Decent quality without huge resources

```bash
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/japanese-gpt-1b
```

---

### 3. rinna/gemma-2-baku-2b - RECOMMENDED
- **Size:** 3B parameters (~6GB download)
- **Year:** 2024 (NEW!)
- **Architecture:** Google Gemma 2
- **Speed:** Medium (1-2 minutes on CPU, ~5-8 sec on GPU)
- **Quality:** ⭐⭐⭐⭐ Very Good
- **RAM needed:** 8-12GB
- **Best for:** Best quality-to-speed ratio

```bash
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/gemma-2-baku-2b
```

**Why Gemma 2 Baku?**
- ✅ 2024 model (newest architecture)
- ✅ Better vocabulary constraint adherence
- ✅ More natural language generation
- ✅ Good balance of speed and quality

---

### 4. rinna/bilingual-gpt-neox-4b
- **Size:** 4B parameters (~8GB download)
- **Year:** 2022
- **Speed:** Slower (3-5 minutes on CPU, ~10-15 sec on GPU)
- **Quality:** ⭐⭐⭐ Good
- **RAM needed:** 10-12GB
- **Best for:** Bilingual (Japanese + English) tasks
- **Note:** Older architecture than Gemma 2 Baku

```bash
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/bilingual-gpt-neox-4b
```

---

### 5. rinna/llama-3-youko-8b - BEST LOCAL QUALITY
- **Size:** 8B parameters (~16GB download)
- **Year:** 2024 (NEW!)
- **Architecture:** Meta Llama 3
- **Speed:** Slow (4-6 minutes on CPU, ~15-20 sec on GPU)
- **Quality:** ⭐⭐⭐⭐⭐ Excellent
- **RAM needed:** 16-20GB
- **Best for:** Maximum local quality

```bash
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/llama-3-youko-8b
```

**Why Llama 3 Youko?**
- ✅ 2024 state-of-the-art architecture
- ✅ Best vocabulary constraint adherence (local)
- ✅ Most natural story generation
- ✅ Worth the wait if you have RAM

---

### 6. rinna/youri-7b
- **Size:** 7B parameters (~14GB download)
- **Year:** 2023
- **Architecture:** Llama 2
- **Speed:** Slow (3-5 minutes on CPU, ~12-18 sec on GPU)
- **Quality:** ⭐⭐⭐⭐ Very Good
- **RAM needed:** 14-16GB
- **Best for:** Alternative to Llama 3 (slightly older)

```bash
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/youri-7b
```

---

## Claude API - BEST OVERALL

- **Size:** N/A (cloud-based)
- **Speed:** ~5 seconds
- **Quality:** ⭐⭐⭐⭐⭐ Excellent
- **Cost:** ~$0.007 per story (with token optimization)
- **Best for:** Best results, strict vocabulary adherence

```bash
# Make sure you have credits and API key file
uv run python japanese_story_gen.py vocab.txt
```

---

## Model Comparison Table

| Model | Size | Year | Arch | Quality | Speed (CPU) | Speed (GPU) | RAM |
|-------|------|------|------|---------|-------------|-------------|-----|
| GPT-2 Medium | 336M | 2020 | GPT-2 | ⭐⭐ | ⚡⚡⚡ 10-30s | ⚡⚡⚡ 3-5s | 2GB |
| GPT-1B | 1.3B | 2021 | GPT-NeoX | ⭐⭐⭐ | ⚡⚡ 1-2min | ⚡⚡⚡ 5-8s | 4-6GB |
| **Gemma 2 Baku** | **3B** | **2024** | **Gemma 2** | **⭐⭐⭐⭐** | **⚡⚡ 1-2min** | **⚡⚡⚡ 5-8s** | **8-12GB** |
| GPT-NeoX 4B | 4B | 2022 | GPT-NeoX | ⭐⭐⭐ | ⚡ 3-5min | ⚡⚡ 10-15s | 10-12GB |
| Youri 7B | 7B | 2023 | Llama 2 | ⭐⭐⭐⭐ | ⚡ 3-5min | ⚡⚡ 12-18s | 14-16GB |
| **Llama 3 Youko** | **8B** | **2024** | **Llama 3** | **⭐⭐⭐⭐⭐** | **⚡ 4-6min** | **⚡⚡ 15-20s** | **16-20GB** |
| **Claude API** | **Cloud** | **2025** | **Sonnet 4.5** | **⭐⭐⭐⭐⭐** | **⚡⚡⚡ 5s** | **⚡⚡⚡ 5s** | **0GB** |

---

## Decision Tree

**Do you have Anthropic API credits?**
- ✅ YES → Use **Claude API** (best quality, fastest)
- ❌ NO → Continue...

**How much RAM do you have?**

### 4-8GB RAM:
```bash
# Use GPT-1B
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/japanese-gpt-1b
```

### 8-16GB RAM (Most people):
```bash
# Use Gemma 2 Baku (RECOMMENDED)
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/gemma-2-baku-2b
```

### 16GB+ RAM:
```bash
# Use Llama 3 Youko (best local quality)
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/llama-3-youko-8b
```

**Do you have any NVIDIA GPU?**
- ✅ YES → 10-20x faster. Use any model comfortably
- ❌ NO → CPU is fine, just slower

---

## Download Times (First Run Only)

Models are cached after first download in `~/.cache/huggingface/`:

| Model | Download Size | Time (fast internet) |
|-------|---------------|---------------------|
| GPT-2 Medium | ~500MB | ~1 minute |
| GPT-1B | ~2.6GB | ~3-5 minutes |
| **Gemma 2 Baku** | ~6GB | ~8-12 minutes |
| GPT-NeoX 4B | ~8GB | ~10-15 minutes |
| Youri 7B | ~14GB | ~15-20 minutes |
| **Llama 3 Youko** | ~16GB | ~20-25 minutes |

**Subsequent runs use cached model (instant load)!**

---

## My Recommendations by Use Case

### For Beginners / Testing:
```bash
# Fast, small, good enough
rinna/japanese-gpt-1b
```

### For Regular Use (Best Balance):
```bash
# 2024 model, great quality-to-speed ratio
rinna/gemma-2-baku-2b
```

### For Best Local Quality:
```bash
# If you have 16GB+ RAM or RTX GPU
rinna/llama-3-youko-8b
```

### For Best Overall Quality:
```bash
# If you have API credits
Claude API (just run without --mode local)
```

---

## Quality vs Vocabulary Constraint Adherence

| Model | Story Quality | Vocabulary Adherence | Notes |
|-------|---------------|---------------------|-------|
| GPT-2 Medium | ⭐⭐ | ⭐⭐ | May introduce ~20% new words |
| GPT-1B | ⭐⭐⭐ | ⭐⭐⭐ | May introduce ~15% new words |
| **Gemma 2 Baku** | **⭐⭐⭐⭐** | **⭐⭐⭐⭐** | **~10% new words, natural** |
| GPT-NeoX 4B | ⭐⭐⭐ | ⭐⭐⭐ | May introduce ~12% new words |
| Youri 7B | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ~8% new words |
| **Llama 3 Youko** | **⭐⭐⭐⭐⭐** | **⭐⭐⭐⭐** | **~5-8% new words** |
| **Claude API** | **⭐⭐⭐⭐⭐** | **⭐⭐⭐⭐⭐** | **~2-5% new words** |

**Note:** These are estimates. Actual adherence varies by vocabulary size and story complexity.

Use `--strict-vocab` flag for stricter constraints (but may reduce story quality).

---

## Installation & Setup

### No GPU (CPU only):
```bash
# Install dependencies
uv sync

# Or with uv run
uv run --with torch --with transformers --with accelerate \
  python japanese_story_gen.py vocab.txt --mode local
```

### With NVIDIA GPU:
```bash
# Install CUDA-enabled PyTorch
uv pip install torch --index-url https://download.pytorch.org/whl/cu121

# Verify GPU detection
python -c "import torch; print(torch.cuda.is_available())"

# Run normally - script auto-detects GPU!
uv run python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/gemma-2-baku-2b
```

---

## Summary

**Quick picks:**

- **Free + Fast:** `rinna/japanese-gpt-1b`
- **Best Balance:** `rinna/gemma-2-baku-2b`
- **Best Local:** `rinna/llama-3-youko-8b`
- **Best Overall:** Claude API



Choose based on your RAM, speed preference, and quality needs. When in doubt, start with **Gemma 2 Baku** - it's the sweet spot
