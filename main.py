import os.path
import time
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Scopes for full access to Gmail, including sending emails
SCOPES = ["https://www.googleapis.com/auth/gmail.modify",
          "https://www.googleapis.com/auth/gmail.send"]

def create_message(sender, to, subject, body):
    """Create a message to send."""
    message = MIMEText(body)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {'raw': raw_message}

def get_replied_messages(service):
    """Get a list of message IDs that have been replied to."""
    try:
        results = service.users().messages().list(userId="me", labelIds=['SENT'], q="subject:Re:").execute()
        messages = results.get("messages", [])
        return [msg['id'] for msg in messages]
    except HttpError as error:
        print(f"An error occurred while retrieving replied messages: {error}")
        return []

def get_unreplied_messages(service, replied_messages):
    """Get new messages that have not been replied to."""
    try:
        results = service.users().messages().list(userId="me", maxResults=10, labelIds=['INBOX'], q="").execute()
        messages = results.get("messages", [])
        new_messages = []
        for message_info in messages:
            message_id = message_info['id']
            if message_id not in replied_messages:
                new_messages.append(message_id)
        return new_messages
    except HttpError as error:
        print(f"An error occurred while retrieving new messages: {error}")
        return []

def main():
    creds = None
    # Check if token.json exists and load credentials
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If no valid credentials, initiate OAuth flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception as e:
                print(f"Failed to refresh token: {e}")
                creds = None
        if not creds:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the new credentials
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    # Build the Gmail service
    service = build("gmail", "v1", credentials=creds)
    
    # Keep track of replied messages
    replied_messages = get_replied_messages(service)

    while True:
        try:
            # Get new messages that haven't been replied to
            new_messages = get_unreplied_messages(service, replied_messages)

            if not new_messages:
                print("No new messages found.")
            else:
                for message_id in new_messages:
                    # Get the message details
                    message = service.users().messages().get(userId="me", id=message_id, format='full').execute()
                    headers = message['payload']['headers']
                    subject = next(header['value'] for header in headers if header['name'] == 'Subject')
                    from_ = next(header['value'] for header in headers if header['name'] == 'From')
                    
                    # Prepare and send a reply
                    reply_subject = f"Re: {subject}"
                    reply_body = "Thank you for your email. This is an automated reply."
                    reply_message = create_message("me", from_, reply_subject, reply_body)
                    service.users().messages().send(userId="me", body=reply_message).execute()
                    
                    # Add the message ID to the list of replied messages
                    replied_messages.append(message_id)
                    print(f"Replied to {from_} with message ID: {message_id}")
            
            # Sleep for a while before checking again
            time.sleep(60)  # Check every 60 seconds

        except HttpError as error:
            print(f"An error occurred: {error}")
            time.sleep(60)  # Sleep before retrying

if __name__ == "__main__":
    main()
