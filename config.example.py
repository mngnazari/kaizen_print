# config.example.py
"""
نمونه فایل تنظیمات ربات
این فایل config.py را از فایل .env می‌خواند

برای استفاده:
1. فایل .env.example را کپی کنید و نام آن را به .env تغییر دهید
2. مقادیر را در فایل .env با اطلاعات واقعی خود پر کنید
"""
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# شناسه ادمین (از .env یا مقدار پیش‌فرض)
ADMIN_ID = int(os.getenv('ADMIN_ID', '0'))

# توکن ربات (از .env)
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    raise ValueError("❌ توکن ربات در فایل .env تنظیم نشده است! لطفاً BOT_TOKEN را در فایل .env قرار دهید.")

# لیست شناسه اپراتورها
OPERATORS_IDS = []

# لیست شناسه ادیتورها
EDITORS_IDS = []

# لیست شناسه ویزیتورها
VISITORS_IDS = []
