#!/usr/bin/env python
# pylint: disable=unused-argument, wrong-import-position
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters, CallbackContext, CallbackQueryHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

TYPEOF, WEIGHT, CRYPTO, CHECK = range(4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Starts the conversation and asks the user about their gender."""
    reply_keyboard = [["Sativa", "Indika", "Hash"]]

    await update.message.reply_text(
        "Choose what type of weed do u want?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True, input_field_placeholder="Boy or Girl?"
        ),
    )

    return TYPEOF


async def typeof(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the selected gender and asks for a photo."""
    user = update.message.from_user
    reply_keyboard = [["1", "2", "5"]]

    await update.message.reply_text(
        "How much grams do u want?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard, one_time_keyboard=True
        ),
    )
    return WEIGHT


async def weight(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the photo and asks for a location."""
    text = update.message.text
    if int(text) == 1:
        pay_amount = 30
    elif int(text) == 2:
        pay_amount = 50
    else:
        pay_amount = 100
    user = update.message.from_user
    reply_keyboard = [["Bitcoin", "Ethereum"]]

    await update.message.reply_text(
        f"To pay {pay_amount}$. Choose the payment option",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard
        )
    )
    return CRYPTO


async def crypto(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Stores the location and asks for some info about the user."""
    text = update.message.text
    if text == "Bitcoin":
        pay_amount = "Your Bitcoin address. "
    else:
        pay_amount = "Your Ethereum address "
    user = update.message.from_user
    keyboard = [
        [
            InlineKeyboardButton("Check status", callback_data="1")
            ]
        ]

    await update.message.reply_text(
        f"{pay_amount} ",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )
    return CHECK


async def check_status(update: Update):
    query = update.callback_query
    query.answer()
    if query.data == '1':
        await update.message.reply_text(
            "The payment is not done"
        )
        return CHECK


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def main() -> None:
    """Run the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token("5531011071:AAGWFFKwFZF0LI4KIA_81GApPzguubXr3ZY").build()

    # Add conversation handler with the states GENDER, PHOTO, LOCATION and BIO
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            TYPEOF: [MessageHandler(filters.Regex("^(Sativa|Indika|Hash)$"), typeof)],
            WEIGHT: [MessageHandler(filters.Regex("^(1|2|5)$"), weight)],
            CRYPTO: [
                MessageHandler(filters.Regex("^(Bitcoin|Ethereum)$"), crypto),
            ],
            CHECK: [MessageHandler(filters.Regex("^(1)$"), check_status)],
        },
        fallbacks=[CommandHandler("cancel", cancel)],
    )

    application.add_handler(conv_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()
