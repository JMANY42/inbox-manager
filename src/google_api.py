import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/tasks"]
HOMEWORK_LIST_NAME = "Homework (from inbox-manager)"

_service = None

def _get_service():
    global _service
    if _service is not None:
        return _service

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    _service = build("tasks", "v1", credentials=creds)
    return _service

def get_homework_list():
    service = _get_service()
    all_lists = service.tasklists().list().execute()
    homework_list = next(
        (tl for tl in all_lists.get("items", []) if tl["title"] == HOMEWORK_LIST_NAME),
        None,
    )
    if homework_list is None:
        homework_list = service.tasklists().insert(body={"title": HOMEWORK_LIST_NAME}).execute()
    return homework_list

def get_assignment_list(homework_list_id):
    return _get_service().tasks().list(tasklist=homework_list_id).execute().get("items", [])

def add_assignment(homework_list_id, new_task_body):
    return _get_service().tasks().insert(tasklist=homework_list_id, body=new_task_body).execute()

def update_assignment(homework_list_id, assignment_id, new_task_body):
    return _get_service().tasks().patch(tasklist=homework_list_id, task=assignment_id, body=new_task_body).execute()

def complete_assignment(homework_list_id, assignment_id):
    return _get_service().tasks().patch(tasklist=homework_list_id, task=assignment_id, body={"status": "completed"}).execute()