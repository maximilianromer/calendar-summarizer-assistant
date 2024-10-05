# Calendar Summarizer Assistant

This guide helps you set up an automated system that sends you daily calendar summaries straight to your phone via Telegram. It integrates Google Calendar and Google Sheets through the Google Cloud Platform, uses the free Google Gemini API to summarize the calendar, and uses a GitHub Action to provide you with an automated message every day.

## Overview

The process works like this:

1. **Google Calendar Data**: Your calendar data is imported into a Google Sheet.
2. **Summary Generation**: A Python script pulls the Google Sheet and uses the Google Gemini API to summarize calendar events.
3. **Telegram Notification**: The summary is sent to you via a Telegram bot.
4. **Automation**: The process runs every day through GitHub Actions.

## Prerequisites

1. **Google Account**: You need a Google account with access to Sheets, Calendar, Google Cloud Platform, and the Gemini API. Most personal accounts work fine.
2. **GitHub Account**: For storing your project code and automating actions (a free account works fine).
3. **Telegram Account**: To set up a bot and recieve messages.

## Google Setup: API and Sheets

### Step 1: Create a Google Sheet

- Create a new Google Sheet where your calendar data will be imported.
- Note down the **Spreadsheet ID**. It can be found in the URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`

### Step 2: Set Up Your Google Cloud Project

1. **Enable Google Sheets and Calendar API**: Go to [Google Cloud Console](https://console.developers.google.com/), create a new project, and enable the Google Sheets and Calendar APIs.
2. **Create Service Account Credentials**:
   - In the **APIs & Services** > **Credentials** section, click **Create Credentials** > **Service Account**.
   - Once created, download the JSON key file.
   - Save this JSON to a secure folder; you'll need it later.
3. **Share the Google Sheet** with the service account email from the JSON file using the standard Google Sheet share feature.

### Step 3: Set Up Your Google Script

1. **Create a Google Script**:

   - On the Google Sheet, click on **Extensions** > **Apps Script**. This will open the Google Apps Script editor in a new tab.

   - In the script editor, delete any default code and paste in [code.gs](https://github.com/maximilianromer/calendar-summarizer-assistant/blob/main/code.gs)
   - Save your script by clicking on the disk icon.

2. **Activate the Calendar API**:

   - In the Apps Script editor, click on the **Services** icon (a plus symbol on the left).
   - Search for **Calendar API**, select it, and click **Add**.

3. **Run and Test the Script**:

   - Click the play button (▶) in the script editor to run your script and test it.
   - You may be prompted to authorize the script—make sure to allow all requested permissions.

Once your script runs, the Google Sheet should instantly populate with the contents of your calendar for the next seven days.

### Step 4: Automate Your Google Sheet

1. **Set Up a Trigger**:
   - In the Google Apps Script editor, click on the **clock icon** on the left sidebar to open the **Triggers** page.
   - Click on **+ Add Trigger**.
   - Under which function to run, select `updateCalendarEvents`.
   - Under event source, select `Time-driven`.
   - Under type of trigger, select `Hour timer`.
   - Under hour interval, select `Every hour`.

This will ensure that your Google Sheet is updated every hour with your calendar events.
## Google Setup: Gemini API
1. Go to the [Google AI for Developers](ai.google.dev) homepage.
2. Select the blue `Get API key in Google AI Studio` button
3. Click `Create API key`
4. Click on the search bar and select the name of the Google Cloud project you created earlier
5. Save the API key provided. Ensure that it is listed as a free plan key.

## Telegram Bot Setup

1. **Create a Bot**: Open Telegram and search for the **BotFather** bot. Send `/newbot` and follow the instructions to create your bot.
2. **Save the Token**: After creating the bot, you'll receive an API token. Save this securely.
3. **Get Your Chat ID**: Search for the **IDBot** bot on Telegram to find your Telegram user ID. Start a chat and send the command `/getid` to receive your chat ID. Save this for later.

## Set Up Your GitHub Repository

### Step 1: Create a Repository

1. **Create a New Repository**: Go to [GitHub](https://github.com/) and log in to your account.
2. **Click on New**: Click the **+ icon** in the top right corner and select **New repository**.
3. **Repository Settings**:
   - **Name**: Give your repository a name (e.g., `calendar-summary`).
   - **Privacy**: Select **Private** to keep your project private.
4. **Create Repository**: Click **Create repository** to finish.

### Step 2: Create Your Main Python Script

In your new repository, create a file named `main-file.py` in your project directory and paste the contents of [main-file.py](https://github.com/maximilianromer/calendar-summarizer-assistant/blob/main/main-file.py) into it

Then, replace `US/Mountain` with your local time zone. You can find the variable for your local time zone [here.](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568)

### Step 3: Create a GitHub Actions Workflow

Create another file. For the title, paste in `.github/workflows/run_script.yml`. Paste the contents of [run_script.yml](https://github.com/maximilianromer/calendar-summarizer-assistant/blob/main/run_script.yml) into the file.

The cron expression set (`0 18 * * *`) runs the script daily at 3:30 PM MST. Adjust this to fit your preferred time using [Crontab](https://crontab.guru/).

## Add Secrets to GitHub Repository

1. **Go to Your Repository**: Navigate to your GitHub repository, and click on **Settings**.
2. **Navigate to Secrets and Variables**: Under **Security**, click on **Secrets and variables**, and then **Actions**.
3. **Add Secrets**: Click **New repository secret** for each of the following secrets:
   - `GOOGLE_API_KEY`: Paste your Google Gemini API key here.
   - `GOOGLE_CREDENTIALS`: Paste the JSON file contents from your Google Service Account here.
   - `SHEET_ID`: Your Google Sheet ID.
   - `TELEGRAM_BOT_TOKEN`: The Telegram bot token you received from BotFather.
   - `TELEGRAM_CHAT_ID`: The chat ID you received from @IDBot.

## Putting It All Together

 - Under the actions tab, if you select `.github/workflows/run_script.yml` and `Run workflow`, you can test the action. After a minute or two, your Telegram account should receive the chat summary message.
 - You should now automatically recieve the chat summary message at the time you set. GitHub leaves you no way of knowing that it is set, so you will have to wait for it to happen automatically to see if you set the time correctly. You can check the actions tab in GitHub for error messages.
 - If you have any issues or ideas for improvement, please let me know!
