#!/bin/bash
# Download Gemma 2 Baku model with aria2c (faster, parallel downloads)
# Install aria2c first: sudo apt install aria2

MODEL_DIR=~/.cache/huggingface/hub/models--rinna--gemma-2-baku-2b/snapshots/main
mkdir -p "$MODEL_DIR"
cd "$MODEL_DIR"

BASE_URL="https://huggingface.co/rinna/gemma-2-baku-2b/resolve/main"

echo "Downloading Gemma 2 Baku model with aria2c..."
echo "This will download ~10.5GB total"
echo "Using 16 connections per file for faster download!"
echo ""

# Check if aria2c is installed
if ! command -v aria2c &> /dev/null; then
    echo "❌ aria2c not found!"
    echo "Install it with: sudo apt install aria2"
    echo "Or use the wget version: ./download_gemma_model.sh"
    exit 1
fi

# aria2c options:
# -x 16: Use 16 connections per file
# -s 16: Split into 16 segments
# -k 1M: Minimum split size 1MB
# -c: Continue/resume downloads

ARIA_OPTS="-x 16 -s 16 -k 1M -c"

# Download config files (small)
echo "Downloading config files..."
aria2c $ARIA_OPTS "${BASE_URL}/config.json"
aria2c $ARIA_OPTS "${BASE_URL}/generation_config.json"
aria2c $ARIA_OPTS "${BASE_URL}/model.safetensors.index.json"
aria2c $ARIA_OPTS "${BASE_URL}/special_tokens_map.json"
aria2c $ARIA_OPTS "${BASE_URL}/tokenizer.json"
aria2c $ARIA_OPTS "${BASE_URL}/tokenizer_config.json"

# Download model weights (large) with progress
echo ""
echo "Downloading model weights..."
echo "Part 1 of 3: 4.99GB (this will take a while)"
aria2c $ARIA_OPTS "${BASE_URL}/model-00001-of-00003.safetensors"

echo ""
echo "Part 2 of 3: 481MB"
aria2c $ARIA_OPTS "${BASE_URL}/model-00002-of-00003.safetensors"

echo ""
echo "Part 3 of 3: 4.98GB"
aria2c $ARIA_OPTS "${BASE_URL}/model-00003-of-00003.safetensors"

echo ""
echo "✅ Download complete!"
echo "Model cached at: $MODEL_DIR"
echo ""
echo "Test it with:"
echo "uv run python japanese_story_gen.py vocab.txt --mode local --model rinna/gemma-2-baku-2b"
