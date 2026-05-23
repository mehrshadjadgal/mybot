import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, BotCommand, BotCommandScopeChat
import json
import os

bot = telebot.TeleBot("8541353617:AAF5IdRRgYCJPdjjcVZHetF1LuGeIdD_el8")

CARD_NUMBER = "5022291606480901"
ADMIN_ID = 961305324
CHANNEL_USERNAME = "@mirv2rayN"

# ==================== فایل‌ها ====================
CONFIG_FILE = "configs.json"
TUTORIAL_FILE = "tutorials.json"
USERS_FILE = "users.json"
REWARD_FILE = "rewards.json"
REFERRED_FILE = "referred.json"

# لود داده‌ها
def load_json(file, default):
    if os.path.exists(file):
        with open(file, 'r', encoding='utf-8') as f:
            return json.load(f)
    with open(file, 'w', encoding='utf-8') as f:
        json.dump(default, f, ensure_ascii=False, indent=4)
    return default

USERS = load_json(USERS_FILE, {})
REWARDS = load_json(REWARD_FILE, [])
TUTORIALS = load_json(TUTORIAL_FILE, {"android": [], "iphone": [], "pc": []})
CONFIGS = load_json(CONFIG_FILE, {})
REFERRED = load_json(REFERRED_FILE, {})

def save_all():
    for file, data in [
        (USERS_FILE, USERS), (REWARD_FILE, REWARDS),
        (TUTORIAL_FILE, TUTORIALS), (CONFIG_FILE, CONFIGS),
        (REFERRED_FILE, REFERRED)
    ]:
        with open(file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

print(f"✅ ربات لود شد | کانفیگ: {len(CONFIGS)} | ویدیو: {sum(len(v) for v in TUTORIALS.values())} | جایزه: {len(REWARDS)}")

# ==================== دکمه بازگشت ====================
def back_button():
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🏠 بازگشت به منوی اصلی", callback_data="main_menu"))
    return markup

# ==================== منوی اصلی ====================
def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(InlineKeyboardButton("🛒 خرید سرویس استارلینک", callback_data="buy"))
    markup.row_width = 2
    markup.add(
        InlineKeyboardButton("📊 سرویس های من", callback_data="my_services"),
        InlineKeyboardButton("💡 آموزش استفاده", callback_data="tutorials"),
        InlineKeyboardButton("👥 دریافت کانفیگ رایگان", callback_data="referral"),
        InlineKeyboardButton("👨‍💻 تیکت پشتیبانی", callback_data="support")
    )
    bot.send_message(chat_id, "✅ منوی اصلی:\n\nلطفاً گزینه مورد نظرت رو انتخاب کن:", reply_markup=markup)

# ==================== دستورات ادمین ====================
def set_admin_commands():
    commands = [
        BotCommand("start", "🔄 شروع / منوی اصلی"),
        BotCommand("addconfig", "➕ اضافه کردن کانفیگ"),
        BotCommand("stock", "📦 مشاهده موجودی کانفیگ‌ها"),
        BotCommand("addvideo", "📹 اضافه کردن ویدیو آموزش"),
        BotCommand("delvideo", "🗑 حذف ویدیو آموزش"),
        BotCommand("addreward", "🎁 گذاشتن کانفیگ رایگان"),
        BotCommand("delconfig", "❌ حذف کانفیگ"),
        BotCommand("broadcast", "📢 ارسال پیام به همه کاربران"),
    ]
    bot.set_my_commands(commands, scope=BotCommandScopeChat(ADMIN_ID))

# ==================== شروع ربات ====================
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = str(message.chat.id)
    if user_id not in USERS:
        USERS[user_id] = {"stars": 0, "referred_by": None}
        save_all()

    if len(message.text.split()) > 1 and message.text.split()[1].startswith("ref_"):
        referrer = message.text.split()[1].split("_")[1]
        handle_referral(referrer, user_id)

    if message.chat.id == ADMIN_ID:
        show_main_menu(message.chat.id)
        set_admin_commands()
        return

    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, message.chat.id)
        is_member = member.status in ["member", "administrator", "creator"]
    except:
        is_member = False

    if is_member:
        bot.send_message(message.chat.id, "✅ شما قبلاً عضو کانال هستید.\nبه ربات خوش آمدید 🔥")
        show_main_menu(message.chat.id)
    else:
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("🔗 عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME.strip('@')}"),
            InlineKeyboardButton("✅ عضو شدم", callback_data="check_membership")
        )
        bot.send_message(message.chat.id, "👋 سلام!\n\nلطفا اول در کانال عضو شوید:", reply_markup=markup)

