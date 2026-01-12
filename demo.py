#!/usr/bin/env python3
"""
Simple demo to show parsed vocabulary from Anki export.
No dependencies required!
"""

import re
from typing import List, Tuple


def parse_anki_vocab(filepath: str) -> List[Tuple[str, str]]:
    """Extract vocabulary words (kanji, reading) from Anki export."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Pattern: word TAB "HTML content"
    pattern = r'^([^\t\n]+)\t"(.+?)"$'
    matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
    
    vocab_words = []
    for kanji, html in matches:
        # Extract reading - HTML has escaped quotes ("" not ")
        furigana_match = re.search(
            r'<div class=""furigana-text"">([^<]+)</div>',
            html
        )
        reading = furigana_match.group(1).strip() if furigana_match else ""
        vocab_words.append((kanji, reading))
    
    return vocab_words


def main():
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python demo.py <anki_file.txt>")
        sys.exit(1)
    
    filepath = sys.argv[1]
    vocab_words = parse_anki_vocab(filepath)
    
    print("="*60)
    print(f"Parsed {len(vocab_words)} Japanese vocabulary words")
    print("="*60)
    
    print("\nFirst 20 words:")
    for i, (kanji, reading) in enumerate(vocab_words[:20], 1):
        print(f"{i:2}. {kanji:10} ({reading})")
    
    if len(vocab_words) > 20:
        print(f"\n... and {len(vocab_words) - 20} more words")
    
    # Create formatted word list (as it would appear in LLM prompt)
    word_list = [kanji for kanji, reading in vocab_words]
    
    formatted = ", ".join(word_list)
    
    print("\n" + "="*60)
    print("Formatted for LLM prompt (words only, no readings):")
    print("="*60)
    print(formatted[:300] + "..." if len(formatted) > 300 else formatted)
    
    print("\n" + "="*60)
    print("Statistics:")
    print("-"*60)
    print(f"Total words: {len(vocab_words)}")
    print(f"Estimated prompt length: ~{len(formatted)} characters")
    print(f"Token savings vs including readings: ~{sum(len(reading) for _, reading in vocab_words) + len(vocab_words)*2} characters")
    print("="*60)


if __name__ == "__main__":
    main()
