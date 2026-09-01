"""Parse Anki exported vocabulary."""

import re
from typing import List, Optional


class AnkiVocabParser:
    """Parse Anki exported vocabulary - extract only the words."""
    
    def __init__(self, filepath: Optional[str] = None):
        self.filepath = filepath
        
    def parse(self, filepath: Optional[str] = None) -> List[str]:
        """
        Extract just the vocabulary words (kanji only).
        
        Args:
            filepath: Path to Anki export file. If not provided, uses instance filepath.
            
        Returns:
            List of vocabulary words (kanji strings)
        """
        filepath = filepath or self.filepath
        if not filepath:
            raise ValueError("No filepath provided")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Pattern: word TAB "HTML content"
        pattern = r'^([^\t\n]+)\t"(.+?)"$'
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        
        return [kanji for kanji, _ in matches]
    
    def parse_with_readings(self, filepath: Optional[str] = None) -> List[dict]:
        """
        Extract words with readings.
        
        Args:
            filepath: Path to Anki export file. If not provided, uses instance filepath.
            
        Returns:
            List of dicts with 'kanji' and 'reading' keys
        """
        filepath = filepath or self.filepath
        if not filepath:
            raise ValueError("No filepath provided")
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        pattern = r'^([^\t\n]+)\t"(.+?)"$'
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)
        
        results = []
        for kanji, html in matches:
            # Extract reading from HTML
            furigana_match = re.search(
                r'<div class=""furigana-text"">([^<]+)</div>',
                html
            )
            reading = furigana_match.group(1).strip() if furigana_match else ""
            results.append({"kanji": kanji, "reading": reading})
        
        return results
    
    def format_for_prompt(self, vocab_words: List[str]) -> str:
        """Format vocabulary list for LLM prompt."""
        return ", ".join(vocab_words)
