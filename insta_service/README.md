# Instagram Automation Service

A simple, lightweight, and robust REST API service designed to automate Instagram interactions. It handles multi-account sessions, challenge resolution, and provides endpoints for common actions like replying to comments and sending DMs. It's built for easy integration with automation platforms like n8n.

---

<div dir="rtl">

# سرویس اتوماسیون اینستاگرام

یک سرویس REST API ساده، سبک و قدرتمند برای اتوماسیون فعالیت‌های اینستاگرام. این سرویس مدیریت چندین حساب کاربری، حل چالش‌های امنیتی اینستاگرام، و ارائه اندپوینت برای عملیات رایج مانند پاسخ به کامنت‌ها و ارسال دایرکت را فراهم می‌کند و برای اتصال آسان به ابزارهای اتومیشن مانند n8n طراحی شده است.

## 🎯 قابلیت‌های کلیدی

-   **مدیریت چند اکانت**: مدیریت همزمان چندین حساب کاربری اینستاگرام.
-   **حل چالش امنیتی**: قابلیت مدیریت چالش‌های لاگین (Challenge) از طریق API.
-   **دریافت کامنت‌ها**: دریافت آخرین کامنت‌های یک پست مشخص.
-   **پاسخ به کامنت**: ریپلای خودکار به یک کامنت خاص.
-   **ارسال دایرکت**: ارسال پیام مستقیم (DM) به هر کاربر.
-   **مدیریت نشست پایدار**: نشست‌ها در فایل `accounts.json` ذخیره می‌شوند تا از لاگین مکرر جلوگیری شود.
-   **کنترل نرخ درخواست**: دارای محدودیت‌های هوشمند برای جلوگیری از مسدود شدن اکانت.
-   **جلوگیری از پاسخ تکراری**: تاریخچه پاسخ‌ها در `replied.json` ذخیره می‌شود.

## 🧰 نصب و اجرا روی سرور

### پیش‌نیازها
-   سرور (ترجیحاً Debian/Ubuntu)
-   `git`

### مراحل نصب
اسکریپت `install.sh` تمام وابستگی‌ها، از جمله پایتون و کتابخانه‌های مورد نیاز را به صورت خودکار نصب می‌کند.

۱. **کلون کردن پروژه:**
   ```bash
   # پروژه را در مسیر دلخواه خود کلون کنید، برای مثال /srv
   git clone https://github.com/YOUR_USERNAME/insta_service.git /srv/insta_service
   ```

۲. **اجرای اسکریپت نصب خودکار:**
   ```bash
   bash /srv/insta_service/install.sh
   ```

۳. **اجرای سرویس:**
   برای اجرای پایدار سرویس در پس‌زمینه، از `nohup` استفاده کنید:
   ```bash
   # به مسیر پروژه بروید
   cd /srv/insta_service
   # محیط مجازی را فعال کنید
   source venv/bin/activate
   # سرویس را اجرا کنید
   nohup uvicorn main:app --host 0.0.0.0 --port 8008 &
   ```
   سرویس روی آدرس `http://YOUR_SERVER_IP:8008` در دسترس خواهد بود.

## 📡 راهنمای کامل API

### `POST /login`
ورود به حساب کاربری اینستاگرام.

**بدنه درخواست (Request Body):**
```json
{
  "username": "my_insta_account",
  "password": "my_secret_password"
}
```

**پاسخ موفق (200 OK):**
```json
{
  "status": "success",
  "username": "my_insta_account"
}
```

**پاسخ در صورت نیاز به چالش (401 Unauthorized):**
این پاسخ به این معناست که اینستاگرام نیاز به تایید هویت دارد.
```json
{
  "detail": {
    "message": "Challenge required. Please solve the challenge and use the /challenge/resolve endpoint.",
    "username": "my_insta_account"
  }
}
```

### `POST /challenge/resolve`
حل چالش امنیتی با استفاده از کد تاییدی که به ایمیل یا شماره تلفن شما ارسال شده است.

**بدنه درخواست (Request Body):**
```json
{
  "username": "my_insta_account",
  "code": "123456"
}
```

**پاسخ موفق (200 OK):**
```json
{
  "status": "success",
  "username": "my_insta_account",
  "message": "Challenge resolved and logged in successfully."
}
```

**پاسخ ناموفق (404 Not Found):**
```json
{
  "detail": "No active challenge found for user 'my_insta_account'."
}
```

### `GET /comments`
دریافت کامنت‌های یک پست.

**پارامترها (Query Parameters):**
-   `username`: اکانتی که برای ارسال درخواست استفاده می‌شود.
-   `url`: آدرس کامل پست اینستاگرام.

**نمونه درخواست:**
`GET http://YOUR_IP:8008/comments?username=my_insta_account&url=https://www.instagram.com/p/Cxyz123abc/`

**پاسخ موفق (200 OK):**
```json
{
  "comments": [
    {
      "pk": "179...",
      "text": "This is a great post!",
      "user": { "pk": "123...", "username": "some_user" },
      "created_at_utc": "..."
    }
  ]
}
```

### `POST /reply`
پاسخ به یک کامنت.

**بدنه درخواست (Request Body):**
```json
{
  "username": "my_insta_account",
  "comment_id": "179...",
  "text": "Thanks for your comment! 🙌"
}
```

**پاسخ موفق (200 OK):**
```json
{
  "status": "success",
  "message": "Replied to comment 179..."
}
```

### `POST /dm`
ارسال پیام دایرکت.

