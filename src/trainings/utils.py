from src.database import DB

def get_current_training_id() -> int:
    data = DB["training"].find_one({"last_session": {"$exists": True}})
    return data['last_session']