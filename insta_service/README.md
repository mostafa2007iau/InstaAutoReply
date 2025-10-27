# Instagram Automation Service

A simple, lightweight, and robust REST API service designed to automate Instagram interactions. It handles multi-account sessions, challenge resolution, and provides endpoints for common actions like replying to comments and sending DMs. It's built for easy integration with automation platforms like n8n.

---

<div dir="rtl">

# سرویس اتوماسیون اینستاگرام

یک سرویس REST API ساده، سبک و قدرتمند برای اتوماسیون فعالیت‌های اینستاگرام. این سرویس مدیریت چندین حساب کاربری، حل چالش‌های امنیتی، و ارائه اندپوینت برای عملیات رایج را فراهم می‌کند و برای اتصال آسان به ابزارهای اتومیشن مانند n8n طراحی شده است.

## 🎯 قابلیت‌های کلیدی

-   **ورود چندگانه**: ورود با رمز عبور یا نشست (session) ذخیره‌شده.
-   **نصب آسان**: اسکریپت نصب هوشمند با قابلیت راه‌اندازی به عنوان سرویس `systemd`.
-   **حل چالش امنیتی**: قابلیت مدیریت چالش‌های لاگین (Challenge) از طریق API.
-   **دریافت کامنت با فیلتر**: دریافت تمام یا تعداد مشخصی از آخرین کامنت‌ها.
-   **شمارش پاسخ مالک**: قابلیت شمارش پاسخ‌های صاحب پست به هر کامنت.

## 🧰 نصب و اجرا

اسکریپت `install.sh` به صورت هوشمند محیط را تشخیص داده و نصب را انجام می‌دهد.

۱. **کلون کردن پروژه:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/insta_service.git /srv/insta_service
   ```

۲. **اجرای اسکریپت نصب:**
   ```bash
   bash /srv/insta_service/install.sh
   ```
   اسکریپت به صورت خودکار سرویس `systemd` را راه‌اندازی می‌کند تا برنامه همیشه در حال اجرا باشد.

**مدیریت سرویس:**
-   **بررسی وضعیت:** `sudo systemctl status insta-auto-reply.service`
-   **مشاهده لاگ‌ها:** `sudo journalctl -u insta-auto-reply.service -f`

## 📡 راهنمای کامل API

### `POST /login`
ورود به حساب کاربری. در صورت موفقیت، نشست برای استفاده‌های بعدی ذخیره می‌شود.

**پاسخ موفق (200 OK):**
```json
{
  "status": "success",
  "username": "my_insta_account"
}
```
-   `status`: وضعیت عملیات.
-   `username`: نام کاربری اکانت لاگین‌شده.

### `POST /challenge/resolve`
حل چالش امنیتی با کد تایید.

**پاسخ موفق (200 OK):**
```json
{
  "status": "success",
  "username": "my_insta_account",
  "message": "Challenge resolved and logged in successfully."
}
```
-   `message`: پیام تایید موفقیت‌آمیز بودن عملیات.

### `GET /comments`
دریافت کامنت‌های یک پست.

**مثال: دریافت ۱۰ کامنت آخر به همراه تعداد پاسخ مالک**
`GET .../comments?username=...&url=...&amount=10&include_owner_reply_count=true`

**پاسخ موفق (200 OK):**
```json
{
  "comments": [
    {
      "pk": "179...",
      "text": "Great post!",
      "user": { "pk": "123...", "username": "some_user" },
      "owner_reply_count": 1
    }
  ]
}
```
-   `comments`: لیستی از آبجکت‌های کامنت. هر آبجکت شامل `pk` (شناسه کامنت)، `text` (متن)، و `user` (اطلاعات کاربر) است.
-   `owner_reply_count`: (اختیاری) تعداد پاسخ‌های مالک پست به این کامنت.

### `POST /reply`
پاسخ به یک کامنت.

**پاسخ موفق (200 OK):**
```json
{
  "status": "success",
  "message": "Replied to comment 179..."
}
```
-   `message`: پیام تایید ارسال پاسخ.

### `POST /dm`
ارسال پیام دایرکت.

**پاسخ موفق (200 OK):**
```json
{
  "status": "success",
  "message": "DM sent to some_user"
}
```
-   `message`: پیام تایید ارسال دایرکت.

### `GET /status`
بررسی وضعیت سرویس.

**پاسخ موفق (200 OK):**
```json
{
  "status": "ok",
  "logged_in_accounts": ["account1", "account2"]
}
```
-   `logged_in_accounts`: لیستی از تمام اکانت‌هایی که با موفقیت لاگین کرده‌اند.

</div>

---

# English Documentation

## 🎯 Core Features

-   **Flexible Login**: Authenticate via password or a pre-saved session.
-   **Robust Installation**: Smart `install.sh` script that sets up a `systemd` service for persistence.
-   **Challenge Resolution**: Built-in API flow to handle Instagram's login challenges.
-   **Advanced Comment Fetching**: Paginate comments and count replies from the post owner.
-   **Persistent Sessions**: Sessions are stored locally in `accounts.json`.

## 🧰 Installation and Deployment

The smart `install.sh` script automates the entire setup.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/insta_service.git /srv/insta_service
    ```

2.  **Run the installation script:**
    ```bash
    bash /srv/insta_service/install.sh
    ```
    The script will automatically configure and enable a `systemd` service to keep the application running.

**Managing the Service:**
-   **Check Status:** `sudo systemctl status insta-auto-reply.service`
-   **View Logs:** `sudo journalctl -u insta-auto-reply.service -f`

## 📡 Full API Reference

### `POST /login`
Logs into an account. On success, the session is saved for future use.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "username": "my_insta_account"
}
```
-   `status`: The result of the operation.
-   `username`: The username of the logged-in account.

### `POST /challenge/resolve`
Resolves a login challenge with a verification code.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "username": "my_insta_account",
  "message": "Challenge resolved and logged in successfully."
}
```
-   `message`: A confirmation that the challenge was resolved.

### `GET /comments`
Fetches comments for a post.

**Example: Get the last 10 comments and include the owner's reply count**
`GET .../comments?username=...&url=...&amount=10&include_owner_reply_count=true`

**Success Response (200 OK):**
```json
{
  "comments": [
    {
      "pk": "179...",
      "text": "Great post!",
      "user": { "pk": "123...", "username": "some_user" },
      "owner_reply_count": 1
    }
  ]
}
```
-   `comments`: A list of comment objects. Each object contains details like `pk` (comment ID), `text`, and `user` info.
-   `owner_reply_count`: (Optional) The number of replies made by the post's owner to this comment.

### `POST /reply`
Replies to a comment.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "Replied to comment 179..."
}
```
-   `message`: A confirmation that the reply was sent.

### `POST /dm`
Sends a direct message.

**Success Response (200 OK):**
```json
{
  "status": "success",
  "message": "DM sent to some_user"
}
```
-   `message`: A confirmation that the DM was sent.

### `GET /status`
Checks the service status.

**Success Response (200 OK):**
```json
{
  "status": "ok",
  "logged_in_accounts": ["account1", "account2"]
}
```
-   `logged_in_accounts`: A list of all usernames that have an active session.
