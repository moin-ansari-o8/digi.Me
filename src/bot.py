"""Main bot orchestrator for digi.Me"""

import time
from typing import Optional
from src.config import Config
from src.whatsapp.connector import WhatsAppConnector
from src.ai.chat_style import ChatStyle
from src.ai.response_generator import ResponseGenerator
from src.storage.database import ChatDatabase


class DigiMeBot:
    """Main bot that orchestrates WhatsApp automation and AI responses"""
    
    def __init__(self):
        """Initialize the bot"""
        # Validate configuration
        errors = Config.validate()
        if errors:
            raise ValueError(f"Configuration errors:\n" + "\n".join(errors))
        
        # Initialize components
        print("Initializing digi.Me bot...")
        
        self.whatsapp = WhatsAppConnector(headless=False)
        self.chat_style = ChatStyle(Config.CHAT_STYLE_PATH)
        self.response_generator = ResponseGenerator(self.chat_style)
        self.database = ChatDatabase(Config.DATABASE_PATH, Config.ENCRYPTION_KEY)
        
        # Initialize approved contacts in database
        self._sync_approved_contacts()
        
        print("Bot initialized successfully!")
    
    def _sync_approved_contacts(self) -> None:
        """Sync approved contacts from config to database"""
        for contact in Config.APPROVED_CONTACTS:
            if not self.database.is_approved_contact(contact):
                self.database.add_approved_contact(contact)
                print(f"Added approved contact: {contact}")
    
    def start(self) -> None:
        """Start the bot"""
        print("Starting digi.Me bot...")
        
        # Connect to WhatsApp
        print("Connecting to WhatsApp Web...")
        self.whatsapp.connect()
        
        print("Bot is running! Monitoring messages...")
        print(f"Auto-reply enabled: {Config.AUTO_REPLY_ENABLED}")
        print(f"Approved contacts: {len(Config.APPROVED_CONTACTS)}")
        print("Press Ctrl+C to stop")
        
        try:
            self._run_loop()
        except KeyboardInterrupt:
            print("\nStopping bot...")
        finally:
            self.stop()
    
    def stop(self) -> None:
        """Stop the bot"""
        print("Disconnecting from WhatsApp...")
        self.whatsapp.disconnect()
        print("Bot stopped.")
    
    def _run_loop(self) -> None:
        """Main message monitoring loop"""
        while True:
            try:
                # Check each approved contact
                for contact in Config.APPROVED_CONTACTS:
                    self._check_and_respond(contact)
                
                # Wait before next check
                time.sleep(Config.CHECK_INTERVAL_SECONDS)
            
            except Exception as e:
                print(f"Error in main loop: {e}")
                time.sleep(5)  # Wait a bit before retrying
    
    def _check_and_respond(self, contact: str) -> None:
        """Check messages from a contact and respond if needed
        
        Args:
            contact: Contact phone number
        """
        # Get unread messages
        messages = self.whatsapp.get_unread_messages(contact)
        
        if not messages:
            return
        
        print(f"\n--- New messages from {contact} ---")
        
        for msg in messages:
            message_text = msg['message']
            timestamp = msg.get('timestamp', 'unknown')
            
            print(f"[{timestamp}] {contact}: {message_text}")
            
            # Store incoming message
            self.database.add_message(
                contact=contact,
                message=message_text,
                is_me=False,
                sender_name=contact
            )
            
            # Generate and send response if auto-reply is enabled
            if Config.AUTO_REPLY_ENABLED:
                response = self._generate_response(contact, message_text)
                
                if response:
                    print(f"[AI Response]: {response}")
                    
                    # Send response
                    if self.whatsapp.send_message(contact, response):
                        # Store AI response
                        self.database.add_message(
                            contact=contact,
                            message=response,
                            is_me=True,
                            replied_by_ai=True
                        )
                        print("✓ Response sent")
                    else:
                        print("✗ Failed to send response")
    
    def _generate_response(self, contact: str, message: str) -> Optional[str]:
        """Generate AI response for a message
        
        Args:
            contact: Contact phone number
            message: Incoming message
        
        Returns:
            Generated response or None if error
        """
        try:
            # Get conversation context
            context = self.database.get_conversation(contact, limit=10)
            
            # Generate response
            response = self.response_generator.generate_response(
                message=message,
                context=context,
                sender_name=contact
            )
            
            return response
        
        except Exception as e:
            print(f"Error generating response: {e}")
            return None
    
    def send_manual_message(self, contact: str, message: str) -> bool:
        """Manually send a message (for dashboard use)
        
        Args:
            contact: Contact phone number
            message: Message to send
        
        Returns:
            True if sent successfully
        """
        if self.whatsapp.send_message(contact, message):
            # Store message
            self.database.add_message(
                contact=contact,
                message=message,
                is_me=True,
                replied_by_ai=False
            )
            return True
        return False
