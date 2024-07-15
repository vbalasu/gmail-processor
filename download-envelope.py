import os.path
import json
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from datetime import datetime
from dateutil import parser
from termcolor import colored

# If modifying these SCOPES, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def to_iso(date_string):
    try:
        output_date = parser.parse(date_string)
        return output_date.isoformat()
    except ValueError:
        return None
    
def main():
    """Fetches all unread emails' envelope information and saves it as JSON."""
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time.
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

    email_data = []
    page_token = None

    ctr = 0
    while True:
        # Call the Gmail API to fetch unread messages
        results = service.users().messages().list(userId='me', q='is:unread category:primary', pageToken=page_token).execute()
        messages = results.get('messages', [])
        page_token = results.get('nextPageToken')

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
                    print(colored(header['value'], 'yellow'))
                    email_info['date'] = to_iso(header['value'])
            email_data.append(email_info)
            ctr = ctr + 1; print(ctr, email_info)

        if not page_token:
            break

    with open('unread_emails.json', 'w') as outfile:
        json.dump(email_data, outfile, indent=4)

    print(f'Successfully saved {len(email_data)} unread emails to unread_emails.json.')

if __name__ == '__main__':
    main()
