from datetime import datetime as dt
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os

def errorNotification(error):
	'''
	Send email informing receipient of price change to product (RX100 III)

	Arguments
	price: float - price of product
	diff: float - change in price of product
	
	returns: nothing

	'''

	#Set properties for mail server
	smtp_server = 'smtp.gmail.com'
	port = 465
	context = ssl.create_default_context()

	#Get sender email and password from env variables
	strFrom = os.environ.get('AMAZON_EMAIL_USER')
	pw = os.environ.get('AMAZON_EMAIL_PASSWORD')

	#Define receipient
	strTo = 'receipient email'

	#Instantiate msg object and assign values
	msg = MIMEMultipart("alternative")
	msg['From'] = strFrom
	msg['To'] = strTo
	msg['Subject'] = f'Price Tracker Failed!'

	#Provide plain text message incase receipient email server denies html
	text = f"Price Tracker for Sony RX100 III has failed.\n\n Error Message: {error}"

	#Assign plain and html parts to email and attach them to message object
	part1 = MIMEText(text,"plain")
	msg.attach(part1)

	# Send the email (this example assumes SMTP authentication is required)	
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(strFrom, pw)
		server.sendmail(strFrom, strTo, msg.as_string())
		# server.sendmail(strFrom, strTo, msg.encode('utf-8'))
		server.quit()