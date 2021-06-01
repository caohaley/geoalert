import smtplib, ssl

# Global Variables
PORT = 465 # For SSL
SENDER_EMAIL = ""
SENDER_PASSWORD = ""
RECEIVER_EMAIL = "engineering+challenge@sprinter.com"
SSL_CONTEXT = None


# Alert Helper Functions

def alertSetup():
	'''
	Set up email alert system once at the beginning of the program.
	'''
	global SENDER_EMAIL
	global SENDER_PASSWORD
	global RECEIVER_EMAIL
	global SSL_CONTEXT
	
	senderEmail = input("Type your outgoing/sender email address now: ")
	if senderEmail != "":
		SENDER_EMAIL = senderEmail
	

	senderPassword = input("Type your outgoing/sender email password now: ")
	if senderPassword != "":
		SENDER_PASSWORD = senderPassword

	receiverEmail = input("Type your receiver email address that you want to receive the alerts on now: ")
	if receiverEmail != "":
		RECEIVER_EMAIL = receiverEmail

	SSL_CONTEXT = ssl.create_default_context()


def sendAlert(alertType, clinicianID):
	'''
	Send email alerts based on type of alert.
	'''
	with smtplib.SMTP_SSL("smtp.gmail.com", PORT, context=SSL_CONTEXT) as server:
		server.login(SENDER_EMAIL, SENDER_PASSWORD)
		message = None

		if alertType == "systemError":
			message = 'Subject: {}\n\n{}'.format("Location Monitor Alert: System Error", "There is a system error. Monitoring is shut down.")

		elif alertType == "inputError":
			message = 'Subject: {}\n\n{}'.format("Location Monitor Alert: Input Error", "There is input error (error in geojson format or data). Monitoring is shut down.")

		elif alertType == "clinicianOutbound":
			message = 'Subject: {}\n\n{}'.format("Location Monitor Alert: Clinician Out of Bound", "Clinician with ID "+str(clinicianID)+" left the expected zone.")

		elif alertType == "APIrequestFailed":
			message = message = 'Subject: {}\n\n{}'.format("Location Monitor Alert: Status API Failed", "Clinician status API failed to respond for clinician with ID "+str(clinicianID)+".")

		else:
			print("alertError")

		server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, message)
