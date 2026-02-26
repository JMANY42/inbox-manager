from dotenv import load_dotenv
import os
import requests

load_dotenv()
def get_emails():
    outlook_access_token = os.getenv("OUTLOOK_ACCESS_TOKEN")
    messages = get_all_outlook_messages(
        access_token=outlook_access_token,
            select="id,subject,body,from",
        )
    return messages

def get_all_outlook_messages(access_token: str, user_id: str = "me", **kwargs) -> list[dict]:
    session = requests.Session()
    session.headers.update({
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
    })
    params = {"$top": kwargs.get("top", 100)}
    if "select" in kwargs:
        params["$select"] = kwargs["select"]
    if "filter" in kwargs:
        params["$filter"] = kwargs["filter"]
    if "orderby" in kwargs:
        params["$orderby"] = kwargs["orderby"]

    url = f"https://graph.microsoft.com/v1.0/{user_id}/mailFolders/inbox/messages"
    all_messages = []

    while url:
        response = session.get(url, params=params if not all_messages else None)
        response.raise_for_status()
        data = response.json()
        all_messages.extend(data.get("value", []))
        url = data.get("@odata.nextLink")
    return all_messages
