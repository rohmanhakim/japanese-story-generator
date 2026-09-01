# Vocabulary Constraint Modes

This project supports two modes for vocabulary constraints when generating stories.

---

## Strict Mode

Use ONLY the vocabulary words provided. No new words allowed.

### Usage
```bash
uv run jp-story vocab.txt --strict
```

### In Code
```python
generator = StoryGenerator(api_key)
story = generator.generate(
    vocab_words,
    strict_vocab=True  # Strict mode
)
```

### When to Use
- Beginner learners who need controlled vocabulary
- Drilling specific word sets
- Testing vocabulary mastery

### Trade-offs
- ✅ Guarantees only known words appear
- ✅ Good for learning reinforcement
- ⚠️ Stories may sound slightly unnatural
- ⚠️ Limited expressiveness

---

## Flexible Mode (Default)

Primarily uses provided vocabulary, but may add common words for natural flow.

### Usage
```bash
uv run jp-story vocab.txt
# or
uv run jp-story vocab.txt --no-strict
```

### In Code
```python
generator = StoryGenerator(api_key)
story = generator.generate(
    vocab_words,
    strict_vocab=False  # Flexible mode (default)
)
```

### When to Use
- Intermediate/advanced learners
- Reading practice with natural Japanese
- When story quality matters more than strict control

### Trade-offs
- ✅ More natural stories
- ✅ Better reading experience
- ⚠️ May contain some unknown words (~5-10%)

---

## Comparison

| Feature | Strict | Flexible |
|---------|--------|----------|
| New words allowed | ❌ No | ⚠️ Minimal |
| Story naturalness | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Vocabulary control | 100% | ~90-95% |
| Best for | Beginners | All levels |

---

## Examples

### Strict Mode Output
```text
Input vocabulary: 食べる, 飲む, 水, 学校, 先生

Output:
私は学校に行きます。先生が水を飲みます。
私はりんごを食べます。（りんご is NOT allowed - violation!）
```

### Flexible Mode Output
```text
Input vocabulary: 食べる, 飲む, 水, 学校, 先生

Output:
私は学校に行って、先生とお昼ご飯を食べました。
水を飲みながら、りんごも食べました。
（りんご is added for natural flow - acceptable）
```

---

## Controlling Vocabulary

### Add more words to Anki deck
The more words you have, the more natural strict mode stories become.

### Use themes
Guide story content to match your vocabulary:
```bash
uv run jp-story vocab.txt --strict --theme "at the restaurant"
```

### Adjust max length
Shorter stories are easier to constrain:
```bash
uv run jp-story vocab.txt --strict --max-length 200
```

---

## Vocabulary Violations

When using `--verify`, the tool shows vocabulary violations:

```
Violations: 5
  部屋 (ホウヤ)    # Word not in vocabulary
  本棚 (ホンダナ)  # Word not in vocabulary
  ...
```

Use this to understand how well the model adhered to your vocabulary list.

---

## Tips

1. **Start with flexible mode** to see natural stories
2. **Switch to strict mode** for vocabulary drilling
3. **Build vocabulary gradually** - larger word lists = better strict stories
4. **Use verification** to check adherence
5. **Combine with themes** to focus on specific vocabulary areas
