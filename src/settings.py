from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_PASSWD = os.getenv("MONGODB_PASSWD")
DB_NAME = os.getenv("DB_NAME")
DB_URI = f"mongodb+srv://powercat_server:{MONGODB_PASSWD}@powercatdb.7m1t69i.mongodb.net/?retryWrites=true&w=majority&appName=PowercatDB"
