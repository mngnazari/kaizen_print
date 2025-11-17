# 🔧 راهنمای راه‌اندازی Configuration

## 📋 مراحل راه‌اندازی

بعد از clone کردن پروژه، این مراحل رو دنبال کن:

### 1️⃣ نصب پکیج‌ها
```bash
pip install -r requirements.txt
```

### 2️⃣ ایجاد فایل config.py
فایل `config.py` را در روت پروژه بساز و محتوای زیر را کپی کن:

```python
# ===============================
# 🔧 Configuration File
# ===============================
import os
from dotenv import load_dotenv

load_dotenv()

# ===============================
# 🤖 Bot Configuration
# ===============================
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ===============================
# 👥 User IDs
# ===============================
ADMIN_ID = int(os.getenv("ADMIN_ID", "YOUR_ADMIN_ID_HERE"))

# آیدی اپراتورها (لیست)
OPERATORS_IDS = []
operators_env = os.getenv("OPERATORS_IDS", "")
if operators_env:
    OPERATORS_IDS = [int(id.strip()) for id in operators_env.split(",") if id.strip()]

# آیدی ادیتورها (لیست)
EDITORS_IDS = []
editors_env = os.getenv("EDITORS_IDS", "")
if editors_env:
    EDITORS_IDS = [int(id.strip()) for id in editors_env.split(",") if id.strip()]

# آیدی ویزیتورها (لیست)
VISITORS_IDS = []
visitors_env = os.getenv("VISITORS_IDS", "")
if visitors_env:
    VISITORS_IDS = [int(id.strip()) for id in visitors_env.split(",") if id.strip()]

# ===============================
# 🗄️ Database Configuration
# ===============================
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./kaizen_bot.db")

# ===============================
# 📝 Logging Configuration
# ===============================
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# ===============================
# 🌐 Other Settings
# ===============================
DEBUG = os.getenv("DEBUG", "False").lower() == "true"
```

### 3️⃣ (اختیاری) استفاده از فایل .env
اگر میخوای از `.env` استفاده کنی:

```bash
cp .env.example .env
```

سپس `.env` را ویرایش کن و مقادیر واقعی را وارد کن.

### 4️⃣ اجرای ربات
```bash
python main.py
```

## ⚠️ نکات مهم

- ✅ فایل `config.py` در `.gitignore` قرار دارد و commit نمیشه
- ✅ فایل `.env` هم در `.gitignore` هست
- ✅ فقط `.env.example` commit میشه
- ✅ هر developer باید `config.py` یا `.env` خودش رو بسازه
- ⚠️ **هیچوقت توکن یا اطلاعات حساس رو commit نکن!**

## 🔑 نحوه دریافت اطلاعات

### Bot Token:
از [@BotFather](https://t.me/BotFather) در تلگرام دریافت کن

### User ID:
از ربات [@userinfobot](https://t.me/userinfobot) آیدی خودت رو بگیر

## 📞 پشتیبانی
اگر مشکلی داشتی، با تیم تماس بگیر.
