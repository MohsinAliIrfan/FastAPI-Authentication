from pymongo import MongoClient
client = MongoClient("mongodb+srv://Mohsin:pakistan123@firstclusterforlearning.rfwfbuk.mongodb.net/")
db = client["Admin_Authentication"]

users = db["admin_data"]
