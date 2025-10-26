# Instagram Automation Service

A simple, lightweight REST API service designed to automate Instagram interactions like replying to comments and sending DMs. It is built to be simple, stateless (using local JSON files for session storage), and easy to integrate with automation platforms like n8n.

---

<div dir="rtl">

# سرویس اتوماسیون اینستاگرام

یک سرویس REST API ساده، سبک و کارآمد برای اتوماسیون فعالیت‌های اینستاگرام مانند پاسخ به کامنت‌ها و ارسال دایرکت مسیج. این سرویس برای اتصال آسان به ابزارهای اتومیشن مانند n8n طراحی شده است.

## 🎯 قابلیت‌های کلیدی

-   **ورود چند اکانت**: مدیریت همزمان چندین حساب کاربری اینستاگرام.
-   **دریافت کامنت‌ها**: دریافت آخرین کامنت‌های یک پست مشخص.
-   **پاسخ به کامنت**: ریپلای خودکار به یک کامنت خاص.
-   **ارسال دایرکت**: ارسال پیام مستقیم (DM) به هر کاربر.
-   **مدیریت نشست (Session)**: نشست‌ها به صورت فایل `accounts.json` در کنار پروژه ذخیره می‌شوند تا از لاگین‌های مکرر جلوگیری شود.
-   **کنترل نرخ درخواست (Rate Limiting)**: دارای محدودیت زمانی بین درخواست‌ها برای جلوگیری از مسدود شدن اکانت.
-   **جلوگیری از پاسخ تکراری**: با ذخیره تاریخچه در `replied.json`، از پاسخ مجدد به یک کامنت جلوگیری می‌شود.

## 🧰 نصب و اجرا روی سرور

### پیش‌نیازها
-   سرور (ترجیحاً Debian/Ubuntu)
-   Python 3.10+
-   `git`

### مراحل نصب

۱. **کلون کردن پروژه:**
   ```bash
   git clone https://github.com/YOUR_USERNAME/insta_service.git
   cd insta_service
   ```

۲. **اجرای اسکریپت نصب خودکار:**
   این اسکریپت پایتون، `venv` و وابستگی‌ها را به صورت خودکار نصب می‌کند.
   ```bash
   bash install.sh
   ```

۳. **فعال‌سازی محیط مجازی:**
   ```bash
   source venv/bin/activate
   ```

۴. **اجرای سرویس:**
   برای اجرای سرویس در پس‌زمینه و مقاوم‌سازی در برابر خاموش شدن ترمینال، از `nohup` استفاده کنید:
   ```bash
   nohup uvicorn main:app --host 0.0.0.0 --port 8008 &
   ```
   سرویس روی آدرس `http://YOUR_SERVER_IP:8008` در دسترس خواهد بود.

## 📡 دسترسی به APIها

| متد    | مسیر        | توضیحات                                       |
| :----- | :----------- | :--------------------------------------------- |
| `GET`  | `/status`    | بررسی وضعیت سرویس و لیست اکانت‌های لاگین‌شده. |
| `POST` | `/login`     | ورود به یک اکانت و ذخیره نشست آن.             |
| `GET`  | `/accounts`  | دریافت لیست تمام اکانت‌های متصل.                |
| `GET`  | `/comments`  | دریافت کامنت‌های یک پست از طریق URL.           |
| `POST` | `/reply`     | پاسخ به یک کامنت مشخص.                         |
| `POST` | `/dm`        | ارسال پیام دایرکت به یک کاربر.                  |

## 🧩 اتصال به n8n

برای اتصال این سرویس به n8n، از نود **HTTP Request** استفاده کنید:

-   **URL**: آدرس اندپوینت مورد نظر، مثلاً: `http://192.168.1.50:8008/reply`
-   **Method**: متد درخواست (`POST` یا `GET`)
-   **Body Content Type**: `JSON`
-   **Body**: داده‌های مورد نیاز را در قالب JSON ارسال کنید. می‌توانید از خروجی نودهای قبلی برای پر کردن مقادیر استفاده کنید.

**مثال برای ریپلای:**
```json
{
  "username": "my_insta_account",
  "comment_id": "{{ $json.comment_id }}",
  "text": "از کامنت شما متشکریم! 🙌"
}
```

</div>

---

# English Documentation

## 🎯 Core Features

-   **Multi-Account Login**: Manage sessions for multiple Instagram accounts simultaneously.
-   **Comment Fetching**: Get the latest comments from any public post.
-   **Comment Replies**: Reply to a specific comment.
-   **Direct Messages**: Send a DM to any Instagram user.
-   **Session Management**: Sessions are stored locally in `accounts.json` to persist logins.
-   **Rate Limiting**: Includes delays and hourly limits to prevent account bans.
-   **Duplicate Prevention**: Tracks replied comments in `replied.json` to avoid sending the same reply twice.

## 🧰 Installation and Server Deployment

### Prerequisites
-   A server (Debian/Ubuntu recommended)
-   Python 3.10+
-   `git`

### Installation Steps

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/YOUR_USERNAME/insta_service.git
    cd insta_service
    ```

2.  **Run the automated installation script:**
    This script will install Python, `venv`, and all required dependencies.
    ```bash
    bash install.sh
    ```

3.  **Activate the virtual environment:**
    ```bash
    source venv/bin/activate
    ```

4.  **Run the service:**
    To run the service persistently in the background, use `nohup`:
    ```bash
    nohup uvicorn main:app --host 0.0.0.0 --port 8008 &
    ```
    The service will be available at `http://YOUR_SERVER_IP:8008`.

## 📡 API Endpoints

| Method | Path         | Description                                     |
| :----- | :----------- | :---------------------------------------------- |
| `GET`  | `/status`    | Check service health and see logged-in accounts.|
| `POST` | `/login`     | Log in an account and save its session.         |
| `GET`  | `/accounts`  | Get a list of all logged-in accounts.           |
| `GET`  | `/comments`  | Get comments from a specific post URL.          |
| `POST` | `/reply`     | Reply to a specific comment.                    |
| `POST` | `/dm`        | Send a direct message to a user.                |

## 🧩 n8n Integration

You can easily connect this service to an n8n workflow using the **HTTP Request** node.

-   **URL**: The endpoint you want to target, e.g., `http://192.168.1.50:8008/reply`
-   **Method**: `POST` or `GET`
-   **Body Content Type**: `JSON`
-   **Body**: Use expressions to pass data from previous nodes.

**Example for a Reply Node:**
```json
{
  "username": "my_insta_account",
  "comment_id": "{{ $json.comment_id }}",
  "text": "Thanks for your comment! 🙌"
}
```