def handle_referral(referrer, new_user):
    if referrer == new_user or referrer not in USERS: return
    if referrer not in REFERRED: REFERRED[referrer] = []
    if new_user in REFERRED[referrer]: return
    try:
        member = bot.get_chat_member(CHANNEL_USERNAME, int(new_user))
        is_member = member.status in ["member", "administrator", "creator"]
    except:
        is_member = False
    if is_member:
        USERS[referrer]["stars"] += 1
        REFERRED[referrer].append(new_user)
        save_all()
        bot.send_message(referrer, f"🎉 یک کاربر جدید با لینک شما وارد شد!\n🌟 ستاره‌های شما: {USERS[referrer]['stars']}")

# ==================== Callback اصلی ====================
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    data = call.data
    chat_id = call.message.chat.id
    user_id = str(call.from_user.id)

    if data == "main_menu":
        bot.delete_message(chat_id, call.message.message_id)
        show_main_menu(chat_id)

    elif data == "check_membership":
        try:
            member = bot.get_chat_member(CHANNEL_USERNAME, chat_id)
            is_member = member.status in ["member", "administrator", "creator"]
        except:
            is_member = False

        if is_member:
            bot.answer_callback_query(call.id, "✅ عضویت تأیید شد!", show_alert=True)
            bot.send_message(chat_id, "✅ عضویت شما تأیید شد!\nبه ربات خوش آمدید 🔥")
            show_main_menu(chat_id)
        else:
            bot.answer_callback_query(call.id, "❌ هنوز عضو کانال نشده‌اید!", show_alert=True)

    elif data == "buy":
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("💰 مبلغ", callback_data="ignore"),
            InlineKeyboardButton("🛍️ محصول", callback_data="ignore"),
            InlineKeyboardButton("💵 250,000 تومان", callback_data="buy_1"),
            InlineKeyboardButton("🔋 ۱ گیگ", callback_data="buy_1"),
            InlineKeyboardButton("💵 500,000 تومان", callback_data="buy_2"),
            InlineKeyboardButton("🔋 ۲ گیگ", callback_data="buy_2"),
            InlineKeyboardButton("💵 1,250,000 تومان", callback_data="buy_5"),
            InlineKeyboardButton("🔋 ۵ گیگ", callback_data="buy_5"),
            InlineKeyboardButton("💵 2,500,000 تومان", callback_data="buy_10"),
            InlineKeyboardButton("🔋 ۱۰ گیگ", callback_data="buy_10"),
            InlineKeyboardButton("💵 5,000,000 تومان", callback_data="buy_20"),
            InlineKeyboardButton("🔋 ۲۰ گیگ", callback_data="buy_20")
        )
        bot.send_message(chat_id, "🛒 خرید سرویس استارلینک\n\nلطفاً پلن مورد نظر را انتخاب کنید:", reply_markup=markup)

    elif data.startswith("buy_"):
        plan_key = data.split("_")[1]
        plans = {"1": "۱ گیگ", "2": "۲ گیگ", "5": "۵ گیگ", "10": "۱۰ گیگ", "20": "۲۰ گیگ"}
        prices = {"1": "250,000 تومان", "2": "500,000 تومان", "5": "1,250,000 تومان", "10": "2,500,000 تومان", "20": "5,000,000 تومان"}
        plan_name = plans.get(plan_key, "نامشخص")
        price = prices.get(plan_key, "نامشخص")
        
        msg = f"""✅ پلن انتخابی: {plan_name}

💰 قیمت: {price}

💳 شماره کارت:
`{CARD_NUMBER}`

📋 روی شماره کارت بزن تا کپی شود

📸 فقط عکس رسید پرداخت را بفرست"""
        bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=back_button())
        bot.register_next_step_handler(call.message, lambda m: handle_receipt(m, plan_name))

    # ==================== بقیه کد بدون تغییر ====================
    elif data == "my_services":
        bot.send_message(chat_id, "📊 **سرویس‌های من**\n\nدر حال حاضر هیچ سرویسی فعال نداری.\nپس از خرید، اینجا نمایش داده می‌شود.", reply_markup=back_button())

    elif data == "tutorials":
        markup = InlineKeyboardMarkup(row_width=1)
        markup.add(
            InlineKeyboardButton("📱 اندروید", callback_data="tutorial_android"),
            InlineKeyboardButton("🍎 آیفون", callback_data="tutorial_iphone"),
            InlineKeyboardButton("💻 کامپیوتر", callback_data="tutorial_pc")
        )
        bot.send_message(chat_id, "💡 آموزش استفاده\n\nسیستم عامل خود را انتخاب کنید:", reply_markup=markup)

    elif data.startswith("tutorial_"):
        platform = data.split("_")[1]
        videos = TUTORIALS.get(platform, [])
        if not videos:
            bot.send_message(chat_id, f"🎥 هنوز ویدیو برای **{platform}** اضافه نشده.", reply_markup=back_button())
            return
        for vid in videos:
            bot.send_video(chat_id, vid[0], caption=vid[1] if len(vid) > 1 else "", supports_streaming=True)

    elif data == "referral":
        stars = USERS.get(user_id, {}).get("stars", 0)
        link = f"https://t.me/{bot.get_me().username}?start=ref_{user_id}"
        msg = f"""👥 **دریافت کانفیگ رایگان**

لینک دعوت شما:
`{link}`

🌟 ستاره‌ها: {stars}/۵

هر دوست جدید که عضو کانال شود + ربات را استارت بزند → ۱ ستاره"""
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🎁 دریافت کانفیگ رایگان", callback_data="claim_free_config"))
        bot.send_message(chat_id, msg, parse_mode="Markdown", reply_markup=markup)

    elif data == "claim_free_config":
        stars = USERS.get(user_id, {}).get("stars", 0)
        if stars < 5:
            bot.answer_callback_query(call.id, f"شما {stars} ستاره دارید. نیاز به ۵ ستاره دارید.", show_alert=True)
            return
        if not REWARDS:
            bot.send_message(chat_id, "❌ موجودی کانفیگ رایگان تمام شده است.\nستاره‌های شما حفظ شد.", reply_markup=back_button())
            return
        config = REWARDS.pop(0)
        USERS[user_id]["stars"] -= 5
        save_all()
        bot.send_message(chat_id, f"🎉 **کانفیگ رایگان شما:**\n\n```{config}```", parse_mode="Markdown")

    elif data == "support":
        bot.send_message(chat_id, "👨‍💻 پیام خود را بنویسید:", reply_markup=back_button())
        bot.register_next_step_handler(call.message, handle_support_message)

    # ==================== بخش حذف کانفیگ ====================
    elif data == "del_normal":
        if call.from_user.id != ADMIN_ID:
            bot.answer_callback_query(call.id, "فقط ادمین!")
            return
        bot.send_message(chat_id, "📌 اسم پلن را بفرست (مثل: 1گیگ):")
        bot.register_next_step_handler_by_chat_id(chat_id, del_normal_plan)

    elif data == "del_reward":
        if call.from_user.id != ADMIN_ID:
            bot.answer_callback_query(call.id, "فقط ادمین!")
            return
        if not REWARDS:
            bot.send_message(chat_id, "❌ هیچ کانفیگ رایگانی وجود ندارد.")
            return
        msg = "🎁 کانفیگ‌های رایگان:\n\n"
        for i, cfg in enumerate(REWARDS, 1):
            msg += f"{i}. {cfg[:60]}...\n"
        bot.send_message(chat_id, msg + "\n🔢 شماره کانفیگی که می‌خوای حذف کنی رو بفرست:")
        bot.register_next_step_handler_by_chat_id(chat_id, del_reward_step)

    # ==================== بخش ویدیو آموزشی ====================
    elif data.startswith("add_tut_"):
        if call.from_user.id != ADMIN_ID:
            bot.answer_callback_query(call.id, "فقط ادمین!")
            return
        platform = data.split("_")[2]
        bot.send_message(chat_id, 
            f"📹 حالا **ویدیو + کپشن** برای بخش **{platform}** بفرست:\n"
            f"می‌تونی کپشن بذاری یا خالی بذاری.")
        bot.register_next_step_handler_by_chat_id(chat_id, lambda m: save_tutorial(m, platform))

    elif data.startswith("del_tut_"):
        if call.from_user.id != ADMIN_ID:
            bot.answer_callback_query(call.id, "فقط ادمین!")
            return
        platform = data.split("_")[2]
        videos = TUTORIALS.get(platform, [])
        if not videos:
            bot.send_message(chat_id, f"❌ هنوز ویدیویی برای **{platform}** وجود ندارد.")
            return
        msg = f"🎥 ویدیوهای {platform}:\n\n"
        for i, v in enumerate(videos, 1):
            caption = v[1][:60] + "..." if len(v) > 1 and v[1] else "بدون کپشن"
            msg += f"{i}. {caption}\n"
        bot.send_message(chat_id, msg + "\n\n🔢 شماره ویدیویی که می‌خوای حذف کنی رو بفرست:")
        bot.register_next_step_handler_by_chat_id(chat_id, lambda m: delete_tutorial_step(m, platform))

    elif data == "ignore":
        bot.answer_callback_query(call.id)

    bot.answer_callback_query(call.id)

