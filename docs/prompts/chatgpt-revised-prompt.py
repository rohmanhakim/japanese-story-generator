constraints = f"""
CONSTRAINTS (STRICT):
1. Primary vocabulary to use (WHITELIST): 
{word_list_str}

2. Allowed particles ONLY:
は、が、を、に、で、と、の、へ、から、まで、より、など

3. You MAY conjugate or inflect whitelist words grammatically.

4. You MAY use the following auxiliary/common words ONLY if unavoidable:
数、時、所、事、人、日、今、前、後

5. At least 90% of all content words MUST come from the whitelist.

6. Output must be:
- Natural Japanese
- Grammatically correct
- Coherent as a short story

7. Maximum length: {max_length} Japanese characters.
8. Do NOT include any explanations, titles, or meta text.
"""

user_prompt = f"""
Write a short Japanese story that satisfies ALL constraints above.

Before producing the final output, internally verify:
- No disallowed characters or words are used
- Character length is within the limit
- Story remains coherent

Then output ONLY the final story text.
"""
