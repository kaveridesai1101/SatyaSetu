"""
Mail Handler for VeriSense
Provides SMTP support for OTP emails with a fallback simulator.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from src.utils.logger import get_logger

logger = get_logger(__name__)

class MailHandler:
    def __init__(self):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.smtp_port = int(os.getenv("SMTP_PORT", 587))
        self.smtp_user = os.getenv("SMTP_USER")
        self.smtp_pass = os.getenv("SMTP_PASSWORD")
        
        # Check if actually configured
        self.enabled = all([self.smtp_server, self.smtp_user, self.smtp_pass])
        if not self.enabled:
            logger.warning("SMTP credentials not found. MailHandler running in SIMULATION mode.")

    @property
    def is_simulated(self):
        return not self.enabled

    def send_otp(self, receiver_email, otp_code):
        """Send OTP via SMTP or simulate if not configured"""
        subject = "🛡️ Reliable Reads: Your Verification Code"
        body = f"""
        <html>
        <body style="font-family: sans-serif; color: #334155;">
            <div style="max-width: 600px; margin: 40px auto; padding: 20px; border: 1px solid #E2E8F0; border-radius: 8px;">
                <h2 style="color: #2563EB; border-bottom: 2px solid #F1F5F9; padding-bottom: 10px;">Verification Required</h2>
                <p>Hello,</p>
                <p>To access the <b>Reliable Reads</b> Verification Studio, please use the following one-time code:</p>
                <div style="background-color: #F8FAFC; padding: 20px; text-align: center; border-radius: 6px; margin: 20px 0;">
                    <span style="font-size: 2rem; font-weight: 800; letter-spacing: 0.2em; color: #0F172A;">{otp_code}</span>
                </div>
                <p style="font-size: 0.875rem; color: #64748B;">This code will expire in 5 minutes. If you did not request this code, please ignore this email.</p>
                <hr style="border: none; border-top: 1px solid #F1F5F9; margin: 20px 0;">
                <p style="font-size: 0.75rem; color: #94A3B8; text-align: center;">🛡️ Reliable Reads | Advanced AI News Verification</p>
            </div>
        </body>
        </html>
        """
        
        if self.enabled:
            try:
                msg = MIMEMultipart()
                msg['From'] = self.smtp_user
                msg['To'] = receiver_email
                msg['Subject'] = subject
                msg.attach(MIMEText(body, 'html'))
                
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_user, self.smtp_pass)
                    server.send_message(msg)
                
                logger.info(f"OTP sent successfully to {receiver_email}")
                return True
            except Exception as e:
                logger.error(f"Failed to send email via SMTP: {e}")
                self._print_sim(receiver_email, otp_code)
                return False
        else:
            self._print_sim(receiver_email, otp_code)
            return True

    def _print_sim(self, email, otp):
        print("\n" + "="*50)
        print(f" [SIMULATED EMAIL SYSTEM]")
        print(f" TO: {email}")
        print(f" SUBJECT: Reliable Reads Verification")
        print(f" CODE: {otp}")
        print("="*50 + "\n")
