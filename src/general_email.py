import html2text
from ollama import chat

def handle_general_email(message):
    email_str = preprocess(message)
    response = send_to_AI(email_str)
    process_response(response)

def preprocess(message):
    email = message["from"]["emailAddress"]["address"]
    subject = message["subject"]
    content = html2text.html2text(message["body"]["content"])

    email_str = f"""{{
    "from": {email},
    "subject": {subject},
    "content": {content}
}}"""
    return email_str

def send_to_AI(email_str):
    prompt = """You are an assistant that helps me process my emails. You will be given a biography about me, instructions, then by the email formatted like 
{
    "from": sender_email,
    "subject": subject,
    "content": content (in plain text)
}. 

Biography: I am a computer science undergraduate student. I have a keen interest in autonomous robotics and cool technology. I am looking for internships.

Instructions:
1. You will look through the email and extract any events that might interest me. Refer to my biography above to make these decisions.
2. If I might want to save the email to refer back to, sort it into one of these categories:
    a. Class announcements
    b. Important
    c. Receipts
If you are confused or unsure about where an email belongs, leave the category empty.
3. If an email is urgent, flag it as urgent.
4. You will decide if this email might be of any further use for me to read myself. If it is not, flag it for deletion. Be conservative with deletion.
5. Always include a ai_processed tag
6. Your response will be in the format 
{
    "events": {
        "title": title,
        "start_time": timestamp (RFC 3339),
        "end_time": timestamp (RFC 3339),
        "location": location (building and room number or address),
        "summary": summary of the event
    },
    "category": category (as defined above),
    "isUrgent": boolean,
    "forDeletion": boolean,
    "ai_processed": true,
}

Here is the email:
""" + email_str
    return prompt

def process_response(response):
    response = chat(
        model='gemma3',
        messages=[{'role': 'user', 'content': 'Hello!'}],
    )
    print(response)

send_to_AI("test")