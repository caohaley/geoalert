# geoalert
Security feature that uses a Clinician Status API to email alert within 5 minutes of a clinician leaving the expected zone.

### How to Use:
You may download and run the python file locally with the command `python3 geoalert.py`. The program will then ask you for clinician IDs to monitor and which sender email, receiver email, and receiver email to use. If you will be using the program many times, you may set the email information constants at the top of `alert.py` and press only enter when prompted to fill in the emails.

#### Note:
Sender email must be a **Gmail** account and must click the option to allow less secure apps to use your account. It is best to use a development account for this and not a personal Gmail account. For more information on less secure apps: https://support.google.com/accounts/answer/6010255?hl=en

