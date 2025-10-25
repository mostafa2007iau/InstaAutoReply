# Instagram Automation Service

A simple, lightweight REST API service to automate Instagram interactions like replying to comments and sending DMs. Designed for easy integration with tools like n8n.

## 🎯 Core Features

-   **Multi-Account Login**: Manage sessions for multiple Instagram accounts.
-   **Comment Fetching**: Get the latest comments from any public post.
-   **Comment Replies**: Reply to a specific comment.
-   **Direct Messages**: Send a DM to any Instagram user.
-   **Session Management**: Sessions are stored locally in `accounts.json`.
-   **Rate Limiting**: Simple sleep intervals to avoid account bans.
-   **Duplicate Prevention**: Keeps track of replied comments in `replied.json`.

## ⚙️ Project Structure

```
insta_service/
├── main.py              # Main FastAPI application
├── accounts.json        # Stores account session data
├── replied.json         # Stores IDs of replied comments
├── requirements.txt     # Python dependencies
├── Dockerfile           # For containerized deployment
└── README.md            # This file
```

## 🧠 Tech Stack

-   **Web Framework**: FastAPI
-   **Instagram Library**: `instagrapi`
-   **Web Server**: Uvicorn
-   **Datastore**: Simple JSON files (no external database needed)

## 📡 API Endpoints

The service runs on `http://YOUR_SERVER_IP:8008`.

| Method | Path         | Description                                     |
| :----- | :----------- | :---------------------------------------------- |
| `GET`  | `/status`    | Check service health and see logged-in accounts.|
| `POST` | `/login`     | Log in an account and save its session.         |
| `GET`  | `/accounts`  | Get a list of all logged-in accounts.           |
| `GET`  | `/comments`  | Get comments from a specific post URL.          |
| `POST` | `/reply`     | Reply to a specific comment.                    |
| `POST` | `/dm`        | Send a direct message to a user.                |

## 🧰 Installation and Setup

### Prerequisites
-   Python 3.10+
-   `git`

### Local Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/insta_service.git
    cd insta_service
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the service:**
    ```bash
    uvicorn main:app --host 0.0.0.0 --port 8008
    ```

The service will be available at `http://YOUR_SERVER_IP:8008`.

### Docker Setup

1.  **Build the Docker image:**
    ```bash
    docker build -t insta-service .
    ```

2.  **Run the Docker container:**
    ```bash
    docker run -d -p 8008:8008 --name insta-service-container insta-service
    ```
    Data (`accounts.json`, `replied.json`) will be stored inside the container. For persistent storage, use volumes:
    ```bash
    docker run -d -p 8008:8008 \
      -v $(pwd)/accounts.json:/app/accounts.json \
      -v $(pwd)/replied.json:/app/replied.json \
      --name insta-service-container insta-service
    ```

## 💬 API Usage Examples

### 1. Login an Account

**Request:** `POST /login`

**Body:**
```json
{
  "username": "my_insta_account",
  "password": "my_secret_password"
}
```

### 2. Get Post Comments

**Request:** `GET /comments?username=my_insta_account&url=https://www.instagram.com/p/Cxyz123abc/`

### 3. Reply to a Comment

**Request:** `POST /reply`

**Body:**
```json
{
  "username": "my_insta_account",
  "comment_id": "12345678901234567",
  "text": "Thanks for your comment! 🙌"
}
```

### 4. Send a Direct Message

**Request:** `POST /dm`

**Body:**
```json
{
  "username": "my_insta_account",
  "target_username": "some_user",
  "message": "Hello, we saw your comment and wanted to reach out."
}
```

## 🧩 n8n Integration

You can easily connect this service to an n8n workflow using the **HTTP Request** node.

-   **URL**: `http://YOUR_SERVER_IP:8008/<endpoint>` (e.g., `http://192.168.1.50:8008/reply`)
-   **Method**: `POST` or `GET`
-   **Body Content Type**: `JSON`
-   **Body**: Use expressions to pass data from previous nodes, like comment IDs or user-generated text.
