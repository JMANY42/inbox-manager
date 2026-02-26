from elearning import assignment_due_soon, assignment_submitted
from outlook import get_emails
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
        pass # GENERAL CASE EMAIL


def main():
    messages = get_emails()
    for email in messages:
        preliminary_sort(email)
        
    
if __name__ == "__main__":
    main()