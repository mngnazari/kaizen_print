#!/usr/bin/env python3
# utils/mapping_generator.py
"""
اسکریپت تولید خودکار فایل نقشه (mapping.txt) برای ادیتورها

نحوه استفاده:
1. فایل‌های اصلی (که بات فرستاده) و فایل‌های پردازش شده رو در یک پوشه قرار بده
2. این اسکریپت رو اجرا کن
3. فایل mapping.txt تولید میشه

قوانین نام‌گذاری:
- تبدیل فرمت: model.3dm → model.stl
- تقسیم فایل: bigpart.stl → bigpart#1.stl, bigpart#2.stl
- بدون تغییر: ready.stl → ready.stl (فقط عکس و zip نیاز داره)
"""

import os
import sys
from pathlib import Path
from typing import List, Dict, Set
import argparse


class MappingGenerator:
    """کلاس تولید فایل نقشه"""

    # فرمت‌های مجاز برای فایل اصلی
    ALLOWED_ORIGINAL_FORMATS = {'.stl', '.3dm', '.zip', '.rar', '.obj', '.step', '.stp'}

    # فرمت فایل نهایی (همیشه STL)
    OUTPUT_FORMAT = '.stl'

    def __init__(self, folder_path: str):
        """
        Args:
            folder_path: مسیر پوشه‌ای که فایل‌ها در آن هستند
        """
        self.folder_path = Path(folder_path)
        if not self.folder_path.exists():
            raise FileNotFoundError(f"پوشه یافت نشد: {folder_path}")

        self.original_files: List[Path] = []
        self.processed_files: List[Path] = []
        self.mappings: List[tuple] = []

    def scan_files(self):
        """اسکن فایل‌های موجود در پوشه"""
        print(f"📂 اسکن پوشه: {self.folder_path}")

        all_files = list(self.folder_path.glob("*"))

        # جداسازی فایل‌های اصلی و پردازش شده
        for file_path in all_files:
            if file_path.is_file():
                suffix = file_path.suffix.lower()

                # فایل‌های STL پردازش شده
                if suffix == self.OUTPUT_FORMAT:
                    self.processed_files.append(file_path)

                # فایل‌های اصلی (غیر STL)
                elif suffix in self.ALLOWED_ORIGINAL_FORMATS:
                    self.original_files.append(file_path)

        print(f"✅ فایل‌های اصلی: {len(self.original_files)}")
        print(f"✅ فایل‌های STL پردازش شده: {len(self.processed_files)}")

    def find_original_for_processed(self, processed_file: Path) -> Path | None:
        """
        پیدا کردن فایل اصلی مربوط به یک فایل پردازش شده

        Args:
            processed_file: فایل STL پردازش شده

        Returns:
            فایل اصلی مرتبط یا None
        """
        processed_stem = processed_file.stem  # نام بدون پسوند

        # چک کردن آیا فایل تقسیم شده است (دارای #)
        if '#' in processed_stem:
            # استخراج نام اصلی قبل از #
            base_name = processed_stem.split('#')[0]
        else:
            base_name = processed_stem

        # جستجو در فایل‌های اصلی
        for original_file in self.original_files:
            original_stem = original_file.stem

            # مطابقت دقیق
            if original_stem == base_name:
                return original_file

        # اگر فایل اصلی پیدا نشد، شاید خودش اصلی باشه
        # (یعنی فایل STL اصلی که تبدیل نشده، فقط باید عکس بگیره)
        original_stl_candidate = self.folder_path / f"{base_name}.stl"

        # چک کن ببین آیا این فایل در لیست processed هست یا نه
        # اگه فقط یک فایل STL با این اسم باشه، پس احتمالاً اصلی است
        matching_stl = [f for f in self.processed_files if f.stem == base_name and '#' not in f.stem]

        if len(matching_stl) == 1 and matching_stl[0] == processed_file:
            # این فایل STL اصلی است
            return processed_file

        return None

    def generate_mappings(self):
        """تولید mapping ها"""
        print("\n🔄 در حال تولید mapping ها...")

        # مجموعه‌ای از فایل‌های اصلی که قبلاً پردازش شده‌اند
        processed_originals: Set[str] = set()

        for processed_file in sorted(self.processed_files):
            original_file = self.find_original_for_processed(processed_file)

            if original_file:
                # نام فایل اصلی برای mapping
                if original_file == processed_file:
                    # فایل STL اصلی که تغییر نکرده
                    original_name = processed_file.name
                else:
                    original_name = original_file.name

                processed_name = processed_file.name

                # اضافه کردن به mappings
                self.mappings.append((original_name, processed_name))
                processed_originals.add(original_name)

                print(f"  ✓ {original_name} → {processed_name}")
            else:
                print(f"  ⚠️  فایل اصلی برای {processed_file.name} پیدا نشد - نادیده گرفته شد")

        # چک کردن فایل‌های اصلی که پردازش نشده‌اند
        unprocessed = []
        for original_file in self.original_files:
            if original_file.name not in processed_originals:
                unprocessed.append(original_file.name)

        if unprocessed:
            print(f"\n⚠️  فایل‌های اصلی که پردازش نشده‌اند:")
            for name in unprocessed:
                print(f"  - {name}")
            print("\n💡 نکته: اگر این فایل‌ها باید پردازش شوند، لطفاً فایل STL مربوط به آن‌ها را ایجاد کنید")

    def save_mapping_file(self, output_path: str = None):
        """
        ذخیره فایل mapping.txt

        Args:
            output_path: مسیر خروجی (پیش‌فرض: همان پوشه)
        """
        if not self.mappings:
            print("\n❌ هیچ mapping ای برای ذخیره وجود ندارد!")
            return

        if output_path is None:
            output_path = self.folder_path / "mapping.txt"
        else:
            output_path = Path(output_path)

        print(f"\n💾 در حال ذخیره فایل mapping در: {output_path}")

        with open(output_path, 'w', encoding='utf-8') as f:
            for original, processed in self.mappings:
                f.write(f"{original}: {processed}\n")

        print(f"✅ فایل mapping با موفقیت ذخیره شد!")
        print(f"📊 تعداد mappings: {len(self.mappings)}")

    def display_preview(self):
        """نمایش پیش‌نمایش فایل mapping"""
        if not self.mappings:
            print("\n❌ هیچ mapping ای برای نمایش وجود ندارد!")
            return

        print("\n" + "="*60)
        print("📄 پیش‌نمایش فایل mapping.txt:")
        print("="*60)

        for original, processed in self.mappings:
            print(f"{original}: {processed}")

        print("="*60)

    def run(self, save: bool = True, preview: bool = True):
        """
        اجرای کامل فرآیند

        Args:
            save: ذخیره فایل mapping
            preview: نمایش پیش‌نمایش
        """
        self.scan_files()
        self.generate_mappings()

        if preview:
            self.display_preview()

        if save and self.mappings:
            self.save_mapping_file()


