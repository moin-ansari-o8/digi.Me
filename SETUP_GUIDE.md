# Setup Guide for digi.Me

This guide will walk you through setting up digi.Me from scratch.

## Prerequisites

1. **Python 3.8 or higher**
   ```bash
   python --version  # Should be 3.8+
   ```

2. **Chrome or Chromium browser**
   - Windows/Mac: Download from https://www.google.com/chrome/
   - Linux: `sudo apt-get install chromium-browser`

3. **WhatsApp Account**
   - Have your phone with WhatsApp installed ready

4. **API Keys**
   - OpenAI: Get from https://platform.openai.com/api-keys
   - OR Cohere: Get from https://dashboard.cohere.ai/api-keys

## Step-by-Step Setup

### 1. Clone the Repository

```bash
git clone https://github.com/moin-ansari-o8/digi.Me.git
cd digi.Me
```

### 2. Install Dependencies

```bash
# Create a virtual environment (recommended)
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit the .env file with your favorite editor
nano .env  # or vim, code, etc.
```

### 4. Required Configuration

Edit `.env` and fill in these **required** fields:

```env
# Choose your AI provider
AI_PROVIDER=openai  # or 'cohere'

# Add your API key (get from provider's website)
OPENAI_API_KEY=sk-...your-key-here...

# Add approved contacts (with country code, e.g., +1234567890)
APPROVED_CONTACTS=+1234567890,+9876543210

# Generate a strong encryption key for security
ENCRYPTION_KEY=my-super-secret-encryption-key-change-this

# Set dashboard credentials
DASHBOARD_USERNAME=admin
DASHBOARD_PASSWORD=strong-password-here
```

### 5. Customize Your Style

Edit `chat-style/my_style.json` to match your personality:

```json
{
  "personality": {
    "tone": "friendly and casual",
    "formality": "informal",
    "humor": "moderate",
    "emoji_usage": "occasional"
  },
  "phrases_i_use": [
    "honestly",
    "you know",
    "for sure"
  ]
}
```

### 6. First Run - Connect WhatsApp

```bash
python main.py bot
```

**What happens:**
1. Chrome browser will open with WhatsApp Web
2. A QR code will appear
3. Open WhatsApp on your phone
4. Tap on the three dots (menu) → "Linked Devices"
5. Tap "Link a Device"
6. Scan the QR code on your computer screen
7. Wait for connection confirmation

**Important:** The session is saved, so you won't need to scan the QR code again on subsequent runs.

### 7. Test the Bot

1. From another phone, send a message to one of your approved contacts
2. Check the bot console - you should see the message received
3. The bot will generate and send a response
4. Check WhatsApp on your phone to see the AI response

### 8. Access the Dashboard

In a new terminal:

```bash
python main.py dashboard
```

Then open your browser to: `http://localhost:5000`

- Login with the credentials you set in `.env`
- View conversation history
- Update chat style
- Send manual messages

## Troubleshooting

### Chrome Driver Issues

If you see "chromedriver not found":

```bash
# The webdriver-manager should auto-install, but if it fails:
pip install --upgrade webdriver-manager
```

### API Key Errors

If you see authentication errors:
- Double-check your API key is correct
- Ensure no extra spaces in `.env`
- Verify your API key has sufficient credits
- For OpenAI: Check at https://platform.openai.com/account/usage
- For Cohere: Check at https://dashboard.cohere.ai/

### Permission Errors

If you see database or file permission errors:

```bash
# Make sure chat_data directory exists and is writable
mkdir -p chat_data
chmod 755 chat_data
```

### WhatsApp Connection Issues

If QR code doesn't appear:
1. Make sure Chrome is installed
2. Try disabling headless mode in `src/whatsapp/connector.py`
3. Check for firewall blocking Chrome
4. Try running with `--no-sandbox` flag (already included)

### Port Already in Use

If dashboard port 5000 is in use:

```bash
# Change port in .env
DASHBOARD_PORT=8080

# Or specify when running
python main.py dashboard --port 8080
```

## Security Best Practices

1. **Never commit `.env` file** - It's already in `.gitignore`
2. **Use a strong ENCRYPTION_KEY** - At least 32 characters
3. **Change default dashboard password** - Don't use 'changeme123'
4. **Keep API keys secure** - Don't share them
5. **Regularly update dependencies** - `pip install --upgrade -r requirements.txt`

## Next Steps

- Read the main [README.md](README.md) for full features
- Customize your chat style for better responses
- Add more example conversations for training
- Monitor the dashboard for conversation insights

## Getting Help

If you encounter issues:
1. Check this guide and the main README
2. Look at the Troubleshooting section
3. Check console logs for error messages
4. Open an issue on GitHub with:
   - What you were trying to do
   - What happened instead
   - Error messages (remove sensitive info)
   - Your Python version and OS

Happy automating! 🤖
