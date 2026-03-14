import re
from datetime import timedelta
from collections import defaultdict
from telegram import Update, ChatMember, ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, ChatMemberHandler, CommandHandler, filters, ContextTypes
from tinydb import TinyDB, Query

BOT_TOKEN = "8715807554:AAED7-mVJikkESVqd6SoVs7bzQQ1CZGULf4"
LOG_CHANNEL_ID = -1003766623456

LINK_PATTERN = re.compile(r"(https?://|www\.|t\.me/)\S+", re.IGNORECASE)
BAD_WORDS = ["am", "sex", "porn", "nude"]

# Database setup
db = TinyDB('warnings_db.json')
warns_table = db.table('warnings')
User = Query()

last_messages = defaultdict(lambda: defaultdict(list))
SPAM_LIMIT = 3

def get_warnings(chat_id, user_id):
    result = warns_table.get((User.chat_id == str(chat_id)) & (User.user_id == str(user_id)))
    return result['count'] if result else 0

def set_warnings(chat_id, user_id, count):
    if warns_table.get((User.chat_id == str(chat_id)) & (User.user_id == str(user_id))):
        warns_table.update({'count': count}, (User.chat_id == str(chat_id)) & (User.user_id == str(user_id)))
    else:
        warns_table.insert({'chat_id': str(chat_id), 'user_id': str(user_id), 'count': count})

async def is_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in [ChatMember.ADMINISTRATOR, ChatMember.OWNER]

async def warn_user(context, chat_id, user_id, name, reason):
    count = get_warnings(chat_id, user_id) + 1
    set_warnings(chat_id, user_id, count)

    if count >= 3:
        await context.bot.restrict_chat_member(
            chat_id=chat_id,
            user_id=user_id,
            permissions=ChatPermissions(can_send_messages=False),
            until_date=timedelta(minutes=5)
        )
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"🔇 {name} has been muted for 5 minutes after 3 warnings!"
        )
        set_warnings(chat_id, user_id, 0)
    else:
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"⚠️ {name}, {reason}! Warning {count}/3"
        )

async def log_deletion(context, name, user_id, text, reason):
    await context.bot.send_message(
        chat_id=LOG_CHANNEL_ID,
        text=f"Deleted message\n"
             f"User: {name} (ID: {user_id})\n"
             f"Message: {text}\n"
             f"Reason: {reason}"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message
    if not message or not message.text:
        return

    if await is_admin(update, context):
        return

    user_id = message.from_user.id
    name = message.from_user.first_name
    chat_id = message.chat_id
    text = message.text.lower()

    if LINK_PATTERN.search(message.text):
        await message.delete()
        await log_deletion(context, name, user_id, message.text, "link")
        await warn_user(context, chat_id, user_id, name, "links are not allowed")
        return

    for word in BAD_WORDS:
        if word.lower() in text:
            await message.delete()
            await log_deletion(context, name, user_id, message.text, f"bad word: {word}")
            await warn_user(context, chat_id, user_id, name, "bad words are not allowed")
            return

    last_messages[chat_id][user_id].append(text)
    last_messages[chat_id][user_id] = last_messages[chat_id][user_id][-SPAM_LIMIT:]

    recent = last_messages[chat_id][user_id]
    is_spam = (
        len(recent) == SPAM_LIMIT and len(set(recent)) == 1
    ) or (
        len(recent) == SPAM_LIMIT and all(len(m) <= 5 for m in recent)
    )

    if is_spam:
        await message.delete()
        await log_deletion(context, name, user_id, message.text, "spam")
        last_messages[chat_id][user_id] = []
        await warn_user(context, chat_id, user_id, name, "stop spamming")
        return

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    result = update.chat_member
    new_member = result.new_chat_member

    if new_member.status == ChatMember.MEMBER:
        name = new_member.user.first_name
        chat_id = result.chat.id
        await context.bot.send_message(
            chat_id=chat_id,
            text=f"👋 Welcome {name} to the group!\n\n"
                 f"📌 Please follow the rules:\n"
                 f"❌ No links allowed\n"
                 f"❌ No bad words\n"
                 f"❌ No spamming\n"
                 f"⚠️ 3 warnings = muted for 5 minutes!"
        )

async def cmd_warn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can use this command!")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a message to warn that user!")
        return
    target = update.message.reply_to_message.from_user
    await warn_user(context, update.message.chat_id, target.id, target.first_name, "you were manually warned by admin")

async def cmd_unwarn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can use this command!")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a message to remove that user's warnings!")
        return
    target = update.message.reply_to_message.from_user
    set_warnings(update.message.chat_id, target.id, 0)
    await update.message.reply_text(f"✅ {target.first_name}'s warnings have been reset!")

async def cmd_mute(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can use this command!")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a message to mute that user!")
        return
    target = update.message.reply_to_message.from_user
    await context.bot.restrict_chat_member(
        chat_id=update.message.chat_id,
        user_id=target.id,
        permissions=ChatPermissions(can_send_messages=False),
        until_date=timedelta(minutes=10)
    )
    await update.message.reply_text(f"🔇 {target.first_name} has been muted for 10 minutes!")

async def cmd_kick(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can use this command!")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a message to kick that user!")
        return
    target = update.message.reply_to_message.from_user
    await context.bot.ban_chat_member(update.message.chat_id, target.id)
    await update.message.reply_text(f"🚫 {target.first_name} has been kicked!")

async def cmd_warnings(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not await is_admin(update, context):
        await update.message.reply_text("❌ Only admins can use this command!")
        return
    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to a message to check that user's warnings!")
        return
    target = update.message.reply_to_message.from_user
    count = get_warnings(update.message.chat_id, target.id)
    await update.message.reply_text(f"⚠️ {target.first_name} has {count}/3 warnings!")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))
    app.add_handler(CommandHandler("warn", cmd_warn))
    app.add_handler(CommandHandler("unwarn", cmd_unwarn))
    app.add_handler(CommandHandler("mute", cmd_mute))
    app.add_handler(CommandHandler("kick", cmd_kick))
    app.add_handler(CommandHandler("warnings", cmd_warnings))
    print("Bot is running...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)