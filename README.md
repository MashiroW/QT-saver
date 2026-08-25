![Alt text](./res/main.png?raw=true "Welcome")

## Summary

<details open>
<summary>Intro</summary>

* **Description**
* **Releases**
</details>

<details open>
<summary>Project Setup</summary>
</details>

<details open>
<summary>QTSaver GUI</summary>

* **Preview**
* **Run the project**
* **Details**
</details>

-----
# Intro
## Description
QTSaver v3.0 saves someone's Instagram stories — public and private, photos and videos — straight to your computer.

Earlier versions worked without ever touching your Instagram credentials, relying on a URL you'd open in your own logged-in browser and a JSON response you'd copy over by hand. Instagram's May 2025 API changes broke that method for good (not just for QTSaver — every tool built the same way stopped working). Version 3.0 is a from-the-ground-up rewrite around a real, authenticated Instagram session (via `instagrapi`), which is what makes story downloading reliable again.

**How it works:**
- You log in once with your Instagram username and password (optionally saved securely to your OS credential store, never as plain text).
- Your session is cached locally so you don't need to log in every time you open the app.
- Add the accounts you want to track by username, and QTSaver fetches their current stories directly through the authenticated session.
- Everything you download is indexed locally, so the built-in Library/Gallery view stays in sync with what's actually on disk.

## Releases
If you are looking for the executables here's where you can get them

Version | Status | Link |
| ------------- | ------------- | ------------- |
| QTSaver v3.0 | Supported | Coming soon |
| QTSaver v2.0.1 (legacy, no-login) | Archived — no longer functional | [v2.0.1](https://github.com/MashiroW/QT-saver/releases/tag/v2.0.1) |

-----
## Project Setup

This project is developed with `Python v3.10`.

### Install the dependencies

In your root folder, do:
  - `pip install --upgrade pip`
  - `pip install -r requirements.txt`

-----

# QTSaver GUI
## Preview
<!-- https://user-images.githubusercontent.com/47890166/213941207-f419cbf5-de93-4e7a-87ab-5c365a819ba7.mp4 -->
https://github.com/user-attachments/assets/77bc609e-2b4d-4627-a3e2-83bc9e87afc9

## Run the project
  - `python gui_new.py`

## Details
On first launch, log in with your Instagram account (2FA/verification codes are supported if your account requires them). From there:

- **Accounts** — add/remove the Instagram accounts you want to track, and pull their current stories.
- **Library** — browse, preview, and manage everything you've downloaded so far.
- **Settings** — change your output folder and manage your session.
- **About** — app info and links.

`config.ini` stores your output path and saved account list. Your Instagram session is cached in `session.json`, kept locally and never committed to the repo.
