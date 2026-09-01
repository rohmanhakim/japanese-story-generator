# Conjugation Handling Guide

This guide explains how the system handles Japanese verb and adjective conjugations.

---

## Overview

Japanese words can appear in many conjugated forms:
- **Verbs:** 食べる → 食べます, 食べた, 食べない, 食べて
- **Adjectives:** 寒い → 寒くない, 寒かった, 寒くて

The system understands these are the same word, just conjugated differently.

---

## Conjugation Verification

The `ConjugationVerifier` class analyzes Japanese text to:
1. Identify conjugated forms
2. Match them to base dictionary forms
3. Report vocabulary violations

### Basic Usage

```python
from japanese_story_generator import ConjugationVerifier

verifier = ConjugationVerifier()
result = verifier.verify(story_text, vocabulary_list)

print(result["conjugations"])  # Words found
print(result["violations"])    # Words not in vocabulary
```

### CLI Usage

```bash
uv run jp-story vocab.txt --verify
```

Output:
```
Conjugations used: 15
  食べます (食べる)
  食べた (食べる)
  飲みました (飲む)
  ...

Violations: 3
  部屋 (ホウヤ)
  本棚 (ホンダナ)
  ...
```

---

## How It Works

### 1. Morphological Analysis

Uses MeCab with UniDic to parse Japanese text:

```
私は学校に行きます
↓
[私] [は] [学校] [に] [行き] [ます]
```

### 2. Conjugation Detection

Identifies conjugation type and form:

| Field | Description | Example |
|-------|-------------|---------|
| surface | Actual form | 食べます |
| base | Dictionary form | 食べる |
| conjugation_type | Verb class | 一段 |
| conjugation_form | Conjugation | 連用形 |

### 3. Vocabulary Matching

Compares base forms against your vocabulary list:

```
食べる (in vocabulary) ✓
部屋 (not in vocabulary) ✗
```

---

## Supported Conjugations

### Verbs

| Form | Example | Detected |
|------|---------|----------|
| ます形 | 食べます | ✓ |
| て形 | 食べて | ✓ |
| た形 | 食べた | ✓ |
| ない形 | 食べない | ✓ |
| 可能形 | 食べられる | ✓ |
| 受身形 | 食べられる | ✓ |
| 使役形 | 食べさせる | ✓ |
| 意志形 | 食べよう | ✓ |
| 条件形 | 食べれば | ✓ |
| 命令形 | 食べろ | ✓ |

### い-Adjectives

| Form | Example | Detected |
|------|---------|----------|
| くない形 | 寒くない | ✓ |
| かった形 | 寒かった | ✓ |
| くて形 | 寒くて | ✓ |
| なら形 | 寒ければ | ✓ |

### な-Adjectives

| Form | Example | Detected |
|------|---------|----------|
| な形 | 元気な | ✓ |
| で形 | 元気で | ✓ |
| だった形 | 元気だった | ✓ |

---

## Strict vs Flexible Mode

### Strict Mode
- Only uses words from your vocabulary list
- All conjugations must be of listed words
- Any new word is a violation

### Flexible Mode (Default)
- Primarily uses your vocabulary
- May add minimal common words
- Violations are words completely outside your list

---

## Common Issues

### Issue: "0 conjugations found"

**Cause:** Vocabulary list may not match story words.

**Solution:** Check that vocabulary words are in dictionary form:
```
✓ 食べる
✗ 食べます (conjugated form)
```

### Issue: Many violations

**Cause:** Story contains many words not in vocabulary.

**Solutions:**
1. Add more words to vocabulary list
2. Use `--strict` mode
3. Use shorter stories (`--max-length 200`)

---

## MeCab Setup

The system uses MeCab for morphological analysis.

### Installation

Already included in dependencies:
```bash
uv sync  # Installs mecab-python3 and unidic-lite
```

### Manual Setup (if needed)

```bash
uv pip install mecab-python3 unidic-lite
```

---

## Example Analysis

### Input
```python
story = "昨日、私は学校で友達と日本語を勉強しました。"
vocab = ["昨日", "学校", "友達", "日本語", "勉強する"]
```

### Output
```python
{
    "conjugations": [
        {"surface": "勉強しました", "base": "勉強する", "form": "連用形+ます形"},
    ],
    "violations": [
        {"surface": "私", "pos": "代名詞"},
        {"surface": "日本語", "pos": "名詞"},
    ]
}
```

---

## Tips

1. **Use dictionary forms** in vocabulary list
2. **Add common words** to reduce violations
3. **Check verification output** to understand story quality
4. **Use themes** to guide vocabulary usage

---

## See Also

- [VOCABULARY_MODES.md](VOCABULARY_MODES.md) - Strict vs flexible constraints
- [SETUP_GUIDE.md](SETUP_GUIDE.md) - Installation and usage
