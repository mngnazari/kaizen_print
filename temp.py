elif data == "customer_group_stats":
# آمار گروهی
    try:
    from datetime import datetime, timedelta
    import jdatetime
    from database.crud import IRAN_TZ

    with database.connection.SessionLocal() as db:
        user = database.crud.get_user(db, user_id)

        if not user:
            await query.message.reply_text("کاربر یافت نشد")
            return

        # دریافت زیرمجموعه‌ها
        referrals = db.query(database.models.User).filter(
            database.models.User.referrer_id == user_id
        ).all()

        print(f"🔍 DEBUG: Found {len(referrals)} referrals")

        # اعضای گروه
        group_members = [user] + referrals

        # زمان فعلی در ایران
        now_iran = datetime.now(IRAN_TZ)
        today_iran = now_iran.date()
        today_start = datetime.combine(today_iran, datetime.min.time()).replace(tzinfo=IRAN_TZ)
        tomorrow_start = today_start + timedelta(days=1)

        # تاریخ شمسی
        persian_date = jdatetime.date.fromgregorian(date=today_iran)

        print(f"🔍 DEBUG: Iran time now: {now_iran}")
        print(f"🔍 DEBUG: Today Iran: {today_iran}")
        print(f"🔍 DEBUG: Persian date: {persian_date}")

        total_today_weight = 0
        user_today_weight = 0
        total_all_weight = 0

        # محاسبه وزن بر اساس فاکتورها
        for member in group_members:
            # وزن فاکتورهای امروز
            today_invoices = db.query(database.models.Invoice).filter(
                database.models.Invoice.customer_id == member.id,
                database.models.Invoice.created_at >= today_start,
                database.models.Invoice.created_at < tomorrow_start
            ).all()

            member_weight_today = sum(inv.weight_grams for inv in today_invoices)

            # وزن کل فاکتورها
            all_invoices = db.query(database.models.Invoice).filter(
                database.models.Invoice.customer_id == member.id
            ).all()

            member_weight_total = sum(inv.weight_grams for inv in all_invoices)

            print(f"🔍 DEBUG: {member.full_name} - Today weight: {member_weight_today}g, Total: {member_weight_total}g")

            total_today_weight += member_weight_today
            total_all_weight += member_weight_total

            if member.id == user_id:
                user_today_weight = member_weight_today

        print(f"🔍 DEBUG: Total today weight: {total_today_weight}g")
        print(f"🔍 DEBUG: Total all-time weight: {total_all_weight}g")

        # محاسبه میانگین روزانه (آخرین 30 روز)
        days_back = 30
        start_period = today_start - timedelta(days=days_back)

        period_invoices = db.query(database.models.Invoice).filter(
            database.models.Invoice.customer_id.in_([m.id for m in group_members]),
            database.models.Invoice.created_at >= start_period,
            database.models.Invoice.created_at < tomorrow_start
        ).all()

        period_weight = sum(inv.weight_grams for inv in period_invoices)
        daily_average = period_weight / days_back if days_back > 0 else 0

        # دریافت تنظیمات سطح گروه از دیتابیس
        silver_threshold = float(database.crud.get_system_setting(db, "group_silver_threshold", "50"))
        gold_threshold = float(database.crud.get_system_setting(db, "group_gold_threshold", "100"))
        silver_discount = float(database.crud.get_system_setting(db, "group_silver_discount", "5"))
        gold_discount = float(database.crud.get_system_setting(db, "group_gold_discount", "10"))

        # تعیین سطح گروه
        if daily_average >= gold_threshold:
            group_level = "طلایی"
            group_emoji = "🥇"
            discount_percent = gold_discount
        elif daily_average >= silver_threshold:
            group_level = "نقره‌ای"
            group_emoji = "🥈"
            discount_percent = silver_discount
        else:
            group_level = "برنزی"
            group_emoji = "🥉"
            discount_percent = 0

        # ایجاد پیام
        message = f"📊 آمار گروه {user.full_name}\n\n"
        message += f"📅 تاریخ: {persian_date.strftime('%Y/%m/%d')}\n"
        message += f"👥 اعضای گروه: {len(group_members)} نفر\n"
        message += f"⚖️ وزن پرینت گروه امروز: {total_today_weight} گرم\n"
        message += f"🎯 سهم شما: {user_today_weight} گرم\n"
        message += f"📊 میانگین روزانه (30 روز): {daily_average:.1f} گرم\n\n"

        message += f"{group_emoji} سطح گروه: {group_level}\n"
        if discount_percent > 0:
            message += f"🎁 تخفیف فعال: {discount_percent}% برای دعوت‌کننده\n"
        message += "\n"

        message += "👥 اعضای گروه:\n"
        for i, member in enumerate(group_members[:5], 1):
            message += f"   {i}. {member.full_name}\n"

        if len(group_members) > 5:
            remaining = len(group_members) - 5
            message += f"   ... و {remaining} نفر دیگر\n"

        # راهنمایی برای ارتقاء سطح
        if group_level == "برنزی":
            needed = silver_threshold - daily_average
            message += f"\n💡 برای ارتقاء به نقره‌ای: {needed:.1f} گرم بیشتر در روز"
        elif group_level == "نقره‌ای":
            needed = gold_threshold - daily_average
            message += f"\n💡 برای ارتقاء به طلایی: {needed:.1f} گرم بیشتر در روز"
        else:
            message += f"\n🎉 تبریک! شما در بالاترین سطح قرار دارید!"

        await query.message.reply_text(message, reply_markup=get_customer_kb(user_id))
        print("🔍 DEBUG: Message sent successfully")

    except Exception as e:
    print(f"❌ Error in group stats: {e}")
    import traceback

    traceback.print_exc()
    await query.message.reply_text(
        "❌ خطایی در نمایش آمار گروهی رخ داد.\n\n"
        "لطفاً از منوی ثابت دکمه 'آمار گروهی' را انتخاب کنید.",
        reply_markup=get_customer_kb(user_id)
    )