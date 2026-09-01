"""OpenRouter API client for story generation."""

from typing import Optional
from openai import OpenAI


class OpenRouterClient:
    """Client for OpenRouter API."""
    
    def __init__(self, api_key: str, model: str = "google/gemma-4-26b-a4b-it:free"):
        """
        Initialize OpenRouter client.
        
        Args:
            api_key: OpenRouter API key
            model: Model identifier (default: google/gemma-4-31b-it:free)
        """
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key
        )
        self.model = model
    
    def generate(
        self,
        prompt: str,
        max_tokens: int = 2000,
        temperature: float = 0.8
    ) -> str:
        """
        Generate text from prompt.
        
        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature
            
        Returns:
            Generated text
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content.strip()
