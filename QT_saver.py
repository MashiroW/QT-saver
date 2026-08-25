from configparser import ConfigParser
import requests
import json
import os
import ast
import subprocess
from crash import *
from tkinter.filedialog import askdirectory
from datetime import datetime
import ig_client

#Relative path
dirname = os.path.dirname(__file__)

# Application configuration
app_config = ConfigParser()
app_config.read(os.path.join(dirname, "./config.ini"))
SYSTEM_SECTION_APP    = app_config.sections()[0]

def getUsers() -> dict:
    """
        Returns a dict as a json object containing the users database
        in the { Id1 : username1, ... , IdN : usernameN}
    """
    return json.loads(str(app_config.get(SYSTEM_SECTION_APP, 'savedusers')))

def addUser(userId, userName) -> int:
    """
        Adds an user to the database.
        Returns 1 in case of failure.
        Returns 0 in case of success.
    """

    savedUsers = getUsers()
    if userId in savedUsers or userName in savedUsers.values():
        return 1

    else:
        savedUsers[userId] = userName
        savedUsers         = json.dumps(ast.literal_eval(str(savedUsers)))

        app_config.set(SYSTEM_SECTION_APP, 'savedusers', str(savedUsers))

        with open('config.ini', 'w') as configfile:
            app_config.write(configfile)
        return 0

def deleteUserByName(userName) -> int:
    """
        Deletes an user from the database by UserName.
        Returns 1 in case of failure.
        Returns 0 in case of success.
    """

    savedUsers = getUsers()
    for key, value in savedUsers.items():
        if value == userName:
            savedUsers.pop(key)
            savedUsers = json.dumps(ast.literal_eval(str(savedUsers)))

            app_config.set(SYSTEM_SECTION_APP, 'savedusers', str(savedUsers))

            with open('config.ini', 'w') as configfile:
                app_config.write(configfile)

            return 0
    return 1

def getOutputPath() -> str:
    """
        Returns the output path from the database in a string
    """

    path = str(app_config.get(SYSTEM_SECTION_APP, 'savepath'))

    if path[0] == ".":
        return dirname[0].capitalize() + dirname[1:] + path[1:].replace("/", "\\")

    else:
        return path.replace("/", "\\")

def setOutputPath():
    """
        Edits the output path from the database from opening the
        windows explorer and letting the user edit its path
    """

    savepath = askdirectory()
    if savepath != "":
        app_config.set(SYSTEM_SECTION_APP, 'savepath', str(savepath))

        with open('config.ini', 'w') as configfile:
            app_config.write(configfile)

def openOuputPath():
    """
        Opens the output path from the database using the
        windows explorer
    """
    try:
        os.startfile(getOutputPath())
    except:
        msgbox(msg="Your folder doesn't exist... yet ?", title="Error", windowtype=0)

def openMediaFile(path : str) -> bool:
    """
        Opens the given file with whatever application Windows has
        associated with it (default photo viewer, video player, etc).
        Returns True on success.
    """
    try:
        os.startfile(path)
        return True
    except Exception:
        return False

def revealInExplorer(path : str) -> bool:
    """
        Opens Windows Explorer with the given file pre-selected
        (equivalent to "Show in folder"). Returns True on success.
    """
    try:
        # Explorer's /select syntax needs the comma *outside* the
        # quoted path: explorer /select,"C:\some path\file.jpg".
        # Passing a list to Popen runs it through list2cmdline, which
        # (since the path itself usually contains spaces) quotes the
        # whole "/select,<path>" token together instead -- a string
        # deliberately isn't split into args, so this reproduces
        # Explorer's own documented syntax exactly.
        subprocess.Popen('explorer /select,"{0}"'.format(os.path.normpath(path)))
        return True
    except Exception:
        return False

def getContentDictFromApi(userId : str, videos : bool = True, photos : bool = True, log = lambda msg: None) -> list:
    """
        Fetches the current stories for the given userId directly
        through a logged-in Instagram session (instagrapi).

        Returns a [dict, str]: a dict in the {URL : type} format
        alongside the userId used.
    """
    return ig_client.fetch_user_stories(userId, videos=videos, photos=photos, log=log)

def resolveUserId(username : str):
    """
        Resolves an Instagram @username to its numeric account id
        using the logged-in session. Returns None if it can't be
        resolved.
    """
    return ig_client.resolve_user_id(username)

def getAccountMeta(userId : str) -> tuple:
    """
        Returns (privacy, username) for the given userId, using the
        logged-in Instagram session. privacy is one of
        "private"/"public"/"unknown"; username may be None.
    """
    return ig_client.get_account_meta(userId)

def getFileByUrl(url : str, type : str, userId : str, dailyFolderState : bool = False, idFolderState : bool = True):
    """
        Downloads from the url in arguement the file to the output
        folder defined in the .ini file.

        If dailyFolderState is set to True, a folder containing
        today's date will be created.

        If idFolderState is set to True, a folder containing the
        userId will be created.

        Returns the saved file's path as a string on success.
        Returns None in case of failure.
    """

    savepath = getOutputPath()

    if dailyFolderState == True:
        date = datetime.today().strftime('%Y-%m-%d')
        savepath = "{0}\{1}".format(savepath, date)

    if idFolderState == True:
        savepath = "{0}\{1}".format(savepath, userId)

    try:
        os.makedirs(savepath, exist_ok=True)
    except FileExistsError:
        pass

    try:
        timestamp = str(datetime.now().timestamp())
        response = requests.get(url, type)
        file_savepath = savepath + "\\" + timestamp + type
        open(file_savepath, "wb").write(response.content)
        return file_savepath

    except:
        return None
