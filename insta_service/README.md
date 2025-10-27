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

در ادامه، مستندات کامل هر اندپوینت به همراه پارامترهای ورودی، نمونه درخواست، و ساختار پاسخ خروجی به تفصیل شرح داده شده است.

---

### `POST /login`
**هدف:** ورود به حساب کاربری اینستاگرام و ذخیره نشست (session) برای استفاده در درخواست‌های بعدی.

**پارامترهای ورودی (Body):**
| نام پروپرتی    | نوع      | توضیحات                                                                 |
| :-------------- | :-------- | :---------------------------------------------------------------------- |
| `username`      | `string`  | **(الزامی)** نام کاربری اینستاگرام.                                      |
| `password`      | `string`  | **(اختیاری)** رمز عبور اکانت. (یکی از سه متد ورود باید انتخاب شود)         |
| `session_json`  | `string`  | **(اختیاری)** نشست ذخیره‌شده به صورت رشته JSON.                         |
| `session_dict`  | `object`  | **(اختیاری)** نشست ذخیره‌شده به صورت آبجکت JSON.                         |

**نمونه درخواست (ورود با رمز عبور):**
```json
{
  "username": "my_insta_account",
  "password": "my_secret_password"
}
```

**ساختار پاسخ خروجی (موفق):**
| نام پروپرتی | نوع     | توضیحات                           |
| :---------- | :------- | :--------------------------------- |
| `status`    | `string` | وضعیت عملیات که `success` خواهد بود. |
| `username`  | `string` | نام کاربری اکانت لاگین‌شده.        |

**نمونه پاسخ خروجی (موفق):**
```json
{
  "status": "success",
  "username": "my_insta_account"
}
```

---

### `POST /challenge/resolve`
**هدف:** حل چالش امنیتی اینستاگرام با استفاده از کد تاییدی که به کاربر ارسال شده است.

**پارامترهای ورودی (Body):**
| نام پروپرتی | نوع     | توضیحات                                  |
| :---------- | :------- | :---------------------------------------- |
| `username`  | `string` | **(الزامی)** نام کاربری اکانت درگیر چالش. |
| `code`      | `string` | **(الزامی)** کد ۶ رقمی تایید.             |

**نمونه درخواست:**
```json
{
  "username": "my_insta_account",
  "code": "123456"
}
```

**ساختار پاسخ خروجی (موفق):**
| نام پروپرتی | نوع     | توضیحات                                       |
| :---------- | :------- | :--------------------------------------------- |
| `status`    | `string` | وضعیت عملیات که `success` خواهد بود.           |
| `username`  | `string` | نام کاربری اکانت.                             |
| `message`   | `string` | پیام تایید موفقیت‌آمیز بودن عملیات.            |

**نمونه پاسخ خروجی (موفق):**
```json
{
  "status": "success",
  "username": "my_insta_account",
  "message": "Challenge resolved and logged in successfully."
}
```

---

### `GET /comments`
**هدف:** دریافت کامنت‌های یک پست با قابلیت فیلترینگ و شمارش پاسخ مالک.

**پارامترهای ورودی (Query):**
| نام پروپرتی                  | نوع      | توضیحات                                                                     |
| :---------------------------- | :-------- | :-------------------------------------------------------------------------- |
| `username`                    | `string`  | **(الزامی)** نام کاربری اکانتی که برای ارسال درخواست استفاده می‌شود.          |
| `url`                         | `string`  | **(الزامی)** آدرس کامل پست اینستاگرام.                                       |
| `amount`                      | `integer` | **(اختیاری)** تعداد کامنت‌های آخر که باید دریافت شوند.                       |
| `fetch_all`                   | `boolean` | **(اختیاری)** اگر `true` باشد، تمام کامنت‌های پست دریافت می‌شوند.            |
| `include_owner_reply_count`   | `boolean` | **(اختیاری)** اگر `true` باشد، تعداد پاسخ‌های مالک پست به هر کامنت شمرده می‌شود. |

**نمونه درخواست:**
`GET http://<IP>:8008/comments?username=my_account&url=https://...&amount=10&include_owner_reply_count=true`

