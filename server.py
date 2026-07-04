import csv
import smtplib
from email.message import EmailMessage
from flask import Flask, render_template, request, redirect, url_for
#, send_from_directory
app=Flask(__name__)
print(__name__)

@app.route('/')
def hello_world():
    return render_template('index.html')

@app.route('/<string:page_name>')
def html_page(page_name):
    return render_template(page_name)

@app.route('/thankyou/<email_address>')
def thanks(email_address=None):
    return render_template('thankyou.html', user=email_address)

def send_email(email_data): 
    email = EmailMessage()
    email['to'] = 'pauldieterich@paulspage.net'
    email['from'] = email_data['email']
    email['subject'] = email_data['subject']
    email.set_content(email_data['message'])
    with smtplib.SMTP_SSL(host='mail.paulspage.net', port=465) as smtp:
      print(f'Attempting to log in')
      smtp.login(email['to'], 'QP(*^N38')
      print(f'Logged in, trying to send message')
      smtp.send_message(email)
      print('woo hoo!')

def persist_email_data(email_data):
   with open('database.txt', mode='a+') as my_file2:
      try:
         my_file2.write(
            f"email: {email_data['email']},\n"
            f"subject: {email_data['subject']},\n"
            f"message: {email_data['message']}"
            )
      except IOError as err:
         print('IO error')
         raise err
      

def persist_email_data_csv(email_data):
   with open('database.csv', mode='a+') as my_file3:
      try:
          email = email_data['email']
          subject = email_data['subject']
          message = email_data['message']
          csv_writer = csv.writer(my_file3, delimiter=',', quotechar=' ', quoting=csv.QUOTE_MINIMAL)
          csv_writer.writerow([email, subject, message])  
      except IOError as err:
         print('IO error')
         raise err

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    if request.method == 'POST':
      email_data = request.form.to_dict()
      #send_email(email_data)
      persist_email_data_csv(email_data)
      return redirect(url_for('thanks', email_address=email_data['email']))
    else:
      return redirect(url_for('html_page', page_name='contact.html'))
        
        
