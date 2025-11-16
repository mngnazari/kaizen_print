#!/usr/bin/env python3
"""
مثال استفاده از Mapping Generator

این فایل یک مثال عملی از نحوه استفاده از ابزار mapping_generator است.
"""

from mapping_generator import MappingGenerator


def example_basic_usage():
    """مثال ساده - استفاده پایه"""
    print("=" * 60)
    print("مثال 1: استفاده پایه")
    print("=" * 60)

    # ایجاد generator برای پوشه فعلی
    generator = MappingGenerator(".")

    # اجرای کامل
    generator.run(save=True, preview=True)


def example_custom_output():
    """مثال با خروجی سفارشی"""
    print("\n" + "=" * 60)
    print("مثال 2: ذخیره در مسیر سفارشی")
    print("=" * 60)

    generator = MappingGenerator(".")

    # اسکن فایل‌ها
    generator.scan_files()

    # تولید mappings
    generator.generate_mappings()

    # نمایش پیش‌نمایش
    generator.display_preview()

    # ذخیره در مسیر دلخواه
    generator.save_mapping_file("my_custom_mapping.txt")


def example_programmatic():
    """مثال استفاده برنامه‌نویسی (بدون ذخیره فایل)"""
    print("\n" + "=" * 60)
    print("مثال 3: استفاده برنامه‌نویسی")
    print("=" * 60)

    generator = MappingGenerator(".")

    generator.scan_files()
    generator.generate_mappings()

    # دسترسی مستقیم به mappings
    print(f"\nتعداد mappings: {len(generator.mappings)}")

    for original, processed in generator.mappings:
        print(f"  {original} → {processed}")

        # میتونید اینجا کارهای دیگه‌ای بکنید
        # مثلاً چک کردن، validation، و غیره


def example_with_error_handling():
    """مثال با مدیریت خطا"""
    print("\n" + "=" * 60)
    print("مثال 4: مدیریت خطا")
    print("=" * 60)

    try:
        generator = MappingGenerator("./test_folder")
        generator.run()
    except FileNotFoundError as e:
        print(f"⚠️  خطا: {e}")
        print("💡 لطفاً مطمئن شوید که پوشه وجود دارد")
    except Exception as e:
        print(f"❌ خطای غیرمنتظره: {e}")


if __name__ == "__main__":
    print("🎓 مثال‌های استفاده از Mapping Generator\n")

    # اجرای مثال‌ها
    example_basic_usage()

    # مثال‌های دیگر (uncomment کنید برای اجرا)
    # example_custom_output()
    # example_programmatic()
    # example_with_error_handling()

    print("\n✅ تمام مثال‌ها اجرا شدند!")
