from app.database import users_collection, emails_collection
from app.oauth_utils import get_google_service
from googleapiclient.errors import HttpError

def fetch_emails(user_email):
    # Fetch user from the database
    user = users_collection.find_one({"email": user_email})
    if not user:
        return {"error": f"User {user_email} not found!"}

    try:
        # Get Google service instance
        service = get_google_service("config/credentials.json", f"tokens/{user_email}.json")

        # Fetch emails from user's inbox
        results = service.users().messages().list(userId="me", labelIds=["INBOX"]).execute()
        messages = results.get("messages", [])

        if not messages:
            return {"message": f"No new emails for user {user_email}."}

        bulk_operations = []
        for msg in messages:
            # Fetch detailed email data
            msg_data = service.users().messages().get(userId="me", id=msg["id"]).execute()

            # Extract required fields
            subject = next((header['value'] for header in msg_data['payload']['headers'] if header['name'] == "Subject"), "")
            sender = next((header['value'] for header in msg_data['payload']['headers'] if header['name'] == "From"), "")

            # Prepare email record
            email_record = {
                "user_email": user_email,
                "email_id": msg["id"],
                "subject": subject,
                "sender": sender,
                "labels": msg_data.get("labelIds", []),
            }

            # Add bulk update operation
            bulk_operations.append(
                pymongo.UpdateOne(
                    {"email_id": msg["id"]},
                    {"$set": email_record},
                    upsert=True
                )
            )

        # Execute bulk operations
        if bulk_operations:
            emails_collection.bulk_write(bulk_operations)

        return {"message": f"Fetched and stored emails for user {user_email}."}

    except HttpError as e:
        return {"error": f"Google API error: {e}"}
    except Exception as e:
        return {"error": f"An error occurred: {e}"}

def reply_email(user_email, message_id, reply_content):
    service = get_google_service("config/credentials.json", f"tokens/{user_email}.json")
    # Fetch the original email to get threadId
    original_email = service.users().messages().get(userId="me", id=message_id).execute()
    thread_id = original_email.get("threadId")

    # Prepare the reply
    message = {
        "raw": base64.urlsafe_b64encode(
            f"To: {user_email}\r\n"
            f"Subject: Re: {original_email['payload']['headers']['Subject']}\r\n\r\n"
            f"{reply_content}".encode("utf-8")
        ).decode("utf-8"),
        "threadId": thread_id,
    }

    # Send the reply
    service.users().messages().send(userId="me", body=message).execute()

def send_email(user_email, recipient, subject, body):
    service = get_google_service("config/credentials.json", f"tokens/{user_email}.json")

    # Prepare the message
    message = {
        "raw": base64.urlsafe_b64encode(
            f"To: {recipient}\r\n"
            f"Subject: {subject}\r\n\r\n"
            f"{body}".encode("utf-8")
        ).decode("utf-8"),
    }

    # Send the email
    service.users().messages().send(userId="me", body=message).execute()

def move_email_to_inbox(user_email, email_id):
    service = get_google_service("config/credentials.json", f"tokens/{user_email}.json")

    try:
        # Use the Gmail API to move the email
        result = service.users.messages.modify(
            userId=user_email,
            id=email_id,
            body={"removeLabelIds": ["INBOX"], "addLabelIds": ["INBOX"]}
        ).execute()

        print(f"Email {email_id} moved to Inbox for user {user_email}.")
        return result
    except Exception as e:
        print(f"An error occurred: {e}")
        raise
