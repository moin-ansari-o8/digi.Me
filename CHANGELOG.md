# Changelog

All notable changes to digi.Me will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-01

### Added
- **WhatsApp Automation**
  - Selenium-based WhatsApp Web connector
  - Session persistence (QR code only needed once)
  - Message listener for approved contacts
  - Automatic message response capability
  - Unread message tracking
  
- **AI Integration**
  - OpenAI GPT-3.5 support
  - Cohere API support
  - Configurable AI provider selection
  - Context-aware response generation
  - Conversation history integration
  
- **Chat Style System**
  - JSON-based personality configuration
  - Customizable tone, formality, and humor
  - Phrase usage patterns
  - Example conversation training
  - Dynamic system prompt generation
  - Style update API
  
- **Secure Storage**
  - SQLite database for chat history
  - Fernet (AES-128) encryption for messages
  - Approved contacts management
  - Encrypted key storage
  - Conversation history retrieval
  
- **Web Dashboard**
  - Flask-based web interface
  - Socket.IO for real-time updates
  - User authentication system
  - Conversation viewer
  - Chat style editor
  - Configuration display
  - Responsive design
  
- **Security Features**
  - Environment-based configuration (.env)
  - Encrypted message storage
  - Approved contacts whitelist
  - Dashboard authentication
  - Secure session management
  - API key protection
  
- **Documentation**
  - Comprehensive README with features
  - Quick Start guide (5-minute setup)
  - Detailed Setup Guide
  - Usage Examples with code samples
  - Security best practices (SECURITY.md)
  - Troubleshooting guide
  - MIT License
  
- **Testing**
  - Test suite for chat style functionality
  - Configuration validation
  - Syntax checking
  
- **Configuration**
  - .env.example template
  - .env.template with detailed comments
  - Flexible configuration options
  - Multiple AI provider support
  - Customizable check intervals

### Security
- Fixed cryptography vulnerabilities:
  - Updated to 42.0.4 (from 41.0.7)
  - Fixes NULL pointer dereference vulnerability
  - Fixes Bleichenbacher timing oracle attack
- Fixed Pillow buffer overflow:
  - Updated to 10.3.0 (from 10.1.0)
- Implemented message encryption
- Added security documentation
- Added approved contacts filtering

### Dependencies
- selenium==4.15.2
- webdriver-manager==4.0.1
- pywhatkit==5.4
- openai==1.3.7
- cohere==4.37
- flask==3.0.0
- flask-cors==4.0.0
- flask-socketio==5.3.5
- sqlalchemy==2.0.23
- cryptography==42.0.4 (security update)
- python-dotenv==1.0.0
- requests==2.31.0
- pillow==10.3.0 (security update)
- python-dateutil==2.8.2
- pytest==7.4.3
- pytest-cov==4.1.0

## [Unreleased]

### Planned Features
- Multi-user support
- Voice message support
- Image message handling
- Advanced analytics dashboard
- Machine learning for style improvement
- Conversation export feature
- Mobile app
- Docker containerization
- Multiple chat style profiles per contact
- Scheduled messages
- Auto-response templates
- Message scheduling
- Contact groups
- Backup/restore functionality

### Known Issues
- WhatsApp Web XPath selectors may change (requires updates)
- Chrome driver compatibility varies by system
- No mobile app (web only)
- No group chat support yet
- Manual QR code scan required on first run

---

## Version History

### Version 1.0.0 (Initial Release)
This is the first stable release of digi.Me with core features:
- WhatsApp automation
- AI-powered responses
- Chat style customization
- Secure storage
- Web dashboard
- Comprehensive documentation

---

**Note**: This project is under active development. Report bugs and request features via GitHub issues.
