from pymongo import MongoClient
from pymongo.errors import BulkWriteError
from app.config import MONGO_URI
from app.database import init_db

# Connect to MongoDB
client = MongoClient(MONGO_URI)

# Access the 'email_control' database
db = client['email_control']

# Insert sample user data into 'users' collection
user_data = [
    {
        "username": "john_doe",
        "email": "john.doe@example.com",
        "password": "hashed_password1",
        "subscription": "premium",
        "created_at": "2025-01-24T18:00:00Z"
    },
    {
        "username": "jane_smith",
        "email": "jane.smith@example.com",
        "password": "hashed_password2",
        "subscription": "basic",
        "created_at": "2025-01-23T15:00:00Z"
    },
    {
        "username": "suhani_mahajan",
        "email": "msuhani1947@gmail.com",
        "password": "hashed_password3",
        "subscription": "premium",
        "created_at": "2025-01-22T12:00:00Z"
    }
]

# Handle duplicates gracefully while inserting users
try:
    db.users.insert_many(user_data, ordered=False)  # 'ordered=False' allows partial inserts
    print("Sample users inserted successfully!")
except BulkWriteError as e:
    for error in e.details['writeErrors']:
        print(f"Duplicate entry for email: {error['keyValue']['email']}. Skipping...")

# Insert sample email data into 'emails' collection
email_data = [
    {
        "sender": "no-reply@example.com",
        "receiver": "john.doe@example.com",
        "subject": "Welcome to Our Service",
        "content": "Hello John, thank you for signing up for our service!",
        "sent_at": "2025-01-23T10:00:00Z",
        "status": "read"
    },
    {
        "sender": "support@example.com",
        "receiver": "jane.smith@example.com",
        "subject": "Support Ticket Update",
        "content": "Hi Jane, your support ticket #12345 has been resolved.",
        "sent_at": "2025-01-24T12:00:00Z",
        "status": "unread"
    },
    {
        "sender": "msuhani1947@gmail.com",
        "receiver": "anushamahajan5@gmail.com",
        "subject": "Meeting Reminder",
        "content": "Hi Anusha, this is a reminder for our meeting tomorrow.",
        "sent_at": "2025-01-25T09:00:00Z",
        "status": "unread"
    }
]

# Handle duplicates gracefully while inserting emails
try:
    db.emails.insert_many(email_data, ordered=False)  # 'ordered=False' allows partial inserts
    print("Sample emails inserted successfully!")
except BulkWriteError as e:
    for error in e.details['writeErrors']:
        print(f"Duplicate email detected: {error['keyValue']}. Skipping...")

# Initialize the database (if needed for additional setup)
init_db()

