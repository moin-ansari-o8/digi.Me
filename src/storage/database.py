"""Database management for secure chat storage"""

from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from cryptography.fernet import Fernet
import base64
import hashlib

Base = declarative_base()


class ChatMessage(Base):
    """Chat message model"""
    __tablename__ = 'chat_messages'
    
    id = Column(Integer, primary_key=True)
    contact = Column(String(50), nullable=False, index=True)
    message = Column(Text, nullable=False)  # Encrypted
    is_me = Column(Boolean, default=False)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    replied_by_ai = Column(Boolean, default=False)
    sender_name = Column(String(100))


class ApprovedContact(Base):
    """Approved contact model"""
    __tablename__ = 'approved_contacts'
    
    id = Column(Integer, primary_key=True)
    phone_number = Column(String(50), unique=True, nullable=False)
    name = Column(String(100))
    added_at = Column(DateTime, default=datetime.utcnow)
    is_active = Column(Boolean, default=True)


class ChatDatabase:
    """Manages secure chat database"""
    
    def __init__(self, db_path: Path, encryption_key: Optional[bytes] = None):
        """Initialize database
        
        Args:
            db_path: Path to SQLite database
            encryption_key: Encryption key for sensitive data
        """
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Setup encryption
        if encryption_key:
            # Derive a proper Fernet key from the provided key
            key = base64.urlsafe_b64encode(
                hashlib.sha256(encryption_key).digest()
            )
            self.cipher = Fernet(key)
        else:
            self.cipher = None
        
        # Create engine and tables
        self.engine = create_engine(f'sqlite:///{db_path}')
        Base.metadata.create_all(self.engine)
        
        # Create session factory
        self.Session = sessionmaker(bind=self.engine)
    
    def _encrypt(self, text: str) -> str:
        """Encrypt text
        
        Args:
            text: Plain text
        
        Returns:
            Encrypted text
        """
        if self.cipher:
            return self.cipher.encrypt(text.encode()).decode()
        return text
    
    def _decrypt(self, encrypted_text: str) -> str:
        """Decrypt text
        
        Args:
            encrypted_text: Encrypted text
        
        Returns:
            Plain text
        """
        if self.cipher:
            return self.cipher.decrypt(encrypted_text.encode()).decode()
        return encrypted_text
    
    def add_message(
        self, 
        contact: str, 
        message: str, 
        is_me: bool = False,
        replied_by_ai: bool = False,
        sender_name: Optional[str] = None
    ) -> int:
        """Add a message to database
        
        Args:
            contact: Contact phone number
            message: Message text
            is_me: Whether message is from me
            replied_by_ai: Whether this is an AI-generated reply
            sender_name: Name of sender
        
        Returns:
            Message ID
        """
        session = self.Session()
        try:
            encrypted_message = self._encrypt(message)
            
            msg = ChatMessage(
                contact=contact,
                message=encrypted_message,
                is_me=is_me,
                replied_by_ai=replied_by_ai,
                sender_name=sender_name
            )
            
            session.add(msg)
            session.commit()
            return msg.id
        
        finally:
            session.close()
    
    def get_conversation(
        self, 
        contact: str, 
        limit: int = 50
    ) -> List[Dict]:
        """Get conversation history with a contact
        
        Args:
            contact: Contact phone number
            limit: Maximum number of messages
        
        Returns:
            List of message dictionaries
        """
        session = self.Session()
        try:
            messages = session.query(ChatMessage)\
                .filter(ChatMessage.contact == contact)\
                .order_by(ChatMessage.timestamp.desc())\
                .limit(limit)\
                .all()
            
            result = []
            for msg in reversed(messages):
                result.append({
                    'id': msg.id,
                    'contact': msg.contact,
                    'message': self._decrypt(msg.message),
                    'is_me': msg.is_me,
                    'timestamp': msg.timestamp.isoformat(),
                    'replied_by_ai': msg.replied_by_ai,
                    'sender_name': msg.sender_name
                })
            
            return result
        
        finally:
            session.close()
    
    def get_all_conversations(self, limit_per_contact: int = 10) -> Dict[str, List[Dict]]:
        """Get all conversations grouped by contact
        
        Args:
            limit_per_contact: Max messages per contact
        
        Returns:
            Dictionary of contact -> messages
        """
        session = self.Session()
        try:
            # Get unique contacts
            contacts = session.query(ChatMessage.contact).distinct().all()
            
            result = {}
            for (contact,) in contacts:
                result[contact] = self.get_conversation(contact, limit_per_contact)
            
            return result
        
        finally:
            session.close()
    
    def add_approved_contact(self, phone_number: str, name: Optional[str] = None) -> int:
        """Add an approved contact
        
        Args:
            phone_number: Phone number
            name: Contact name
        
        Returns:
            Contact ID
        """
        session = self.Session()
        try:
            contact = ApprovedContact(
                phone_number=phone_number,
                name=name
            )
            
            session.add(contact)
            session.commit()
            return contact.id
        
        finally:
            session.close()
    
    def get_approved_contacts(self) -> List[Dict]:
        """Get all approved contacts
        
        Returns:
            List of contact dictionaries
        """
        session = self.Session()
        try:
            contacts = session.query(ApprovedContact)\
                .filter(ApprovedContact.is_active == True)\
                .all()
            
            return [
                {
                    'id': c.id,
                    'phone_number': c.phone_number,
                    'name': c.name,
                    'added_at': c.added_at.isoformat()
                }
                for c in contacts
            ]
        
        finally:
            session.close()
    
    def is_approved_contact(self, phone_number: str) -> bool:
        """Check if a contact is approved
        
        Args:
            phone_number: Phone number to check
        
        Returns:
            True if approved, False otherwise
        """
        session = self.Session()
        try:
            contact = session.query(ApprovedContact)\
                .filter(ApprovedContact.phone_number == phone_number)\
                .filter(ApprovedContact.is_active == True)\
                .first()
            
            return contact is not None
        
        finally:
            session.close()
