# Manual Model Download Guide

If HuggingFace's automatic download is too slow, you can download models manually and place them in the cache directory.

---

## Why Download Manually?

**Advantages:**
- ✅ Use faster download managers (aria2c, IDM, etc.)
- ✅ Resume interrupted downloads
- ✅ Multiple connections for faster speed
- ✅ Download on different machine/network, then transfer
- ✅ Download once, use on multiple machines

---

## Method 1: Automated Scripts (Easiest)

### Option A: Using wget (Built-in)

```bash
# Download and run the script
bash scripts/download_gemma_model.sh

# If interrupted, just run again - it will resume!
```

**Features:**
- ✅ Resumable downloads
- ✅ No extra installation needed
- ✅ Automatic cache directory setup

---

### Option B: Using aria2c (Faster!)

```bash
# Install aria2c first
sudo apt install aria2

# Run the download script
bash scripts/download_gemma_model_aria2c.sh
```

**Features:**
- ✅ 16 parallel connections per file
- ✅ Much faster than wget
- ✅ Resumable
- ✅ Better for slow/unstable connections

**Speed comparison:**
- wget: Single connection (~60 kB/s in your case)
- aria2c: 16 connections (~up to 16x faster!)

---

## Method 2: Manual Browser Download

### Step 1: Visit the Model Page

Go to: https://huggingface.co/rinna/gemma-2-baku-2b/tree/main

### Step 2: Download These Files

**Config files (small, <1MB each):**
- ✅ `config.json`
- ✅ `generation_config.json`
- ✅ `model.safetensors.index.json`
- ✅ `special_tokens_map.json`
- ✅ `tokenizer.json`
- ✅ `tokenizer_config.json`

**Model weights (large!):**
- ✅ `model-00001-of-00003.safetensors` (4.99GB)
- ✅ `model-00002-of-00003.safetensors` (481MB)
- ✅ `model-00003-of-00003.safetensors` (4.98GB)

**Total: ~10.5GB**

### Step 3: Create Cache Directory

```bash
mkdir -p ~/.cache/huggingface/hub/models--rinna--gemma-2-baku-2b/snapshots/main
```

### Step 4: Move Downloaded Files

```bash
# Move all downloaded files to cache
mv ~/Downloads/config.json ~/.cache/huggingface/hub/models--rinna--gemma-2-baku-2b/snapshots/main/
mv ~/Downloads/generation_config.json ~/.cache/huggingface/hub/models--rinna--gemma-2-baku-2b/snapshots/main/
# ... and so on for all files
```

### Step 5: Test It

```bash
uv run python japanese_story_gen.py vocab.txt \
  --mode local \
  --model rinna/gemma-2-baku-2b

# Should load instantly from cache!
```

---

## Method 3: Download on Fast Network, Transfer to Your PC

If you have access to a faster network elsewhere:

### Step 1: Download on Fast Machine

```bash
# On the fast machine
bash script/download_gemma_model.sh

# Or let transformers download it
python -c "from transformers import AutoModel; AutoModel.from_pretrained('rinna/gemma-2-baku-2b')"
```

### Step 2: Compress the Cache

```bash
# On the fast machine
cd ~/.cache/huggingface/hub/
tar -czf gemma-2-baku-2b.tar.gz models--rinna--gemma-2-baku-2b/
```

### Step 3: Transfer to Your Machine

```bash
# Copy via USB, network, whatever
# Then on your machine:
cd ~/.cache/huggingface/hub/
tar -xzf gemma-2-baku-2b.tar.gz
```

---

## Understanding the Cache Directory Structure

```
~/.cache/huggingface/hub/
└── models--rinna--gemma-2-baku-2b/
    └── snapshots/
        └── main/  (or a commit hash like "abc123...")
            ├── config.json
            ├── generation_config.json
            ├── model-00001-of-00003.safetensors
            ├── model-00002-of-00003.safetensors
            ├── model-00003-of-00003.safetensors
            ├── model.safetensors.index.json
            ├── special_tokens_map.json
            ├── tokenizer.json
            └── tokenizer_config.json
```

