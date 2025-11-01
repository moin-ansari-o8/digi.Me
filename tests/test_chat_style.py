"""Tests for chat style functionality"""

import json
import pytest
from pathlib import Path
from src.ai.chat_style import ChatStyle


def test_chat_style_loading(tmp_path):
    """Test loading chat style from JSON"""
    # Create a test style file
    style_data = {
        "name": "Test Style",
        "personality": {
            "tone": "friendly",
            "formality": "informal"
        },
        "phrases_i_use": ["test", "example"],
        "example_conversations": []
    }
    
    style_file = tmp_path / "test_style.json"
    with open(style_file, 'w') as f:
        json.dump(style_data, f)
    
    # Load style
    chat_style = ChatStyle(style_file)
    
    assert chat_style.style_data["name"] == "Test Style"
    assert chat_style.style_data["personality"]["tone"] == "friendly"


def test_system_prompt_generation(tmp_path):
    """Test system prompt generation"""
    style_data = {
        "personality": {
            "tone": "casual",
            "formality": "informal",
            "humor": "high",
            "emoji_usage": "frequent"
        },
        "phrases_i_use": ["honestly", "you know"],
        "phrases_i_avoid": ["literally"],
        "response_rules": {
            "max_length": 500,
            "use_contractions": True
        }
    }
    
    style_file = tmp_path / "test_style.json"
    with open(style_file, 'w') as f:
        json.dump(style_data, f)
    
    chat_style = ChatStyle(style_file)
    prompt = chat_style.get_system_prompt()
    
    assert "casual" in prompt
    assert "informal" in prompt
    assert "honestly" in prompt
    assert "literally" in prompt


def test_add_example_conversation(tmp_path):
    """Test adding example conversations"""
    style_data = {
        "name": "Test Style",
        "example_conversations": []
    }
    
    style_file = tmp_path / "test_style.json"
    with open(style_file, 'w') as f:
        json.dump(style_data, f)
    
    chat_style = ChatStyle(style_file)
    chat_style.add_example_conversation("How are you?", "I'm good, thanks!")
    
    # Reload to verify persistence
    with open(style_file, 'r') as f:
        saved_data = json.load(f)
    
    assert len(saved_data["example_conversations"]) == 1
    assert saved_data["example_conversations"][0]["context"] == "How are you?"
    assert saved_data["example_conversations"][0]["my_response"] == "I'm good, thanks!"


def test_update_style(tmp_path):
    """Test updating style data"""
    style_data = {
        "name": "Original",
        "personality": {
            "tone": "formal"
        }
    }
    
    style_file = tmp_path / "test_style.json"
    with open(style_file, 'w') as f:
        json.dump(style_data, f)
    
    chat_style = ChatStyle(style_file)
    chat_style.update_style({
        "personality": {
            "tone": "casual"
        }
    })
    
    assert chat_style.style_data["personality"]["tone"] == "casual"
    assert chat_style.style_data["name"] == "Original"  # Should preserve other fields


def test_get_max_response_length(tmp_path):
    """Test getting max response length"""
    style_data = {
        "response_rules": {
            "max_length": 750
        }
    }
    
    style_file = tmp_path / "test_style.json"
    with open(style_file, 'w') as f:
        json.dump(style_data, f)
    
    chat_style = ChatStyle(style_file)
    
    assert chat_style.get_max_response_length() == 750


def test_default_max_response_length(tmp_path):
    """Test default max response length"""
    style_data = {}
    
    style_file = tmp_path / "test_style.json"
    with open(style_file, 'w') as f:
        json.dump(style_data, f)
    
    chat_style = ChatStyle(style_file)
    
    assert chat_style.get_max_response_length() == 500  # Default


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
