"""Chat style management for maintaining user's tone and personality"""

import json
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime


class ChatStyle:
    """Manages chat style configuration and training"""
    
    def __init__(self, style_path: Path):
        """Initialize chat style manager
        
        Args:
            style_path: Path to the chat style JSON file
        """
        self.style_path = style_path
        self.style_data = self._load_style()
    
    def _load_style(self) -> Dict:
        """Load style from JSON file"""
        if not self.style_path.exists():
            raise FileNotFoundError(f"Chat style file not found: {self.style_path}")
        
        with open(self.style_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_system_prompt(self) -> str:
        """Generate system prompt for AI based on chat style
        
        Returns:
            System prompt string
        """
        personality = self.style_data.get("personality", {})
        phrases_use = self.style_data.get("phrases_i_use", [])
        phrases_avoid = self.style_data.get("phrases_i_avoid", [])
        response_rules = self.style_data.get("response_rules", {})
        
        prompt = f"""You are an AI assistant that mimics a specific person's communication style.

PERSONALITY:
- Tone: {personality.get('tone', 'friendly')}
- Formality: {personality.get('formality', 'informal')}
- Humor level: {personality.get('humor', 'moderate')}
- Emoji usage: {personality.get('emoji_usage', 'occasional')}
- Response length: {personality.get('response_length', 'concise')}

LANGUAGE PATTERNS:
"""
        
        if phrases_use:
            prompt += f"- Commonly use phrases: {', '.join(phrases_use)}\n"
        
        if phrases_avoid:
            prompt += f"- Avoid phrases: {', '.join(phrases_avoid)}\n"
        
        prompt += f"""
RESPONSE RULES:
- Maximum length: {response_rules.get('max_length', 500)} characters
- Use contractions: {response_rules.get('use_contractions', True)}
- Capitalization: {response_rules.get('capitalization', 'normal')}
- Punctuation: {response_rules.get('punctuation_style', 'minimal')}

Respond naturally as this person would, maintaining their unique communication style."""
        
        return prompt
    
    def get_example_conversations(self) -> List[Dict]:
        """Get example conversations for context
        
        Returns:
            List of example conversation dictionaries
        """
        return self.style_data.get("example_conversations", [])
    
    def get_greeting(self) -> str:
        """Get a random greeting from the style
        
        Returns:
            Greeting string
        """
        import random
        greetings = self.style_data.get("language_patterns", {}).get("greetings", ["Hi!"])
        return random.choice(greetings)
    
    def get_farewell(self) -> str:
        """Get a random farewell from the style
        
        Returns:
            Farewell string
        """
        import random
        farewells = self.style_data.get("language_patterns", {}).get("farewells", ["Bye!"])
        return random.choice(farewells)
    
    def update_style(self, updates: Dict) -> None:
        """Update chat style with new data
        
        Args:
            updates: Dictionary with style updates
        """
        # Deep merge updates into style_data
        self._deep_merge(self.style_data, updates)
        self._save_style()
    
    def add_example_conversation(self, context: str, response: str) -> None:
        """Add a new example conversation for training
        
        Args:
            context: Context or question
            response: User's typical response
        """
        if "example_conversations" not in self.style_data:
            self.style_data["example_conversations"] = []
        
        self.style_data["example_conversations"].append({
            "context": context,
            "my_response": response,
            "added_at": datetime.now().isoformat()
        })
        self._save_style()
    
    def _save_style(self) -> None:
        """Save style data to JSON file"""
        with open(self.style_path, 'w', encoding='utf-8') as f:
            json.dump(self.style_data, f, indent=2, ensure_ascii=False)
    
    def _deep_merge(self, base: Dict, updates: Dict) -> None:
        """Deep merge updates into base dictionary
        
        Args:
            base: Base dictionary to update
            updates: Updates to merge
        """
        for key, value in updates.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                self._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get_max_response_length(self) -> int:
        """Get maximum response length from style
        
        Returns:
            Maximum response length
        """
        return self.style_data.get("response_rules", {}).get("max_length", 500)
