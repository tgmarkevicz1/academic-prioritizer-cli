import os
import stat
from dotenv import load_dotenv
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

load_dotenv()  # loads .env into environment variables

SCOPES = [
    "https://www.googleapis.com/auth/drive.metadata.readonly",
    "https://www.googleapis.com/auth/calendar.readonly"
]

ALLOWED_SERVICES = {"drive": "v3", "calendar": "v3"}
CREDENTIALS_PATH = os.environ.get("GOOGLE_CREDENTIALS_PATH", "secrets/credentials.json")
TOKEN_PATH = os.environ.get("GOOGLE_TOKEN_PATH", "token.json")


def get_service(service_name, version):
    if service_name not in ALLOWED_SERVICES:
        raise ValueError(f"Unsupported service: {service_name}")

    creds = None

    if os.path.exists(TOKEN_PATH):
        creds = Credentials.from_authorized_user_file(TOKEN_PATH, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDENTIALS_PATH):
                raise FileNotFoundError(f"Credentials file not found: {CREDENTIALS_PATH}")
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)

        with open(TOKEN_PATH, "w") as token:
            token.write(creds.to_json())
        os.chmod(TOKEN_PATH, stat.S_IRUSR | stat.S_IWUSR)  # chmod 600

    return build(service_name, version, credentials=creds)