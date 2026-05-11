import os
from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

TOKEN = os.getenv("dzen_publications_bot")

INDIA_GROUP_ID = -1003261155661
VIETNAM_GROUP_ID = -1003984357381
GLOBAL_CHANNEL = "@DzenObmenGlobal"

APPLICATION_LINK = "https://t.me/dzen_exchange_bot"
REVIEWS_LINK = "https://t.me/DzenObmenGlobal/2"

user_state = {}
user_target = {}

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    [[KeyboardButton("📝 СОЗДАТЬ ПОСТ")]],
    resize_keyboard=True
)

CHANNELS_KEYBOARD = ReplyKeyboardMarkup(
    [
        [KeyboardButton("🇮🇳 ИНДИЯ")],
        [KeyboardButton("🇻🇳 ВЬЕТНАМ")],
        [KeyboardButton("🌍 ГЛОБАЛ")],
    ],
    resize_keyboard=True
)

POST_BUTTONS = InlineKeyboardMarkup([
    [InlineKeyboardButton("ОСТАВИТЬ ЗАЯВКУ", url=APPLICATION_LINK)],
    [InlineKeyboardButton("ОТЗЫВЫ", url=REVIEWS_LINK)],
    ]
])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_state[user_id] = None
    user_target[user_id] = None

    await update.message.reply_text(
        "✅ ДЗЕН ПУБЛИКАТОР\n\n"
        "Нажмите кнопку ниже, чтобы создать новый пост.",
        reply_markup=MAIN_KEYBOARD
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text or ""

    if text == "📝 СОЗДАТЬ ПОСТ":
        user_state[user_id] = "choose_channel"
        user_target[user_id] = None

        await update.message.reply_text(
            "✅ Куда опубликовать пост?",
            reply_markup=CHANNELS_KEYBOARD
        )
        return

    if text == "🇮🇳 ИНДИЯ":
        user_target[user_id] = INDIA_GROUP_ID
        user_state[user_id] = "waiting_post"

        await update.message.reply_text(
            "✅ Выбрана ИНДИЯ.\n\n"
            "Теперь отправьте пост: текст, фото, видео или медиа с подписью."
        )
        return

    if text == "🇻🇳 ВЬЕТНАМ":
        user_target[user_id] = VIETNAM_GROUP_ID
        user_state[user_id] = "waiting_post"

        await update.message.reply_text(
            "✅ Выбран ВЬЕТНАМ.\n\n"
            "Теперь отправьте пост: текст, фото, видео или медиа с подписью."
        )
        return

    if text == "🌍 ГЛОБАЛ":
        user_target[user_id] = GLOBAL_CHANNEL
        user_state[user_id] = "waiting_post"

        await update.message.reply_text(
            "✅ Выбран ГЛОБАЛ.\n\n"
            "Теперь отправьте пост: текст, фото, видео или медиа с подписью."
        )
        return

    if user_state.get(user_id) == "waiting_post":
        target = user_target.get(user_id)

        if not target:
            await update.message.reply_text(
                "❌ Сначала выберите канал.",
                reply_markup=MAIN_KEYBOARD
            )
            return

        try:
            await context.bot.copy_message(
                chat_id=target,
                from_chat_id=update.message.chat_id,
                message_id=update.message.message_id,
                reply_markup=POST_BUTTONS
            )

            user_state[user_id] = None
            user_target[user_id] = None

            await update.message.reply_text(
                "✅ ОПУБЛИКОВАНО\n\n"
                "Можно создать следующий пост.",
                reply_markup=MAIN_KEYBOARD
            )

        except Exception as e:
            user_state[user_id] = None
            user_target[user_id] = None

            await update.message.reply_text(
                f"❌ ОШИБКА ПУБЛИКАЦИИ:\n{e}\n\n"
                "Нажмите «СОЗДАТЬ ПОСТ» и попробуйте снова.",
                reply_markup=MAIN_KEYBOARD
            )

        return

    await update.message.reply_text(
        "Нажмите «СОЗДАТЬ ПОСТ».",
        reply_markup=MAIN_KEYBOARD
    )


def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.ALL, handle_message))

    print("BOT STARTED")
    app.run_polling()


if __name__ == "__main__":
    main()
