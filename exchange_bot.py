import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, CommandHandler,
    CallbackQueryHandler, ContextTypes, MessageHandler, filters
)


TOKEN = os.getenv("dzen_exchange_bot")

ADMIN_LINK = "https://t.me/+XFM8A0Le-sM2NWYy"
REVIEWS_LINK = "https://t.me/DzenObmenGlobal/2"
ORDERS_CHAT_ID = -1003902164090


async def delete_amount_messages(context, chat_id):
    for key in ["amount_prompt_message_id", "amount_message_id"]:
        message_id = context.user_data.get(key)
        if message_id:
            try:
                await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            except:
                pass
            context.user_data.pop(key, None)


def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("→ оформить обмен", callback_data="exchange")],
        [InlineKeyboardButton("→ служба поддержки", url=ADMIN_LINK)],
        [InlineKeyboardButton("→ отзывы клиентов", url=REVIEWS_LINK)],
    ])


def currency_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("→ USDT tether", callback_data="receive_usdt")],
        [InlineKeyboardButton("→ INR индийские рупии", callback_data="receive_inr")],
        [InlineKeyboardButton("→ VND вьетнамские донги", callback_data="receive_vnd")],
        [InlineKeyboardButton("→ служба поддержки", url=ADMIN_LINK)],
        [InlineKeyboardButton("← назад", callback_data="back_main")],
    ])


def amount_buttons():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("→ продолжить", callback_data="go_next")],
        [InlineKeyboardButton("→ изменить сумму", callback_data="change_amount")],
        [InlineKeyboardButton("→ служба поддержки", url=ADMIN_LINK)],
        [InlineKeyboardButton("← назад", callback_data="back_currency")],
    ])


def method_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("→ зачисление на карту", callback_data="method_card")],
        [InlineKeyboardButton("→ выдача через банкомат", callback_data="method_atm")],
        [InlineKeyboardButton("→ получение наличных", callback_data="method_cash")],
        [InlineKeyboardButton("→ оплата услуг", callback_data="method_services")],
        [InlineKeyboardButton("→ служба поддержки", url=ADMIN_LINK)],
        [InlineKeyboardButton("← назад", callback_data="back_amount_buttons")],
    ])


def exchange_keyboard_usdt():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("→ RUB российский рубль", callback_data="exchange_rub")],
        [InlineKeyboardButton("→ INR индийские рупии", callback_data="exchange_inr")],
        [InlineKeyboardButton("→ VND вьетнамские донги", callback_data="exchange_vnd")],
        [InlineKeyboardButton("→ служба поддержки", url=ADMIN_LINK)],
        [InlineKeyboardButton("← назад", callback_data="back_amount_buttons")],
    ])


def exchange_keyboard_inr_vnd():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("→ USDT tether", callback_data="exchange_usdt")],
        [InlineKeyboardButton("→ RUB российский рубль", callback_data="exchange_rub")],
        [InlineKeyboardButton("→ служба поддержки", url=ADMIN_LINK)],
        [InlineKeyboardButton("← назад", callback_data="back_method")],
    ])


