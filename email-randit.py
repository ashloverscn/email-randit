import base64
import pandas as pd
from random import randint, choices
from email.message import EmailMessage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from requests import HTTPError
from jinja2 import Template
import ssl
import smtplib
import logging
import time
import sys
import pdfkit
import os
import os.path
import string
from datetime import date
import uuid
import datetime

sdate = date.today().strftime("%d-%m-%Y")
ldate = date.today().strftime("%d-%B-%Y")

path_wkhtmltopdf = r'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'
config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)

logging.basicConfig(filename='mail.log', level=logging.DEBUG)

totalSend = 1
if(len(sys.argv) > 1):
    totalSend = int(sys.argv[1])

emaildf = pd.read_csv('gmail.csv')
contactsData = pd.read_csv('contacts.csv')
subjects = pd.read_csv('subject.csv')
bodies = ['body.txt', 'body2.txt', 'body3.txt', 'body4.txt', 'body5.txt']
From = pd.read_csv('from.csv')

f = open("tfn.txt", "r")
tfn = f.read()
bodies = ['body.txt', 'body2.txt', 'body3.txt', 'body4.txt', 'body5.txt', ]
file_exe_name = ['Invoice_' + sdate, 'Bill_' + sdate, 'Receipt_' + sdate, 'Statement_' + sdate]

def send_mail(name, email, emailId, password, host, port, bodyFile, subjectWord, fromName, file_exe_name):
    newMessage = MIMEMultipart()

    # Invoice Number and Subject
    invoiceNo = randint(1000000, 9999999)
    transaction_id = randint(10000000000, 99999999999)
    rand_string = ''.join(choices(string.ascii_uppercase, k=5))
    rand_string0 = ''.join(choices(string.ascii_uppercase, k=5)) + str(randint(1000, 9999)) + ''.join(choices(string.ascii_uppercase, k=2))
    subject = subjectWord + " #" + rand_string + str(invoiceNo) + rand_string0
    newMessage['Subject'] = subject
    #newMessage['From'] = f"{name}{num}<{emailId}>"
    newMessage['From'] = f"{fromName}<{emailId}>"
    newMessage['To'] = email
    transaction_id = randint(100000000, 999999999)
    random_id = randint(100000000, 999999999)
    xyz_id = (uuid.uuid4())

    # Mail Body Content
    body = open(bodyFile, 'r').read()
    body = body.replace('$email', email)
    body = body.replace('$name', name)
    body = body.replace('$product_no', rand_string + str(randint(10000, 99999)))
    body = body.replace('$invoice_no', str(transaction_id))
    body = body.replace('$digi_no', str(xyz_id))
    body = body.replace('$date', str(ldate))
    body = body.replace('$charge', str(randint(10, 99)))

    # Mail PDF File
    html = open('./contents/html_code.html', 'r').read()
    html = html.replace('$email', email)
    html = html.replace('$product_no', rand_string + str(randint(10000, 99999)))
    html = html.replace('$invoice_no', str(transaction_id))
    html = html.replace('$name', name)
    html = html.replace('$email', email)
    html = html.replace('$digi_no', str(xyz_id))
    html = html.replace('$tfn', tfn)
    html = html.replace('$date', str(ldate))
    html = html.replace('$charge', str(randint(10, 99)))

    # saving the changes to html_code.html
    with open('./cache/html_code.html', 'w') as f:
        f.write(html)
        f.close

    file = str(file_exe_name) + str(invoiceNo) + ".pdf"
    pdfkit.from_file('./cache/html_code.html', './cache/' + str(file), configuration=config)

    newMessage.attach(MIMEText(body))

    try:
        with open('./cache/' + str(file), 'rb') as f:
            payload = MIMEBase('application', 'octet-stream', Name=file)
            # payload = MIMEBase('application', 'pdf', Name=pdfname)
            payload.set_payload(f.read())

            # enconding the binary into base64
            encoders.encode_base64(payload)

            # add header with pdf name
            payload.add_header('Content-Decomposition',
                               'attachment', filename=file)
            newMessage.attach(payload)

        if(str(port) == 'API'):
           SCOPES = ['https://mail.google.com/']
           creds = None
           if os.path.exists("./credentials/" + str(emailId) + "-token.json"):
               creds = Credentials.from_authorized_user_file("./credentials/" + str(emailId) + "-token.json", SCOPES)
           if not creds or not creds.valid:
               if creds and creds.expired and creds.refresh_token:
                   creds.refresh(Request())
               else:
                   flow = InstalledAppFlow.from_client_secrets_file(
                       "./credentials/" + str(emailId) + ".json", SCOPES
                       )
                   creds = flow.run_local_server(port=0)
               with open("./credentials/" + str(emailId) + "-token.json", "w") as token:
                      token.write(creds.to_json())
           service = build("gmail", "v1", credentials=creds)
           create_message = {'raw': base64.urlsafe_b64encode(newMessage.as_bytes()).decode()}
           try:
               message = (service.users().messages().send(userId="me", body=create_message).execute())
               print(F'sent message to {message} Message Id: {message["id"]}')
               contactsData.at[int(i) , 'sent'] = 'sent'
               contactsData.to_csv('contacts.csv', sep=',', index=None, na_rep='NaN', header=['name', 'email', 'sent'])
           except HTTPError as error:
               print(F'An error occurred: {error}')
               message = None

        if(port == '465'):
           AUTHREQUIRED = 1
           context = ssl.create_default_context()
           mailserver = smtplib.SMTP_SSL(host, 465, context=context)
           mailserver.login(emailId, password)
           mailserver.sendmail(emailId, email, newMessage.as_string())
           mailserver.quit()
           contactsData.at[int(i) , 'sent'] = 'sent'
           contactsData.to_csv('contacts.csv', sep=',', index=None, na_rep='NaN', header=['name', 'email', 'sent'])
        if(port == '587'):
           AUTHREQUIRED = 1
           mailserver = smtplib.SMTP(host, 587)
           mailserver.ehlo()
           mailserver.starttls()
           mailserver.ehlo()
           mailserver.login(emailId, password)
           mailserver.sendmail(emailId, email, newMessage.as_string())
           mailserver.quit()
           contactsData.at[int(i) , 'sent'] = 'sent'
           contactsData.to_csv('contacts.csv', sep=',', index=None, na_rep='NaN', header=['name', 'email', 'sent'])

        os.remove('./cache/' + str(file))
             
        print(f"send to {email} by {emailId} successfully : {totalSend}")
        logging.info(
                f"send to {email} by {emailId} successfully : {totalSend}")

    except smtplib.SMTPResponseException as e:
        print(e)
        error_code = e.smtp_code
        error_message = e.smtp_error
        print(f"send to {email} by {emailId} failed")
        logging.info(f"send to {email}  by {emailId} failed")
        print(f"error code: {error_code}")
        print(f"error message: {error_message}")
        logging.info(f"error code: {error_code}")
        logging.info(f"error message: {error_message}")

        remove_email(emailId, password)