**بدنه درخواست (Request Body):**
```json
{
  "username": "my_insta_account",
  "target_username": "some_user",
  "message": "Hello, we saw your comment and wanted to reach out."
}
```

**پاسخ موفق (200 OK):**
```json
{
  "status": "success",
  "message": "DM sent to some_user"
}
```

## 🧩 راهنمای پیشرفته اتصال به n8n
برای مدیریت کامل فرآیند لاگین (شامل حل چالش) در n8n، می‌توانید از یک **IF Node** استفاده کنید.

1.  **HTTP Request (Login):** یک نود برای ارسال درخواست به `/login` بسازید.
2.  **IF Node:** خروجی نود لاگین را بررسی کنید.
    -   **شرط:** `{{ $json.status }}` برابر با `success` است یا خیر.
    -   اگر `true` بود، به مسیر اصلی ورک‌فلو (مثلاً دریافت کامنت‌ها) بروید.
    -   اگر `false` بود، یعنی نیاز به حل چالش دارید.
3.  **HTTP Request (Resolve Challenge):** در مسیر `false`، یک نود دیگر برای ارسال کد تایید به `/challenge/resolve` قرار دهید. (می‌توانید کد را به صورت دستی یا از طریق یک نود دیگر دریافت کنید).

این الگو تضمین می‌کند که ورک‌فلوی شما حتی در صورت بروز چالش امنیتی نیز به درستی کار کند.

</div>

---

# English Documentation

## 🎯 Core Features

-   **Multi-Account Management**: Handle multiple Instagram account sessions simultaneously.
-   **Challenge Resolution**: Built-in API flow to handle Instagram's login challenges.
-   **Comment Fetching**: Get the latest comments from any public post.
-   **Comment Replies**: Reply to a specific comment.
-   **Direct Messages**: Send a DM to any Instagram user.
-   **Persistent Sessions**: Sessions are stored in `accounts.json` to avoid repeated logins.
-   **Rate Limiting**: Smart delays and limits to prevent account bans.
-   **Duplicate Prevention**: Reply history is tracked in `replied.json`.

## 🧰 Installation and Deployment

### Prerequisites
-   A server (Debian/Ubuntu recommended)
-   `git`

### Installation Steps
The `install.sh` script automates the entire setup, including Python and all dependencies.

1.  **Clone the repository:**
    ```bash
    # Clone the project into your desired path, e.g., /srv
    git clone https://github.com/YOUR_USERNAME/insta_service.git /srv/insta_service
    ```

2.  **Run the automated installation script:**
    ```bash
    bash /srv/insta_service/install.sh
    ```

3.  **Run the service:**
    For persistent background execution, use `nohup`.
    ```bash
    # Navigate to the project directory
    cd /srv/insta_service
    # Activate the virtual environment
    source venv/bin/activate
    # Run the service
    nohup uvicorn main:app --host 0.0.0.0 --port 8008 &
    ```
    The service will be available at `http://YOUR_SERVER_IP:8008`.

## 📡 Full API Reference

### `POST /login`
Logs into an Instagram account.

**Request Body:**
```json
{
  "username": "my_insta_account",
  "password": "my_secret_password"
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "username": "my_insta_account"
}
```

**Challenge Required Response (401 Unauthorized):**
Indicates that Instagram requires identity verification.
```json
{
  "detail": {
    "message": "Challenge required. Please solve the challenge and use the /challenge/resolve endpoint.",
    "username": "my_insta_account"
  }
}
```

### `POST /challenge/resolve`
Resolves a login challenge using the verification code sent to your email or phone.

**Request Body:**
```json
{
  "username": "my_insta_account",
  "code": "123456"
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "username": "my_insta_account",
  "message": "Challenge resolved and logged in successfully."
}
```

**Error Response (404 Not Found):**
```json
{
  "detail": "No active challenge found for user 'my_insta_account'."
}
```

### `GET /comments`
Fetches comments for a post.

**Query Parameters:**
-   `username`: The account to use for the request.
-   `url`: The full URL of the Instagram post.

**Example Request:**
`GET http://YOUR_IP:8008/comments?username=my_insta_account&url=https://www.instagram.com/p/Cxyz123abc/`

**Success Response (200 OK):**
```json
{
  "comments": [
    {
      "pk": "179...",
      "text": "This is a great post!",
      "user": { "pk": "123...", "username": "some_user" },
      "created_at_utc": "..."
    }
  ]
}
```

### `POST /reply`
Replies to a comment.

**Request Body:**
```json
{
  "username": "my_insta_account",
  "comment_id": "179...",
  "text": "Thanks for your comment! 🙌"
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Replied to comment 179..."
}
```

### `POST /dm`
Sends a direct message.

**Request Body:**
```json
{
  "username": "my_insta_account",
  "target_username": "some_user",
  "message": "Hello, we saw your comment and wanted to reach out."
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "DM sent to some_user"
}
```

## 🧩 Advanced n8n Integration Guide
To fully manage the login flow (including challenge resolution) in n8n, you can use an **IF Node**.

1.  **HTTP Request (Login):** Create a node to send the request to `/login`. Configure it to "Never Error" so you can inspect the output.
2.  **IF Node:** Check the output of the login node.
    -   **Condition:** `{{ $json.status }}` is equal to `success`.
    -   If `true`, proceed with the main workflow (e.g., fetching comments).
    -   If `false`, it means a challenge is required.
3.  **HTTP Request (Resolve Challenge):** On the `false` path, add another node to send the verification code to `/challenge/resolve`. You can get the code manually or from another automated source.

This pattern ensures your workflow is robust and can handle security challenges gracefully.