def final_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("→ завершить", callback_data="finish")],
        [InlineKeyboardButton("→ служба поддержки", url=ADMIN_LINK)],
        [InlineKeyboardButton("← назад", callback_data="back_exchange")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()

    await update.message.reply_text(
        "<b>💹 ДОБРО ПОЖАЛОВАТЬ В ДЗЕН ОБМЕН</b>",
        parse_mode="HTML"
    )

    await update.message.reply_text(
        "<b>✅ выберите действие:</b>",
        reply_markup=main_keyboard(),
        parse_mode="HTML"
    )


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    data = query.data
    chat_id = query.message.chat_id

    if data == "exchange":
        await query.edit_message_text(
            "<b>✅ выберите валюту получения:</b>",
            reply_markup=currency_keyboard(),
            parse_mode="HTML"
        )

    elif data.startswith("receive_"):
        currency = {
            "receive_usdt": "USDT tether",
            "receive_inr": "INR индийские рупии",
            "receive_vnd": "VND вьетнамские донги"
        }[data]

        context.user_data["currency"] = currency
        context.user_data["step"] = "waiting_amount"

        msg = await query.edit_message_text(
            f"<b>✅ введите сумму получения: {currency}</b>",
            parse_mode="HTML"
        )
        context.user_data["amount_prompt_message_id"] = msg.message_id

    elif data == "go_next":
        await delete_amount_messages(context, chat_id)

        if context.user_data.get("currency") == "USDT tether":
            await query.edit_message_text(
                "<b>✅ выберите валюту обмена:</b>",
                reply_markup=exchange_keyboard_usdt(),
                parse_mode="HTML"
            )
        else:
            await query.edit_message_text(
                "<b>✅ выберите способ получения:</b>",
                reply_markup=method_keyboard(),
                parse_mode="HTML"
            )

    elif data == "change_amount":
        await delete_amount_messages(context, chat_id)

        currency = context.user_data.get("currency", "")
        context.user_data["step"] = "waiting_amount"

        msg = await query.edit_message_text(
            f"<b>✅ введите сумму получения: {currency}</b>",
            parse_mode="HTML"
        )
        context.user_data["amount_prompt_message_id"] = msg.message_id

    elif data == "back_currency":
        await delete_amount_messages(context, chat_id)
        context.user_data.clear()

        await query.edit_message_text(
            "<b>✅ выберите валюту получения:</b>",
            reply_markup=currency_keyboard(),
            parse_mode="HTML"
        )

    elif data == "back_amount_buttons":
        await query.edit_message_text(
            "<b>✅ выберите действие:</b>",
            reply_markup=amount_buttons(),
            parse_mode="HTML"
        )

    elif data in ["method_card", "method_atm", "method_cash", "method_services"]:
        methods = {
            "method_card": "зачисление на карту",
            "method_atm": "выдача через банкомат",
            "method_cash": "получение наличных",
            "method_services": "оплата услуг"
        }

        context.user_data["method"] = methods[data]

        await query.edit_message_text(
            "<b>✅ выберите валюту обмена:</b>",
            reply_markup=exchange_keyboard_inr_vnd(),
            parse_mode="HTML"
        )

    elif data in ["exchange_usdt", "exchange_rub", "exchange_inr", "exchange_vnd"]:
        exchanges = {
            "exchange_usdt": "USDT tether",
            "exchange_rub": "RUB российский рубль",
            "exchange_inr": "INR индийские рупии",
            "exchange_vnd": "VND вьетнамские донги"
        }

        exchange = exchanges[data]
        context.user_data["exchange_currency"] = exchange

        user = query.from_user
        username = f"@{user.username}" if user.username else "нет username"
        contact_link = f"tg://user?id={user.id}"

        order_text = (
            "🆕 новая заявка\n\n"
            f"клиент: {user.first_name}\n"
            f"username: {username}\n"
            f"id: {user.id}\n"
            f"контакт: {contact_link}\n\n"
            f"валюта получения: {context.user_data.get('currency')}\n"
            f"сумма получения: {context.user_data.get('amount')}\n"
            f"способ получения: {context.user_data.get('method', 'не указано')}\n"
            f"валюта обмена: {exchange}"
        )

        await context.bot.send_message(
            chat_id=ORDERS_CHAT_ID,
            text=order_text
        )

        await query.edit_message_text(
            "<b>✅ заявка принята\n\nожидайте, менеджер свяжется с вами в ближайшее время.</b>",
            reply_markup=final_keyboard(),
            parse_mode="HTML"
        )

    elif data == "back_exchange":
        if context.user_data.get("currency") == "USDT tether":
            await query.edit_message_text(
                "<b>✅ выберите валюту обмена:</b>",
                reply_markup=exchange_keyboard_usdt(),
                parse_mode="HTML"
            )
        else:
            await query.edit_message_text(
                "<b>✅ выберите валюту обмена:</b>",
                reply_markup=exchange_keyboard_inr_vnd(),
                parse_mode="HTML"
            )

    elif data == "back_method":
        await query.edit_message_text(
            "<b>✅ выберите способ получения:</b>",
            reply_markup=method_keyboard(),
            parse_mode="HTML"
        )

    elif data == "back_main":
        context.user_data.clear()

        await query.edit_message_text(
            "<b>✅ выберите действие:</b>",
            reply_markup=main_keyboard(),
            parse_mode="HTML"
        )

    elif data == "finish":
        context.user_data.clear()

        await query.edit_message_text(
            "<b>✅ выберите действие:</b>",
            reply_markup=main_keyboard(),
            parse_mode="HTML"
        )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("step") != "waiting_amount":
        return

    text = update.message.text.strip()

    if not text.isdigit():
        await update.message.reply_text("Введите только цифры")
        return

    context.user_data["amount"] = text
    context.user_data["amount_message_id"] = update.message.message_id
    context.user_data["step"] = "amount_entered"

    await update.message.reply_text(
        "<b>✅ выберите действие:</b>",
        reply_markup=amount_buttons(),
        parse_mode="HTML"
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Бот запущен")
    app.run_polling()


if __name__ == "__main__":
    main()
