#!/bin/bash
# Download Gemma 2 Baku model manually with wget
# This allows resuming if interrupted!

MODEL_DIR=~/.cache/huggingface/hub/models--rinna--gemma-2-baku-2b/snapshots/main
mkdir -p "$MODEL_DIR"
cd "$MODEL_DIR"

BASE_URL="https://huggingface.co/rinna/gemma-2-baku-2b/resolve/main"

echo "Downloading Gemma 2 Baku model files..."
echo "This will download ~10.5GB total"
echo "Downloads are resumable - you can Ctrl+C and restart!"
echo ""

# Download config files (small, fast)
echo "Downloading config files..."
wget -c "${BASE_URL}/config.json"
wget -c "${BASE_URL}/generation_config.json"
wget -c "${BASE_URL}/model.safetensors.index.json"
wget -c "${BASE_URL}/special_tokens_map.json"
wget -c "${BASE_URL}/tokenizer.json"
wget -c "${BASE_URL}/tokenizer_config.json"

# Download model weights (large, slow)
echo ""
echo "Downloading model weights (this will take a while)..."
echo "Part 1 of 3: 4.99GB"
wget -c "${BASE_URL}/model-00001-of-00003.safetensors"

echo "Part 2 of 3: 481MB"
wget -c "${BASE_URL}/model-00002-of-00003.safetensors"

echo "Part 3 of 3: 4.98GB"
wget -c "${BASE_URL}/model-00003-of-00003.safetensors"

echo ""
echo "✅ Download complete!"
echo "Model is now cached at: $MODEL_DIR"
echo ""
echo "You can now run:"
echo "uv run python japanese_story_gen.py vocab.txt --mode local --model rinna/gemma-2-baku-2b"
