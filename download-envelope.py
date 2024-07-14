import os.path
import json
import base64
import re
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('gmail', 'v1', credentials=creds)

    # Call the Gmail API
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])

    email_data = []

    if not messages:
        print('No unread messages found.')
    else:
        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id']).execute()
            headers = msg['payload']['headers']
            email_info = {
                "id": message['id']
            }
            for header in headers:
                if header['name'] == 'From':
                    email_info['from'] = header['value']
                if header['name'] == 'To':
                    email_info['to'] = header['value']
                if header['name'] == 'Subject':
                    email_info['subject'] = header['value']
                if header['name'] == 'Date':
                    email_info['date'] = header['value']
            email_data.append(email_info)

    with open('unread_emails.json', 'w') as outfile:
        json.dump(email_data, outfile, indent=4)

if __name__ == '__main__':
    main()
