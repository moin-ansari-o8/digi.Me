"""Configuration management for digi.Me"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Base paths
    BASE_DIR = Path(__file__).parent.parent
    CHAT_DATA_DIR = BASE_DIR / "chat_data"
    CHAT_STYLE_DIR = BASE_DIR / "chat-style"
    
    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    COHERE_API_KEY = os.getenv("COHERE_API_KEY", "")
    AI_PROVIDER = os.getenv("AI_PROVIDER", "openai")
    
    # WhatsApp Configuration
    WHATSAPP_PHONE_NUMBER = os.getenv("WHATSAPP_PHONE_NUMBER", "")
    APPROVED_CONTACTS = [
        contact.strip() 
        for contact in os.getenv("APPROVED_CONTACTS", "").split(",")
        if contact.strip()
    ]
    
    # Database Configuration
    DATABASE_PATH = BASE_DIR / os.getenv("DATABASE_PATH", "chat_data/chat_history.db")
    ENCRYPTION_KEY = os.getenv("ENCRYPTION_KEY", "").encode() if os.getenv("ENCRYPTION_KEY") else None
    
    # Dashboard Configuration
    DASHBOARD_HOST = os.getenv("DASHBOARD_HOST", "0.0.0.0")
    DASHBOARD_PORT = int(os.getenv("DASHBOARD_PORT", "5000"))
    DASHBOARD_SECRET_KEY = os.getenv("DASHBOARD_SECRET_KEY", "dev-secret-key-change-in-production")
    DASHBOARD_USERNAME = os.getenv("DASHBOARD_USERNAME", "admin")
    DASHBOARD_PASSWORD = os.getenv("DASHBOARD_PASSWORD", "changeme123")
    
    # Chat Style Configuration
    CHAT_STYLE_PATH = BASE_DIR / os.getenv("CHAT_STYLE_PATH", "chat-style/my_style.json")
    
    # Automation Settings
    AUTO_REPLY_ENABLED = os.getenv("AUTO_REPLY_ENABLED", "true").lower() == "true"
    CHECK_INTERVAL_SECONDS = int(os.getenv("CHECK_INTERVAL_SECONDS", "10"))
    MAX_RESPONSE_LENGTH = int(os.getenv("MAX_RESPONSE_LENGTH", "500"))
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        errors = []
        
        if cls.AI_PROVIDER == "openai" and not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required when AI_PROVIDER is 'openai'")
        
        if cls.AI_PROVIDER == "cohere" and not cls.COHERE_API_KEY:
            errors.append("COHERE_API_KEY is required when AI_PROVIDER is 'cohere'")
        
        if not cls.APPROVED_CONTACTS:
            errors.append("APPROVED_CONTACTS must have at least one contact")
        
        if not cls.ENCRYPTION_KEY:
            errors.append("ENCRYPTION_KEY is required for secure storage")
        
        return errors
