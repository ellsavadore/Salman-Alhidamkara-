# Bulk Email Automation Script
# Author: Salman Alhidamkara

import smtplib
import csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import getpass

class EmailAutomation:
    def __init__(self, smtp_server, port, email_sender, password):
        self.smtp_server = smtp_server
        self.port = port
        self.email_sender = email_sender
        self.password = password
        
    def send_email(self, recipient, subject, body, attachment_path=None):
        """Kirim email ke satu penerima"""
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email_sender
            msg['To'] = recipient
            msg['Subject'] = subject
            
            msg.attach(MIMEText(body, 'html'))
            
            # Tambah attachment jika ada
            if attachment_path:
                with open(attachment_path, 'rb') as attachment:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(attachment.read())
                    encoders.encode_base64(part)
                    part.add_header(
                        'Content-Disposition',
                        f'attachment; filename={attachment_path.split("/")[-1]}'
                    )
                    msg.attach(part)
            
            # Kirim email
            with smtplib.SMTP(self.smtp_server, self.port) as server:
                server.starttls()
                server.login(self.email_sender, self.password)
                server.send_message(msg)
            
            print(f"[SUCCESS] Email sent to {recipient}")
            return True
            
        except Exception as e:
            print(f"[ERROR] Failed to send to {recipient}: {e}")
            return False
    
    def send_bulk_email(self, recipients_data, subject_template, body_template):
        """Kirim email massal dengan personalisasi"""
        success_count = 0
        fail_count = 0
        
        for data in recipients_data:
            recipient = data.get('email')
            name = data.get('name', 'Customer')
            
            # Personalisasi subject dan body
            subject = subject_template.replace('{name}', name)
            body = body_template.replace('{name}', name)
            
            if self.send_email(recipient, subject, body):
                success_count += 1
            else:
                fail_count += 1
        
        print(f"\n=== SUMMARY ===")
        print(f"Total: {len(recipients_data)}")
        print(f"Success: {success_count}")
        print(f"Failed: {fail_count}")
    
    def load_recipients_from_csv(self, csv_file):
        """Load daftar penerima dari file CSV"""
        recipients = []
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                recipients.append(row)
        return recipients

def main():
    print("=" * 50)
    print("   BULK EMAIL AUTOMATION TOOL")
    print("   Author: Salman Alhidamkara")
    print("=" * 50)
    
    # Konfigurasi SMTP
    print("\nSMTP Configuration:")
    smtp_server = input("SMTP Server (contoh: smtp.gmail.com): ")
    port = int(input("Port (contoh: 587): "))
    email_sender = input("Email pengirim: ")
    password = getpass.getpass("Password: ")
    
    # Template email
    print("\nEmail Template:")
    subject_template = input("Subject (gunakan {name} untuk personalisasi): ")
    print("Body (gunakan {name} untuk personalisasi, ketik 'END' untuk selesai):")
    lines = []
    while True:
        line = input()
        if line == 'END':
            break
        lines.append(line)
    body_template = '\n'.join(lines)
    
    # Data penerima
    print("\nRecipient Data:")
    print("1. Input manual")
    print("2. Load dari CSV")
    choice = input("Pilih: ")
    
    recipients = []
    if choice == "1":
        while True:
            name = input("Nama (atau 'done' untuk selesai): ")
            if name.lower() == 'done':
                break
            email = input(f"Email untuk {name}: ")
            recipients.append({'name': name, 'email': email})
    else:
        csv_file = input("Nama file CSV: ")
        recipients = EmailAutomation.load_recipients_from_csv(None, csv_file)
    
    # Kirim email
    email_tool = EmailAutomation(smtp_server, port, email_sender, password)
    email_tool.send_bulk_email(recipients, subject_template, body_template)

if __name__ == "__main__":
    main()
