"""Conjugation verification using fugashi (MeCab wrapper)."""

from typing import List, Dict
import fugashi


class ConjugationVerifier:
    """Verify conjugations and vocabulary usage in Japanese text."""
    
    def __init__(self):
        """Initialize fugashi tagger."""
        self.tagger = fugashi.Tagger()
    
    def verify(self, story: str, vocab: List[str]) -> Dict:
        """
        Verify conjugations used and vocabulary violations.
        
        Args:
            story: Japanese text to analyze
            vocab: List of vocabulary words (dictionary forms)
            
        Returns:
            Dict with 'conjugations' and 'violations'
        """
        vocab_set = set(vocab)
        conjugations_used = []
        violations = []
        
        words = self.tagger(story)
        
        for word in words:
            surface = word.surface
            if not surface.strip():
                continue
            
            f = word.feature
            pos1 = f.pos1
            lemma = f.lemma
            cType = f.cType  # Conjugation type (e.g., "五段-カ行")
            cForm = f.cForm  # Conjugation form (e.g., "連用形-一般")
            
            # Skip non-lexical tokens
            if pos1 in {"助詞", "助動詞", "記号", "補助記号"}:
                continue
            
            # Extract base lemma (remove POS suffix like "行く-動詞" → "行く")
            lemma_base = lemma.split("-")[0] if "-" in lemma else lemma
            
            # Check if this word (or its base form) is in vocabulary
            # Handle サ変 verbs: 勉強 (noun) + する → match 勉強する in vocab
            suru_form = lemma_base + "する" if pos1 == "名詞" else None
            
            if (lemma_base in vocab_set or 
                lemma in vocab_set or 
                (suru_form and suru_form in vocab_set)):
                conjugations_used.append({
                    "surface": surface,
                    "base": lemma_base,
                    "conjugation_type": cType,
                    "conjugation_form": cForm,
                    "pos": pos1,
                })
            else:
                # Only track content words as violations
                if pos1 in {"名詞", "動詞", "形容詞", "形状詞"}:
                    violations.append({
                        "surface": surface,
                        "suspected_base": lemma_base,
                        "pos": pos1,
                    })
        
        return {
            "conjugations": conjugations_used,
            "violations": violations,
        }


def verify_conjugations(story: str, vocab: List[str]) -> Dict:
    """
    Convenience function to verify conjugations.
    
    Args:
        story: Japanese text to analyze
        vocab: List of vocabulary words (dictionary forms)
        
    Returns:
        Dict with 'conjugations' and 'violations'
    """
    verifier = ConjugationVerifier()
    return verifier.verify(story, vocab)
