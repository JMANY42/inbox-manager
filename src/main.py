from elearning import assignment_due_soon, assignment_submitted
from outlook import get_emails
from general_email import handle_general_email

def preliminary_sort(message):
    subject = message["subject"]
    from_email = message["from"]["emailAddress"]["address"]

    # Sort by email type for future processes
    if from_email == 'eLearning-Notification@utdallas.edu' and 'due soon' in subject:
        assignment_due_soon(message)
    
    if from_email == 'eLearning-Notification@utdallas.edu' and 'Submission received' in subject:
        assignment_submitted(message)

    elif from_email == 'no-reply@notify.cloudflare.com' and '[Alert] Tunnel APT_Server' in subject:
        pass # NOT SURE WHAT TO DO MAYBE JUST FLAG AS IMPORTANT
    
    else:
        handle_general_email(message)


def main():
    print("starting email fetch...")
    messages = get_emails()
    print("successfully fetched emails!")
    for email in messages:
        preliminary_sort(email)
        pass
        
    
if __name__ == "__main__":
    main()
