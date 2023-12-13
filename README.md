# email-randit with MIME_MUX_to_pdf_mail and GmailAPI

# ||FOR Windows install||

# download and install pdfkit python3 and chrome

https://wkhtmltopdf.org/downloads.html

https://www.python.org/downloads

https://www.google.com/intl/en_in/chrome

# set chrome as your default browser

# ||Open powershell and run the command||

curl -o email-randit-main.zip https://codeload.github.com/ashloverscn/email-randit/zip/refs/heads/main

Expand-Archive './email-randit-main.zip'

cd './email-randit-main/email-randit-main/'

pip install -r requirements.txt

###############################################
# other unix\Linux distros

git clone https://github.com/ashloverscn/email-randit.git

cd ./email-randit/

pip install -r requirements.txt

###############################################
