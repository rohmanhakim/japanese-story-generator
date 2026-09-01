#!/usr/bin/env python3
"""
Experiment: Analyze vocabulary violations when generating stories.
Tests how vocabulary size affects story coherence and violations.
"""

import os
import sys
import json
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from japanese_story_generator import AnkiVocabParser, StoryGenerator, ConjugationVerifier


def clean_vocab(word: str) -> str:
    """Clean HTML entities from vocabulary."""
    return word.replace('&nbsp;', '').strip()


def run_experiment(vocab_file: str, output_dir: str = None):
    """Run vocabulary violation experiment."""
    
    # Parse vocabulary
    parser = AnkiVocabParser(vocab_file)
    raw_vocab = parser.parse()
    vocab = [clean_vocab(w) for w in raw_vocab]
    
    print(f"Total vocabulary: {len(vocab)} words")
    print(f"Sample: {vocab[:10]}")
    print()
    
    # Get API key
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        print("Error: Set OPENROUTER_API_KEY environment variable")
        return
    
    # Initialize
    generator = StoryGenerator(api_key=api_key)
    verifier = ConjugationVerifier()
    
    # Test with different vocabulary sizes
    test_sizes = [10, 20, 30, 50, 74]  # Test with these sizes
    
    results = []
    
    for size in test_sizes:
        if size > len(vocab):
            continue
            
        test_vocab = vocab[:size]
        print(f"\n{'='*60}")
        print(f"Testing with {size} words: {test_vocab[:5]}...")
        print(f"{'='*60}")
        
        try:
            # Generate story with strict vocab
            story = generator.generate(
                vocab_words=test_vocab,
                theme="daily life",
                max_length=300,
                strict_vocab=True
            )
            
            print(f"\nGenerated Story ({len(story)} chars):")
            print("-" * 40)
            print(story)
            print("-" * 40)
            
            # Verify vocabulary usage
            verification = verifier.verify(story, test_vocab)
            
            # Analyze violations
            violations = verification.get("violations", [])
            matched = verification.get("conjugations", [])
            compounds = verification.get("compounds", [])
            
            print(f"\nVerification Results:")
            print(f"  Matched words: {len(matched)}")
            print(f"  Compounds found: {len(compounds)}")
            print(f"  Violations: {len(violations)}")
            
            if violations:
                print(f"\n  Violation words:")
                for v in violations[:10]:  # Show first 10
                    print(f"    - {v}")
                if len(violations) > 10:
                    print(f"    ... and {len(violations) - 10} more")
            
            result = {
                "vocab_size": size,
                "story_length": len(story),
                "matched_count": len(matched),
                "compound_count": len(compounds),
                "violation_count": len(violations),
                "violations": violations,
                "story_preview": story[:200]
            }
            results.append(result)
            
        except Exception as e:
            print(f"Error: {e}")
            results.append({
                "vocab_size": size,
                "error": str(e)
            })
    
    # Save results
    if output_dir:
        output_path = Path(output_dir) / "experiment_results.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(results, f, ensure_ascii=False, indent=2)
        print(f"\nResults saved to: {output_path}")
    
    # Summary
    print(f"\n{'='*60}")
    print("EXPERIMENT SUMMARY")
    print(f"{'='*60}")
    print(f"{'Vocab Size':<12} {'Story Len':<12} {'Matched':<10} {'Violations':<12} {'Violation %':<12}")
    print("-" * 60)
    
    for r in results:
        if "error" in r:
            print(f"{r['vocab_size']:<12} ERROR: {r['error'][:30]}")
        else:
            violation_pct = (r['violation_count'] / (r['matched_count'] + r['violation_count']) * 100) if (r['matched_count'] + r['violation_count']) > 0 else 0
            print(f"{r['vocab_size']:<12} {r['story_length']:<12} {r['matched_count']:<10} {r['violation_count']:<12} {violation_pct:.1f}%")
    
    return results


if __name__ == "__main__":
    vocab_file = "/home/arif/my-japanese-vocabulary-test.txt"
    output_dir = "/home/arif/Projects/japanese-story-generator/experiments"
    
    run_experiment(vocab_file, output_dir)
