# Japanese Verb Conjugations in Vocabulary-Constrained Generation

## The Problem

**Your Anki deck has:** 来る (kuru - to come)  
**Story needs:** 来ます, 来た, 来ない, 来て, 来られる, 来よう, etc.

**Question:** How to make the AI understand that conjugations are allowed?

---

## Solution Overview

There are **4 main approaches**, ranging from easiest to most complex:

| Approach | Difficulty | Effectiveness | Best For |
|----------|-----------|---------------|----------|
| **1. Explicit prompting** | ⭐ Easy | ⭐⭐⭐⭐⭐ High | All users |
| **2. Example-based** | ⭐⭐ Medium | ⭐⭐⭐⭐ Good | Claude API |
| **3. Expand vocabulary** | ⭐⭐⭐ Hard | ⭐⭐⭐ Medium | Large decks |
| **4. Programmatic expansion** | ⭐⭐⭐⭐ Very Hard | ⭐⭐⭐⭐⭐ Perfect | Advanced users |

---

## Solution 1: Explicit Prompting - RECOMMENDED

### What It Is:
Tell the AI explicitly that conjugations are allowed.

### Implementation:

**Updated prompt (already applied to the script):**

```
【重要なルール】
1. リストの単語を主に使用してください
2. 動詞・形容詞の活用形は自由に使えます
   例：来る → 来ます、来た、来ない、来て、来られる
   例：寒い → 寒くない、寒かった、寒くて
3. 助詞（は、が、を、に、で、と、の、など）は使用できます
4. 自然で文法的に正しい物語を書いてください
```

**English version (for Claude API):**

```
**IMPORTANT: You may conjugate verbs and adjectives freely:**
- For verbs: All forms are allowed (ます形, て形, た形, ない形, etc.)
- Example: 来る → 来ます、来た、来ない、来て、来られる、来よう
- For い-adjectives: 寒い → 寒くない、寒かった、寒くて
- For な-adjectives: 元気 → 元気な、元気で、元気だった
```

### Pros:
- ✅ Very easy to implement
- ✅ Works immediately
- ✅ No changes to vocabulary needed
- ✅ Model understands intent clearly

### Cons:
- ⚠️ Relies on model understanding instructions
- ⚠️ Weaker models may still struggle

### Test It:

```bash
# Your updated script already has this!
uv run python japanese_story_gen.py My_Japanese_Vocabulary2.txt

# The AI should now freely use:
# 来る → 来ます、来た、来ている、来られる
# 行く → 行きます、行った、行こう
# 食べる → 食べます、食べた、食べて
```

---

## Solution 2: Example-Based Prompting

### What It Is:
Show the AI examples of conjugations in the prompt.

### Implementation:

**Add to your prompt:**

```python
# After vocabulary list, add examples:
prompt += """
【活用の例】
来る：来ます、来た、来て、来ない、来られる
行く：行きます、行った、行って、行かない
食べる：食べます、食べた、食べて、食べない
寒い：寒い、寒くない、寒かった、寒くて
元気：元気、元気な、元気だった、元気で
"""
```

### Pros:
- ✅ Very clear to the model
- ✅ Works well with Claude API
- ✅ Shows exactly what's allowed

### Cons:
- ⚠️ Makes prompt longer
- ⚠️ Tedious to list all conjugations
- ⚠️ Only practical for small vocabularies

### When to Use:
- Small vocabulary (<50 words)
- Using Claude API (good at following examples)
- Want maximum clarity

---

## Solution 3: Expand Vocabulary with Common Forms

### What It Is:
Add common conjugated forms to your Anki deck.

### Implementation:

**Manually add entries:**

```
Original deck:
来る(くる)

Expanded deck:
来る(くる)
来ます(きます)
来た(きた)
来て(きて)
```

### How to Bulk Add in Anki:

**Step 1: Export your deck**
```
Anki → File → Export → Notes in Plain Text (.txt)
```

**Step 2: Create conjugations**

