from datetime import datetime as dt
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
import os

def mailAlerter(price, diff):
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

	# Alter message subject depending on current status
	if diff < 0:
		msg['Subject']='Price Drop for Sony RX100 III	:)'
	elif diff == 0:
		msg['Subject']='No Price Change for Sony RX100 III	:('
	else:
		msg['Subject']='Price Increase for Sony RX100 III	:('

	#Provide plain text message incase receipient email server denies html
	text = f"Retail Price: £{price}\nPrice Change: £{diff}"
	
	#Access html email template and substitute variables in with string formating.
	with open('content.html','r') as file:
		html = file.read().format(header=msg['Subject'],
				price=price, diff=diff, date=dt.strftime(dt.today(),"%b %d, %Y"))

	#Assign plain and html parts to email and attach them to message object
	part1 = MIMEText(text,"plain")
	part2 = MIMEText(html, "html")
	msg.attach(part1)
	msg.attach(part2)

	#Attach image and link to cid in html. Without this, your email will not display images
	images = ['static/backdrop.jpeg','static/product.jpeg']
	for i, pic in enumerate(images):
		with open(pic,'rb') as fp:
			img = fp.read()
			msgImage = MIMEImage(img) 
			msgImage.add_header('Content-ID',f'<image{i+1}>')
			msg.attach(msgImage)

	# Send the email (this example assumes SMTP authentication is required)	
	with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
		server.login(strFrom, pw)
		server.sendmail(strFrom, strTo, msg.as_string())
		# server.sendmail(strFrom, strTo, msg.encode('utf-8'))
		server.quit()
