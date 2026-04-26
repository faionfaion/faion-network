# .env.tpl — 1Password inject template
# Usage: op inject -i .env.tpl -o .env && chmod 600 .env
#
# Requires: op CLI + OP_SERVICE_ACCOUNT_TOKEN in environment
# Safe to commit: contains vault references, not actual secrets

# Database
DATABASE_URL={{ op://ServerVault/Database/url }}

# Redis (not a secret, literal value is fine)
REDIS_URL=redis://localhost:6379/0

# Message Broker
RABBITMQ_URL={{ op://ServerVault/RabbitMQ/url }}

# AI Keys
ANTHROPIC_API_KEY={{ op://ServerVault/Anthropic/api-key }}

# Authentication
JWT_SECRET={{ op://ServerVault/JWT/secret }}
JWT_ALGORITHM=HS256
JWT_EXPIRATION_MINUTES=1440

# Telegram
TELEGRAM_BOT_TOKEN={{ op://ServerVault/TelegramBot/token }}
TELEGRAM_CHAT_ID={{ op://ServerVault/TelegramBot/chat-id }}

# Application (non-secret literal values)
LOG_LEVEL=INFO
DEBUG=false
ENVIRONMENT=production
