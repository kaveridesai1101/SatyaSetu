# 🍃 Connect Your App to MongoDB Atlas (Detailed Guide)

You selected **MongoDB Atlas** as your database. Here is how to get your connection string (URI) step-by-step.

## Step 1: Create an Account
1.  Go to **[MongoDB.com/atlas](https://www.mongodb.com/cloud/atlas/register)**.
2.  Sign up (Google Sign-In is fastest).
3.  You might be asked to fill a short survey (Role, Goal) - just select anything (e.g., "Student", "Learning").

## Step 2: Create a Cluster
1.  On the "Deploy a database" screen, select the **M0 Free** tier (the option on the right).
2.  Choose a provider (AWS) and region (e.g., N. Virginia or whichever is green/free).
3.  Name your cluster "Cluster0" (default) or "VeriSense".
4.  Click **"Create"**. (It takes 1-3 minutes to deploy).

## Step 3: Create a Database User
1.  You will see "Security Quickstart".
2.  **Username**: Enter `admin`.
3.  **Password**: Enter a simple password (e.g., `password123`). **Write this down!**
4.  Click **"Create User"**.

## Step 4: Allow Network Access
1.  Scroll down to "IP Access List".
2.  Click **"Add My Current IP Address"** OR strictly for testing/development, enter `0.0.0.0/0` (Allow Access from Anywhere).
3.  Click **"Finish and Close"**.

## Step 5: Get the Connection String
1.  Go to your **Database** dashboard (click "Database" on the left sidebar).
2.  Click the **"Connect"** button on your cluster card.
3.  Select **"Drivers"**.
4.  Ensure **Driver** is set to `Python` and **Version** is `3.6 or later`.
5.  **Copy the connection string.** It looks like this:
    ```
    mongodb+srv://admin:<password>@cluster0.abcde.mongodb.net/?retryWrites=true&w=majority
    ```

## Step 6: Paste into Your Project
1.  Open the file named `.env` in your project folder (`c:/Users/kusum/OneDrive/Desktop/Fake News Detector for Students`).
    *   *If you don't see `.env`, check for `.env.example`, rename it to `.env`.*
2.  Find `MONGODB_URI=...`
3.  Paste your copied string.
4.  **Important**: Replace `<password>` with the actual password you created in Step 3 (remove the `< >` brackets).
    *   *Example*: `mongodb+srv://admin:password123@cluster0...`
5.  Save the file.

## Step 7: Restart the App
1.  In your terminal, stop the app (Ctrl+C).
2.  Run it again:
    ```bash
    streamlit run app.py
    ```
3.  Check the terminal. It should say: `Successfully connected to MongoDB Atlas`.
