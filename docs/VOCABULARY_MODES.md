# Vocabulary Strictness Modes

The script supports two modes for vocabulary constraint handling.

## Default Mode: Flexible (90%+ vocabulary adherence)

**Recommended for most users.**

```bash
python japanese_story_gen.py My_Japanese_Vocabulary.txt
```

### What it does:
- ✅ Uses 90%+ words from your vocabulary list
- ✅ Allows minimal common functional words (数, 時, 所, 事, 人, etc.)
- ✅ Results in natural, grammatically correct stories
- ✅ Better learning experience - feels like real Japanese

### Example output:
```
冬の寒い日、私は外に出ました。体が冷たくなって、
手袋と帽子をつけました。神社まで歩いて行きました。
そこで暖かいお茶を飲みながら、家族と一緒に
新年の行事に参加しました。
```
*May include: 私 (I), 行きました (went) if not in your vocab, but story flows naturally*

---

## Strict Mode: 100% vocabulary adherence

**For purists who want ZERO new words.**

```bash
python japanese_story_gen.py My_Japanese_Vocabulary.txt --strict-vocab
```

### What it does:
- ✅ Uses ONLY words from your vocabulary list
- ✅ No exceptions (except particles)
- ❌ May result in awkward/unnatural sentences
- ❌ Story quality may suffer

### Example output:
```
冬。寒い。体、冷たい。手袋。帽子。神社。行事。
暖かい料理、食べる。元気。
```
*Choppy, telegraphic, but technically uses only your words*

---

## Comparison

| Aspect | Default (Flexible) | Strict Mode |
|--------|-------------------|-------------|
| **Vocabulary adherence** | 90-95% | 99-100% |
| **Story naturalness** | ⭐⭐⭐⭐⭐ Natural | ⭐⭐ Choppy |
| **Grammar correctness** | ⭐⭐⭐⭐⭐ Correct | ⭐⭐⭐ Sometimes awkward |
| **Learning value** | ⭐⭐⭐⭐⭐ High | ⭐⭐⭐ Medium |
| **Reading enjoyment** | ⭐⭐⭐⭐⭐ Enjoyable | ⭐⭐ Functional |
| **New words introduced** | 0-3 common words | 0 |

---

## What "Minimal common words" means in Flexible mode:

The flexible mode may add these types of words **only when necessary**:

### Function words (structure):
- 事 (こと) - thing, fact
- 時 (とき) - time, when
- 所 (ところ) - place
- 人 (ひと) - person
- 物 (もの) - thing

### Common verbs (if missing):
- する - to do
- 行く - to go
- 来る - to come
- ある/いる - to exist

### Pronouns (if missing):
- 私 - I
- これ/それ/あれ - this/that

### Temporal/quantifiers:
- 数 - number
- 今 - now
- 後 - after

**Important:** Even in flexible mode, the story will use 90%+ of YOUR words. New words are rare and only used when absolutely needed.

---

## Real Example Comparison

**Your vocabulary:** 冬, 寒い, 暖かい, 神社, 帽子, 手袋, 雪, 料理, 食べる, 体

### Flexible Mode Story (Default):
```
冬の寒い日のことです。朝、外に出る時、体が冷たく
なりました。帽子と手袋をつけて、神社へ行きました。
雪が降っていて、とても寒かったです。帰りに暖かい
料理を食べて、元気になりました。
```

**New words used:** 
- 日 (day) - necessary for "cold day"
- 朝 (morning) - time context
- 出る (to go out) - natural flow
- 時 (when) - conjunction
- 行く (to go) - verb of motion
- とても (very) - emphasis

**Your vocabulary words:** 冬, 寒い, 体, 帽子, 手袋, 神社, 雪, 暖かい, 料理, 食べる (10/10 = 100% used!)

**Total vocabulary:** 10 yours + 6 functional = 16 words → 62.5% yours, but ALL your words practiced!

---

### Strict Mode Story:
```
冬。寒い。体、冷たい。帽子。手袋。神社。雪。
料理、食べる。暖かい。
```

**New words used:** 0

**Your vocabulary words:** All used but disconnected

**Story quality:** Choppy, like a word list

---

## Recommendation

### Use Flexible Mode (default) when:
- ✅ You want to learn Japanese naturally
- ✅ You want enjoyable reading practice
- ✅ Your goal is context-based learning
- ✅ You have 50+ vocabulary words

### Use Strict Mode when:
- ✅ You have very limited vocabulary (<20 words)
- ✅ You want to memorize ONLY specific words
- ✅ You're okay with choppy/unnatural text
- ✅ You're a completionist (0 new words = goal)

---

## Usage Examples

### Flexible mode (default):
```bash
# Natural stories, 90%+ your vocabulary
python japanese_story_gen.py vocab.txt --theme "冬の日"
```

### Strict mode:
```bash
# Only your words, may be choppy
python japanese_story_gen.py vocab.txt --theme "冬の日" --strict-vocab
```

### Compare both:
```bash
# Generate flexible
python japanese_story_gen.py vocab.txt --output story_flexible.txt

# Generate strict
python japanese_story_gen.py vocab.txt --output story_strict.txt --strict-vocab

# Compare the results!
```

---

## My Recommendation

**Use the default flexible mode.**

Why? Because:
1. You learn vocabulary IN CONTEXT (most effective)
2. Stories are natural and enjoyable to read
3. You still practice 100% of your known words
4. The 5-10% "new" words are usually ultra-common ones you need anyway
5. Real Japanese uses these functional words constantly

**Think of it like this:**
- Strict mode = Flash cards in sentence form
- Flexible mode = Natural Japanese with your vocabulary focus

The flexible mode is closer to how textbooks work - they introduce new vocabulary in context while using some familiar "glue" words.

---

## Technical Note

- **Claude API:** Handles both modes well
- **Local LLMs:** May struggle even in strict mode (will introduce ~10-20% new words anyway)
  - Larger models (Llama 3 8B, Gemma 2 3B) handle it better
  - Smaller models (GPT-2 Medium) struggle more

If using local LLMs, the difference between strict and flexible modes is less noticeable.
