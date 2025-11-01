# digi.Me 🤖

**Your AI Twin for WhatsApp** - An intelligent Python application that automates WhatsApp conversations while maintaining your unique communication style.

## 🌟 Features

- **WhatsApp Automation**: Seamless integration with WhatsApp Web using Selenium
- **AI-Powered Responses**: Uses OpenAI or Cohere to generate contextual replies
- **Personality Matching**: Maintains your unique tone and communication style
- **Secure Storage**: Encrypted chat history with SQLite database
- **Approved Contacts**: Only responds to whitelisted contacts
- **Chat Style System**: JSON-based personality configuration with training capability
- **Web Dashboard**: Modern interface for chat review and manual control
- **Real-time Monitoring**: Live updates and message tracking

## 📋 Requirements

- Python 3.8+
- Chrome/Chromium browser
- OpenAI API key or Cohere API key
- WhatsApp account

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone https://github.com/moin-ansari-o8/digi.Me.git
cd digi.Me
pip install -r requirements.txt
```

### 2. Configure

```bash
# Copy example configuration
cp .env.example .env

# Edit .env with your details
nano .env
```

**Required Configuration**:
- `OPENAI_API_KEY` or `COHERE_API_KEY`: Your AI provider API key
- `APPROVED_CONTACTS`: Comma-separated phone numbers (with country code)
- `ENCRYPTION_KEY`: A secure key for encrypting chat data
- `DASHBOARD_USERNAME` and `DASHBOARD_PASSWORD`: Dashboard login credentials

### 3. Customize Your Style

Edit `chat-style/my_style.json` to define your communication personality:

```json
{
  "personality": {
    "tone": "friendly and casual",
    "formality": "informal",
    "emoji_usage": "occasional"
  },
  "phrases_i_use": ["honestly", "you know", "for sure"],
  "example_conversations": [...]
}
```

### 4. Run

**Start the Bot** (WhatsApp automation):
```bash
python main.py bot
```

**Start the Dashboard** (Web interface):
```bash
python main.py dashboard
```

**Start Both** (Separate terminals recommended):
```bash
# Terminal 1
python main.py dashboard

# Terminal 2
python main.py bot
```

## 📱 Using the Bot

1. **First Run**: 
   - The bot will open WhatsApp Web
   - Scan the QR code with your phone
   - The session will be saved for future runs

2. **Automatic Responses**:
   - Bot monitors approved contacts for new messages
   - Generates responses using your AI provider
   - Maintains conversation context
   - Stores all chats securely

3. **Manual Control**:
   - Access dashboard at `http://localhost:5000`
   - Review conversations
   - Send manual messages
   - Update chat style

## 🎨 Dashboard Features

Access the web dashboard at `http://localhost:5000` (default):

- **Chats Tab**: View all conversations, read message history
- **Chat Style Tab**: Update your communication style in real-time
- **Configuration Tab**: View current bot settings
- Real-time connection status indicator
- Responsive design for mobile and desktop

## 🔒 Security

- **Encrypted Storage**: All messages are encrypted using Fernet (AES)
- **Environment Variables**: API keys stored securely in `.env`
- **Approved Contacts**: Only responds to whitelisted numbers
- **Session Management**: Secure dashboard authentication
- **Data Privacy**: All data stored locally, no external database

## 📁 Project Structure

```
digi.Me/
├── src/
│   ├── whatsapp/          # WhatsApp automation
│   │   └── connector.py   # Selenium-based WhatsApp connector
│   ├── ai/                # AI integration
│   │   ├── chat_style.py  # Style management
│   │   └── response_generator.py  # AI response generation
│   ├── storage/           # Data storage
│   │   └── database.py    # Encrypted database
│   ├── dashboard/         # Web interface
│   │   ├── app.py         # Flask application
│   │   └── templates/     # HTML templates
│   ├── config.py          # Configuration management
│   └── bot.py             # Main bot orchestrator
├── chat-style/            # Personality definitions
│   └── my_style.json      # Your communication style
├── chat_data/             # Encrypted chat storage
├── main.py                # Entry point
├── requirements.txt       # Dependencies
├── .env.example           # Example configuration
└── README.md              # This file
```

## 🛠️ Configuration Options

See `.env.example` for all available options:

- **AI_PROVIDER**: Choose between `openai` or `cohere`
- **AUTO_REPLY_ENABLED**: Enable/disable automatic responses
- **CHECK_INTERVAL_SECONDS**: How often to check for new messages
- **MAX_RESPONSE_LENGTH**: Maximum characters in AI responses
- **DASHBOARD_PORT**: Web dashboard port

## 🎯 Chat Style Training

Add example conversations to improve response quality:

1. Through Dashboard:
   - Go to "Chat Style" tab
   - Add context and example responses
   - Save to update the bot's behavior

2. Manually edit JSON:
   - Edit `chat-style/my_style.json`
   - Add to `example_conversations` array
   - Restart bot to apply changes

## 🐛 Troubleshooting

**QR Code doesn't appear**:
- Ensure Chrome/Chromium is installed
- Try running without headless mode
- Check browser console for errors

**Bot doesn't respond**:
- Verify approved contacts are correct (include country code)
- Check API key is valid
- Ensure `AUTO_REPLY_ENABLED=true` in `.env`

**Database errors**:
- Ensure `ENCRYPTION_KEY` is set
- Check write permissions in `chat_data/` directory

**Dashboard won't load**:
- Check port 5000 is not in use
- Verify `DASHBOARD_SECRET_KEY` is set
- Check Flask logs for errors

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 📄 License

This project is provided as-is for educational and personal use.

## ⚠️ Disclaimer

- This tool is for personal use only
- Ensure you comply with WhatsApp's Terms of Service
- Use responsibly and respect privacy
- The developers are not responsible for any misuse

## 🙏 Acknowledgments

- OpenAI for GPT models
- Cohere for AI capabilities
- Selenium for browser automation
- Flask for web framework

---

**Made with ❤️ for automating conversations while keeping your unique voice**
