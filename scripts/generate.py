#!/usr/bin/env python3
"""CLI for story generation."""

import argparse
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from japanese_story_generator import AnkiVocabParser, StoryGenerator, ConjugationVerifier
from openai import RateLimitError, NotFoundError, AuthenticationError, APIConnectionError


def main():
    parser = argparse.ArgumentParser(description="Generate Japanese stories")
    parser.add_argument("anki_file", help="Anki export file (.txt)")
    parser.add_argument("--theme", help="Story theme")
    parser.add_argument("--api-key", help="OpenRouter API key")
    parser.add_argument("--model", default="google/gemma-4-26b-a4b-it:free", help="OpenRouter model")
    parser.add_argument("--output", default="story.txt", help="Output file")
    parser.add_argument("--strict", action="store_true", help="Strict vocabulary mode")
    parser.add_argument("--max-length", type=int, default=500, help="Max story length")
    parser.add_argument("--verify", action="store_true", help="Verify conjugations")
    parser.add_argument("--show-vocab", action="store_true", help="Show vocabulary list")
    
    args = parser.parse_args()
    
    # Get API key
    api_key = args.api_key or os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: API key required. Use --api-key or set OPENROUTER_API_KEY")
        return 1
    
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
    
    generator = StoryGenerator(api_key, model=args.model)
    
    try:
        story = generator.generate(
            vocab_words,
            theme=args.theme,
            max_length=args.max_length,
            strict_vocab=args.strict
        )
    except RateLimitError:
        print(f"\n⚠️  Rate limit exceeded for model: {args.model}")
        print("\nFree models have strict rate limits. Try:")
        print("  1. Wait a few minutes and retry")
        print("  2. Use a different model: --model 'openai/gpt-4o-mini'")
        print("  3. Add your own API key: https://openrouter.ai/settings/integrations")
        return 1
    except NotFoundError:
        print(f"\n❌ Model not found: {args.model}")
        print("\nThe model may not exist or is not available for free.")
        print("Check available models at: https://openrouter.ai/models")
        return 1
    except AuthenticationError:
        print("\n❌ Invalid API key")
        print("\nCheck your OPENROUTER_API_KEY or use --api-key flag.")
        return 1
    except APIConnectionError:
        print("\n❌ Could not connect to OpenRouter")
        print("\nCheck your internet connection and try again.")
        return 1
    except Exception as e:
        error_str = str(e).lower()
        if "not a valid model" in error_str or "400" in error_str:
            print(f"\n❌ Invalid model: {args.model}")
            print("\nCheck available models at: https://openrouter.ai/models")
        elif "insufficient credits" in error_str or "billing" in error_str:
            print("\n❌ Insufficient credits")
            print("\nAdd credits at: https://openrouter.ai/credits")
        else:
            print(f"\n❌ Error: {e}")
        return 1
    
    # Display and save
    print(f"\n{'='*50}")
    print(f"Story ({len(story)} characters):")
    print(f"{'='*50}")
    print(story)
    print(f"{'='*50}")
    
    with open(args.output, 'w', encoding='utf-8') as f:
        f.write(story)
    
    print(f"\nSaved to: {args.output}")
    
    # Verify conjugations if requested
    if args.verify:
        print("\nVerifying conjugations...")
        verifier = ConjugationVerifier()
        result = verifier.verify(story, vocab_words)
        
        print(f"\nConjugations used: {len(result['conjugations'])}")
        for conj in result['conjugations'][:10]:
            print(f"  {conj['surface']} ({conj['base']})")
        
        print(f"\nViolations: {len(result['violations'])}")
        for v in result['violations'][:10]:
            print(f"  {v['surface']} ({v['suspected_base']})")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