Use a script or manually add:

```python
# Quick Python script
base_verbs = ["来る", "行く", "食べる", "見る", "聞く"]

conjugations = {
    "来る": ["来ます", "来た", "来て", "来ない"],
    "行く": ["行きます", "行った", "行って", "行かない"],
    "食べる": ["食べます", "食べた", "食べて", "食べない"],
    # ... etc
}

# Generate Anki import format
for verb, forms in conjugations.items():
    for form in forms:
        print(f"{form}\t{verb}の活用形")
```

**Step 3: Import back to Anki**
```
Anki → File → Import → Select .txt file
```

### Pros:
- ✅ Guarantees conjugations are available
- ✅ Explicit in vocabulary list
- ✅ Works with any model

### Cons:
- ❌ Very tedious (hundreds of forms!)
- ❌ Vocabulary list becomes huge
- ❌ Maintenance nightmare
- ❌ Not practical for >20 verbs

### When to Use:
- Small vocabulary (<30 verbs)
- Want absolute control
- Have time to maintain

**Verdict: NOT RECOMMENDED for most users**

---

## Solution 4: Programmatic Vocabulary Expansion - ADVANCED

### What It Is:
Automatically generate conjugations when creating the prompt.

### Implementation:

**Add a conjugation module:**

```python
class JapaneseConjugator:
    """Generate common conjugations for Japanese verbs/adjectives."""
    
    def __init__(self):
        # Verb patterns
        self.verb_patterns = {
            # Godan verbs (う verbs)
            'う': ['います', 'いた', 'いて', 'わない'],
            'く': ['きます', 'いた', 'いて', 'かない'],
            'ぐ': ['ぎます', 'いだ', 'いで', 'がない'],
            'す': ['します', 'した', 'して', 'さない'],
            'つ': ['ちます', 'った', 'って', 'たない'],
            'ぬ': ['にます', 'んだ', 'んで', 'なない'],
            'ぶ': ['びます', 'んだ', 'んで', 'ばない'],
            'む': ['みます', 'んだ', 'んで', 'まない'],
            'る': ['ります', 'った', 'って', 'らない'],
            
            # Ichidan verbs (る verbs)
            'ichidan': ['ます', 'た', 'て', 'ない', 'られる'],
            
            # Irregular
            'する': ['します', 'した', 'して', 'しない', 'できる'],
            '来る': ['来ます', '来た', '来て', '来ない', '来られる'],
        }
    
    def conjugate_verb(self, verb: str) -> List[str]:
        """Generate common conjugations for a verb."""
        if verb == 'する':
            return ['します', 'した', 'して', 'しない', 'できる']
        elif verb == '来る':
            return ['来ます', '来た', '来て', '来ない', '来られる']
        elif verb.endswith('る') and len(verb) > 2:
            # Likely ichidan (need proper detection logic)
            stem = verb[:-1]
            return [stem + form for form in ['ます', 'た', 'て', 'ない', 'られる']]
        else:
            # Godan verb detection (simplified)
            last_char = verb[-1]
            if last_char in self.verb_patterns:
                stem = verb[:-1]
                return [stem + form for form in self.verb_patterns[last_char]]
        
        return []
    
    def conjugate_i_adjective(self, adj: str) -> List[str]:
        """Generate conjugations for い-adjective."""
        if not adj.endswith('い'):
            return []
        
        stem = adj[:-1]
        return [
            adj,                    # 寒い
            stem + 'くない',         # 寒くない
            stem + 'かった',         # 寒かった
            stem + 'くて',           # 寒くて
            stem + 'ければ',         # 寒ければ
        ]
    
    def conjugate_na_adjective(self, adj: str) -> List[str]:
        """Generate conjugations for な-adjective."""
        return [
            adj,            # 元気
            adj + 'な',     # 元気な
            adj + 'だ',     # 元気だ
            adj + 'で',     # 元気で
            adj + 'だった', # 元気だった
        ]

# Usage in your script:
def expand_vocabulary(vocab_words: List[Tuple[str, str]]) -> List[str]:
    """Expand vocabulary with conjugations."""
    conjugator = JapaneseConjugator()
    expanded = []
    
    for word, reading in vocab_words:
        expanded.append(word)
        
        # Detect and conjugate
        if word.endswith('る') or word in ['する', '来る']:
            # Likely verb
            conjugations = conjugator.conjugate_verb(word)
            expanded.extend(conjugations)
        elif word.endswith('い'):
            # Likely い-adjective
            conjugations = conjugator.conjugate_i_adjective(word)
            expanded.extend(conjugations)
        # Add more detection logic for な-adjectives, etc.
    
    return expanded
```

