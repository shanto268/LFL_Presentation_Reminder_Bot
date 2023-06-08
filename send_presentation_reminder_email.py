# -*- coding: utf-8 -*-
__author__ =  "Sadman Ahmed Shanto"
__date__ = "07/18/2022"
__email__ = "shanto@usc.edu"

import datetime
from HelperFunctions import *

if __name__ == "__main__":
    # weekday choice (day in advance)
    p_date = str(datetime.date.today() + datetime.timedelta(days=7))

    # liquid nitrogen appt time
    p_time = "10:00"

    # content of email
    """
    Logic:
    """
    if not LabCitizenDay():
        # read emission file to see whose turn this week (i.e. at execution)
        recipient_name, recipient_email = extract_lab_maintainer()

        # create email for lab maintainer
        content = f"Hi {recipient_name},\n\nThis is a reminder that you are scheduled for a presentation talk on {p_date} at {p_time}.\n\nLooking Forward to it 🤩,\nLFL Bot."
        subjectLine = "LFL Lab Presentation Reminder ({})".format(p_date)

        # send email to lab maintainer
        send_email_with_calendar_invite(recipient_email, subjectLine, content, p_date, p_time)

        # update the record
        update_record()
    else:
        emailContent = f"Hi <name>,\n\nThis is a reminder that next week ({p_date} at {p_time}) we will be participating in Lab Citizen\Clean-Up Day.\n\nThanks for taking care of our beautiful LFLab 🥰,\nLFL Bot"
        sender = Emailer(email_list=[""], textList=[], subjectLine=f"Lab Citizen Day ({p_date})", emailContent=emailContent)
        sender.send_email_json("lab_members.json")
