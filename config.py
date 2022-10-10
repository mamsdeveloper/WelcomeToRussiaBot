import dotenv
from pathlib import Path

dotenv_path = Path.cwd() / '.env'
config = dotenv.dotenv_values(dotenv_path)

TOKEN = config['TOKEN']
ADMIN_CHAT_ID = config['ADMIN_CHAT_ID']
WEBHOOK_SECRET = config['WEBHOOK_SECRET']
WEBHOOK_HOST = config['WEBHOOK_HOST']
WEBHOOK_URL = WEBHOOK_HOST + WEBHOOK_SECRET