# ==================== ارسال پیام به همه کاربران ====================
@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    if message.chat.id != ADMIN_ID:
        return
    bot.send_message(ADMIN_ID, "📢 پیام خود را بنویسید. این پیام به **همه کاربران** ارسال خواهد شد:")
    bot.register_next_step_handler(message, send_broadcast_to_all)

def send_broadcast_to_all(message):
    if message.chat.id != ADMIN_ID:
        return
    count = 0
    for user_id in list(USERS.keys()):
        try:
            bot.send_message(int(user_id), f"📢 پیام از مدیریت:\n\n{message.text}")
            count += 1
        except:
            pass
    bot.send_message(ADMIN_ID, f"✅ پیام با موفقیت به {count} کاربر ارسال شد.")

# ==================== بقیه توابع بدون هیچ تغییری ====================
pending_orders = {}
support_tickets = {}

def handle_receipt(message, plan_name):
    if message.photo:
        forwarded = bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
        pending_orders[forwarded.message_id] = {"user_id": message.chat.id, "plan": plan_name}
        bot.send_message(ADMIN_ID, f"""🛎️ سفارش جدید
👤 کاربر: {message.chat.id}
📦 پلن: {plan_name}

🔄 روی این پیام ریپلای کن و فقط بنویس: **تایید**""")
        bot.send_message(message.chat.id, "✅ رسید ارسال شد. منتظر تأیید باشید...", reply_markup=back_button())
    else:
        bot.send_message(message.chat.id, "❌ فقط عکس رسید بفرست.", reply_markup=back_button())

