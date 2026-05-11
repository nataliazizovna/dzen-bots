import os
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("dzen_publications_bot")

INDIA_GROUP_ID = -1003261155661
VIETNAM_GROUP_ID = -1003984357381
GLOBAL_CHANNEL = "@DzenObmenGlobal"

APPLICATION_LINK = "https://t.me/dzen_exchange_bot"
REVIEWS_LINK = "https://t.me/DzenObmenGlobal/2"

user_state = {}
user_target = {}

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [[KeyboardButton("📝 Создать пост")]],
    resize_keyboard=True
)

CHANNELS_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🇮🇳 Индия")],
        [KeyboardButton("🇻🇳 Вьетнам")],
        [KeyboardButton("🌍 Глобал")],
    ],
    resize_keyboard=True
)

POST_KEYBOARD = InlineKeyboardMarkup([
    [InlineKeyboardButton("➡️ ОСТАВИТЬ ЗАЯВКУ", url=APPLICATION_LINK)],
    [InlineKeyboardButton("📣 ОТЗЫВЫ", url=REVIEWS_LINK)],
])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state.clear()
    await update.message.reply_text(
        "✅ ДЗЕН ПУБЛИКАТОР\n\nНажмите «Создать пост».",
        reply_markup=MAIN_KEYBOARD
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text if update.message.text else ""

    if text == "📝 Создать пост":
        await update.message.reply_text(
            "✅ Куда опубликовать?",
            reply_markup=CHANNELS_KEYBOARD
        )
        return

    if text == "🇮🇳 Индия":
        user_target[user_id] = INDIA_GROUP_ID
        user_state[user_id] = "waiting_post"
        await update.message.reply_text("✅ Индия выбрана. Теперь отправьте пост.")
        return

    if text == "🇻🇳 Вьетнам":
        user_target[user_id] = VIETNAM_GROUP_ID
        user_state[user_id] = "waiting_post"
        await update.message.reply_text("✅ Вьетнам выбран. Теперь отправьте пост.")
        return

    if text == "🌍 Глобал":
        user_target[user_id] = GLOBAL_CHANNEL
        user_state[user_id] = "waiting_post"
        await update.message.reply_text("✅ Глобал выбран. Теперь отправьте пост.")
        return

    if user_state.get(user_id) == "waiting_post":
        target = user_target.get(user_id)

        try:
            await context.bot.copy_message(
    chat_id=target,
    from_chat_id=update.message.chat_id,
    message_id=update.message.message_id
)
            user_state[user_id] = None
            user_target[user_id] = None

            await update.message.reply_text(
                "✅ Опубликовано\n\nМожно создать следующий пост.",
                reply_markup=MAIN_KEYBOARD
            )

        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка публикации:\n{e}")
        return

    await update.message.reply_text(
        "Нажмите «Создать пост».",
        reply_markup=MAIN_KEYBOARD
    )


app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("BOT STARTED")
app.run_polling()