### Pros:
- ✅ Automatic - no manual work
- ✅ Always up-to-date
- ✅ Comprehensive coverage
- ✅ Maintainable

### Cons:
- ❌ Complex to implement correctly
- ❌ Japanese conjugation rules are intricate
- ❌ Ichidan vs Godan detection is hard
- ❌ False positives (見る vs 見ます、見た is easy, but 食べる requires stem detection)

### When to Use:
- Large vocabulary (100+ verbs)
- Programming expertise
- Want automated solution
- Can handle false positives

### Better Approach:
Use an existing Japanese NLP library!

**Option A: Use sudachipy**
```bash
pip install sudachipy

# In your script:
from sudachipy import tokenizer, dictionary

tokenizer_obj = dictionary.Dictionary().create()
mode = tokenizer.Tokenizer.SplitMode.C

# Analyze words
tokens = tokenizer_obj.tokenize("食べる", mode)
for token in tokens:
    # Get normalized form, conjugations, etc.
    print(token.dictionary_form())
```

**Option B: Use spaCy with Japanese support**
```bash
pip install spacy[ja]
python -m spacy download ja_core_news_sm

# In your script:
import spacy
nlp = spacy.load("ja_core_news_sm")

doc = nlp("食べる")
for token in doc:
    print(token.lemma_)  # Base form
```

**Option C: Use JapaneseTokenizer library**
```bash
pip install JapaneseTokenizer

# Already handles conjugations
```

---

## Comparison Table

| Solution | Setup Time | Maintenance | Accuracy | Scalability |
|----------|-----------|-------------|----------|-------------|
| **1. Explicit prompting** | 5 min | None | 90% | ✅ Great |
| **2. Example-based** | 30 min | Low | 95% | ⚠️ OK for small vocab |
| **3. Manual expansion** | Hours | High | 100% | ❌ Poor |
| **4. Programmatic** | Days | Low | 85-95% | ✅ Excellent |

---

## Recommended Approach by Use Case

### For Most Users:
**Use Solution 1: Explicit Prompting** ✅

Your updated script already has this. Just run:

```bash
uv run python japanese_story_gen.py My_Japanese_Vocabulary.txt
```

The AI should now understand:
- 来る can be conjugated to 来ます, 来た, 来て, etc.
- 寒い can be conjugated to 寒くない, 寒かった, etc.

### For Small Vocabulary (<50 words):
**Combine Solutions 1 + 2**

Add explicit examples in prompt:
```python
prompt += """
【活用の例】
来る：来ます、来た、来て
行く：行きます、行った、行って
寒い：寒い、寒くない、寒かった
"""
```

### For Large Vocabulary (300+ words):
**Use Solution 4: Programmatic**

Implement with sudachipy or spaCy for automatic conjugation generation.

---

## Testing Your Updated Script

### Test 1: Verify conjugations are used

```bash
uv run python japanese_story_gen.py My_Japanese_Vocabulary2.txt \
  --output test_conjugations.txt
```

**Look for:**
- ✅ 来る → 来ます, 来た, 来て
- ✅ 行く → 行きます, 行った, 行こう
- ✅ 食べる → 食べます, 食べた, 食べて
- ✅ 寒い → 寒くない, 寒かった

