import json
import os
import time
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from instagrapi import Client
from instagrapi.exceptions import LoginRequired, ChallengeRequired

# --- Configuration ---
ACCOUNTS_FILE = Path("accounts.json")
REPLIED_FILE = Path("replied.json")
CHALLENGES_FILE = Path("challenges.json")
RATE_LIMIT_DELAY = 5  # seconds
HOURLY_REPLY_LIMIT = 30

# --- FastAPI App Initialization ---
app = FastAPI(
    title="Instagram Automation Service",
    description="A simple REST API to interact with Instagram via instagrapi.",
    version="1.0.0"
)

# --- Pydantic Models for Request Bodies ---
class LoginPayload(BaseModel):
    username: str
    password: str

class ChallengePayload(BaseModel):
    username: str
    code: str

class ReplyPayload(BaseModel):
    username: str
    comment_id: str
    text: str

class DMPayload(BaseModel):
    username: str
    target_username: str
    message: str

# --- Helper Functions for Data Persistence ---
def load_json_data(filepath: Path):
    """Loads data from a JSON file, creating it if it doesn't exist."""
    if not filepath.exists():
        filepath.write_text("{}", encoding='utf-8')
        return {}
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        if not content:
            return {}
        return json.loads(content)

def save_json_data(filepath: Path, data):
    """Saves data to a JSON file."""
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def load_accounts():
    """Loads all account sessions."""
    return load_json_data(ACCOUNTS_FILE)

def save_accounts(accounts_data):
    """Saves all account sessions."""
    save_json_data(ACCOUNTS_FILE, accounts_data)

def load_challenges():
    """Loads all pending challenges."""
    return load_json_data(CHALLENGES_FILE)

def save_challenges(challenges_data):
    """Saves all pending challenges."""
    save_json_data(CHALLENGES_FILE, challenges_data)

def load_replied_log():
    """Loads the log of replied comments."""
    data = load_json_data(REPLIED_FILE)
    return data.get("replies", [])

def save_replied_log(replies):
    """Saves the log of replied comments."""
    save_json_data(REPLIED_FILE, {"replies": replies})

# --- Instagrapi Client Management ---
def get_client(username: str) -> Client:
    """
    Retrieves an authenticated instagrapi client for a given username.
    Raises HTTPException if the session is invalid or not found.
    """
    accounts = load_accounts()
    if username not in accounts:
        raise HTTPException(status_code=404, detail=f"Account '{username}' not logged in.")

    cl = Client()
    try:
        cl.set_settings(accounts[username])
        # The following line is a lightweight check to see if the session is valid.
        cl.get_timeline_feed()
        return cl
    except LoginRequired:
        raise HTTPException(status_code=403, detail=f"Session for '{username}' has expired. Please log in again.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An unexpected error occurred: {str(e)}")

@app.on_event("startup")
async def startup_event():
    """Initialize data files on startup."""
    if not ACCOUNTS_FILE.exists():
        save_accounts({})
    if not REPLIED_FILE.exists():
        save_replied_log([])
    if not CHALLENGES_FILE.exists():
        save_challenges({})

# --- API Endpoints ---

@app.get("/status", summary="Check Service Status")
def get_status():
    """Check the health of the service and list logged-in accounts."""
    accounts = load_accounts()
    return {"status": "ok", "logged_in_accounts": list(accounts.keys())}

@app.post("/login", summary="Login an Instagram Account")
def login(payload: LoginPayload):
    """
    Logs in an Instagram account.
    If a challenge is required, it saves the temporary state for resolution.
    """
    cl = Client()
    try:
        cl.login(payload.username, payload.password)
        accounts = load_accounts()
        accounts[payload.username] = cl.get_settings()
        save_accounts(accounts)
        return {"status": "success", "username": payload.username}
    except ChallengeRequired as e:
        challenges = load_challenges()
        challenges[payload.username] = cl.get_settings()
        save_challenges(challenges)
        raise HTTPException(
            status_code=401,
            detail={
                "message": "Challenge required. Please solve the challenge and use the /challenge/resolve endpoint.",
                "username": payload.username,
            }
        )
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Login failed: {str(e)}")

@app.post("/challenge/resolve", summary="Resolve a Login Challenge")
def resolve_challenge(payload: ChallengePayload):
    """
    Resolves a login challenge using a verification code.
    """
    challenges = load_challenges()
    if payload.username not in challenges:
        raise HTTPException(status_code=404, detail=f"No active challenge found for user '{payload.username}'.")

    cl = Client()
    cl.set_settings(challenges[payload.username])

    try:
        cl.challenge_code_handler(payload.code)

        # On success, save the final session and remove the pending challenge
        accounts = load_accounts()
        accounts[payload.username] = cl.get_settings()
        save_accounts(accounts)

        del challenges[payload.username]
        save_challenges(challenges)

        return {"status": "success", "username": payload.username, "message": "Challenge resolved and logged in successfully."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to resolve challenge: {str(e)}")

@app.get("/accounts", summary="List Logged-in Accounts")
def get_accounts():
    """Returns a list of all usernames for which a session is stored."""
    accounts = load_accounts()
    return {"accounts": list(accounts.keys())}

@app.get("/comments", summary="Get Post Comments")
def get_comments(username: str = Query(...), url: str = Query(...)):
    """
    Fetches the latest comments for a specific Instagram post.
    - **username**: The account to use for the request.
    - **url**: The URL of the Instagram post.
    """
    cl = get_client(username)
    try:
        media_id = cl.media_id(cl.media_pk_from_url(url))
        comments = cl.media_comments(media_id)
        return {"comments": [comment.dict() for comment in comments]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch comments: {str(e)}")

@app.post("/reply", summary="Reply to a Comment")
def reply_to_comment(payload: ReplyPayload):
    """
    Replies to a specific comment.
    Prevents replying to the same comment twice and enforces an hourly rate limit.
    """
    replies_log = load_replied_log()

    # 1. Check for duplicate replies
    if any(entry["comment_id"] == payload.comment_id for entry in replies_log):
        raise HTTPException(status_code=409, detail="This comment has already been replied to.")

    # 2. Enforce hourly rate limit
    current_time = time.time()
    one_hour_ago = current_time - 3600

    user_replies_in_last_hour = [
        r for r in replies_log
        if r["username"] == payload.username and r["timestamp"] > one_hour_ago
    ]

    if len(user_replies_in_last_hour) >= HOURLY_REPLY_LIMIT:
        raise HTTPException(status_code=429, detail=f"Hourly reply limit of {HOURLY_REPLY_LIMIT} reached for user '{payload.username}'.")

    cl = get_client(payload.username)
    try:
        time.sleep(RATE_LIMIT_DELAY)  # Per-request delay
        cl.comment_reply(payload.comment_id, payload.text)

        # Log the new reply
        new_reply = {
            "comment_id": payload.comment_id,
            "username": payload.username,
            "timestamp": current_time,
            "text": payload.text
        }
        replies_log.append(new_reply)
        save_replied_log(replies_log)

        return {"status": "success", "message": f"Replied to comment {payload.comment_id}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to reply: {str(e)}")

@app.post("/dm", summary="Send Direct Message")
def send_direct_message(payload: DMPayload):
    """Sends a direct message to a specific user."""
    cl = get_client(payload.username)
    try:
        target_user = cl.user_info_by_username(payload.target_username)
        user_id = target_user.pk

        time.sleep(RATE_LIMIT_DELAY)  # Rate limiting
        cl.direct_send(payload.message, user_ids=[user_id])

        return {"status": "success", "message": f"DM sent to {payload.target_username}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send DM: {str(e)}")