**ساختار پاسخ خروجی (موفق):**
| نام پروپرتی | نوع    | توضیحات                                                                                                                              |
| :---------- | :------ | :------------------------------------------------------------------------------------------------------------------------------------ |
| `comments`  | `array` | لیستی از آبجکت‌های کامنت. هر آبجکت شامل `pk` (شناسه کامنت)، `text` (متن)، `user` (شامل `pk` و `username` کاربر)، و `created_at_utc` است. |
| `owner_reply_count` | `integer` | (در صورت درخواست) تعداد پاسخ‌های مالک پست به این کامنت.                                                                        |

**نمونه پاسخ خروجی (موفق):**
```json
{
  "comments": [
    {
      "pk": "179...",
      "text": "Great post!",
      "user": { "pk": "123...", "username": "some_user" },
      "created_at_utc": "...",
      "owner_reply_count": 1
    }
  ]
}
```

---

### `POST /reply`
**هدف:** ارسال پاسخ به یک کامنت مشخص.

**پارامترهای ورودی (Body):**
| نام پروپرتی   | نوع     | توضیحات                                      |
| :------------- | :------- | :-------------------------------------------- |
| `username`     | `string` | **(الزامی)** اکانتی که برای پاسخ استفاده می‌شود. |
| `comment_id`   | `string` | **(الزامی)** شناسه کامنتی که به آن پاسخ داده می‌شود (`pk`). |
| `text`         | `string` | **(الزامی)** متن پاسخ.                       |

**نمونه درخواست:**
```json
{
  "username": "my_insta_account",
  "comment_id": "179...",
  "text": "Thanks! 🙌"
}
```

**ساختار پاسخ خروجی (موفق):**
| نام پروپرتی | نوع     | توضیحات                   |
| :---------- | :------- | :------------------------- |
| `status`    | `string` | وضعیت عملیات.              |
| `message`   | `string` | پیام تایید ارسال پاسخ.    |

**نمونه پاسخ خروجی (موفق):**
```json
{
  "status": "success",
  "message": "Replied to comment 179..."
}
```

---

### `POST /dm`
**هدف:** ارسال پیام دایرکت به یک کاربر.

**پارامترهای ورودی (Body):**
| نام پروپرتی       | نوع     | توضیحات                                        |
| :----------------- | :------- | :---------------------------------------------- |
| `username`         | `string` | **(الزامی)** اکانتی که برای ارسال DM استفاده می‌شود. |
| `target_username`  | `string` | **(الزامی)** نام کاربری گیرنده پیام.            |
| `message`          | `string` | **(الزامی)** متن پیام.                         |

**نمونه درخواست:**
```json
{
  "username": "my_insta_account",
  "target_username": "some_user",
  "message": "Hello there!"
}
```

**ساختار پاسخ خروجی (موفق):**
| نام پروپرتی | نوع     | توضیحات                   |
| :---------- | :------- | :------------------------- |
| `status`    | `string` | وضعیت عملیات.              |
| `message`   | `string` | پیام تایید ارسال دایرکت.   |

**نمونه پاسخ خروجی (موفق):**
```json
{
  "status": "success",
  "message": "DM sent to some_user"
}
```

---

### `GET /status`
**هدف:** بررسی وضعیت کلی سرویس و مشاهده اکانت‌های لاگین‌شده.

**پاسخ موفق (200 OK):**
```json
{
  "status": "ok",
  "logged_in_accounts": ["account1", "account2"]
}
```
-   `status`: وضعیت سلامت سرویس.
-   `logged_in_accounts`: لیستی از نام‌های کاربری که نشست فعال دارند.

## 🧩 راهنمای جامع اتصال به n8n

اتصال این سرویس به n8n بسیار ساده است. در ادامه یک سناریوی کامل (دریافت کامنت و ارسال پاسخ) شرح داده شده است.

**مرحله ۱: دریافت کامنت‌ها (HTTP Request Node)**
-   **Method:** `GET`
-   **URL:** `http://<YOUR_IP>:8008/comments`
-   **Send Query Parameters:** `true`
-   **Parameters:**
    -   `username`: نام اکانتی که لاگین کرده‌اید.
    -   `url`: آدرس پست مورد نظر.

**مرحله ۲: جداسازی کامنت‌ها (Split in Batches Node)**
-   خروجی مرحله قبل یک آرایه از کامنت‌هاست. این نود به شما اجازه می‌دهد هر کامنت را به صورت جداگانه پردازش کنید.
-   **Field to Split:** `={{ $json.comments }}`

