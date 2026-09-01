"""Conjugation verification using fugashi (MeCab wrapper)."""

from typing import List, Dict, Tuple
import fugashi


class ConjugationVerifier:
    """Verify conjugations and vocabulary usage in Japanese text."""
    
    def __init__(self):
        """Initialize fugashi tagger."""
        self.tagger = fugashi.Tagger()
    
    def _normalize_vocab(self, vocab: List[str]) -> Tuple[set, set, dict]:
        """
        Normalize vocabulary for matching.
        
        Returns:
            Tuple of (vocab_set, readings_set, reading_to_word_map)
        """
        vocab_set = set(vocab)
        readings_set = set()
        reading_to_word = {}
        
        # Pre-process vocabulary to extract readings
        for word in vocab:
            result = self.tagger(word)
            for token in result:
                if token.feature.pron:
                    # Convert katakana reading to hiragana for matching
                    reading = self._katakana_to_hiragana(token.feature.pron)
                    readings_set.add(reading)
                    reading_to_word[reading] = word
                if token.feature.kana:
                    kana = self._katakana_to_hiragana(token.feature.kana)
                    readings_set.add(kana)
                    reading_to_word[kana] = word
        
        return vocab_set, readings_set, reading_to_word
    
    def _katakana_to_hiragana(self, text: str) -> str:
        """Convert katakana to hiragana."""
        result = []
        for char in text:
            # Katakana range: 30A0-30FF, Hiragana range: 3040-309F
            code = ord(char)
            if 0x30A0 <= code <= 0x30FF:
                result.append(chr(code - 0x60))
            else:
                result.append(char)
        return ''.join(result)
    
    def _check_compound_words(self, tokens: list, vocab_set: set) -> Tuple[List[dict], List[int]]:
        """
        Check for compound words by combining consecutive nouns.
        
        Returns:
            Tuple of (found_compounds, indices_to_skip)
        """
        found_compounds = []
        indices_to_skip = set()
        
        # Check 2-word and 3-word combinations
        for window_size in [2, 3]:
            for i in range(len(tokens) - window_size + 1):
                # Skip if any token in window is already matched
                if any(j in indices_to_skip for j in range(i, i + window_size)):
                    continue
                
                # Check if all tokens in window are nouns
                window_tokens = tokens[i:i + window_size]
                if not all(t.feature.pos1 == '名詞' for t in window_tokens):
                    continue
                
                # Combine surface forms
                combined = ''.join(t.surface for t in window_tokens)
                
                if combined in vocab_set:
                    found_compounds.append({
                        'surface': combined,
                        'tokens': [t.surface for t in window_tokens],
                        'pos': '名詞 (compound)',
                        'indices': list(range(i, i + window_size))
                    })
                    indices_to_skip.update(range(i, i + window_size))
        
        return found_compounds, list(indices_to_skip)
    
    def verify(self, story: str, vocab: List[str]) -> Dict:
        """
        Verify conjugations used and vocabulary violations.
        
        Args:
            story: Japanese text to analyze
            vocab: List of vocabulary words (dictionary forms)
            
        Returns:
            Dict with 'conjugations', 'violations', and 'compounds'
        """
        vocab_set, readings_set, reading_to_word = self._normalize_vocab(vocab)
        conjugations_used = []
        violations = []
        matched_indices = set()
        
        tokens = list(self.tagger(story))
        
        # First pass: check for compound words
        compounds, compound_indices = self._check_compound_words(tokens, vocab_set)
        matched_indices.update(compound_indices)
        
        # Second pass: check individual tokens
        for i, token in enumerate(tokens):
            if i in matched_indices:
                continue
                
            surface = token.surface
            if not surface.strip():
                continue
            
            f = token.feature
            pos1 = f.pos1
            lemma = f.lemma
            orthBase = f.orthBase
            pron = f.pron
            kana = f.kana
            cType = f.cType
            cForm = f.cForm
            
            # Skip non-lexical tokens
            if pos1 in {"助詞", "助動詞", "記号", "補助記号"}:
                continue
            
            # Extract base lemma (remove POS suffix like "行く-動詞" → "行く")
            lemma_base = lemma.split("-")[0] if "-" in lemma else lemma
            
            # Handle サ変 verbs: 勉強 (noun) + する → match 勉強する in vocab
            suru_form = lemma_base + "する" if pos1 == "名詞" else None
            
            # Convert reading to hiragana for matching
            pron_hira = self._katakana_to_hiragana(pron) if pron else ""
            kana_hira = self._katakana_to_hiragana(kana) if kana else ""
            
            # Check multiple matching criteria
            matched = False
            matched_word = None
            match_type = None
            
            # 1. Direct lemma match
            if lemma_base in vocab_set:
                matched = True
                matched_word = lemma_base
                match_type = "lemma"
            # 2. Lemma exact match
            elif lemma in vocab_set:
                matched = True
                matched_word = lemma
                match_type = "lemma_exact"
            # 3. Surface form match (NEW)
            elif surface in vocab_set:
                matched = True
                matched_word = surface
                match_type = "surface"
            # 4. OrthBase match (NEW) 
            elif orthBase in vocab_set:
                matched = True
                matched_word = orthBase
                match_type = "orthBase"
            # 5. サ変 verb form
            elif suru_form and suru_form in vocab_set:
                matched = True
                matched_word = suru_form
                match_type = "suru_form"
            # 6. Reading-based match (NEW)
            elif pron_hira in readings_set:
                matched = True
                matched_word = reading_to_word.get(pron_hira)
                match_type = "reading_pron"
            elif kana_hira in readings_set:
                matched = True
                matched_word = reading_to_word.get(kana_hira)
                match_type = "reading_kana"
            
            if matched:
                matched_indices.add(i)
                conjugations_used.append({
                    "surface": surface,
                    "base": lemma_base,
                    "matched_word": matched_word,
                    "match_type": match_type,
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
                        "reading": pron_hira,
                    })
        
        return {
            "conjugations": conjugations_used,
            "violations": violations,
            "compounds": compounds,
            "matched_indices": list(matched_indices),
        }


def verify_conjugations(story: str, vocab: List[str]) -> Dict:
    """
    Convenience function to verify conjugations.
    
    Args:
        story: Japanese text to analyze
        vocab: List of vocabulary words (dictionary forms)
        
    Returns:
        Dict with 'conjugations', 'violations', and 'compounds'
    """
    verifier = ConjugationVerifier()
    return verifier.verify(story, vocab)
