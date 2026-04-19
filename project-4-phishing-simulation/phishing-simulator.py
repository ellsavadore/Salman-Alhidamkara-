# Phishing Simulation Script for Educational Purpose Only
# Gunakan script ini hanya untuk pelatihan keamanan yang sah

import random
import datetime

class PhishingSimulator:
    def __init__(self, target_name, target_email):
        self.target_name = target_name
        self.target_email = target_email
        self.simulation_date = datetime.datetime.now()
        
    def display_banner(self):
        print("=" * 60)
        print("   PHISHING SIMULATION TOOL - EDUCATIONAL PURPOSE")
        print("   Author: Salman Alhidamkara")
        print("=" * 60)
        
    def generate_email_template(self, template_type):
        templates = {
            "password_reset": f"""
            Subject: Security Alert - Password Reset Required
            
            Dear {self.target_name},
            
            Our system detected suspicious activity on your account.
            Please reset your password immediately by clicking the link below:
            
            [RESET PASSWORD LINK - SIMULATION MODE]
            
            This is a SIMULATED phishing attempt for security training.
            Do not click on suspicious links in real emails.
            
            - IT Security Team
            """,
            
            "account_verification": f"""
            Subject: Account Verification Required
            
            Dear {self.target_name},
            
            Due to new security policies, please verify your account:
            
            [VERIFY ACCOUNT LINK - SIMULATION MODE]
            
            This is a SIMULATED phishing attempt for security training.
            Always verify sender email address before clicking links.
            
            - Security Team
            """,
            
            "invoice_attachment": f"""
            Subject: Invoice #INV-{random.randint(1000,9999)} - Payment Required
            
            Dear {self.target_name},
            
            Please find attached invoice for recent purchase.
            
            [VIEW INVOICE LINK - SIMULATION MODE]
            
            This is a SIMULATED phishing attempt for security training.
            Be cautious with email attachments from unknown senders.
            
            - Billing Department
            """
        }
        return templates.get(template_type, templates["password_reset"])
    
    def run_simulation(self):
        self.display_banner()
        print(f"\nSimulation Date: {self.simulation_date}")
        print(f"Target: {self.target_name} ({self.target_email})")
        print("\n" + "=" * 60)
        print("GENERATED PHISHING EMAIL TEMPLATE (SIMULATION MODE)")
        print("=" * 60)
        
        template_type = random.choice(["password_reset", "account_verification", "invoice_attachment"])
        email = self.generate_email_template(template_type)
        print(email)
        
        print("\n" + "=" * 60)
        print("EDUCATIONAL NOTES:")
        print("1. Jangan pernah klik link mencurigakan di email")
        print("2. Verifikasi alamat email pengirim")
        print("3. Jangan berikan password ke siapapun")
        print("4. Gunakan Two-Factor Authentication (2FA)")
        print("=" * 60)
        
        return {"status": "simulation_completed", "template_used": template_type}

def main():
    print("Phishing Simulation Tool (Educational)")
    print("-" * 40)
    
    name = input("Masukkan nama target simulasi: ")
    email = input("Masukkan email target simulasi: ")
    
    simulator = PhishingSimulator(name, email)
    result = simulator.run_simulation()
    
    print(f"\nSimulation result: {result['status']}")
    print("Template yang digunakan:", result['template_used'])

if __name__ == "__main__":
    main()
