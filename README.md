# Email Automation System

## Overview
This project is a Python-based email automation system built using Flask, Celery, Redis, and MongoDB. The system allows users to send, reply, and manage emails efficiently through an API. The app uses asynchronous tasks for sending emails to ensure smooth operation, even when handling multiple requests. The system also integrates email fetching and moving messages to the inbox.

## Features
- Send emails asynchronously using Celery.
- Fetch emails for users from external sources.
- Add new emails to the database.
- Reply to emails with predefined content.
- Move emails to the inbox.
- CRUD operations for email management and user management.

## Dependencies
- Python 3.x
- Flask
- Flask-Cors (for cross-origin requests)
- Celery (for asynchronous tasks)
- Redis (message broker for Celery)
- MongoDB (for storing user and email data)
- Requests (for HTTP requests)

## Setup

### Step 1: Install Required Libraries
Run the following command to install the required dependencies:
```bash
pip install -r requirements.txt
```
### Step 2: Install and Configure Redis
To use Celery, you need to have Redis installed as the message broker. Follow these steps:

Install Redis:
On Linux/macOS: brew install redis
On Windows: Use WSL or Docker.
Start Redis server:
```bash
redis-server
```

### Step 3: Set Up MongoDB
Ensure MongoDB is running and accessible. You can install it from here.

### Step 4: Create config/credentials.json for Email API (If applicable)
If you’re using a service like Gmail, create a config/credentials.json file with your credentials. Ensure that the correct credentials are provided for the service.

### Step 5: Configure the App
No additional configuration is needed unless you're integrating a specific email service. However, ensure Redis and MongoDB are set up correctly as the app depends on them for messaging and data storage.

### Step 6: Implement Email Logic
The email logic is defined in the app/email_handler.py file, where functions like send_email, fetch_emails, and move_email_to_inbox are implemented.

### Step 7: Run the Application
Start the Flask app by running the following command:
```bash
python main.py
```
Start the Celery worker for asynchronous tasks:
```bash
celery -A main.celery worker --loglevel=info

```

### Step 8: API Endpoints
The following endpoints are available:

1. POST /send_email
Sends an email asynchronously.
Request body:
json
```bash
{
  "user_email": "user@example.com",
  "recipient": "recipient@example.com",
  "subject": "Test Subject",
  "body": "This is the email body"
}

```

2. GET /fetch_emails
Fetches emails for users and processes them.
3. GET /users
Retrieves a list of all users in the system.
4. GET /emails
Retrieves a list of all emails stored in the system.
5. POST /emails
Adds a new email to the database.

Request body:
```bash
{
  "sender": "sender@example.com",
  "receiver": "receiver@example.com",
  "subject": "Test Subject",
  "content": "This is the email content",
  "status": "sent"
}

```
6. POST /reply_email

Replies to an email.
Request body:
```bash
{
  "user_email": "user@example.com",
  "message_id": "unique_message_id",
  "reply_content": "This is the reply"
}

```
7. POST /move_to_inbox

Moves an email to the inbox.
Request body:
```bash
{
  "user_email": "user@example.com",
  "email_id": "unique_email_id"
}

```

### Step 9: Monitor Results
After starting the app and performing actions via Postman or other API clients, you should see the following logs:
```bash
(env) C:\Users\user\Desktop\EmailProgram>python main.py
 * Running on http://127.0.0.1:5000 (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 134-966-085
127.0.0.1 - - [24/Jan/2025 23:35:23] "POST /send_email HTTP/1.1" 202 -
127.0.0.1 - - [24/Jan/2025 23:35:55] "GET /emails HTTP/1.1" 200 -
127.0.0.1 - - [24/Jan/2025 23:36:30] "POST /move_to_inbox HTTP/1.1" 200 -

```
