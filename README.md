![Alt text](./res/main.png?raw=true "Welcome")

## Summary

<details open>
<summary>Intro</summary>

* **Description**
* **Features list comparaison**
* **Releases**
</details>

<details open>
<summary>Projects Setup</summary>
</details>

<details open>
<summary>QTSaver GUI (Actual)</summary>

* **Preview**
* **Run the project**
* **Details**
</details>

<details open>
<summary>Legacy versions</summary>

* <sub>Old GUI (Legacy)</sub>
* <sub>QTSaver CLI</sub>


</details>

-----
# Intro
## Description
- This script is used to save someone's stories on Instagram.
- It can save EVERY story (public&private) you have access to with your account.
- This script DOESN'T USE your credentials.
- You will need to have your Instagram account logged in your usual browser.

## Features List Comparaison
Feature | QT_Saver GUI | QT_Saver GUI (Legacy) | QT_Saver CLI (Legacy)
| ------------- | ------------- | ------------- | ------------- |
| Download Public and Private Stories  | YES  | YES  | YES  |
| Store accounts IDs  | YES  | Only one ID manually through the `.ini` file  | Only one ID manually through the `.ini` file  |
| Editing the accounts list while running | YES | NO | NO |
| Editing the ouput folder while running | YES | NO | NO |
| Folder creation by Id option | YES | NO | NO |
| Folder creation by date option | YES | NO | NO |
| Supports the use of unsaved IDs | YES | YES | NO |
| Supports relative paths | YES | NO | NO |
| Error log output | YES | YES | NO |
| Download pics and/or vids option | YES | NO | NO |
| Progress shown while downloading | YES | NO | YES |
| Light mode | YES | NO | NO |
| Dark mode | YES | YES | YES |

## Releases
If you are looking for the executables here's where you can get them

Version | Status | Link | 
| ------------- | ------------- | ------------- |
| QT_Saver GUI (!Recommended!) | Supported | [v2.0](https://github.com/MashiroW/QT-saver/releases/tag/v2.0) |
| QT_Saver GUI (Legacy) | NOT Supported | URL_TO_ADD_HERE LATER |

-----
## Project Setup

These three projects have been developed with `Python v.3.10.7`.
This setup here works with all the QT_Saver version.

### Generate a requirements.txt file
In your root folder, do:

  - `pip install pipreqs`
  - `python -m pipreqs.pipreqs . --force`

### Install the dependencies

In your root folder, do:
  - `pip install --upgrade pip`
  - `pip install pipreqs`
  - `pip install -r requirements.txt`
-----

# QTSaver GUI
## Preview
https://user-images.githubusercontent.com/47890166/213941207-f419cbf5-de93-4e7a-87ab-5c365a819ba7.mp4

## Run the script
  - `python ./new_gui.py`
  
## Details
The `config.ini` file allows you to access all your options data and also works as the accounts database.

-----
# Legacy versions (CLI & GUI)
## QTSaver GUI (Legacy)
### Preview
![image](https://user-images.githubusercontent.com/47890166/213942991-b6066f5d-13b7-4412-8152-c587a966448d.png)

### Run the script
  - `python ./gui.py`

## Details
The `config.ini` file allows you to access all your options.
In that file the only two fields that are related to this Legacy version are `userid=` and `savepath=`

## QTSaver GUI (Legacy)
### Run the script
  - `python ./QT_saver.py`

## Details
The `config.ini` file allows you to access all your options.
In that file the only two fields that are related to this Legacy version are `userid=` and `savepath=`
