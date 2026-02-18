# SMTP Alternative: Mailtrap Guide ✉️

If your Gmail SMTP is not working (which is common due to Google's strict security), **Mailtrap** is the best alternative for developers to test email/OTP flows.

## What is Mailtrap?
It is a "Fake SMTP Server" that intercepts all outgoing emails from your app and shows them in its own dashboard. It is free and takes 2 minutes to set up.

## Step-by-Step Setup

1.  **Sign Up**: Go to [mailtrap.io](https://mailtrap.io/) and create a free account.
2.  **Access Inbox**: Go to "Email Testing" > "Inboxes".
3.  **Get Credentials**:
    *   Click on "My Inbox".
    *   Under "SMTP Settings", copy your credentials.
4.  **Update your `.env`**:
    ```env
    SMTP_SERVER=sandbox.smtp.mailtrap.io
    SMTP_PORT=2525
    SMTP_USER=your_mailtrap_user_id
    SMTP_PASSWORD=your_mailtrap_password
    ```
5.  **Restart App**: Run `streamlit run app.py` again.

## Why use this?
- No need to reveal your real password.
- No need to configure 2-Step Verification for Gmail.
- Works perfectly for student project demonstrations.
