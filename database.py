from pymongo import MongoClient

# NOTE: In production, move this to a .env file
# For development, using direct connection string
client = MongoClient("mongodb+srv://<db_user>:<db_password>@todo-alerter.w2fgmqz.mongodb.net/")
db = client["financeapp"]



users_collection = db["users"]
records_collection = db["records"]