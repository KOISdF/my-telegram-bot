from pathlib import Path
from dotenv import load_dotenv
import os

# Загружаем .env
env_path = Path(__file__).parent / ".env"
print(f"Путь к .env: {env_path} | Существует: {env_path.exists()}")
load_dotenv(dotenv_path=env_path)

# Выводим переменные
print("BOT_TOKEN:", os.environ.get("BOT_TOKEN"))
print("ADMIN_ID:", os.environ.get("ADMIN_ID"))
print("GROUP_ID:", os.environ.get("GROUP_ID"))
