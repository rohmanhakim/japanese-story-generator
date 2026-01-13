#!/usr/bin/env python3
"""
Japanese Story Generator - Simplified Version
Only extracts vocabulary words (kanji only).
The LLM already knows readings and meanings!
"""

import re
from typing import List


class AnkiVocabParser:
    """Parse Anki exported vocabulary - extract only the words."""
    
    def __init__(self, filepath: str):
        self.filepath = filepath
        
    def parse(self) -> List[str]:
        """
        Extract just the vocabulary words (kanji only).
        
        Returns:
            List of words (strings)
        """
        with open(self.filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern: word TAB "HTML content"
        pattern = r'^([^\t\n]+)\t"(.+?)"$'
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        
        vocab_words = []
        for kanji, html in matches:
            # Just append the word itself
            # We don't need readings - LLM already knows them!
            vocab_words.append(kanji)
        
        return vocab_words
    
    def format_for_prompt(self, vocab_words: List[str]) -> str:
        """Format vocabulary list for LLM prompt."""
        return ", ".join(vocab_words)


# Local LLM version
def generate_story_local(vocab_words: List[str], 
                        model_name: str = "rinna/japanese-gpt2-medium",
                        theme: str = None,
                        max_length: int = 800):
    """Generate story using local LLM (HuggingFace transformers)."""
    import torch
    from transformers import AutoTokenizer, AutoModelForCausalLM
    
    print(f"Loading model: {model_name}")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None
    )
    
    # Create word list
    parser = AnkiVocabParser("")
    word_list_str = parser.format_for_prompt(vocab_words)
    
    # Create prompt
    prompt = f"""以下の語彙を使って、{max_length}文字以内の短い物語を書いてください。

【語彙リスト】
{word_list_str}

【重要なルール】
1. リストの単語を主に使用してください
2. 動詞・形容詞の活用形は自由に使えます
   例：来る → 来ます、来た、来ない、来て、来られる
   例：寒い → 寒くない、寒かった、寒くて
3. 助詞（は、が、を、に、で、と、の、など）は使用できます
4. 自然で文法的に正しい物語を書いてください

"""
    
    if theme:
        prompt += f"【テーマ】{theme}\n\n"
    
    prompt += "【物語】\n"
    
    # Tokenize
    inputs = tokenizer(prompt, return_tensors="pt")
    
    if torch.cuda.is_available():
        inputs = inputs.to('cuda')
    
    with torch.no_grad():
        outputs = model.generate(
            inputs.input_ids,
            max_new_tokens=max_length,
            temperature=0.7,  # Slightly lower = more focused
            top_p=0.95,  # Slightly higher = more diversity
            top_k=50,
            do_sample=True,
            repetition_penalty=1.1,  # MILD penalty (1.2 was too strong!)
            no_repeat_ngram_size=2,  # Only block 2-word repetitions (not 3)
            pad_token_id=tokenizer.pad_token_id,
            eos_token_id=tokenizer.eos_token_id,
        )
    
    generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    story = generated_text[len(prompt):].strip()
    
    # Better truncation at sentence boundaries
    if len(story) > max_length:
        story = story[:max_length]
        # Try to end at a proper sentence boundary
        for delimiter in ['。', '！', '？', '」']:
            last_delim = story.rfind(delimiter)
            if last_delim > max_length * 0.8:  # At least 80% of target length
                story = story[:last_delim + 1]
                break
    
    return story


