# -*- coding: utf-8 -*-
"""
====================================================================
Program : Google_Sheets_Bot/send_presentation_reminder_email.py
====================================================================
Summary:
"""
__author__ =  "Sadman Ahmed Shanto"
__date__ = "10/02/2022"
__email__ = "shanto@usc.edu"


from HelperFunctions import *
from ReadSheets import ReadSheets
from dotenv import load_dotenv


if __name__ == "__main__":
    # weekday choice (day in advance)

    load_dotenv(".env")
    sheets_id = os.environ.get("SHEETS_ID")
    range_query = 'A:D'
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']

    gs_info = ReadSheets(sheets_id,range_query,scopes).get_values()
    name, email, p_title, p_date = extract_email_info(gs_info)
    # print(gs_info)
    get_earliest_presentation(gs_info)

    subject = "Presentation Reminder ({})".format(p_date)
    email_list = [email]
    content = f"Hi {name},\n\nThis is a reminder that you have a presentation talk - \"{p_title}\" - on {p_date}.\n\nLooking Forward to it 🤩,\nLFL Bot."

    # craft_email(subject, content, email_list)


