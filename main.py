from flask import Flask, jsonify, request
from flask_cors import CORS
from app.email_handler import fetch_emails, reply_email, send_email, move_email_to_inbox
from app.database import users_collection, emails_collection
from datetime import datetime
from celery import Celery

app = Flask(__name__)
celery = Celery(app.name, broker="redis://localhost:6379/0")
CORS(app)

# Celery task to send email asynchronously
@celery.task
def send_email_task(user_email, recipient, subject, body):
    send_email(user_email, recipient, subject, body)
    
@app.route('/send_email', methods=['POST'])
def send_an_email():
    data = request.json
    user_email = data["user_email"]
    recipient = data["recipient"]
    subject = data["subject"]
    body = data["body"]
    send_email_task.apply_async(args=[user_email, recipient, subject, body])  # Send asynchronously using Celery
    return "Email send request submitted!", 202

@app.route('/fetch_emails', methods=['GET'])
def fetch_all_emails():
    try:
        users = users_collection.find()
        for user in users:
            fetch_emails(user["email"])
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    return jsonify({"message": "Emails fetched successfully!"}), 200

# Endpoint to fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    users = list(users_collection.find({}, {'_id': 0}))  # Exclude MongoDB '_id'
    return jsonify(users), 200

# Endpoint to fetch all emails
@app.route('/emails', methods=['GET'])
def get_emails():
    emails = list(emails_collection.find({}, {'_id': 0}))  # Exclude MongoDB '_id'
    return jsonify(emails), 200

# Endpoint to add a new email
@app.route('/emails', methods=['POST'])
def add_email():
    data = request.json

    # Validate input
    required_fields = ["sender", "receiver", "subject", "content", "status"]
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Field '{field}' is missing"}), 400

    # Prepare email document
    email = {
        "sender": data["sender"],
        "receiver": data["receiver"],
        "subject": data["subject"],
        "content": data["content"],
        "sent_at": datetime.utcnow().isoformat() + "Z",  # Current UTC time in ISO format
        "status": data["status"]
    }

    # Insert into the collection
    emails_collection.insert_one(email)
    return jsonify({"message": "Email sent successfully!"}), 201

@app.route('/reply_email', methods=['POST'])
def reply_to_email():
    data = request.json
    user_email = data["user_email"]
    message_id = data["message_id"]
    reply_content = data["reply_content"]
    reply_email(user_email, message_id, reply_content)
    return "Reply sent successfully!"

@app.route('/move_to_inbox', methods=['POST'])
def move_email():
    data = request.json
    user_email = data["user_email"]
    email_id = data["email_id"]
    move_email_to_inbox(user_email, email_id)
    return "Email moved to Inbox successfully!"

if __name__ == '__main__':
    app.run(debug=True)

