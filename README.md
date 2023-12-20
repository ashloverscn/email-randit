# email-randit with MIME_MUX_to_pdf_mail and GmailAPI

# ||FOR Windows install||

# NOTE: you may use ramdisk to increse data rw speed for non nvme memory users
https://www.maketecheasier.com/setup-ram-disk-windows/
https://beebom.com/create-ram-disk-windows-10-super-fast-read-write-speeds/

# download and install pdfkit chrome and python3

https://wkhtmltopdf.org/downloads.html

https://www.google.com/intl/en_in/chrome

# set chrome as your default browser

# use this binary if you just want to use it and skip everything else after this 

https://mega.nz/file/ky0jkA7K#GKBbu951rqtYaSx-_vsHevDlfDa8u0iFPbXwyBcgdRg

# continue if not using binary 

https://www.python.org/downloads

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
