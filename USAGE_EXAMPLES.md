# Usage Examples for digi.Me

This document provides practical examples of using digi.Me in various scenarios.

## Basic Usage

### Starting the Bot

```bash
# Simple bot start
python main.py bot

# The bot will:
# 1. Load configuration from .env
# 2. Connect to WhatsApp Web
# 3. Monitor approved contacts
# 4. Auto-reply with AI-generated responses
```

### Starting the Dashboard

```bash
# Start web interface
python main.py dashboard

# Access at: http://localhost:5000
# Login with credentials from .env
```

### Running Both Services

```bash
# Terminal 1: Dashboard
python main.py dashboard

# Terminal 2: Bot
python main.py bot
```

## Configuration Examples

### Example 1: Using OpenAI

```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-abc123...
APPROVED_CONTACTS=+1234567890,+19876543210
ENCRYPTION_KEY=my-super-secret-key-32-chars-min
AUTO_REPLY_ENABLED=true
CHECK_INTERVAL_SECONDS=10
```

### Example 2: Using Cohere

```env
AI_PROVIDER=cohere
COHERE_API_KEY=your-cohere-key-here
APPROVED_CONTACTS=+442071234567
ENCRYPTION_KEY=another-secure-encryption-key
AUTO_REPLY_ENABLED=true
CHECK_INTERVAL_SECONDS=15
```

### Example 3: Manual Mode Only

```env
AI_PROVIDER=openai
OPENAI_API_KEY=sk-proj-abc123...
APPROVED_CONTACTS=+1234567890
ENCRYPTION_KEY=my-secure-key
AUTO_REPLY_ENABLED=false  # Disable auto-reply
```

## Chat Style Examples

### Example 1: Professional Style

```json
{
  "name": "Professional Assistant",
  "personality": {
    "tone": "professional and courteous",
    "formality": "formal",
    "humor": "minimal",
    "emoji_usage": "rare",
    "response_length": "concise"
  },
  "phrases_i_use": [
    "Thank you for",
    "I appreciate",
    "Please let me know",
    "I'll be happy to assist"
  ],
  "phrases_i_avoid": [
    "gonna",
    "wanna",
    "yeah"
  ],
  "response_rules": {
    "max_length": 300,
    "use_contractions": false,
    "capitalization": "proper",
    "punctuation_style": "formal"
  }
}
```

### Example 2: Casual Friend Style

```json
{
  "name": "Casual Friend",
  "personality": {
    "tone": "warm and friendly",
    "formality": "very informal",
    "humor": "high",
    "emoji_usage": "frequent",
    "response_length": "medium"
  },
  "phrases_i_use": [
    "haha",
    "lol",
    "dude",
    "awesome",
    "totally",
    "for sure"
  ],
  "language_patterns": {
    "greetings": ["Heyyy!", "Yo!", "What's good?", "Sup!"],
    "farewells": ["Later!", "Peace!", "Catch ya later!", "Cya!"]
  },
  "response_rules": {
    "max_length": 500,
    "use_contractions": true,
    "capitalization": "casual",
    "punctuation_style": "minimal"
  }
}
```

### Example 3: Tech Expert Style

```json
{
  "name": "Tech Expert",
  "personality": {
    "tone": "knowledgeable and helpful",
    "formality": "semi-formal",
    "humor": "moderate",
    "emoji_usage": "occasional"
  },
  "phrases_i_use": [
    "actually",
    "basically",
    "in terms of",
    "essentially",
    "from a technical standpoint"
  ],
  "example_conversations": [
    {
      "context": "How do I fix this bug?",
      "my_response": "Let me help you debug that. First, check the console logs to see what error message you're getting. Then we can trace it back to the source."
    },
    {
      "context": "Which framework should I use?",
      "my_response": "It really depends on your use case. For rapid prototyping, I'd recommend Flask. For larger apps with more features, Django might be better. What are you building?"
    }
  ]
}
```

## API Usage Examples

### Accessing Chat History

```python
from src.storage.database import ChatDatabase
from src.config import Config

# Initialize database
db = ChatDatabase(Config.DATABASE_PATH, Config.ENCRYPTION_KEY)

# Get conversation with a contact
messages = db.get_conversation("+1234567890", limit=50)

for msg in messages:
    sender = "Me" if msg['is_me'] else msg['contact']
    print(f"{sender}: {msg['message']}")
```

### Updating Chat Style Programmatically

