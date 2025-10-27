# Instagram Automation Service

A simple, lightweight, and robust REST API service designed to automate Instagram interactions. It handles multi-account sessions, challenge resolution, and provides endpoints for common actions like replying to comments and sending DMs. It's built for easy integration with automation platforms like n8n.

---

<div dir="rtl">

# سرویس اتوماسیون اینستاگرام

یک سرویس REST API ساده، سبک و قدرتمند برای اتوماسیون فعالیت‌های اینستاگرام. این سرویس مدیریت چندین حساب کاربری، حل چالش‌های امنیتی، و ارائه اندپوینت برای عملیات رایج را فراهم می‌کند و برای اتصال آسان به ابزارهای اتومیشن مانند n8n طراحی شده است.

## 🎯 قابلیت‌های کلیدی

-   **ورود چندگانه**: ورود با رمز عبور یا نشست (session) ذخیره‌شده.
-   **حل چالش امنیتی**: قابلیت مدیریت چالش‌های لاگین (Challenge) از طریق API.
-   **دریافت کامنت با فیلتر**: دریافت تمام یا تعداد مشخصی از آخرین کامنت‌ها.
-   **مدیریت نشست پایدار**: نشست‌ها در فایل `accounts.json` ذخیره می‌شوند.
-   **کنترل نرخ درخواست**: دارای محدودیت‌های هوشمند برای جلوگیری از مسدود شدن اکانت.

## 🧰 نصب و اجرا

اسکریپت `install.sh` تمام وابستگی‌ها را به صورت خودکار نصب می‌کند.

۱. **کلون کردن پروژه:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/insta_service.git /srv/insta_service
   ```

۲. **اجرای اسکریپت نصب:**
   ```bash
   bash /srv/insta_service/install.sh
   ```

۳. **اجرای سرویس:**
   ```bash
   cd /srv/insta_service
   source venv/bin/activate
   nohup uvicorn main:app --host 0.0.0.0 --port 8008 &
   ```

## 📡 راهنمای کامل API

### `POST /login`
ورود به حساب کاربری اینستاگرام با استفاده از رمز عبور یا نشست (session).

**۱. ورود با رمز عبور:**
```json
{
  "username": "my_insta_account",
  "password": "my_secret_password"
}
```

**۲. ورود با نشست (JSON String):**
```json
{
  "username": "my_insta_account",
  "session_json": "{\"sessionid\": \"...\", \"ds_user_id\": \"...\", ...}"
}
```

**۳. ورود با نشست (JSON Object):**
```json
{
  "username": "my_insta_account",
  "session_dict": {
    "sessionid": "...",
    "ds_user_id": "...",
    "csrftoken": "..."
  }
}
```

**پاسخ موفق (200 OK):**
```json
{
  "status": "success",
  "username": "my_insta_account"
}
```

**پاسخ ناموفق (403 Forbidden):**
در صورتی که نشست نامعتبر یا منقضی باشد.
```json
{
  "detail": "The provided session is invalid or expired."
}
```

### `POST /challenge/resolve`
حل چالش امنیتی با کد تایید ارسال‌شده.

**بدنه درخواست:**
```json
{
  "username": "my_insta_account",
  "code": "123456"
}
```

### `GET /comments`
دریافت کامنت‌های یک پست با قابلیت فیلترینگ.

**پارامترها:**
-   `username` (string, required): اکانت مورد استفاده.
-   `url` (string, required): آدرس پست.
-   `amount` (integer, optional): تعداد کامنت‌های آخر که باید دریافت شوند.
-   `fetch_all` (boolean, optional): اگر `true` باشد، تمام کامنت‌ها دریافت می‌شوند.

**مثال ۱: دریافت ۲۰ کامنت آخر**
`GET .../comments?username=...&url=...&amount=20`

**مثال ۲: دریافت همه کامنت‌ها**
`GET .../comments?username=...&url=...&fetch_all=true`


### `POST /reply`
پاسخ به یک کامنت.

**بدنه درخواست:**
```json
{
  "username": "my_insta_account",
  "comment_id": "179...",
  "text": "Thanks! 🙌"
}
```

### `POST /dm`
ارسال پیام دایرکت.

**بدنه درخواست:**
```json
{
  "username": "my_insta_account",
  "target_username": "some_user",
  "message": "Hello there!"
}
```

</div>

---

# English Documentation

## 🎯 Core Features

-   **Flexible Login**: Authenticate via password or a pre-saved session.
-   **Challenge Resolution**: Built-in API flow to handle Instagram's login challenges.
-   **Paginated Comment Fetching**: Retrieve all comments or a specific number of recent ones.
-   **Persistent Sessions**: Sessions are stored locally in `accounts.json`.
-   **Rate Limiting**: Smart delays and limits to prevent account bans.

## 🧰 Installation and Deployment

The `install.sh` script automates the entire setup.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/insta_service.git /srv/insta_service
    ```

2.  **Run the installation script:**
    ```bash
    bash /srv/insta_service/install.sh
    ```

3.  **Run the service:**
    ```bash
    cd /srv/insta_service
    source venv/bin/activate
    nohup uvicorn main:app --host 0.0.0.0 --port 8008 &
    ```

## 📡 Full API Reference

### `POST /login`
Logs into an Instagram account using a password or a session.

**1. Login with Password:**
```json
{
  "username": "my_insta_account",
  "password": "my_secret_password"
}
```

**2. Login with Session (JSON String):**
```json
{
  "username": "my_insta_account",
  "session_json": "{\"sessionid\": \"...\", \"ds_user_id\": \"...\", ...}"
}
```

**3. Login with Session (JSON Object):**
```json
{
  "username": "my_insta_account",
  "session_dict": {
    "sessionid": "...",
    "ds_user_id": "...",
    "csrftoken": "..."
  }
}
```

**Success Response (200 OK):**
```json
{
  "status": "success",
  "username": "my_insta_account"
}
```

**Error Response (403 Forbidden):**
Returned if the provided session is invalid or expired.
```json
{
  "detail": "The provided session is invalid or expired."
}
```

### `POST /challenge/resolve`
Resolves a login challenge using a verification code.

**Request Body:**
```json
{
  "username": "my_insta_account",
  "code": "123456"
}
```

### `GET /comments`
Fetches comments for a post with optional pagination.

**Query Parameters:**
-   `username` (string, required): The account to use for the request.
-   `url` (string, required): The URL of the post.
-   `amount` (integer, optional): The number of recent comments to fetch.
-   `fetch_all` (boolean, optional): If `true`, fetches all comments.

**Example 1: Get the last 20 comments**
`GET .../comments?username=...&url=...&amount=20`

**Example 2: Get all comments**
`GET .../comments?username=...&url=...&fetch_all=true`


### `POST /reply`
Replies to a comment.

**Request Body:**
```json
{
  "username": "my_insta_account",
  "comment_id": "179...",
  "text": "Thanks! 🙌"
}
```

### `POST /dm`
Sends a direct message.

**Request Body:**
```json
{
  "username": "my_insta_account",
  "target_username": "some_user",
  "message": "Hello there!"
}
```
