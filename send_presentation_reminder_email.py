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

    load_dotenv(".env")
    sheets_id = os.environ.get("SHEETS_ID")
    range_query = 'A:D'
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
    day_notice=3

    try:
        gs_info = ReadSheets(sheets_id,range_query,scopes).get_values()
        # print(gs_info)
        df = create_df(gs_info)
        df = create_priority_column(df,day_notice)
        name, email, p_title, p_date, days_left = extract_email_info(df)

        p_date =  datetime.datetime.strftime(p_date, '%m/%d/%Y')

        subject = "Presentation Reminder ({})".format(p_date)
        email_list = [email]
        content = f"Hi {name},\n\nThis is a reminder that you have a presentation talk - \"{p_title}\" - on {p_date}.\n\nLooking Forward to it 🤩,\nLFL Bot."

        craft_email(subject, content, email_list)

    except Exception as e:
        if e == "\'invalid_grant: Token has been expired or revoked.\', {\'error\': \'invalid_grant\', \'error_description\': \'Token has been expired or revoked.\'":
            subject = "Token Issue"
            email_list = [f"{__email__}"]
            content = f"Hi {__author__},\n\nLettng you know the token issue was encountered. Working on the resolution now.\n\n`{e}`"
            craft_email(subject, content, email_list)
            os.system("rm token.json")
            os.system("python send_presentation_reminder_email.py")
        else:
            subject = "No One Signed Up for Presentation"
            email_list = [f"{__email__}"]
            content = f"Hi {__author__},\n\nThis is the exact Exception Message from the LFL bot.\n\n`{e}`"
            craft_email(subject, content, email_list)




