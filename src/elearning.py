import sys
import re
import html2text
from dateutil import parser
from zoneinfo import ZoneInfo

from google_api import get_homework_list, get_assignment_list, add_assignment, update_assignment, complete_assignment

def assignment_due_soon(message):
    # extract class, assignment, and due date
    # check task
    # update/create task
    # upload task to google calander

    class_number, assignment_name, due_date = extract_info(message["body"]["content"])    
    
    # convert due date format
    due_date = convert_due_date(due_date)

    # create new task body
    title = f"{class_number}: {assignment_name}"
    new_task_body = {
        "title": title,
        "notes": "Added automatically by inbox-manager",
        "due": due_date,
    }
    
    # get google api ids
    homework_list_id, assignment_id = get_api_ids(title)
    
    # update or add new assignment
    if assignment_id:
        update_assignment(homework_list_id, assignment_id, new_task_body)
    else:
        add_assignment(homework_list_id, new_task_body)

def assignment_submitted(message):
    # extract class, assignment, and due date
    # update task to completed
    # upload task to google calander
    class_number, assignment_name, due_date = extract_info(message["body"]["content"])
    
    # compose title
    title = f"{class_number}: {assignment_name}"
    
    # get google api ids
    homework_list_id, assignment_id = get_api_ids(title)

    if not assignment_id:
        sys.exit(f"ERROR: Error fetching assingment id\n\tassignment: {title}")
    # mark the assignemt completed
    complete_assignment(homework_list_id, assignment_id)

def get_api_ids(title):
    homework_list = get_homework_list()
    homework_list_id = homework_list["id"]
    assignment_list = get_assignment_list(homework_list_id)
    assignment_id = get_assignment_id(assignment_list, title)
    return homework_list_id, assignment_id


def extract_info(message):
    text = html2text.html2text(message)
    # Extract class number (the 4-digit course number after CS-)
    class_match = re.search(r'CS-(\d{4})-', text)
    class_number = 'CS '+class_match.group(1) if class_match else None

    # Extract assignment name
    assignment_match = re.search(r'^(?:\|\s+(?!\|)|Title:\s+)(.+)', text, re.MULTILINE)
    assignment_name = assignment_match.group(1).strip() if assignment_match else None

    # Extract due date
    due_match = re.search(r'Due (.+)', text)
    due_date = due_match.group(1).strip() if due_match else None

    if not (class_number and assignment_name and (due_date or "submission" in text)):
        sys.exit(f'ERROR: Error extracting information\n\tClass Number: ${class_number}\n\tAssignment Name: ${assignment_name}\n\tDue Date: ${due_date}')
    
    return class_number, assignment_name, due_date

def get_assignment_id(assignment_list, title):
    for assignment in assignment_list:
        if assignment["title"] == title:
            return assignment["id"]
    return None

def convert_due_date(date_str):
    tzinfos = {
        "CST": ZoneInfo("America/Chicago")
    }
    dt = parser.parse(date_str, tzinfos=tzinfos)
    # Use midnight UTC on the local date, ignoring the actual time
    return dt.strftime("%Y-%m-%dT00:00:00.000Z")