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
    p_time = "2:30 PM"

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
        send_email(recipient_email, subjectLine, content)

        # update the record
        update_record()
    else:
        pass
