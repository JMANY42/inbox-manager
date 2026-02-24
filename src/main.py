from elearning import assignment_due_soon, assignment_submitted

def preliminary_sort(message):
    subject = message["subject"]
    sender_email = message["sender"]["emailAddress"]["address"]

    # Sort by email type for future processes
    if sender_email == 'eLearning-Notification@utdallas.edu' and 'due soon' in subject:
        assignment_due_soon(message)
    
    if sender_email == 'eLearning-Notification@utdallas.edu' and 'Submission received' in subject:
        assignment_submitted(message)

    elif sender_email == 'no-reply@notify.cloudflare.com' and '[Alert] Tunnel APT_Server' in subject:
        pass # NOT SURE WHAT TO DO MAYBE JUST FLAG AS IMPORTANT
    
    else:
        pass # GENERAL CASE EMAIL


def main():
    preliminary_sort({
        "subject": "Submission received",
        "sender": {
            "emailAddress": {
                "name": "eLearning-Notification@utdallas.edu",
                "address": "eLearning-Notification@utdallas.edu"
            }
        },
        "body": {
            "contentType": "html",
            "content": "<html><head>\r\n<meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"></head><body>Your submission was successful!<br><br>You can save or print this confirmation for your records. You can also view your receipts on your My Grades page.<br><br>Submission details:<br>Confirmation number: 9c0c1e34766f4b458b0e749de73fd472<br>Course: CS 3354.HON - Software Engineering - S26<br>Course ID: 2262-UTDAL-CS-3354-SECHON-24915<br>Title: Homework 1<br>Submission date: Feb 19, 2026 9:33 PM<br>Size of written submission: 0 bytes<br>Size and name of files received: CS 3354 HW1.pdf (236.6 kb) <br>Unique Item ID (for administrator use only): _8770459_1<br></body></html>"
        },
    })
    
if __name__ == "__main__":
    main()