def handle_support_message(message):
    if message.chat.id == ADMIN_ID: return
    forwarded = bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)
    support_tickets[forwarded.message_id] = message.chat.id
    bot.send_message(message.chat.id, "✅ پیام شما به ادمین ارسال شد.\nمنتظر پاسخ باشید.", reply_markup=back_button())

@bot.message_handler(func=lambda m: m.chat.id == ADMIN_ID and m.reply_to_message)
def reply_to_support(message):
    replied_id = message.reply_to_message.message_id
    if replied_id in support_tickets:
        user_id = support_tickets[replied_id]
        bot.send_message(user_id, message.text)
        bot.send_message(ADMIN_ID, "✅ پاسخ شما به کاربر ارسال شد.")
    elif replied_id in pending_orders:
        order = pending_orders[replied_id]
        user_id = order["user_id"]
        plan = order["plan"]
        bot.send_message(user_id, message.text)
        if "تایید" in message.text or "confirm" in message.text.lower():
            if plan in CONFIGS and CONFIGS[plan]:
                config = CONFIGS[plan].pop(0)
                save_all()
                bot.send_message(user_id, f"✅ خرید شما تأیید شد!\n\nکانفیگ {plan}:\n```{config}```", parse_mode="Markdown")
                bot.send_message(ADMIN_ID, f"✅ کانفیگ {plan} به کاربر ارسال شد.")
            else:
                bot.send_message(user_id, "⚠️ کانفیگ این پلن تمام شده است.")
        pending_orders.pop(replied_id, None)

