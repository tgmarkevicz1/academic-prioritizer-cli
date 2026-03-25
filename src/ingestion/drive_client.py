import os
from .google_auth import get_service

FOLDER_ID = os.environ.get("GOOGLE_DRIVE_FOLDER_ID")


def get_files_in_folder(service, folder_id):
    """Recursively get all files within a folder and its subfolders."""
    all_files = []
    page_token = None

    while True:
        results = service.files().list(
            q=f"'{folder_id}' in parents and trashed=false",
            fields="nextPageToken, files(id, name, modifiedTime, mimeType)",
            pageToken=page_token,
        ).execute()

        items = results.get("files", [])

        for item in items:
            if item["mimeType"] == "application/vnd.google-apps.folder":
                all_files.extend(get_files_in_folder(service, item["id"]))
            else:
                all_files.append(item)

        page_token = results.get("nextPageToken")
        if not page_token:
            break

    return all_files


def get_drive_files():
    service = get_service("drive", "v3")
    return get_files_in_folder(service, FOLDER_ID)
