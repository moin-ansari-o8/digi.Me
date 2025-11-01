"""AI response generation using OpenAI or Cohere"""

from typing import List, Dict, Optional
import openai
import cohere
from src.config import Config
from src.ai.chat_style import ChatStyle


class ResponseGenerator:
    """Generate responses using AI with chat style"""
    
    def __init__(self, chat_style: ChatStyle):
        """Initialize response generator
        
        Args:
            chat_style: ChatStyle instance for personality
        """
        self.chat_style = chat_style
        self.provider = Config.AI_PROVIDER
        
        if self.provider == "openai":
            openai.api_key = Config.OPENAI_API_KEY
            self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        elif self.provider == "cohere":
            self.client = cohere.Client(Config.COHERE_API_KEY)
        else:
            raise ValueError(f"Unsupported AI provider: {self.provider}")
    
    def generate_response(
        self, 
        message: str, 
        context: Optional[List[Dict]] = None,
        sender_name: Optional[str] = None
    ) -> str:
        """Generate a response to a message
        
        Args:
            message: The incoming message to respond to
            context: Previous conversation context
            sender_name: Name of the message sender
        
        Returns:
            Generated response string
        """
        if self.provider == "openai":
            return self._generate_openai(message, context, sender_name)
        else:
            return self._generate_cohere(message, context, sender_name)
    
    def _generate_openai(
        self, 
        message: str, 
        context: Optional[List[Dict]] = None,
        sender_name: Optional[str] = None
    ) -> str:
        """Generate response using OpenAI
        
        Args:
            message: The incoming message
            context: Previous conversation context
            sender_name: Name of sender
        
        Returns:
            Generated response
        """
        messages = [
            {"role": "system", "content": self.chat_style.get_system_prompt()}
        ]
        
        # Add example conversations as context
        for example in self.chat_style.get_example_conversations():
            messages.append({
                "role": "user",
                "content": example.get("context", "")
            })
            messages.append({
                "role": "assistant",
                "content": example.get("my_response", "")
            })
        
        # Add conversation context
        if context:
            for ctx in context[-5:]:  # Last 5 messages for context
                role = "assistant" if ctx.get("is_me", False) else "user"
                messages.append({
                    "role": role,
                    "content": ctx.get("message", "")
                })
        
        # Add current message
        user_message = message
        if sender_name:
            user_message = f"{sender_name}: {message}"
        
        messages.append({"role": "user", "content": user_message})
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=messages,
                max_tokens=self.chat_style.get_max_response_length(),
                temperature=0.8
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            print(f"Error generating OpenAI response: {e}")
            return "Sorry, I couldn't process that right now."
    
    def _generate_cohere(
        self, 
        message: str, 
        context: Optional[List[Dict]] = None,
        sender_name: Optional[str] = None
    ) -> str:
        """Generate response using Cohere
        
        Args:
            message: The incoming message
            context: Previous conversation context
            sender_name: Name of sender
        
        Returns:
            Generated response
        """
        # Build conversation history
        chat_history = []
        
        if context:
            for ctx in context[-5:]:  # Last 5 messages for context
                role = "CHATBOT" if ctx.get("is_me", False) else "USER"
                chat_history.append({
                    "role": role,
                    "message": ctx.get("message", "")
                })
        
        # Build preamble with style
        preamble = self.chat_style.get_system_prompt()
        
        # Add examples to preamble
        examples = self.chat_style.get_example_conversations()
        if examples:
            preamble += "\n\nExample conversations:\n"
            for ex in examples[:3]:  # Limit to 3 examples
                preamble += f"Q: {ex.get('context', '')}\n"
                preamble += f"A: {ex.get('my_response', '')}\n\n"
        
        # Format message
        user_message = message
        if sender_name:
            user_message = f"{sender_name}: {message}"
        
        try:
            response = self.client.chat(
                message=user_message,
                chat_history=chat_history,
                preamble=preamble,
                model="command",
                temperature=0.8,
                max_tokens=self.chat_style.get_max_response_length()
            )
            
            return response.text.strip()
        
        except Exception as e:
            print(f"Error generating Cohere response: {e}")
            return "Sorry, I couldn't process that right now."
