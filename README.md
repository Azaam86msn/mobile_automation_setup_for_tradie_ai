# Appium Behave Mobile Automation Framework

A clean and modular **Android mobile automation framework** built using **Python**, **Appium (UiAutomator2)**, **Selenium 4**, and **Behave BDD**, designed for smooth execution on **BrowserStack App Automate**.

---

## 🚀 Features

* Behave BDD structure
* Appium (UiAutomator2) for Android automation
* BrowserStack cloud device execution
* `.env`-based configuration
* Stable waits and reusable steps
* Automatic screenshot support

---

## 📦 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Azaam86msn/mobile_automation_setup_for_tradie_ai.git
cd mobile_automation_setup_for_tradie_ai
```

### 2. Create & Activate Virtual Environment

```bash
python3 -m venv .venv
```

Activate:

* **Windows:**

  ```powershell
  .\.venv\Scripts\activate
  ```
* **macOS/Linux:**

  ```bash
  source .venv/bin/activate
  ```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## ⚙️ Environment Configuration

Create a `.env` file:

```env
BROWSERSTACK_USERNAME=your_browserstack_username
BROWSERSTACK_ACCESS_KEY=your_browserstack_access_key
BROWSERSTACK_APP_URL=bs://your_uploaded_app_url

DEVICE_NAME=Google Pixel 5
PLATFORM_VERSION=12.0
BUILD_NAME=behave-build-01

TEST_USER_EMAIL=your_email@example.com
TEST_USER_PASSWORD=your_password
```

Do **not** commit this file.

---

## 📤 Uploading the App to BrowserStack

Upload manually or via API:

```bash
curl -u "USERNAME:ACCESS_KEY" \
-X POST "https://api-cloud.browserstack.com/app-automate/upload" \
-F "file=@/path/to/app.apk"
```

Copy the returned `bs://` link into your `.env`.

---

## 🧪 Running Tests

Run all tests:

```bash
behave
```

Run a single feature:

```bash
behave features/login.feature
```

Run a scenario:

```bash
behave -n "scenario name"
```

---

## 📁 Project Structure

```
appium-behave/
├── .env
├── behave.ini
├── requirements.txt
├── screenshots/
├── features/
│   ├── login.feature
│   ├── environment.py
│   └── steps/
│       └── steps_app.py
└── .venv/
```

---

## 📝 Notes

* Ensure BrowserStack credentials and app URL are correct.
* `.env` must be in the root folder.
* Screenshots are saved in `screenshots/`.
* Increase wait times if elements load slowly.
