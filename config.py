# config.py
"""
تنظیمات و کانفیگ اصلی ربات
"""
import os
from dotenv import load_dotenv

# بارگذاری متغیرهای محیطی از فایل .env
load_dotenv()

# شناسه ادمین (از .env یا مقدار پیش‌فرض)
ADMIN_ID = int(os.getenv('ADMIN_ID', '2138687434'))

# توکن ربات (از .env)
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    raise ValueError("❌ توکن ربات در فایل .env تنظیم نشده است! لطفاً BOT_TOKEN را در فایل .env قرار دهید.")

# لیست شناسه اپراتورها
OPERATORS_IDS = []

# لیست شناسه ادیتورها
EDITORS_IDS = [7045273026]

# لیست شناسه ویزیتورها
VISITORS_IDS = []
