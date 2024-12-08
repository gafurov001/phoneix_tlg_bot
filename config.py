import os

from dotenv import load_dotenv

load_dotenv()

bot_token: str = os.getenv("BOT_TOKEN")
group_id_1 = int(os.getenv("GROUP_ID_1"))
group_id_2 = int(os.getenv("GROUP_ID_2"))


secret_key: str = os.getenv('SECRET_KEY')
username: str = os.getenv('ADMIN_USERNAME')
password: str = os.getenv('ADMIN_PASSWORD')