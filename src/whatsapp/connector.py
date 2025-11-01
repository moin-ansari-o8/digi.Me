"""WhatsApp Web automation using Selenium"""

import time
from typing import List, Optional, Dict, Tuple
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager


class WhatsAppConnector:
    """Manages WhatsApp Web connection and message handling"""
    
    def __init__(self, headless: bool = False):
        """Initialize WhatsApp connector
        
        Args:
            headless: Run browser in headless mode
        """
        self.driver = None
        self.headless = headless
        self.wait = None
        self.last_checked_messages = {}
    
    def connect(self) -> None:
        """Connect to WhatsApp Web"""
        chrome_options = Options()
        
        # User data directory to save session
        chrome_options.add_argument("--user-data-dir=/tmp/whatsapp-session")
        
        if self.headless:
            chrome_options.add_argument("--headless")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Initialize driver
        service = Service(ChromeDriverManager().install())
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.wait = WebDriverWait(self.driver, 30)
        
        # Open WhatsApp Web
        self.driver.get("https://web.whatsapp.com")
        
        print("Waiting for WhatsApp Web to load...")
        print("Please scan QR code if this is first time...")
        
        # Wait for the main page to load
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            print("WhatsApp Web connected successfully!")
        except TimeoutException:
            print("Timeout waiting for WhatsApp Web. Make sure you scanned the QR code.")
            raise
    
    def disconnect(self) -> None:
        """Disconnect from WhatsApp Web"""
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def search_contact(self, contact: str) -> bool:
        """Search for a contact
        
        Args:
            contact: Contact name or phone number
        
        Returns:
            True if contact found, False otherwise
        """
        try:
            # Find search box
            search_box = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            
            # Clear and enter contact
            search_box.click()
            search_box.clear()
            search_box.send_keys(contact)
            time.sleep(2)
            
            # Click on the contact
            contact_elem = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f'//span[@title="{contact}"]'))
            )
            contact_elem.click()
            time.sleep(1)
            
            return True
        
        except (TimeoutException, NoSuchElementException):
            print(f"Contact {contact} not found")
            return False
    
    def get_unread_messages(self, contact: str) -> List[Dict]:
        """Get unread messages from a contact
        
        Args:
            contact: Contact name or phone number
        
        Returns:
            List of message dictionaries
        """
        if not self.search_contact(contact):
            return []
        
        try:
            # Get all messages in the chat
            messages = self.driver.find_elements(By.XPATH, '//div[@class="_akbu"]//div[@class="copyable-text"]')
            
            unread = []
            current_messages = []
            
            for msg in messages:
                try:
                    # Check if message is from contact (not from me)
                    parent = msg.find_element(By.XPATH, './ancestor::div[@class="_akbu"]')
                    is_from_me = "message-out" in parent.get_attribute("class")
                    
                    if not is_from_me:
                        # Get message text
                        text_elem = msg.find_element(By.XPATH, './/span[@class="_ao3e"]')
                        message_text = text_elem.text
                        
                        # Get timestamp
                        time_elem = msg.find_element(By.XPATH, './/span[@class="_ao_h"]')
                        timestamp = time_elem.text
                        
                        current_messages.append({
                            'contact': contact,
                            'message': message_text,
                            'timestamp': timestamp
                        })
                
                except NoSuchElementException:
                    continue
            
            # Filter to only new messages
            last_count = self.last_checked_messages.get(contact, 0)
            if len(current_messages) > last_count:
                unread = current_messages[last_count:]
                self.last_checked_messages[contact] = len(current_messages)
            
            return unread
        
        except Exception as e:
            print(f"Error getting messages from {contact}: {e}")
            return []
    
    def send_message(self, contact: str, message: str) -> bool:
        """Send a message to a contact
        
        Args:
            contact: Contact name or phone number
            message: Message to send
        
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.search_contact(contact):
            return False
        
        try:
            # Find message input box
            message_box = self.wait.until(
                EC.presence_of_element_located((
                    By.XPATH, 
                    '//div[@contenteditable="true"][@data-tab="10"]'
                ))
            )
            
            # Type and send message
            message_box.click()
            message_box.send_keys(message)
            message_box.send_keys(Keys.ENTER)
            
            time.sleep(1)
            return True
        
        except Exception as e:
            print(f"Error sending message to {contact}: {e}")
            return False
    
    def get_all_chats(self) -> List[str]:
        """Get list of all chat contacts
        
        Returns:
            List of contact names
        """
        try:
            # Get all chat elements
            chats = self.driver.find_elements(By.XPATH, '//span[@title]')
            
            contact_names = []
            for chat in chats:
                title = chat.get_attribute("title")
                if title and title not in contact_names:
                    contact_names.append(title)
            
            return contact_names
        
        except Exception as e:
            print(f"Error getting chats: {e}")
            return []
    
    def has_unread_indicator(self, contact: str) -> bool:
        """Check if contact has unread messages indicator
        
        Args:
            contact: Contact name or phone number
        
        Returns:
            True if has unread messages, False otherwise
        """
        try:
            # Search for unread indicator for the contact
            unread_badge = self.driver.find_elements(
                By.XPATH, 
                f'//span[@title="{contact}"]/ancestor::div[contains(@class, "_ak8l")]//span[@class="_ahzz"]'
            )
            
            return len(unread_badge) > 0
        
        except Exception:
            return False