def main():
    """تابع اصلی برای اجرا از خط فرمان"""
    parser = argparse.ArgumentParser(
        description="تولید خودکار فایل mapping.txt برای ادیتورها",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
مثال‌های استفاده:

  # تولید mapping از پوشه فعلی
  python mapping_generator.py

  # تولید mapping از پوشه مشخص
  python mapping_generator.py /path/to/files

  # فقط نمایش پیش‌نمایش بدون ذخیره
  python mapping_generator.py --no-save

  # ذخیره بدون نمایش پیش‌نمایش
  python mapping_generator.py --no-preview

نمونه ساختار فایل‌ها:
  files/
  ├── model.3dm          (فایل اصلی)
  ├── model.stl          (فایل پردازش شده)
  ├── bigpart.stl        (فایل اصلی)
  ├── bigpart#1.stl      (قسمت 1)
  ├── bigpart#2.stl      (قسمت 2)
  └── ready.stl          (فایل اصلی بدون تغییر)

خروجی mapping.txt:
  model.3dm: model.stl
  bigpart.stl: bigpart#1.stl
  bigpart.stl: bigpart#2.stl
  ready.stl: ready.stl
        """
    )

    parser.add_argument(
        'folder',
        nargs='?',
        default='.',
        help='مسیر پوشه حاوی فایل‌ها (پیش‌فرض: پوشه فعلی)'
    )

    parser.add_argument(
        '--no-save',
        action='store_true',
        help='عدم ذخیره فایل mapping (فقط نمایش پیش‌نمایش)'
    )

    parser.add_argument(
        '--no-preview',
        action='store_true',
        help='عدم نمایش پیش‌نمایش'
    )

    parser.add_argument(
        '-o', '--output',
        help='مسیر خروجی فایل mapping (پیش‌فرض: mapping.txt در همان پوشه)'
    )

    args = parser.parse_args()

    try:
        print("🚀 شروع تولید فایل mapping...")
        print()

        generator = MappingGenerator(args.folder)
        generator.scan_files()
        generator.generate_mappings()

        if not args.no_preview:
            generator.display_preview()

        if not args.no_save:
            generator.save_mapping_file(args.output)

        print("\n🎉 عملیات با موفقیت انجام شد!")

    except Exception as e:
        print(f"\n❌ خطا: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
