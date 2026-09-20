"""
Optional usage-data capture via Firebase Firestore.

Design principles (matching ai_chat.py's pattern):
  - Never crashes the app if Firebase isn't configured -- is_configured()
    gates every call site, and every write is wrapped in try/except so a
    Firestore hiccup never breaks the user's actual experience.
  - Logs a deliberately narrow set of fields -- enough for basic usage
    analytics (how many charts generated, which categories people ask
    about, which languages are used), not a full copy of the person's
    entire report. No name, no contact info is collected anywhere in this
    app to begin with, so there's nothing more identifying to accidentally
    over-log here than the birth data the person already typed in.
"""
import datetime

try:
    import firebase_admin
    from firebase_admin import credentials, firestore
except ImportError:
    firebase_admin = None

_client = None
_init_attempted = False


def _get_secrets():
    try:
        import streamlit as st
        if "firebase" in st.secrets:
            return dict(st.secrets["firebase"])
    except Exception:
        pass
    return None


def is_configured() -> bool:
    return firebase_admin is not None and _get_secrets() is not None


def _client_or_none():
    """Lazily initialize the Firebase app exactly once per process."""
    global _client, _init_attempted
    if _client is not None:
        return _client
    if _init_attempted:
        return None
    _init_attempted = True

    secrets = _get_secrets()
    if not secrets or firebase_admin is None:
        return None

    try:
        if not firebase_admin._apps:
            cred = credentials.Certificate(secrets)
            firebase_admin.initialize_app(cred)
        _client = firestore.client()
        return _client
    except Exception:
        return None


def log_chart_request(data: dict):
    """data: e.g. {timestamp, lang, mode, gender, birth_year, birth_month,
    day_master, bureau_name, life_palace_stars, current_year}"""
    db = _client_or_none()
    if db is None:
        return
    try:
        payload = dict(data)
        payload.setdefault("timestamp", datetime.datetime.utcnow().isoformat())
        db.collection("chart_requests").add(payload)
    except Exception:
        pass  # never let logging failures affect the user's experience


def log_chat_message(data: dict):
    """data: e.g. {timestamp, lang, chart_key, category, question, answer}"""
    db = _client_or_none()
    if db is None:
        return
    try:
        payload = dict(data)
        payload.setdefault("timestamp", datetime.datetime.utcnow().isoformat())
        db.collection("chat_logs").add(payload)
    except Exception:
        pass
