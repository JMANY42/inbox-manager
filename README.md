# Inbox Manager

This is a (hopefully) simple project dedicated to help me keep me inbox clean as well as notify me of any actually important emails. The scope of this project includes:

- delete junk email
- delete emails that do not pertain to me
- automatically add assignment due dates to my google calander
- automatically add cool events I want to go to to my google calander
- sort emails that I want to keep into folders

## Plan
Right now my very surface level concept of a plan is to use a LLM/agent/something AI to analyze the email content and make a decision about the fate of the email (delete, sort, flag, extract to calander) automatically.

I will first focus on my @utdallas.edu email because it gets the most cluttered and is the most important in my day to day life, but hope to expand to my gmails as well.

I will launch this manager on my personal server to keep it active 24/7 and plan to host my own LLM or agent to make decisions for me because I have a server with a gpu and I might as well use it.

If this is actually useful, I might consider launching this into an app people other than me can use.

## Update

UTD won't let me access the outlook API for "security concerns" with giving a student access to the graph API endpoint. So, if I still want to manage my utd email (which I do), I need a work around. I also can't just forward all the emails to an external inbox.

### Option 1 - Browser Automation

Create a simple browser automation to log into outlook every x minutes and load any new emails and make any necessary changes through simulated human inputs.

### Option 2 - Download the entire inbox

Download the enitre inbox every x minutes and sort emails locally. Not sure how to sort the inbox with this method.

## Updated Plan

I think I'm going to stick with option 1 and simulate human inputs. This definently is violating some terms of agreement but I don't really care about that. Hopefully captcha isn't too much of an issue. The underlying sorting and rules will be the same, this just makes getting each email a million times harder.  

## Update 2

I can get a valid access token through the microsoft graph explorer. From what I can tell, I can use this token anywhere (it works in postman) and it expires after 24 hours. So the only thing I need to make a web automation for is getting that token and only run it once a day. This is definently the best way forward. 