def start_mail_system():
    global totalSend
    global i
    j = 0
    k = 0
    l = 0
    m = 0
    o = 0

    for i in range(len(contactsData)):
        if(contactsData.at[int(i) , 'sent'] != 'sent'):
            emaildf = pd.read_csv('gmail.csv')
            if(j >= len(emaildf)):
                j = 0
            time.sleep(0)
            send_mail(contactsData.at[int(i), 'name'], contactsData.at[int(i), 'email'], emaildf.at[int(j), 'email'],
                      emaildf.at[int(j), 'password'], emaildf.at[int(j), 'host'], emaildf.at[int(j), 'port'], bodies[k], subjects.at[int(l), 'subject'], From.at[int(m), 'from_name'], file_exe_name[o])
            totalSend += 1
            j = j + 1
            k = k + 1
            l = l + 1
            m = m+1
            if j == len(emaildf):
                j = 0
            if k == len(bodies):
                k = 0
            if l == len(subjects):
                l = 0
            if m == len(From):
                m = 0
            if o == len(file_exe_name):
                o = 0
    quit()

def remove_email(emailId, password):
    df = pd.read_csv('gmail.csv')
    index = df[df['email'] == emailId].index
    df.drop(index, inplace=True)
    df.to_csv('gmail.csv', index=False)
    print(f"{emailId} removed from gmail.csv")
    logging.info(f"{emailId} removed from gmail.csv")


try:
    for i in range(6):
        start_mail_system()
except KeyboardInterrupt as e:
    print(f"\n\ncode stopped by user")
