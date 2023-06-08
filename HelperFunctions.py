from dotenv import load_dotenv
from Emailer import *
import os, json
import datetime
import pandas as pd
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from ics import Calendar, Event
from dateutil import tz

def send_email_with_calendar_invite(recipient_email, subjectLine, content, p_date, p_time):
    # Create a calendar event
    event = Event()

    # Get the local timezone
    local_tz = tz.gettz('America/Los_Angeles')  # Replace with your actual timezone

    # Set the event begin time with the timezone
    event.begin = '{}T{}:00'.format(p_date, p_time)
    event.begin = event.begin.replace(tzinfo=local_tz)

    # Set event name
    event.name = subjectLine.replace("Reminder ","")

    # Add the event to a calendar
    calendar = Calendar(events=[event])

    # Convert the event to an ics string
    ics_string = str(calendar)

    # send email to lab maintainer with the calendar invite attached
    send_email_invite(recipient_email, subjectLine, content, ics_string)


def create_df(gs_info):
    df = pd.DataFrame(gs_info, columns=gs_info[0])
    df.drop(index=df.index[0], 
            axis=0, 
            inplace=True)
    return df


def create_priority_column(df, day_notice=3):
    d = datetime.datetime.today()
    next_monday = next_weekday(d, 0)
    df['Presentation Date (MM/DD/YYY)'] = pd.to_datetime(df['Presentation Date (MM/DD/YYY)'])
    df["daysLeft"] = (df["Presentation Date (MM/DD/YYY)"] - pd.Timestamp.now().normalize()).dt.days

    df = df[df["daysLeft"]>0]
    df = df[df["daysLeft"]<=day_notice]

    # print(df)
    return df

"""
START
"""

def find_first_monday(year, month, day):
    d = datetime.date(year, int(month), 7)
    offset = -d.weekday() #weekday = 0 means monday
    return d + datetime.timedelta(offset)

def LabCitizenDay():
    today = datetime.date.today()
    # get next monday date
    next_monday = today + datetime.timedelta(days=1)
    # all first monday's for the present year
    all_first_mondays = [find_first_monday(today.year, i, today.day) for i in range(1,13,1)]
    if next_monday in all_first_mondays:
        return True
    else:
        return False
"""
END
"""

def extract_email_info(df):
    last_entry = df.values.tolist()[0]
    # print(last_entry)
    return last_entry

def next_weekday(d, weekday):
    days_ahead = weekday - d.weekday()
    if days_ahead <= 0: # Target day already happened this week
        days_ahead += 7
    return d + datetime.timedelta(days_ahead)



def get_earliest_presentation(gs_info):
    d = datetime.datetime.today()
    next_monday = next_weekday(d, 0)
    diffs = []

    for i,info in enumerate(gs_info[1:]):
        dt_obj = datetime.datetime.strptime(info[-1], '%m/%d/%Y')
        diff = dt_obj - next_monday
        diffs.append((i,diff))


def craft_email(subject, content, email_list, text_list=[]):
    Email = Emailer(email_list, text_list,
            subjectLine=subject,
            emailContent=content)
    Email.alert()


def create_reminder(instruction):
    check_symbol = "-"
    # check_symbol = "-"
    return "{} {}\n".format(check_symbol, instruction)

def create_step(reminder):
    check_symbol = "☐"
    # check_symbol = "-"
    return "{} {}\n".format(check_symbol, reminder)

def get_header(name, date_maintenance):
    header = "Hi {},\n\nThis is a reminder that tomorrow ({}) is your turn to do the LFL Lab Maintenance. Please refer to the following checklist.\n\n".format(name, date_maintenance)
    return header

def get_signature(bot_name="LFL Bot"):
    salute = "🫡 "
    # salute = ""
    return "\n\nThank you for your service {},\n{}".format(salute, bot_name)

def get_reminders(reminders_list):
    reminders = []
    for reminder_string in reminders_list:
        reminders.append(create_reminder(reminder_string))
    prompt = "\n\nSome safety considerations from EH&S:\n"
    reminders = "".join(reminders)
    return prompt + reminders + "\n"


def create_email_content(name, date_maintenance, instructions, reminders, bot_name="LFL Bot"):
    header = get_header(name, date_maintenance)
    steps = []
    for instruction in instructions:
        steps.append(create_step(instruction))
    body = "".join(steps)
    reminders = get_reminders(reminders)
    signature = get_signature(bot_name)
    return header + body + reminders + signature

def extract_lab_maintainer():
    load_dotenv(".env")
    user_id = str(os.environ.get("USER_ID"))
    user_name, user_email = get_user_info(user_id)
    return user_name, user_email

def get_user_info(user_id):
    f = open("lab_members.json")
    data = json.load(f)
    user_name, user_email = data[user_id]["name"], data[user_id]["email"]
    return user_name, user_email

def get_last_user_id():
    f = open("lab_members.json")
    data = json.load(f)
    id_num = int(list(data.keys())[-1])
    return id_num

def send_email(email,subjectLine, emailContent):
    sms_list = ['']
    sender = Emailer(email, sms_list, subjectLine, emailContent)
    sender.send_email()

def send_email_invite(to, subject, body, ics_string):
    load_dotenv(".env")
    EMAIL_ID = str(os.environ.get("EMAIL_ID"))
    SMTP_SERVER = os.environ.get("SMTP_SERVER")
    SMTP_PORT = 587
    GMAIL_PASSWORD =  os.environ.get("PASSWD")

    msg = MIMEMultipart()
    msg['From'] = EMAIL_ID
    msg['To'] = to
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    # Attach the ics file
    part = MIMEBase('application', 'octet-stream')
    part.set_payload(ics_string)
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', 'attachment; filename="invite.ics"')
    msg.attach(part)

    # Connect to the mail server
    server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
    server.starttls()

    # Login to the email account
    server.login(EMAIL_ID, GMAIL_PASSWORD)

    # Send the email
    text = msg.as_string()
    server.sendmail(EMAIL_ID, to, text)

    # Disconnect from the mail server
    server.quit()

def update_record(f=".env"):
    # Read in the file
    load_dotenv(f)
    last_id = get_last_user_id()

    with open(f, 'r') as file :
        filedata = file.read()

    # Replace the target string
    user_id = int(os.environ.get("USER_ID"))
    target = "ID="+str(user_id)

    if user_id != last_id:
        update = "ID="+str(user_id+1)
    else:
        update = "ID="+str(1)

    filedata = filedata.replace(target, update)

    # Write the file out again
    with open(f, 'w') as file:
        file.write(filedata)
