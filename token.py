import os
import argparse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# If modifying these scopes, delete the file token.json.
# 'https://www.googleapis.com/auth/drive.file' allows uploading and managing 
# files created or opened by this app.
SCOPES = ['https://www.googleapis.com/auth/drive.file']

def authenticate_gdrive(credentials_file):
    """Authenticates the user and generates token.json."""
    creds = None
    
    # The file token.json stores the user's access and refresh tokens.
    # It is created automatically when the authorization flow completes for the first time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # You must download 'credentials.json' from your Google Cloud Console
            flow = InstalledAppFlow.from_client_secrets_file(
                credentials_file, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    print("token.json generated successfully.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate token.json for Google Drive API.")
    parser.add_argument('--oath', required=True, help="Path to credentials.json")
    args = parser.parse_args()

    if os.path.exists(args.oath):
        authenticate_gdrive(args.oath)
    else:
        print(f"Error: Credentials file '{args.oath}' not found.")
