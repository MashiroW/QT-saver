import json
import os
from datetime import datetime

dirname = os.path.dirname(__file__)
INDEX_PATH = os.path.join(dirname, "downloads_index.json")


def _load() -> list:
    if not os.path.exists(INDEX_PATH):
        return []
    try:
        with open(INDEX_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save(entries: list):
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(entries, f, indent=2)


def record_download(path: str, account_id: str, username: str, kind: str, privacy: str):
    """
        Records one downloaded file in the local gallery index.

        kind: "photo" or "video"
        privacy: "public", "private", or "unknown" -- whether the
        source account was public or private at download time.
    """
    entries = _load()
    entries.append({
        "path": path,
        "account_id": account_id,
        "username": username or account_id,
        "kind": kind,
        "privacy": privacy,
        "timestamp": datetime.now().isoformat(timespec="seconds"),
    })
    _save(entries)


def get_entries(profile: str = None, privacy: str = None) -> list:
    """
        Returns index entries newest-download-first, optionally
        filtered by account_id (profile) and/or privacy
        ("public"/"private"). Entries whose file has since been
        moved/deleted are skipped.
    """
    entries = [e for e in _load() if os.path.exists(e.get("path", ""))]

    if profile:
        entries = [e for e in entries if e.get("account_id") == profile]
    if privacy:
        entries = [e for e in entries if e.get("privacy") == privacy]

    entries.sort(key=lambda e: e.get("timestamp", ""), reverse=True)
    return entries


def remove_entry(path: str):
    """
        Removes the index entry for the given file path, if any. Does
        not touch the file itself -- callers are responsible for
        deleting it from disk separately.
    """
    entries = [e for e in _load() if e.get("path") != path]
    _save(entries)


def get_known_profiles() -> list:
    """
        Returns a sorted list of (account_id, username) pairs seen in
        the index so far, for populating the Gallery's profile filter.
    """
    seen = {}
    for e in _load():
        seen[e.get("account_id")] = e.get("username") or e.get("account_id")
    return sorted(seen.items(), key=lambda kv: kv[1].lower())