### Test 2: Compare with strict mode

```bash
# Flexible mode (default) - should use conjugations freely
uv run python japanese_story_gen.py vocab.txt \
  --output test_flexible.txt

# Strict mode - still allows conjugations
uv run python japanese_story_gen.py vocab.txt \
  --strict-vocab \
  --output test_strict.txt
```

Both should now use conjugations properly!

---

## Common Issues & Solutions

### Issue 1: Model still not using conjugations

**Problem:** AI uses only dictionary forms

**Solution:**
```python
# Make the instruction even more explicit:
prompt = """
重要：動詞や形容詞は必ず活用形を使ってください！
辞書形だけでなく、ます形、た形、て形などを自由に使用してください。

例：
❌ 私は昨日学校に行く。
✅ 私は昨日学校に行きました。

❌ 今日は寒い。昨日も寒い。
✅ 今日は寒い。昨日も寒かった。
"""
```

### Issue 2: Wrong conjugations

**Problem:** 来た (kita) vs 北 (kita - north) confusion

**Solution:** Use readings in prompt
```python
# Instead of: 来る
# Use: 来る(くる) with reading to disambiguate
```

### Issue 3: Over-conjugation

**Problem:** Model creates non-existent forms

**Example:**
- ❌ 来るます (double conjugation)
- ❌ 食べるた (wrong stem)

**Solution:** Add negative examples
```python
prompt += """
【禁止事項】
❌ 来るます（誤）→ ✅ 来ます（正）
❌ 食べるた（誤）→ ✅ 食べた（正）
"""
```

---

## Advanced: Conjugation Verification

Want to verify if the AI used correct conjugations? Add post-processing:

```python
def verify_conjugations(story: str, vocab: List[str]) -> dict:
    """Check if conjugations in story are valid."""
    import MeCab
    
    mecab = MeCab.Tagger()
    parsed = mecab.parse(story)
    
    violations = []
    conjugations_used = []
    
    for line in parsed.split('\n'):
        if line == 'EOS' or not line:
            continue
        
        parts = line.split('\t')
        surface = parts[0]  # The word as written
        features = parts[1].split(',')
        base_form = features[6]  # Dictionary form
        
        if base_form in vocab:
            conjugations_used.append({
                'surface': surface,
                'base': base_form,
                'valid': True
            })
        elif surface not in vocab and base_form not in vocab:
            violations.append({
                'surface': surface,
                'suspected_base': base_form
            })
    
    return {
        'conjugations': conjugations_used,
        'violations': violations
    }
```

---

## Summary

### ✅ What You Should Do NOW:

**Your script is already updated!** Just run it:

```bash
uv run python japanese_story_gen.py My_Japanese_Vocabulary.txt
```

The explicit conjugation instructions have been added to both:
- Local model prompt (Japanese instructions)
- Claude API prompt (English instructions)

### Expected Behavior:

**Your 147-word vocabulary includes:**
- 来る, 行く, 見る, 聞く, 話す, 食べる, 飲む, 買う...

**AI can now use:**
- 来る → 来ます, 来た, 来て, 来ない, 来られる
- 行く → 行きます, 行った, 行って, 行こう
- 食べる → 食べます, 食べた, 食べて, 食べない

All without adding hundreds of conjugation entries to your Anki deck.

### If Issues Persist:

1. Try Solution 2 (add examples)
2. Test with Claude API (better instruction following)
3. Consider Solution 4 for 300+ word vocabularies

---

## Quick Reference Card

**Problem:** AI doesn't know 来ます is OK when deck has 来る

**Quick Fix:** ✅ Already applied to your script!

**Test Command:**
```bash
uv run python japanese_story_gen.py My_Japanese_Vocabulary2.txt
```

**Expected:** Story uses 来ます, 来た, 来て freely ✅

**If not working:** Add explicit examples (Solution 2)

**Long-term:** Implement programmatic expansion (Solution 4) for 300+ words
