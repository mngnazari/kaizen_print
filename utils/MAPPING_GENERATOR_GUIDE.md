# 📘 راهنمای استفاده از Mapping Generator

## 📝 توضیحات

این ابزار برای **ادیتورها** طراحی شده تا فایل `mapping.txt` رو به صورت خودکار تولید کنه.

---

## 🎯 چطوری کار میکنه؟

1. شما فایل‌های اصلی که از بات دریافت کردید رو با فایل‌های پردازش شده‌ای که ساختید در یک پوشه قرار میدید
2. این اسکریپت رو اجرا میکنید
3. فایل `mapping.txt` خودکار تولید میشه و آماده ارسال به بات است

---

## 📂 ساختار پوشه

مثال:
```
my_files/
├── model.3dm          # فایل اصلی (از بات)
├── model.stl          # فایل تبدیل شده
├── bigpart.stl        # فایل اصلی (از بات)
├── bigpart#1.stl      # قسمت 1 تقسیم شده
├── bigpart#2.stl      # قسمت 2 تقسیم شده
├── bigpart#3.stl      # قسمت 3 تقسیم شده
└── ready.stl          # فایل آماده (بدون تغییر)
```

---

## 🚀 نحوه استفاده

### **روش 1: از ترمینال**

```bash
# رفتن به پوشه فایل‌ها
cd /path/to/my_files

# اجرای اسکریپت
python ../utils/mapping_generator.py
```

### **روش 2: مشخص کردن مسیر پوشه**

```bash
python utils/mapping_generator.py /path/to/my_files
```

### **روش 3: فقط نمایش پیش‌نمایش (بدون ذخیره)**

```bash
python utils/mapping_generator.py --no-save
```

### **روش 4: ذخیره در مسیر دیگر**

```bash
python utils/mapping_generator.py -o /path/to/output/mapping.txt
```

---

## 📋 خروجی

### **فایل `mapping.txt` تولید شده:**

```
model.3dm: model.stl
bigpart.stl: bigpart#1.stl
bigpart.stl: bigpart#2.stl
bigpart.stl: bigpart#3.stl
ready.stl: ready.stl
```

این فایل رو در تلگرام به بات ارسال میکنی و بعد فایل‌های مربوطه رو میفرستی.

---

## 🎓 مثال‌های کاربردی

### **مثال 1: تبدیل فرمت**

**ورودی:**
- `car.3dm` (اصلی)
- `car.stl` (تبدیل شده)

**خروجی mapping:**
```
car.3dm: car.stl
```

**فایل‌هایی که باید بفرستی:**
- `car.stl`
- `car.jpg`
- `car.zip`

---

### **مثال 2: تقسیم یک فایل بزرگ**

**ورودی:**
- `house.stl` (اصلی - بزرگ)
- `house#1.stl` (قسمت 1)
- `house#2.stl` (قسمت 2)

**خروجی mapping:**
```
house.stl: house#1.stl
house.stl: house#2.stl
```

**فایل‌هایی که باید بفرستی:**
- `house#1.stl`, `house#1.jpg`, `house#1.zip`
- `house#2.stl`, `house#2.jpg`, `house#2.zip`

---

### **مثال 3: ترکیبی**

**ورودی:**
```
files/
├── head.3dm
├── head.stl
├── body.zip
├── body.stl
├── leg.stl          (اصلی - بزرگ)
├── leg#1.stl
├── leg#2.stl
└── arm.stl          (آماده، بدون تغییر)
```

**خروجی mapping:**
```
head.3dm: head.stl
body.zip: body.stl
leg.stl: leg#1.stl
leg.stl: leg#2.stl
arm.stl: arm.stl
```

---

## ⚙️ قوانین نام‌گذاری

### ✅ **درست:**

```
model.3dm → model.stl
part.stl → part#1.stl
part.stl → part#2.stl
ready.stl → ready.stl
```

### ❌ **اشتباه:**

```
model_new.stl        # نام اصلی باید model.3dm باشه
part_1.stl           # باید part#1.stl باشه (با # نه _)
bigpart-1.stl        # باید bigpart#1.stl باشه (با # نه -)
```

---

## 🔍 خروجی اسکریپت

```
🚀 شروع تولید فایل mapping...

📂 اسکن پوشه: /path/to/files
✅ فایل‌های اصلی: 3
✅ فایل‌های STL پردازش شده: 5

🔄 در حال تولید mapping ها...
  ✓ model.3dm → model.stl
  ✓ bigpart.stl → bigpart#1.stl
  ✓ bigpart.stl → bigpart#2.stl
  ✓ bigpart.stl → bigpart#3.stl
  ✓ ready.stl → ready.stl

============================================================
📄 پیش‌نمایش فایل mapping.txt:
============================================================
model.3dm: model.stl
bigpart.stl: bigpart#1.stl
bigpart.stl: bigpart#2.stl
bigpart.stl: bigpart#3.stl
ready.stl: ready.stl
============================================================

💾 در حال ذخیره فایل mapping در: /path/to/files/mapping.txt
✅ فایل mapping با موفقیت ذخیره شد!
📊 تعداد mappings: 5

🎉 عملیات با موفقیت انجام شد!
```

---

## 💡 نکات مهم

1. **فایل‌های اصلی** باید دقیقاً همون اسمی که از بات دریافت کردی رو داشته باشن
2. برای **تقسیم فایل** از `#` استفاده کن: `filename#1.stl`, `filename#2.stl`
3. اگه فایل **بدون تغییر** باشه، بازم در mapping بنویس: `file.stl: file.stl`
4. همیشه **قبل از ارسال**، پیش‌نمایش mapping رو چک کن

---

## ❓ سوالات متداول

**Q: اگه فایل اصلی رو ندارم چی؟**
A: اگه فایل STL اصلی رو داری و نخواستی تغییر بدی، همون رو بنویس: `file.stl: file.stl`

**Q: چند تا فایل میتونم از یک اصلی بسازم؟**
A: هرچقدر که بخوای! فقط با # شماره‌گذاری کن: `#1`, `#2`, `#3`, ...

**Q: پسوند فایل‌ها مهمه؟**
A: بله! فایل‌های پردازش شده باید حتماً `.stl` باشن

**Q: اگه اشتباه شد چی؟**
A: فایل mapping رو دستی ویرایش کن، یا فایل‌ها رو تغییر بده و دوباره اسکریپت رو اجرا کن

---

## 📞 پشتیبانی

اگه مشکلی داشتی یا نیاز به کمک داشتی، با ادمین تماس بگیر.

---

**ساخته شده با ❤️ برای ادیتورهای کایزن پرینت**
