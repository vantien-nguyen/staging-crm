import json
import logging
import os

from django.core.files import File
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseUpload

logger = logging.getLogger(__file__)


def get_object_or_none(classmodel, **kwargs):
    try:
        return classmodel.objects.get(**kwargs)
    except classmodel.MultipleObjectsReturned as _:
        logger.error(f"Multiple objects returned of model {classmodel}")
    except classmodel.DoesNotExist:
        return None


def upload_file(file: File) -> str:
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    credentials_json = json.loads(os.getenv("GOOGLE_DRIVE_CREDENTIALS_JSON"))
    credentials = Credentials.from_service_account_info(credentials_json, scopes=SCOPES)
    drive_service = build("drive", "v3", credentials=credentials)
    media = MediaIoBaseUpload(file.file, mimetype=file.content_type, resumable=True)

    try:
        uploaded_file = (
            drive_service.files()
            .create(
                body={"name": file.name},
                media_body=media,
                fields="id",
            )
            .execute()
        )
        logger.info(f"File {file.name} uploaded successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return ""

    drive_service.permissions().create(
        fileId=uploaded_file.get("id"), body={"type": "anyone", "role": "reader"}
    ).execute()

    return "https://drive.google.com/file/d/{}/view".format(uploaded_file.get("id"))


def delete_file(file: File) -> bool:
    SCOPES = ["https://www.googleapis.com/auth/drive.file"]
    credentials_json = json.loads(os.getenv("GOOGLE_DRIVE_CREDENTIALS_JSON"))
    credentials = Credentials.from_service_account_info(credentials_json, scopes=SCOPES)
    drive_service = build("drive", "v3", credentials=credentials)
    file_id = file.url.split("/")[5]

    try:
        drive_service.files().delete(fileId=file_id).execute()
        logger.info(f"File with ID {file_id} deleted successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        return False

    return True