check your huggingface snapshots
```bash
ls -lh ~/.cache/huggingface/hub/models--rinna--gemma-2-baku-2b/snapshots/*/
```

**Key points:**
- Model name with `--` instead of `/`
- Can be `snapshots/main` or `snapshots/<commit-hash>`
- All files must be in the same directory

---

## Alternative: Use Smaller Model

Instead of downloading 10.5GB, consider:

### rinna/japanese-gpt-1b (2.6GB)

```bash
bash download_gpt1b_model.sh
```

**Direct URLs for GPT-1B:**
```
https://huggingface.co/rinna/japanese-gpt-1b/tree/main
```

Files to download:
- config.json
- generation_config.json
- pytorch_model.bin (2.6GB - single file!)
- special_tokens_map.json
- tokenizer_config.json
- vocab.txt

**Much faster to download!**

---

## Troubleshooting

### "Model not found" after manual download

**Check file locations:**
```bash
ls -lh ~/.cache/huggingface/hub/models--rinna--gemma-2-baku-2b/snapshots/main/

# Should show all 9 files
# If empty, you put files in wrong location
```

### Files are there but model won't load

**Check permissions:**
```bash
chmod -R 755 ~/.cache/huggingface/hub/models--rinna--gemma-2-baku-2b/
```

### Want to use different cache location

**Set environment variable:**
```bash
export HF_HOME=/path/to/different/cache
export TRANSFORMERS_CACHE=/path/to/different/cache

# Then download or copy files there
```

---

## Comparison: Download Methods

| Method | Speed | Resumable | Ease | Best For |
|--------|-------|-----------|------|----------|
| **Auto (transformers)** | Slow | ❌ No | Easy | Good connections |
| **wget script** | Medium | ✅ Yes | Easy | Linux users |
| **aria2c script** | Fast | ✅ Yes | Medium | Power users |
| **Browser + IDM** | Fast | ✅ Yes | Medium | Windows users |
| **Transfer from fast network** | N/A | N/A | Hard | Slow home internet |

---

## Download Manager Recommendations

### Linux:
- **aria2c** - Command line, very fast
  ```bash
  sudo apt install aria2
  ```

### Windows:
- **Internet Download Manager (IDM)** - GUI, commercial
- **Free Download Manager** - GUI, free
- **aria2** with GUI (qBittorrent, uGet)

### macOS:
- **aria2** via Homebrew
  ```bash
  brew install aria2
  ```

---

## Expected Download Times

At different speeds:

| Speed | Gemma 2 (10.5GB) | GPT-1B (2.6GB) |
|-------|------------------|----------------|
| 60 kB/s | ~48 hours 😱 | ~12 hours |
| 500 kB/s | ~6 hours | ~1.5 hours |
| 5 MB/s | ~35 minutes | ~9 minutes |
| 50 MB/s | ~3.5 minutes | ~52 seconds |

**Use aria2c to potentially get 5-10x speedup!**

---

## Quick Commands

### Download Gemma 2 Baku with aria2c:
```bash
sudo apt install aria2
bash download_gemma_model_aria2c.sh
```

### Check download progress:
```bash
# In another terminal
watch -n 1 du -sh ~/.cache/huggingface/hub/models--rinna--gemma-2-baku-2b/
```

### List cached models:
```bash
ls -lh ~/.cache/huggingface/hub/
```

### Delete a cached model (free up space):
```bash
rm -rf ~/.cache/huggingface/hub/models--rinna--gemma-2-baku-2b/
```

---

## After Download Complete

Test your model:

```bash
# Should load instantly from cache
uv run python japanese_story_gen.py My_Japanese_Vocabulary.txt \
  --mode local \
  --model rinna/gemma-2-baku-2b

# You should see:
# "Loading model: rinna/gemma-2-baku-2b"
# And it starts generating immediately (no download!)
```

---

## Summary

**Best approach for slow internet:**

1. ✅ **Use aria2c script** for faster parallel downloads
2. ✅ **Or download GPT-1B** instead (only 2.6GB)
3. ✅ **Or use Claude API** (no download needed!)