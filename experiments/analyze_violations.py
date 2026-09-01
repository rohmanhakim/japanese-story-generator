#!/usr/bin/env python3
"""
Analyze true violations vs false positives in story generation.
"""

import json
from pathlib import Path


# Load experiment results
results_path = Path("/home/arif/Projects/japanese-story-generator/experiments/experiment_results.json")
with open(results_path, 'r', encoding='utf-8') as f:
    results = json.load(f)

# Known vocabulary (from the test file)
known_vocab = {
    '暖かい', '寒い', '体', '喉', '帽子', '薬局', '混ぜる', '薄い', '塩', '鍋料理',
    '置く', '買う', '椅子', '机', '家族', '寿司', '病気', '降る', '薬', '持つ',
    '寝る', '寂しい', '仕事', '切る', '駅', '夜', '青い', '黒い', '黄色', '簡単',
    '楽しい', '屋', '玉ねぎ', '新しい', '外', '人', '彼', '彼女', '友達', '学生',
    '会社', '今日', '昨日', '月', '今', '午後', '来る', '聞く', '食べる', '使う',
    '小さい', '良い', '高い', '多い', '上', '中', '後ろ', '右', '近い', '家',
    '車', '水', '木', '川', '雨', '魚', '野菜', '米', '昼', '暇', '嫌い',
    '思う', '住む', 'お願い'
}

# Also include compound word parts
vocab_parts = set()
for word in known_vocab:
    # Add individual characters for compound words
    for char in word:
        if len(char) == 1:
            vocab_parts.add(char)

print(f"Known vocabulary: {len(known_vocab)} words")
print()

# Analyze each experiment
for r in results:
    if 'error' in r:
        continue
    
    print(f"\n{'='*60}")
    print(f"Vocab Size: {r['vocab_size']}")
    print(f"{'='*60}")
    
    # Parse violations
    violations = r.get('violations', [])
    
    # Categorize violations
    true_violations = []
    false_positives = []
    
    for v in violations:
        surface = v.get('surface', '')
        suspected_base = v.get('suspected_base', '')
        
        # Check if it's in our vocabulary (either surface or base form)
        if surface in known_vocab or suspected_base in known_vocab:
            false_positives.append(v)
        # Check if it's a part of a compound word
        elif any(surface in word or word in surface for word in known_vocab):
            false_positives.append(v)
        else:
            true_violations.append(v)
    
    print(f"\nViolations breakdown:")
    print(f"  Total violations reported: {len(violations)}")
    print(f"  False positives (in vocab but different form): {len(false_positives)}")
    print(f"  TRUE violations (not in vocab): {len(true_violations)}")
    
    if true_violations:
        print(f"\n  TRUE violations to learn:")
        seen = set()
        for v in true_violations:
            surface = v.get('surface', '')
            if surface not in seen:
                print(f"    - {surface} ({v.get('pos', '?')})")
                seen.add(surface)
    
    if false_positives:
        print(f"\n  False positives (verification issue):")
        seen = set()
        for v in false_positives:
            surface = v.get('surface', '')
            if surface not in seen:
                print(f"    - {surface} -> {v.get('suspected_base', '?')}")
                seen.add(surface)