# ==================== توابع ادمین ====================

@bot.message_handler(commands=['addconfig'])
def add_config(message):
    if message.chat.id != ADMIN_ID: return
    bot.send_message(ADMIN_ID, "📌 اسم پلن را بفرست (مثلاً: 1گیگ)")
    bot.register_next_step_handler(message, wait_for_plan_name)

temp_plan = temp_count = temp_configs = None

def wait_for_plan_name(message):
    global temp_plan
    temp_plan = message.text.strip()
    bot.send_message(ADMIN_ID, f"✅ حالا چند کانفیگ برای **{temp_plan}** می‌خواهی اضافه کنی؟")
    bot.register_next_step_handler(message, wait_for_count)

def wait_for_count(message):
    global temp_count
    try:
        temp_count = int(message.text)
        bot.send_message(ADMIN_ID, f"حالا {temp_count} تا کانفیگ بفرست (یکی یکی):")
        bot.register_next_step_handler(message, save_multiple_configs)
    except:
        bot.send_message(ADMIN_ID, "❌ فقط عدد!")

def save_multiple_configs(message):
    global temp_configs
    if not temp_configs: temp_configs = []
    temp_configs.append(message.text.strip())
    if len(temp_configs) < temp_count:
        bot.send_message(ADMIN_ID, f"✅ {len(temp_configs)}/{temp_count} دریافت شد. بعدی:")
        bot.register_next_step_handler(message, save_multiple_configs)
    else:
        if temp_plan not in CONFIGS: CONFIGS[temp_plan] = []
        CONFIGS[temp_plan].extend(temp_configs)
        save_all()
        bot.send_message(ADMIN_ID, f"🎉 {temp_count} کانفیگ برای {temp_plan} ذخیره شد.")
        temp_configs = []

@bot.message_handler(commands=['stock'])
def admin_stock(message):
    if message.chat.id != ADMIN_ID: return
    text = "📦 **موجودی کامل کانفیگ‌ها**\n\n"
    for plan, cfgs in CONFIGS.items():
        text += f"🔹 {plan} ({len(cfgs)} عدد):\n"
        for i, cfg in enumerate(cfgs, 1):
            text += f"   {i}. `{cfg[:60]}...`\n"
        text += "\n"
    bot.send_message(message.chat.id, text if CONFIGS else "هیچ کانفیگی موجود نیست.")

@bot.message_handler(commands=['addvideo'])
def admin_add_video(message):
    if message.chat.id != ADMIN_ID: return
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📱 اندروید", callback_data="add_tut_android"),
        InlineKeyboardButton("🍎 آیفون", callback_data="add_tut_iphone"),
        InlineKeyboardButton("💻 ویندوز", callback_data="add_tut_pc")
    )
    bot.send_message(message.chat.id, "📍 برای کدام بخش ویدیو **اضافه** کنم؟", reply_markup=markup)

