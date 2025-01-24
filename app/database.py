from pymongo import MongoClient
from app.config import MONGO_URI

# Create MongoDB client
client = MongoClient(MONGO_URI)
db = client.get_database()

# Collections
users_collection = db['users']
emails_collection = db['emails']

# Initialize database function
def init_db():
    print("Initializing the database...")
    # Example: Ensure indexes or initial data setup
    users_collection.create_index("email", unique=True)
    print("Users collection index created.")

