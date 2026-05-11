import os

from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
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

user_state = {}
user_target = {}

MAIN_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🌍 Выбрать канал")],
    ],
    resize_keyboard=True
)

CHANNELS_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("🇮🇳 Индия")],
        [KeyboardButton("🇻🇳 Вьетнам")],
        [KeyboardButton("🌍 Глобал")],
    ],
    resize_keyboard=True
)

CREATE_POST_KEYBOARD = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton("📝 Создать пост")],
        [KeyboardButton("🌍 Выбрать канал")],
    ],
    resize_keyboard=True
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_state[update.effective_user.id] = None

    await update.message.reply_text(
        "🌍 Куда публиковать пост?",
        reply_markup=CHANNELS_KEYBOARD
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text

    if text == "🌍 Выбрать канал":
        await update.message.reply_text(
            "🌍 Выберите канал:",
            reply_markup=CHANNELS_KEYBOARD
        )
        return

    if text == "🇮🇳 Индия":
        user_target[user_id] = INDIA_GROUP_ID

        await update.message.reply_text(
            "✅ Выбрана Индия\n\nТеперь нажмите «Создать пост»",
            reply_markup=CREATE_POST_KEYBOARD
        )
        return

    if text == "🇻🇳 Вьетнам":
        user_target[user_id] = VIETNAM_GROUP_ID

        await update.message.reply_text(
            "✅ Выбран Вьетнам\n\nТеперь нажмите «Создать пост»",
            reply_markup=CREATE_POST_KEYBOARD
        )
        return

    if text == "🌍 Глобал":
        user_target[user_id] = GLOBAL_CHANNEL

        await update.message.reply_text(
            "✅ Выбран Глобал\n\nТеперь нажмите «Создать пост»",
            reply_markup=CREATE_POST_KEYBOARD
        )
        return

    if text == "📝 Создать пост":
        user_state[user_id] = "waiting_post"

        await update.message.reply_text(
            "📸 Отправьте фото или видео с текстом."
        )
        return

    if user_state.get(user_id) == "waiting_post":

        target = user_target.get(user_id)

        if not target:
            await update.message.reply_text(
                "❌ Сначала выберите канал."
            )
            return

        try:

            if update.message.photo:

                photo = update.message.photo[-1].file_id

                await context.bot.send_photo(
                    chat_id=target,
                    photo=photo,
                    caption=update.message.caption or ""
                )

            elif update.message.video:

                video = update.message.video.file_id

                await context.bot.send_video(
                    chat_id=target,
                    video=video,
                    caption=update.message.caption or ""
                )

            else:

                await context.bot.send_message(
                    chat_id=target,
                    text=text
                )

            await update.message.reply_text(
                "✅ Опубликовано\n\nМожно сразу создать следующий пост.",
                reply_markup=MAIN_KEYBOARD
            )

            user_state[user_id] = None

        except Exception as e:

            await update.message.reply_text(
                f"❌ Ошибка публикации:\n{e}"
            )


app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.ALL, handle_message))

print("BOT STARTED")

app.run_polling()
