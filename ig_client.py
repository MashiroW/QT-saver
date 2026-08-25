import os

from instagrapi import Client
from instagrapi.exceptions import TwoFactorRequired

try:
    import keyring
    HAS_KEYRING = True
except ImportError:
    HAS_KEYRING = False

dirname = os.path.dirname(__file__)
SESSION_PATH = os.path.join(dirname, "session.json")

KEYRING_SERVICE = "QTSaver-Instagram"
KEYRING_LAST_USER_KEY = "__last_username__"

_client = None
_username = None


class LoginCancelled(Exception):
    """
        Raised when the user closes/cancels a verification code
        prompt instead of answering it.
    """
    pass


def is_logged_in() -> bool:
    return _client is not None


def current_username() -> str:
    return _username


def get_remembered_username():
    """
        Returns the username of the last account that was
        successfully logged in with "remember password" checked,
        or None. Read from the OS credential store, never from a file.
    """
    if not HAS_KEYRING:
        return None
    try:
        return keyring.get_password(KEYRING_SERVICE, KEYRING_LAST_USER_KEY)
    except Exception:
        return None


def get_saved_password(username: str):
    """
        Returns the remembered password for the given username from
        the OS credential store (Windows Credential Manager, etc.),
        or None if nothing is saved.
    """
    if not HAS_KEYRING or not username:
        return None
    try:
        return keyring.get_password(KEYRING_SERVICE, username)
    except Exception:
        return None


def forget_saved_login(username: str = None):
    """
        Deletes the cached session file and, if a username is given,
        removes its remembered password (and the "last username"
        pointer) from the OS credential store.
    """
    global _client, _username

    if os.path.exists(SESSION_PATH):
        os.remove(SESSION_PATH)

    if HAS_KEYRING and username:
        for key in (username, KEYRING_LAST_USER_KEY):
            try:
                keyring.delete_password(KEYRING_SERVICE, key)
            except Exception:
                pass

    _client = None
    _username = None


def try_restore_session(log=lambda msg: None) -> bool:
    """
        Attempts to restore a previously saved Instagram session from
        session.json without needing any credentials. Returns True if
        a valid session was restored.
    """
    global _client, _username

    if not os.path.exists(SESSION_PATH):
        return False

    log("Checking saved Instagram session...")
    cl = Client()
    try:
        cl.load_settings(SESSION_PATH)
        info = cl.account_info()
    except Exception as e:
        log("Saved session is no longer valid ({0}), you'll need to log in again.".format(e))
        return False

    _client = cl
    _username = info.username
    log("Session restored, logged in as @{0}.".format(_username))
    return True


def login(username: str, password: str, remember: bool = False,
          code_prompt=None, log=lambda msg: None) -> None:
    """
        Logs in to Instagram with the given credentials.

        If Instagram asks for a verification code (either a
        checkpoint/challenge, or classic 2FA), code_prompt(message) is
        called to obtain it. It must return the code as a string (or
        a falsy value to cancel), and is expected to block the caller
        since this whole function is meant to run off the GUI thread.

        On success the session is cached to session.json, and if
        remember is True the password is stored in the OS credential
        store (never written to a plain file).
    """
    global _client, _username

    cl = Client()

    def _challenge_handler(challenge_username, choice):
        if code_prompt is None:
            raise RuntimeError("Instagram requires a verification code, but no prompt was provided")
        code = code_prompt("Instagram sent a verification code (SMS/Email). Enter it to continue:")
        if not code:
            raise LoginCancelled("Login cancelled: verification code required")
        return code

    cl.challenge_code_handler = _challenge_handler

    log("Logging in to Instagram as @{0}...".format(username))
    try:
        cl.login(username, password)
    except TwoFactorRequired:
        if code_prompt is None:
            raise
        log("Two-factor authentication required.")
        code = code_prompt("Enter your 2FA code (SMS or authenticator app):")
        if not code:
            raise LoginCancelled("Login cancelled: 2FA verification code required")
        cl.login(username, password, verification_code=code.strip())

    cl.dump_settings(SESSION_PATH)
    log("Login successful, session saved locally.")

    if remember:
        if HAS_KEYRING:
            try:
                keyring.set_password(KEYRING_SERVICE, username, password)
                keyring.set_password(KEYRING_SERVICE, KEYRING_LAST_USER_KEY, username)
                log("Password remembered securely in your OS credential store.")
            except Exception as e:
                log("Could not save the password securely ({0}), you'll need to re-enter it next time.".format(e))
        else:
            log("The 'keyring' package isn't available, so the password can't be remembered securely.")

    _client = cl
    _username = username


def resolve_user_id(username: str):
    """
        Resolves an Instagram @username to its numeric account id
        using the logged-in session. Returns None if it can't be
        resolved (unknown username, not logged in, etc).
    """
    if _client is None:
        return None
    try:
        username = username.strip().lstrip("@")
        return _client.user_id_from_username(username)
    except Exception:
        return None


def get_account_meta(user_id: str) -> tuple:
    """
        Returns (privacy, username) for the given account id, using
        the logged-in session. privacy is "private"/"public"/"unknown";
        username is None if it couldn't be resolved. Used to tag
        downloaded content in the local gallery index.
    """
    if _client is None:
        return "unknown", None
    try:
        info = _client.user_info(str(user_id))
        return ("private" if info.is_private else "public"), info.username
    except Exception:
        return "unknown", None


def fetch_user_stories(user_id: str, videos: bool = True, photos: bool = True, log=lambda msg: None) -> tuple:
    """
        Fetches the current stories of the given userId through the
        logged-in Instagram private-API session (instagrapi).

        Returns a (dict, userId) tuple where the dict is in the
        {url : ".mp4"/".jpg"} format.
    """
    if _client is None:
        raise RuntimeError("Not logged in to Instagram yet")

    log("Fetching stories for account id {0}...".format(user_id))
    stories = _client.user_stories_v1(str(user_id))
    log("Found {0} story item(s).".format(len(stories)))

    output_dict = {}
    for story in stories:
        # media_type: 1 = photo, 2 = video
        if story.media_type == 2 and videos and story.video_url:
            output_dict[str(story.video_url)] = ".mp4"
        elif story.media_type == 1 and photos and story.thumbnail_url:
            output_dict[str(story.thumbnail_url)] = ".jpg"

    return output_dict, str(user_id)
