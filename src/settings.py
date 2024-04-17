from dotenv import load_dotenv
import os

load_dotenv()
MONGODB_PASSWD = os.getenv("MONGODB_PASSWD")
DB_URI = f"mongodb+srv://powercat_server:{MONGODB_PASSWD}@cluster0.flwq2ws.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
DB_NAME = "powercat"