**مرحله ۳: ارسال پاسخ (HTTP Request Node)**
-   این نود به نود قبلی متصل می‌شود و برای هر کامنت یک بار اجرا می‌شود.
-   **Method:** `POST`
-   **URL:** `http://<YOUR_IP>:8008/reply`
-   **Body Content Type:** `JSON`
-   **Body Parameters:**
    -   `username`: نام اکانت پاسخ‌دهنده.
    -   `comment_id`: `={{ $json.pk }}` (این عبارت `pk` یا همان شناسه کامنت را از ورودی نود می‌خواند).
    -   `text`: متن پاسخی که می‌خواهید ارسال کنید.

**نکته برای مدیریت چالش:**
-   در ورک‌فلوی لاگین، بعد از نود `HTTP Request` مربوط به `/login`، یک نود **IF** قرار دهید.
-   **شرط:** `{{ $json.detail.message }}` را بررسی کنید که آیا حاوی کلمه `Challenge` است یا خیر.
-   اگر `true` بود، یک نود دیگر برای فراخوانی `/challenge/resolve` قرار دهید.

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

Below is a comprehensive guide to each endpoint, including its input parameters, an example request, and the structure of a successful output response.

---

### `POST /login`
**Purpose:** Logs into an Instagram account and saves the session for future requests.

**Input Body Parameters:**
| Property Name   | Type     | Description                                                                 |
| :-------------- | :------- | :-------------------------------------------------------------------------- |
| `username`      | `string` | **(Required)** The Instagram username.                                      |
| `password`      | `string` | **(Optional)** The account password. (One of the three auth methods must be used) |
| `session_json`  | `string` | **(Optional)** A previously saved session as a JSON string.                 |
| `session_dict`  | `object` | **(Optional)** A previously saved session as a JSON object.                 |

**Example Request (Using Password):**
```json
{
  "username": "my_insta_account",
  "password": "my_secret_password"
}
```

**Success Response Structure:**
| Property Name | Type     | Description                        |
| :------------ | :------- | :--------------------------------- |
| `status`      | `string` | The result of the operation (`success`). |
| `username`    | `string` | The username of the logged-in account. |

**Example Success Response:**
```json
{
  "status": "success",
  "username": "my_insta_account"
}
```

---

### `POST /challenge/resolve`
**Purpose:** Resolves a security challenge using the verification code sent to the user.

**Input Body Parameters:**
| Property Name | Type     | Description                                     |
| :------------ | :------- | :---------------------------------------------- |
| `username`    | `string` | **(Required)** The username of the account facing the challenge. |
| `code`        | `string` | **(Required)** The 6-digit verification code.   |

**Example Request:**
```json
{
  "username": "my_insta_account",
  "code": "123456"
}
```

**Success Response Structure:**
| Property Name | Type     | Description                           |
| :------------ | :------- | :------------------------------------ |
| `status`      | `string` | The result of the operation (`success`).  |
| `username`    | `string` | The username of the account.          |
| `message`     | `string` | A confirmation of the successful action. |

**Example Success Response:**
```json
{
  "status": "success",
  "username": "my_insta_account",
  "message": "Challenge resolved and logged in successfully."
}
```

---

### `GET /comments`
**Purpose:** Fetches comments for a post with optional filtering and owner reply count.

**Input Query Parameters:**
| Property Name               | Type      | Description                                                                     |
| :-------------------------- | :-------- | :------------------------------------------------------------------------------ |
| `username`                  | `string`  | **(Required)** The username of the logged-in account to use for the request.    |
| `url`                       | `string`  | **(Required)** The full URL of the Instagram post.                              |
| `amount`                    | `integer` | **(Optional)** The number of recent comments to fetch.                          |
| `fetch_all`                 | `boolean` | **(Optional)** If `true`, fetches all comments on the post.                     |
| `include_owner_reply_count` | `boolean` | **(Optional)** If `true`, counts replies from the post owner for each comment.    |

**Example Request:**
`GET http://<IP>:8008/comments?username=my_account&url=https://...&amount=10&include_owner_reply_count=true`

