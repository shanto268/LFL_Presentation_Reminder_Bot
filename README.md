# LFL Presentation Reminder File

## To Do:

- Implement the following scheduler:
    - [ ]  Read DB
    - [ ]  FIFO structure for all FALSE entries
    - [ ]  Pop to get info
    - [ ]  Send email
    - [ ]  Overwrite the FALSE to TRUE on remote DB


## Installation:

- Clone the repo
- Create the .env file with the following variables
    ```
    EMAIL_ID=''
    PASSWD=''
    SMTP_SERVER='smtp.gmail.com'
    SHEETS_ID=''
    ```
- Copy over the `token.json` and `credentials.json` files
- Run the code `$ python send_presentation_reminder_email.py` 
- Update the `email_service.bat` file and create a Windows Scheduler Task
