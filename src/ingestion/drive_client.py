from .google_auth import get_service

def get_drive_files():
    service = get_service("drive", "v3")

    results = service.files().list(
        pageSize=20,
        fields="files(id, name, modifiedTime)"
    ).execute()

    return results.get("files", [])
