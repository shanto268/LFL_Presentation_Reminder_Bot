# -*- coding: utf-8 -*-
__author__ =  "Sadman Ahmed Shanto"
__date__ = "07/18/2022"
__email__ = "shanto@usc.edu"

from HelperFunctions import *
from datetime import datetime, timedelta

if __name__ == "__main__":
    # weekday choice (day in advance)
    p_date = str((datetime.today() + timedelta(days=7)).date())

    # meeting time
    p_time = "10:30"

    # meeting place
    p_place = "SSC 319"

    """
    Logic:
    """
    if not LabCitizenDay():
        # read emission file to see whose turn this week (i.e. at execution)
        recipient_name, recipient_email = extract_lab_maintainer()

        # create email for lab maintainer
        signature = "\n\nLooking Forward to it 🤩,\nLFL Bot."
        subjectLine = "LFL Lab Presentation Reminder ({})".format(p_date)

        # Combine date and time into a datetime object
        start_time = datetime.strptime(f"{p_date} {p_time}", "%Y-%m-%d %H:%M")

        # Add one hour to start_time to get end_time
        end_time = start_time + timedelta(hours=1)

        # Convert datetime objects back to strings in ISO format
        start_time_str = start_time.isoformat()
        end_time_str = end_time.isoformat()

        # event link for calendar
        event_link = create_event(subjectLine, p_place, f'Presenter: {recipient_name}', start_time_str, end_time_str)
        slack_content = f"Hi all,\n\nThis is a reminder that {recipient_name} is going to be giving a presentation talk on {p_date} at {p_time} AM."

        # content
        slack_content = f"{slack_content}\n\nAdd to your Google Calendar 🗓️: {event_link}{signature}"
        email_content = f"Hi {recipient_name},\n\nThis is a reminder that you are scheduled for a presentation talk on {p_date} at {p_time} AM.{signature}"

        # send message to slack
        send_slack_message(slack_content,slack_channel="general")

        # send email to lab maintainer
        send_email_with_calendar_invite(recipient_email, subjectLine, email_content, p_date, p_time)

        # update the record
        update_record()
    else:
        emailContent = f"Hi <name>,\n\nThis is a reminder that next week ({p_date} at {p_time}) we will be participating in Lab Citizen\Clean-Up Day.\n\nThanks for taking care of our beautiful LFLab 🥰,\nLFL Bot"
        sender = Emailer(email_list=[""], textList=[], subjectLine=f"Lab Citizen Day ({p_date})", emailContent=emailContent)
        sender.send_email_json("lab_members.json")

