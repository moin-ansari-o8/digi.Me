# Quick Start Guide - Get Running in 5 Minutes

Follow these steps to get digi.Me up and running quickly.

## ⚡ Fast Setup (5 minutes)

### Step 1: Install (1 minute)

```bash
# Clone repository
git clone https://github.com/moin-ansari-o8/digi.Me.git
cd digi.Me

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Configure (2 minutes)

```bash
# Copy example config
cp .env.example .env

# Edit .env file - replace these values:
nano .env
```

**Minimum required in `.env`:**

```env
# Get from https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-proj-your-key-here

# Your phone number and approved contacts (with country code)
WHATSAPP_PHONE_NUMBER=+1234567890
APPROVED_CONTACTS=+9876543210,+1122334455

# Generate a random string (32+ characters)
ENCRYPTION_KEY=randomly-generated-secure-key-minimum-32-chars
```

**Save and close** (Ctrl+O, Enter, Ctrl+X in nano)

### Step 3: Run (2 minutes)

```bash
# Start the bot
python main.py bot
```

**What happens:**
1. Chrome opens with WhatsApp Web
2. Scan QR code with your phone
3. Bot starts monitoring approved contacts
4. Auto-replies to messages!

## 🎉 You're Done!

The bot is now running and will:
- ✅ Monitor messages from approved contacts
- ✅ Generate AI responses in your style
- ✅ Store chat history securely
- ✅ Auto-reply within 10 seconds

## 📱 Test It

1. Send a message from an approved contact to your WhatsApp
2. Watch the bot console - you'll see the message
3. Check WhatsApp - AI response sent!

## 🎨 Optional: Web Dashboard

In a **new terminal**:

```bash
cd digi.Me
python main.py dashboard
```

Open browser: `http://localhost:5000`

**Default login:**
- Username: `admin`
- Password: `changeme123` (change this in `.env`!)

## 🛠️ Customize Your Style

Edit `chat-style/my_style.json` to match your personality:

```json
{
  "personality": {
    "tone": "friendly and casual",
    "formality": "informal",
    "emoji_usage": "occasional"
  },
  "phrases_i_use": ["honestly", "you know", "totally"]
}
```

Restart the bot to apply changes.

## 🔥 Tips

**Tip 1: Test before auto-reply**
```env
AUTO_REPLY_ENABLED=false  # In .env
```
Use dashboard to test responses first!

**Tip 2: Faster responses**
```env
CHECK_INTERVAL_SECONDS=5  # In .env (default is 10)
```

**Tip 3: Shorter responses**
```env
MAX_RESPONSE_LENGTH=200  # In .env (default is 500)
```

## ⚠️ Important

- **Keep `.env` secret** - Never share or commit it
- **Use strong encryption key** - At least 32 random characters
- **Change default password** - Don't use 'changeme123'
- **Verify approved contacts** - Only trusted numbers!

## 📚 Learn More

- [Full README](README.md) - Complete features and documentation
- [Setup Guide](SETUP_GUIDE.md) - Detailed setup instructions
- [Usage Examples](USAGE_EXAMPLES.md) - Code examples and recipes

## 🐛 Common Issues

**"No module named X"**
```bash
pip install -r requirements.txt
```

**"OPENAI_API_KEY is required"**
- Make sure you copied `.env.example` to `.env`
- Add your API key to `.env`

**"Chrome driver not found"**
```bash
pip install --upgrade webdriver-manager
```

**"QR code doesn't appear"**
- Make sure Chrome is installed
- Check terminal for errors

## 🎯 Next Steps

1. ✅ Bot is running
2. ✅ Test with approved contacts
3. ✅ Check dashboard
4. ⬜ Customize your chat style
5. ⬜ Add more example conversations
6. ⬜ Adjust settings in `.env`

## 💬 Need Help?

- Check [Troubleshooting](README.md#-troubleshooting) in README
- Review [SETUP_GUIDE.md](SETUP_GUIDE.md) for details
- Open an issue on GitHub

---

**You're all set! Your AI twin is now handling your WhatsApp messages.** 🤖✨
