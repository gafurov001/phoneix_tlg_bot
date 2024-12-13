import os

from dotenv import load_dotenv

load_dotenv()

bot_token: str = os.getenv("BOT_TOKEN")
group_id_1 = int(os.getenv("GROUP_ID_1"))
group_id_2 = int(os.getenv("GROUP_ID_2"))
amalyot_group_id = int(os.getenv("AMALIYOT_GROUP_ID"))
platforma_group_id = int(os.getenv("PLATFORMA_GROUP_ID"))


secret_key: str = os.getenv('SECRET_KEY')
username: str = os.getenv('ADMIN_USERNAME')
password: str = os.getenv('ADMIN_PASSWORD')