```python
from src.ai.chat_style import ChatStyle
from src.config import Config

# Load style
style = ChatStyle(Config.CHAT_STYLE_PATH)

# Add new example
style.add_example_conversation(
    context="What's the weather like?",
    response="Not sure, haven't checked yet. But it was pretty nice earlier!"
)

# Update personality
style.update_style({
    "personality": {
        "emoji_usage": "frequent"
    }
})
```

### Generating Manual Response

```python
from src.ai.chat_style import ChatStyle
from src.ai.response_generator import ResponseGenerator
from src.config import Config

# Initialize
style = ChatStyle(Config.CHAT_STYLE_PATH)
generator = ResponseGenerator(style)

# Generate response
response = generator.generate_response(
    message="Hey, how are you?",
    context=[],
    sender_name="John"
)

print(response)
```

## Dashboard Usage

### Reviewing Conversations

1. Login to dashboard at `http://localhost:5000`
2. Click on "Chats" tab
3. Select a contact from the sidebar
4. View full conversation history
5. Messages sent by AI are highlighted in green

### Updating Chat Style

1. Go to "Chat Style" tab
2. Edit individual fields or full JSON
3. Click "Save Style"
4. Changes take effect immediately for new responses

### Viewing Configuration

1. Go to "Configuration" tab
2. View current settings:
   - AI provider
   - Auto-reply status
   - Check interval
   - Max response length

## Advanced Scenarios

### Scenario 1: Different Styles for Different Contacts

Create multiple style files:

```bash
chat-style/
├── professional.json
├── casual.json
└── tech.json
```

Switch styles by updating `.env`:

```env
CHAT_STYLE_PATH=chat-style/professional.json
```

### Scenario 2: Training from Chat History

```python
from src.storage.database import ChatDatabase
from src.ai.chat_style import ChatStyle
from src.config import Config

db = ChatDatabase(Config.DATABASE_PATH, Config.ENCRYPTION_KEY)
style = ChatStyle(Config.CHAT_STYLE_PATH)

# Get your messages
conversations = db.get_all_conversations(limit_per_contact=20)

# Extract your responses to train style
for contact, messages in conversations.items():
    for msg in messages:
        if msg['is_me'] and not msg['replied_by_ai']:
            # This is your actual response
            prev_msg = [m for m in messages if not m['is_me']]
            if prev_msg:
                style.add_example_conversation(
                    context=prev_msg[-1]['message'],
                    response=msg['message']
                )
```

### Scenario 3: Monitoring Bot Health

```python
from src.whatsapp.connector import WhatsAppConnector

# In a monitoring script
connector = WhatsAppConnector()
connector.connect()

# Check connection status
try:
    chats = connector.get_all_chats()
    print(f"Connected! Found {len(chats)} chats")
except Exception as e:
    print(f"Connection failed: {e}")
    # Send alert to admin
```

## Troubleshooting Examples

### Check Configuration

```python
from src.config import Config

# Validate configuration
errors = Config.validate()
if errors:
    print("Configuration errors:")
    for error in errors:
        print(f"  - {error}")
else:
    print("Configuration is valid!")
```

### Test Database Connection

```python
from src.storage.database import ChatDatabase
from src.config import Config

try:
    db = ChatDatabase(Config.DATABASE_PATH, Config.ENCRYPTION_KEY)
    contacts = db.get_approved_contacts()
    print(f"Database OK. Found {len(contacts)} approved contacts")
except Exception as e:
    print(f"Database error: {e}")
```

### Test AI Connection

```python
from src.ai.chat_style import ChatStyle
from src.ai.response_generator import ResponseGenerator
from src.config import Config

try:
    style = ChatStyle(Config.CHAT_STYLE_PATH)
    gen = ResponseGenerator(style)
    response = gen.generate_response("Test message")
    print(f"AI OK. Response: {response}")
except Exception as e:
    print(f"AI error: {e}")
```

## Best Practices

### 1. Start with Manual Mode

When first setting up:
```env
AUTO_REPLY_ENABLED=false
```

Test responses in the dashboard before enabling auto-reply.

### 2. Use Descriptive Contact Names

Store contact names in database:
```python
db.add_approved_contact("+1234567890", "John Smith")
```

### 3. Regular Style Updates

Review conversations weekly and add good examples to your style:
```bash
# Check dashboard for natural conversations
# Add them to chat-style/my_style.json
```

### 4. Backup Your Data

```bash
# Backup chat database
cp chat_data/chat_history.db chat_data/backup_$(date +%Y%m%d).db

# Backup chat style
cp chat-style/my_style.json chat-style/backup_$(date +%Y%m%d).json
```

### 5. Monitor API Usage

Check your API provider's usage dashboard regularly to avoid unexpected costs.

---

**Happy automating with digi.Me!** 🤖