@bot.message_handler(commands=['delvideo'])
def admin_del_video(message):
    if message.chat.id != ADMIN_ID: return
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📱 اندروید", callback_data="del_tut_android"),
        InlineKeyboardButton("🍎 آیفون", callback_data="del_tut_iphone"),
        InlineKeyboardButton("💻 ویندوز", callback_data="del_tut_pc")
    )
    bot.send_message(message.chat.id, "📍 از کدام بخش ویدیو **حذف** کنم؟", reply_markup=markup)

def save_tutorial(message, platform):
    if message.video:
        caption = message.caption or "آموزش استفاده از فیلترشکن"
        TUTORIALS[platform].append([message.video.file_id, caption])
        save_all()
        bot.send_message(message.chat.id, f"✅ ویدیو با موفقیت برای **{platform}** ذخیره شد.")
    else:
        bot.send_message(message.chat.id, "❌ لطفاً یک **ویدیو** بفرست (نه عکس یا فایل دیگه).")

def delete_tutorial_step(message, platform):
    try:
        idx = int(message.text.strip()) - 1
        if 0 <= idx < len(TUTORIALS[platform]):
            TUTORIALS[platform].pop(idx)
            save_all()
            bot.send_message(message.chat.id, f"✅ ویدیو شماره {idx+1} با موفقیت حذف شد.")
        else:
            bot.send_message(message.chat.id, "❌ شماره وارد شده خارج از محدوده است.")
    except:
        bot.send_message(message.chat.id, "❌ لطفاً فقط عدد بفرست (مثلاً ۱).")

@bot.message_handler(commands=['delconfig'])
def admin_del_config(message):
    if message.chat.id != ADMIN_ID: return
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("📦 کانفیگ‌های معمولی", callback_data="del_normal"),
        InlineKeyboardButton("🎁 کانفیگ‌های رایگان", callback_data="del_reward")
    )
    bot.send_message(message.chat.id, "کدام نوع کانفیگ را می‌خواهید حذف کنید؟", reply_markup=markup)

def del_normal_plan(message):
    if message.chat.id != ADMIN_ID: return
    plan = message.text.strip()
    if plan in CONFIGS and CONFIGS[plan]:
        text = f"📦 کانفیگ‌های {plan}:\n\n"
        for i, c in enumerate(CONFIGS[plan], 1):
            text += f"{i}. {c[:50]}...\n"
        bot.send_message(message.chat.id, text)
        bot.send_message(message.chat.id, "🔢 شماره کانفیگی که می‌خوای حذف کنی رو بفرست:")
        bot.register_next_step_handler(message, lambda m: del_normal_config(m, plan))
    else:
        bot.send_message(message.chat.id, "❌ پلن پیدا نشد یا کانفیگی در این پلن وجود ندارد.")

def del_normal_config(message, plan):
    if message.chat.id != ADMIN_ID: return
    try:
        idx = int(message.text.strip()) - 1
        if 0 <= idx < len(CONFIGS[plan]):
            CONFIGS[plan].pop(idx)
            save_all()
            bot.send_message(message.chat.id, f"✅ کانفیگ شماره {idx+1} با موفقیت حذف شد.")
        else:
            bot.send_message(message.chat.id, "❌ شماره وارد شده خارج از محدوده است.")
    except:
        bot.send_message(message.chat.id, "❌ لطفاً فقط عدد بفرست (مثلاً ۱).")

def del_reward_step(message):
    if message.chat.id != ADMIN_ID: return
    try:
        idx = int(message.text.strip()) - 1
        if 0 <= idx < len(REWARDS):
            REWARDS.pop(idx)
            save_all()
            bot.send_message(message.chat.id, f"✅ کانفیگ رایگان شماره {idx+1} با موفقیت حذف شد.")
        else:
            bot.send_message(message.chat.id, "❌ شماره وارد شده خارج از محدوده است.")
    except:
        bot.send_message(message.chat.id, "❌ لطفاً فقط عدد بفرست (مثلاً ۱).")

if __name__ == "__main__":
    bot.infinity_polling()