# Claude API version
def generate_story_claude(vocab_words: List[str],
                         api_key: str,
                         theme: str = None,
                         max_length: int = 800,
                         strict_vocab: bool = False):
    """Generate story using Claude API."""
    import anthropic
    from anthropic import APIError, APIConnectionError, RateLimitError, AuthenticationError
    
    try:
        client = anthropic.Anthropic(api_key=api_key)
        
        # Create word list
        parser = AnkiVocabParser("")
        word_list_str = parser.format_for_prompt(vocab_words)
        
        # Create prompt based on strictness
        if strict_vocab:
            # Strict mode: NO new words allowed
            constraints = f"""**STRICT CONSTRAINTS:**
1. Use ONLY words from this list: {word_list_str}
2. You may use basic particles (は、が、を、に、で、と、の、へ、から、など)
3. **IMPORTANT: You may conjugate verbs and adjectives freely:**
   - For verbs: All forms are allowed (ます形, て形, た形, ない形, etc.)
   - Example: 来る → 来ます、来た、来ない、来て、来られる、来よう
   - For い-adjectives: 寒い → 寒くない、寒かった、寒くて
   - For な-adjectives: 元気 → 元気な、元気で、元気だった
4. Do NOT introduce any new vocabulary words not in the list
5. Make the story natural and engaging"""
        else:
            # Flexible mode: Minimal new words allowed for natural flow
            constraints = f"""**CONSTRAINTS:**
1. PRIMARY vocabulary to use: {word_list_str}
2. You may use basic particles (は、が、を、に、で、と、の、へ、から、まで、より、など)
3. **IMPORTANT: You may conjugate verbs and adjectives freely:**
   - For verbs: All forms are allowed (ます形, て形, た形, ない形, 可能形, etc.)
   - Example: 来る → 来ます、来た、来ない、来て、来られる、来よう
   - For い-adjectives: 寒い → 寒くない、寒かった、寒くて
   - For な-adjectives: 元気 → 元気な、元気で、元気だった
4. You may use minimal additional common words (数, 時, 所, 事, 人, etc.) ONLY when absolutely necessary for natural flow
5. Aim to use 90%+ of words from the provided vocabulary list
6. Make the story natural, engaging, and grammatically correct

Focus on creating a natural story that teaches the vocabulary in context."""
        
        user_prompt = f"""Please write a short Japanese story (maximum {max_length} characters) using primarily the vocabulary words provided below.

{constraints}

"""
        
        if theme:
            user_prompt += f"**THEME:** {theme}\n\n"
        
        user_prompt += "Write the story in Japanese only (no English):"
        
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=2000,
            temperature=0.8,
            messages=[{"role": "user", "content": user_prompt}]
        )
        
        return message.content[0].text.strip()
        
    except AuthenticationError as e:
        raise Exception(f"Authentication failed - invalid API key: {e}")
    except RateLimitError as e:
        raise Exception(f"Rate limit exceeded: {e}")
    except APIError as e:
        # This catches the 400 error for insufficient credits
        if e.status_code == 400 or 'credit' in str(e).lower():
            raise Exception(f"Insufficient credits or billing issue: {e}")
        raise Exception(f"API error ({e.status_code}): {e}")
    except APIConnectionError as e:
        raise Exception(f"Connection error - check your internet: {e}")
    except Exception as e:
        raise Exception(f"Unexpected error: {e}")


def main():
    import argparse
    import os
    from pathlib import Path
    
    parser = argparse.ArgumentParser(
        description='Generate Japanese stories from Anki vocabulary'
    )
    parser.add_argument('anki_file', help='Anki export file (.txt)')
    parser.add_argument('--mode', choices=['local', 'claude'], default='claude',
                       help='Generation mode: local LLM or Claude API')
    parser.add_argument('--model', default='rinna/gemma-2-baku-2b',
                       help='Model name for local mode')
    parser.add_argument('--theme', help='Story theme (optional)')
    parser.add_argument('--api-key', help='Anthropic API key (for Claude mode)')
    parser.add_argument('--api-key-file', default='anthropic-api-key.txt',
                       help='File containing API key (default: anthropic-api-key.txt)')
    parser.add_argument('--strict-vocab', action='store_true',
                       help='Strict mode: Use ONLY provided vocabulary (no additional words)')
    parser.add_argument('--output', default='story.txt', help='Output file')
    parser.add_argument('--show-vocab', action='store_true',
                       help='Show vocabulary list')
    
    args = parser.parse_args()
    
    # Parse vocabulary
    print(f"Parsing: {args.anki_file}")
    vocab_parser = AnkiVocabParser(args.anki_file)
    vocab_words = vocab_parser.parse()
    print(f"Found {len(vocab_words)} words")
    
    if args.show_vocab:
        print("\nVocabulary:")
        for word in vocab_words[:20]:
            print(f"  {word}")
        if len(vocab_words) > 20:
            print(f"  ... and {len(vocab_words) - 20} more")
        print()
    
    # Generate story
    print("Generating story...")
    if args.theme:
        print(f"Theme: {args.theme}")
    
    if args.mode == 'claude':
        # Try to get API key from multiple sources (in order of priority):
        # 1. Command line argument --api-key
        # 2. Environment variable ANTHROPIC_API_KEY
        # 3. File (anthropic-api-key.txt by default)
        api_key = args.api_key or os.getenv('ANTHROPIC_API_KEY')
        
        if not api_key and args.api_key_file:
            # Try to read from file
            key_file = Path(args.api_key_file)
            if key_file.exists():
                try:
                    with open(key_file, 'r', encoding='utf-8') as f:
                        api_key = f.read().strip()
                    print(f"✓ Loaded API key from {args.api_key_file}")
                except Exception as e:
                    print(f"Warning: Could not read {args.api_key_file}: {e}")
        
        if not api_key:
            print("Error: API key required. Please either:")
            print("  1. Create a file 'anthropic-api-key.txt' with your API key")
            print("  2. Set ANTHROPIC_API_KEY environment variable")
            print("  3. Use --api-key argument")
            return 1
        
        try:
            story = generate_story_claude(
                vocab_words, 
                api_key, 
                theme=args.theme,
                strict_vocab=args.strict_vocab
            )
        except Exception as e:
            print(f"Error generating story: {e}")
            return 1
    else:
        story = generate_story_local(
            vocab_words,
            model_name=args.model,
            theme=args.theme
        )
    
    # Display and save
    print("\n" + "="*50)
    print(f"Story ({len(story)} characters):")
    print("="*50)
    print(story)
    print("="*50)
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(story)
    
    print(f"\nSaved to: {args.output}")
    
    return 0


if __name__ == '__main__':
    import sys
    sys.exit(main())