**Success Response Structure:**
| Property Name       | Type    | Description                                                                                                     |
| :------------------ | :------ | :-------------------------------------------------------------------------------------------------------------- |
| `comments`          | `array` | A list of comment objects. Each object contains details like `pk` (ID), `text`, and `user` info.                  |
| `owner_reply_count` | `integer` | (If requested) The number of replies made by the post's owner to this specific comment.                         |

**Example Success Response:**
```json
{
  "comments": [
    {
      "pk": "179...",
      "text": "Great post!",
      "user": { "pk": "123...", "username": "some_user" },
      "created_at_utc": "...",
      "owner_reply_count": 1
    }
  ]
}
```

---

### `POST /reply`
**Purpose:** Sends a reply to a specific comment.

**Input Body Parameters:**
| Property Name | Type     | Description                                         |
| :------------ | :------- | :-------------------------------------------------- |
| `username`    | `string` | **(Required)** The account to use for replying.     |
| `comment_id`  | `string` | **(Required)** The ID (`pk`) of the comment to reply to. |
| `text`        | `string` | **(Required)** The content of the reply.            |

**Example Request:**
```json
{
  "username": "my_insta_account",
  "comment_id": "179...",
  "text": "Thanks! 🙌"
}
```

**Success Response Structure:**
| Property Name | Type     | Description                         |
| :------------ | :------- | :---------------------------------- |
| `status`      | `string` | The result of the operation.        |
| `message`     | `string` | A confirmation that the reply was sent. |

**Example Success Response:**
```json
{
  "status": "success",
  "message": "Replied to comment 179..."
}
```

---

### `POST /dm`
**Purpose:** Sends a direct message to a user.

**Input Body Parameters:**
| Property Name     | Type     | Description                               |
| :---------------- | :------- | :---------------------------------------- |
| `username`        | `string` | **(Required)** The account to use for sending the DM. |
| `target_username` | `string` | **(Required)** The username of the recipient. |
| `message`         | `string` | **(Required)** The content of the message.    |

**Example Request:**
```json
{
  "username": "my_insta_account",
  "target_username": "some_user",
  "message": "Hello there!"
}
```

**Success Response Structure:**
| Property Name | Type     | Description                       |
| :------------ | :------- | :-------------------------------- |
| `status`      | `string` | The result of the operation.      |
| `message`     | `string` | A confirmation that the DM was sent. |

**Example Success Response:**
```json
{
  "status": "success",
  "message": "DM sent to some_user"
}
```

---

### `GET /status`
**Purpose:** Checks the overall health of the service and lists logged-in accounts.

**Success Response Structure:**
| Property Name        | Type    | Description                                  |
| :------------------- | :------ | :------------------------------------------- |
| `status`             | `string`| The health status of the service (`ok`).     |
| `logged_in_accounts` | `array` | A list of usernames that have active sessions. |

**Example Success Response:**
```json
{
  "status": "ok",
  "logged_in_accounts": ["account1", "account2"]
}
```

## 🧩 Comprehensive n8n Integration Guide

Connecting this service to n8n is straightforward. Here’s a complete workflow for fetching comments and replying to each one.

**Step 1: Fetch Comments (HTTP Request Node)**
-   **Method:** `GET`
-   **URL:** `http://<YOUR_IP>:8008/comments`
-   **Send Query Parameters:** `true`
-   **Parameters:**
    -   `username`: The username of your logged-in account.
    -   `url`: The URL of the target post.

**Step 2: Split Comments (Split in Batches Node)**
-   The previous node returns an array of comments. This node lets you process each comment individually.
-   **Field to Split:** `={{ $json.comments }}`

**Step 3: Reply to Each Comment (HTTP Request Node)**
-   Connect this node after the "Split in Batches" node. It will run once for each comment.
-   **Method:** `POST`
-   **URL:** `http://<YOUR_IP>:8008/reply`
-   **Body Content Type:** `JSON`
-   **Body Parameters:**
    -   `username`: The username of your replying account.
    -   `comment_id`: `={{ $json.pk }}` (This expression dynamically gets the comment ID from the input).
    -   `text`: The reply text you want to send.

**Handling Login Challenges in n8n:**
-   After your `/login` HTTP Request node, add an **IF Node**.
-   **Condition:** Check if `{{ $json.detail.message }}` contains the word `Challenge`.
-   **On the `true` path**, add another HTTP Request node to call `/challenge/resolve` with the required code.
-   **On the `false` path**, continue your normal workflow.
