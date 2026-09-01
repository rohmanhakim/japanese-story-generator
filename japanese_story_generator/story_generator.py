"""Story generation using vocabulary-constrained prompting."""

from typing import List, Optional
from .openrouter import OpenRouterClient


class StoryGenerator:
    """Generate Japanese stories using known vocabulary."""
    
    def __init__(self, api_key: str, model: str = "google/gemma-4-26b-a4b-it:free"):
        """
        Initialize story generator.
        
        Args:
            api_key: OpenRouter API key
            model: Model identifier
        """
        self.client = OpenRouterClient(api_key, model)
    
    def generate(
        self,
        vocab_words: List[str],
        theme: Optional[str] = None,
        max_length: int = 500,
        strict_vocab: bool = True
    ) -> str:
        """
        Generate a story using only the provided vocabulary.
        
        Args:
            vocab_words: List of vocabulary words to use
            theme: Optional story theme
            max_length: Maximum story length in characters
            strict_vocab: If True, use ONLY provided words
            
        Returns:
            Generated story in Japanese
        """
        word_list = ", ".join(vocab_words)
        
        if strict_vocab:
            constraints = f"""1. Use ONLY words from this list: {word_list}
2. You may use basic particles (は、が、を、に、で、と、の)
3. You may conjugate verbs and adjectives freely
4. Do NOT introduce any new vocabulary"""
        else:
            constraints = f"""1. PRIMARY vocabulary to use: {word_list}
2. You may use basic particles
3. You may conjugate verbs and adjectives freely
4. Aim to use 90%+ of words from the provided list"""
        
        prompt = f"""Write a short Japanese story (maximum {max_length} characters).

【Constraints】
{constraints}

{"【Theme】" + theme if theme else ""}

Write the story in Japanese only:"""
        
        return self.client.generate(prompt, max_tokens=1000)
    
    def generate_with_questions(
        self,
        vocab_words: List[str],
        level: str = "n5",
        theme: Optional[str] = None,
        max_length: int = 500
    ) -> dict:
        """
        Generate story with comprehension questions.
        
        Args:
            vocab_words: List of vocabulary words to use
            level: JLPT level (n5-n1)
            theme: Optional story theme
            max_length: Maximum story length in characters
            
        Returns:
            Dict with 'story', 'questions', and 'vocab_used'
        """
        word_list = ", ".join(vocab_words)
        
        if level in ["n5", "n4"]:
            question_format = """Questions (in English, multiple choice):
1. [Question]?
   A) [Option]
   B) [Option]
   C) [Option]
   
Answer: [Letter]"""
        else:
            question_format = """Questions:
1. [Question in Japanese]?
   Answer: [Answer in English]"""
        
        prompt = f"""Write a short Japanese story using ONLY these words: {word_list}

【Output Format】
Story:
[The story in Japanese]

Comprehension Questions:
{question_format}"""
        
        response = self.client.generate(prompt, max_tokens=1500)
        
        # Parse response
        story, questions = self._parse_response(response)
        
        return {
            "story": story,
            "questions": questions,
            "vocab_used": vocab_words
        }
    
    def _parse_response(self, response: str) -> tuple:
        """
        Parse story and questions from response.
        
        Args:
            response: Raw LLM response
            
        Returns:
            Tuple of (story, questions)
        """
        # Simple parsing - can be improved
        parts = response.split("Comprehension Questions:")
        story = parts[0].replace("Story:", "").strip()
        questions = parts[1].strip() if len(parts) > 1 else ""
        
        return story, questions
