# gmail-processor

https://chatgpt.com/share/49b4a4f0-b2d0-4e23-9e8e-80b16bd17b67


## How to quickly download only the envelope information (from, to, subject, date) for all unread Gmail messages? I want to leave the messages unread on the server, and download this information as JSON to my local machine

To quickly download only the envelope information (from, to, subject, date) for all unread Gmail messages, you can use the Gmail API provided by Google. The following steps outline how to achieve this using Python:

### Prerequisites
1. **Google Cloud Project**: Set up a Google Cloud project and enable the Gmail API.
2. **OAuth 2.0 Credentials**: Create OAuth 2.0 credentials for desktop applications and download the `credentials.json` file.
3. **Python Environment**: Ensure you have Python installed along with the `google-auth`, `google-auth-oauthlib`, `google-auth-httplib2`, and `google-api-python-client` libraries. You can install these using pip:

    ```bash
    pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client
    ```

### Steps to Download Envelope Information

1. **Set Up Authentication**: Use the `credentials.json` to authenticate your application and get access to the Gmail API.

2. **Fetch Unread Emails**: Use the Gmail API to fetch the list of unread emails.

3. **Extract Envelope Information**: Extract the required envelope information from the fetched emails.

4. **Save as JSON**: Save the extracted information in a JSON file.

Here’s a Python script that demonstrates these steps:


[download-envelope.py](./download-envelope.py)

### Explanation
1. **Authentication**: The script first handles authentication. If a valid token exists (`token.json`), it uses it. Otherwise, it initiates the OAuth 2.0 flow.
2. **Fetch Messages**: It then fetches unread messages using the `list` method with the query parameter `q='is:unread'`.
3. **Extract Headers**: For each message, it retrieves the headers (from, to, subject, date) and appends this information to a list.
4. **Save to JSON**: Finally, it saves the collected data into a JSON file (`unread_emails.json`).

### Notes
- Ensure that the `credentials.json` file is in the same directory as your script.
- The script fetches only the envelope information and leaves the messages unread on the server.
- You can modify the script to fetch additional headers if needed.

This script should help you quickly download the envelope information of unread Gmail messages and save it as a JSON file on your local machine.

## What is the expected output? Show a sample unread_emails.json

The expected output of the script is a JSON file (`unread_emails.json`) containing an array of objects, each representing an unread email with its envelope information (from, to, subject, date). 

Here is a sample `unread_emails.json` file:

```json
[
    {
        "id": "176b29a1c34a9a3e",
        "from": "example.sender@gmail.com",
        "to": "your.email@gmail.com",
        "subject": "Meeting Reminder",
        "date": "Mon, 14 Jul 2024 09:30:00 -0700"
    },
    {
        "id": "176b29a1c34a9a3f",
        "from": "newsletter@news.com",
        "to": "your.email@gmail.com",
        "subject": "Weekly Newsletter",
        "date": "Sun, 13 Jul 2024 16:00:00 -0700"
    },
    {
        "id": "176b29a1c34a9a40",
        "from": "friend@example.com",
        "to": "your.email@gmail.com",
        "subject": "Let's catch up!",
        "date": "Fri, 11 Jul 2024 18:45:00 -0700"
    }
]
```


### Explanation of the JSON structure:

- **id**: The unique identifier of the email message.
- **from**: The sender's email address.
- **to**: The recipient's email address (your email).
- **subject**: The subject line of the email.
- **date**: The date and time when the email was sent.

Each object in the array represents one unread email, containing the essential envelope information without the email's body content. This output helps you keep track of unread messages while leaving them unread on the server.