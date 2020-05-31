
"""
First, a few callback functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import sqlite3
import logging
import os
import telebot #Telegram BOT API

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, DictPersistence, BasePersistence, Dispatcher)
from telegram import User, TelegramObject
from dotenv import load_dotenv
load_dotenv()

from db import DB


# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)


START, LOCALITY, CITY, PINCODE, REQ, STANDARD, BOARD, MEDIUM, SUBJECTS, CONTACT, EMAIL, DETAILS, CONFIRM, END = range(
    14)



def start(update, context):
    """Send a message when the command /start is issued."""
    name = message.from_user.first_name
    print (name)
    update.message.reply_text(
'Hi!' message 
'Welcome to SumRuxBookExchange.'
'Thank you for choosing us to help you.'
'This is a free service by Sumrux for academic books for covid-19 recovery.'
'Let us know the details of the books you are looking for and the books you have.'

'Please let us know your current City?'
		)
    return CITY


def city(update, context):
    user = update.message.from_user
    context.user_data['City'] = update.message.text
    logger.info("City of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'What is your locality?',
        reply_markup=ReplyKeyboardRemove())

    return PINCODE


def pincode(update, context):
    user = update.message.from_user
    context.user_data['Locality'] = update.message.text
    logger.info("Locality of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        '''
Thankyou, you have made it easier for us to find you a match
We do need some more information to help you find a suitable bookmatch.

What is your pincode?''',
        reply_markup=ReplyKeyboardRemove())

    return REQ


def req(update, context):
    reply_keyboard = [['Need', 'Have']]
    context.user_data['Pincode'] = update.message.text
    user = update.message.from_user
    logger.info("Pincode of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Do you need book or have book?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return STANDARD


def standard(update, context):
    user = update.message.from_user
    context.user_data['Req'] = update.message.text
    logger.info("Requirement of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        '''
Thankyou for trusting us with your information.
We are on our way to connect you with other readers around you.
Which standard books are you looking for/Have?''',
        reply_markup=ReplyKeyboardRemove())

    return BOARD


def board(update, context):
    user = update.message.from_user
    context.user_data['Standard'] = update.message.text
    logger.info("Books of standard %s: %s",
                user.first_name, update.message.text)
    update.message.reply_text(
        'Almost there. Do you have any specific board in mind (CBS/ICSE etc.)?',
        reply_markup=ReplyKeyboardRemove())

    return MEDIUM


def medium(update, context):
    reply_keyboard = [['English', 'Hindi']]
    context.user_data['Board'] = update.message.text
    user = update.message.from_user
    logger.info("Books of Board %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'Do you want English Medium or Hindi Medium Books?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

    return SUBJECTS


def subjects(update, context):
    user = update.message.from_user
    context.user_data['Medium'] = update.message.text
    logger.info("Books of Medium %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        'One last thing. Which subjects are you looking for?',
        reply_markup=ReplyKeyboardRemove())

    return CONTACT


def contact(update, context):
    user = update.message.from_user
    context.user_data['Subjects'] = update.message.text
    logger.info("Books of Subjects for %s: %s",
                user.first_name, update.message.text)
    update.message.reply_text(
        'Could you please share with us your phone number?',
        reply_markup=ReplyKeyboardRemove())

    return EMAIL


def email(update, context):
    user = update.message.from_user
    context.user_data['Contact'] = update.message.text
    logger.info("Contact Number of %s: %s",
                user.first_name, update.message.text)
    update.message.reply_text(
        '''
We are glad you are trusting us with your information
If you could give us your email ID, it would help us send you the relevant information
What is your email?
''',
        reply_markup=ReplyKeyboardRemove())

    return CONFIRM


def confirm(update, context):
    reply_keyboard = [['Yes', 'No']]
    context.user_data['Email'] = update.message.text
    user = update.message.from_user
    logger.info("Details of %s: %s", user.first_name, update.message.text)
    update.message.reply_text(
        f'''
Thankyou for all your help. Please press yes to confirm your details.
City : {context.user_data["City"]}, 
Locality : {context.user_data["Locality"]}, 
Pincode : {context.user_data["Pincode"]}, 
Requirement : {context.user_data["Req"]}, 
Standard : {context.user_data["Standard"]}, 
Board : {context.user_data["Board"]}, 
Medium : {context.user_data["Medium"]}, 
Subjects : {context.user_data["Subjects"]}, 
Contact : {context.user_data["Contact"]}, 
Email : {context.user_data["Email"]}
''',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    return END


def end(update, context):
    user = update.message.from_user
    context.user_data['Confirm'] = update.message.text
    if update.message.text == "Yes":
        logger.info("Confirmation of%s: %s",
                    user.first_name, update.message.text)
        update.message.reply_text(
            'I hope we are of help to you. Happy reading!', reply_markup=ReplyKeyboardRemove())
        db = DB()
        db.setup()
        db.add_item(**context.user_data)
        return ConversationHandler.END

    else:
        return START


def cancel(update, context):
    user = update.message.from_user
    logger.info("User %s ended the conversation.", user.first_name)
    update.message.reply_text('Bye! I hope we can talk again some day.',
                              reply_markup=ReplyKeyboardRemove())

    return ConversationHandler.END


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    # will Create the Updater and pass it our bot's token.
    # Make sure to set use_context=True to use the new context based callbacks

    updater = Updater(
        os.getenv("TELEGRAM_TOKEN",""), use_context=True)

    bot = telebot.Telebot(os.getenv("TELEGRAM_TOKEN"))
    @bot.message_handler(commands=['info'])



    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states INFO, LOCATION, BIO, CLASSNAMES
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

            CITY: [MessageHandler(Filters.text, city)],

            PINCODE: [MessageHandler(Filters.text, pincode)],

            REQ: [MessageHandler(Filters.text, req)],

            STANDARD: [MessageHandler(Filters.text, standard)],

            BOARD: [MessageHandler(Filters.text, board)],


            MEDIUM: [MessageHandler(Filters.text, medium)],

            SUBJECTS: [MessageHandler(Filters.text, subjects)],

            CONTACT: [MessageHandler(Filters.text, contact)],

            EMAIL: [MessageHandler(Filters.text, email)],


            CONFIRM: [MessageHandler(Filters.text, confirm)],

            END: [MessageHandler(Filters.text, end)]

        },

        fallbacks=[CommandHandler('cancel', cancel)], )

    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    #    press ctrl c for stopping the bot
    # SIGTERM or SIGABRT. This should be used most of the time
    # start_polling() is non-blocking and will stop the bot.
    updater.idle()
    # d.add_item(CITY, PINCODE, STANDARD, BOARD, MEDIUM, SUBJECTS, NUMBER, EMAIL, REQ, CONFIRM)
    # print(CITY, PINCODE, STANDARD, BOARD, MEDIUM,
    #       SUBJECTS, NUMBER, EMAIL, REQ, CONFIRM)

    # d.get_items()


if __name__ == '__main__':
    main()
