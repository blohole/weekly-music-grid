# Bluesky Weekly 3x3 Chart Bot

This bot automatically generates a 3x3 grid of your top albums from the last 7 days using **Last.fm** data and posts it to **Bluesky**. It runs automatically every Sunday via GitHub Actions.

![Weekly Chart Bot Status](https://github.com/minty-ice/weekly-music-grid/actions/workflows/main.yml/badge.svg)

---

## 🚀 Setup Instructions for New Users

### 1. Requirements
You will need:
* A **Last.fm** account (with scrobbles).
* A **Bluesky** account.
* A **GitHub** account.

### 2. Get Your API Keys
1. **Last.fm API:** Go to [Last.fm API Create](https://www.last.fm/api/account/create) and get an **API Key**. (You can leave 'Callback URL' blank).
2. **Bluesky App Password:** Go to Bluesky Settings > Moderation > **App Passwords**. Create one named "ChartBot" and copy the password.

### 3. Configure the Code
Edit the `bot.py` file in this repository:
* Change `LASTFM_USER` to your Last.fm username.
* Change `BSKY_HANDLE` to your Bluesky handle (e.g., `user.bsky.social`).

### 4. Add Secrets to GitHub (Crucial!)
GitHub needs your passwords to run the script. **Do not** paste them into the code.
1. In your GitHub repo, go to **Settings** > **Secrets and variables** > **Actions**.
2. Click **New repository secret** and add:
   * **Name:** `LASTFM_API_KEY` | **Value:** (Your Last.fm Key)
   * **Name:** `BSKY_PASSWORD` | **Value:** (Your Bluesky App Password)

---

##  How it Works
The bot uses a **GitHub Action** (defined in `.github/workflows/main.yml`) that follows this logic:



* **Schedule:** Every Sunday at 14:00 UTC.
* **Libraries:** Uses `Pillow` for image processing and `atproto` for the Bluesky API.
* **Post Format:** A 3x3 image grid with a text list of the top albums.

---

##  Manual Testing
Want to see it work right now?
1. Go to the **Actions** tab in this repo.
2. Click **Weekly Bluesky 3x3** on the left.
3. Click the **Run workflow** dropdown and hit the green button.