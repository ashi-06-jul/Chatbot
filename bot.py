
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
import re

from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler, DictPersistence, BasePersistence, Dispatcher)
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
    update.message.reply_text(
        '''
Hi! Welcome to SumRuxBookExchange.
Thank you for choosing us to help you.
This is a free service by Sumrux for academic books for covid-19 recovery.
Let us know the details of the books you are looking for and the books you have.

Please let us know your current City?
		''')
    return CITY


def city(update, context):
    context.user_data['City'] = update.message.text
    user = update.message.from_user
    regex=r"^[a-z A-Z]+$"
    if(re.search(regex,context.user_data['City'])):
        logger.info("City of %s: %s",user.first_name, update.message.text)
        update.message.reply_text(
        'What is your locality?',
        reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text('Please enter valid City Name',reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['City'] = update.message.text
        return CITY

    return PINCODE


def pincode(update, context):
    context.user_data['Locality'] = update.message.text
    user = update.message.from_user
    regex=r"^[a-z A-Z]+$"
    if(re.search(regex,context.user_data['Locality'])):
        logger.info("Locality of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
        '''
Thankyou, you have made it easier for us to find you a match
We do need some more information to help you find a suitable bookmatch.

What is your pincode?''',
        reply_markup=ReplyKeyboardRemove())
    else:
         update.message.reply_text('Please enter valid Locality Name',reply_markup=ReplyKeyboardRemove())
         user = update.message.from_user
         context.user_data['Locality'] = update.message.text
         return PINCODE
    return REQ


def req(update, context): 
    context.user_data['Pincode'] = update.message.text
    user = update.message.from_user
    regex=r"[0-9]{6}"
    if(re.search(regex, context.user_data['Pincode'])):
        logger.info("Pincode of %s: %s", user.first_name, update.message.text)
        reply_keyboard = [['Need', 'Have']]
        update.message.reply_text(
        'Do you need book or have book?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    else:
        update.message.reply_text('Please enter a valid Pincode',reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['Pincode'] = update.message.text
        return REQ
        
    return STANDARD


def standard(update, context):
    context.user_data['Req'] = update.message.text
    user = update.message.from_user
    if(context.user_data['Req']=="Need"):
        logger.info("Requirement of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
        '''
Thankyou for trusting us with your information.
We are on our way to connect you with other readers around you.
Which standard books are you looking for/Have, Enter standard in digits from 1 to 12?''',
        reply_markup=ReplyKeyboardRemove())
    elif(context.user_data['Req']=="Have"):
        logger.info("Requirement of %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
        '''
Thankyou for trusting us with your information.
We are on our way to connect you with other readers around you.
Which standard books are you looking for/Have, Enter standard in digits from 1 to 12?''',
        reply_markup=ReplyKeyboardRemove())
    else:
        reply_keyboard = [['Need', 'Have']]
        update.message.reply_text('Please enter that you Need/Have books',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        user = update.message.from_user
        context.user_data['Req'] = update.message.text
        return STANDARD

    return BOARD


def board(update, context):   
    context.user_data['Standard'] = update.message.text 
    user = update.message.from_user
    regex=r"^([1-9]|1[012])$"
    if(re.search(regex,context.user_data['Standard'])):
        logger.info("Books of standard %s: %s", user.first_name, update.message.text)
        reply_keyboard = [['CBSE', 'ICSE', 'UP']]
        update.message.reply_text('Almost there. Do you have any specific board in mind (CBSE/ICSE/UP etc.)?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
        
    else:
        update.message.reply_text('Please enter valid Standard from 1 to 12',reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['Standard'] = update.message.text
        return BOARD

    return MEDIUM


def medium(update, context):
    context.user_data['Board'] = update.message.text
    user = update.message.from_user
    if(context.user_data['Board']=="CBSE"):
        logger.info("Books of Board %s: %s", user.first_name, update.message.text)
        reply_keyboard = [['English', 'Hindi']]
        update.message.reply_text(
        'Do you want English Medium or Hindi Medium Books?',
        reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    elif (context.user_data['Board']=="UP"):
            logger.info("Books of Board %s: %s", user.first_name, update.message.text)
            reply_keyboard = [['English', 'Hindi']]
            update.message.reply_text(
            'Do you want English Medium or Hindi Medium Books?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    elif (context.user_data['Board']=="ICSE"):
            logger.info("Books of Board %s: %s", user.first_name, update.message.text)
            reply_keyboard = [['English', 'Hindi']]
            update.message.reply_text(
            'Do you want English Medium or Hindi Medium Books?',
            reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))
    else:
        update.message.reply_text('Please enter valid Board',reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['Board'] = update.message.text
        return MEDIUM
    return SUBJECTS


def subjects(update, context):
    context.user_data['Medium'] = update.message.text
    user = update.message.from_user
    if(context.user_data['Medium']=="English"):
        logger.info("Books of Medium %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
        'One last thing. Which subjects are you looking for?',
        reply_markup=ReplyKeyboardRemove())
    elif(context.user_data['Medium']=="Hindi"):
        logger.info("Books of Medium %s: %s", user.first_name, update.message.text)
        update.message.reply_text(
        'One last thing. Which subjects are you looking for?',
        reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text('Please enter valid Medium',reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['Medium'] = update.message.text
        return SUBJECTS

        

    return CONTACT


def contact(update, context):
    context.user_data['Subjects'] = update.message.text
    user = update.message.from_user
    regex=r"^[a-z A-Z]+$"
    if(re.search(regex,context.user_data['Subjects'])):
        logger.info("Books of Subjects for %s: %s",
                user.first_name, update.message.text)
        update.message.reply_text(
        'Could you please share with us your phone number?',
        reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text('Please enter valid Subjects',reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['Subjects'] = update.message.text
        return CONTACT
     

    return EMAIL


def email(update, context):
    context.user_data['Contact'] = update.message.text
    user = update.message.from_user
    regex=r"[6789]\d{9}$"
    if(re.search(regex,context.user_data['Contact'])):
        logger.info("Contact Number of %s: %s",
                user.first_name, update.message.text)
        update.message.reply_text(
        '''
We are glad you are trusting us with your information
If you could give us your email ID, it would help us send you the relevant information
What is your email?
''',
        reply_markup=ReplyKeyboardRemove())
    else:
        update.message.reply_text('Please enter valid Standard',reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['Contact'] = update.message.text
        return EMAIL

    return CONFIRM


def confirm(update, context):    
    regex = r'^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'
    context.user_data['Email'] = update.message.text
    if(re.search(regex,context.user_data['Email'])):
        user = update.message.from_user
        logger.info("Details of %s: %s", user.first_name, update.message.text)
        reply_keyboard = [['Yes', 'No']]
        update.message.reply_text(
        f'''
Thankyou for all /your help. Please press yes to confirm your details.
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
    else:
        update.message.reply_text('Please enter a valid Email Id',reply_markup=ReplyKeyboardRemove())
        user = update.message.from_user
        context.user_data['Email'] = update.message.text
        return CONFIRM
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

    elif(update.message.text == "No"):
         update.message.reply_text(
            'Please enter /start for entering details again', reply_markup=ReplyKeyboardRemove())
         return START
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
