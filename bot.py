
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
from telegram import (ReplyKeyboardMarkup, ReplyKeyboardRemove)
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters,
                          ConversationHandler)

#Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

START, LOCALITY,CITY,PINCODE, STANDARD, BOARD, MEDIUM, SUBJECTS, EMAIL,REQ, END, DYNAMIC_DATA_ENTRY = range(12)
locality=""
city=""
pincode=0
standard=""
board=""
medium=""
subjects=""
email=""
req=""
"""def start(update, context):
	user=update.message.from_user
	logger.info("locality of%s: %s", user.first_name, update.message.text)
	update.message.reply_text(
        'Hi! Welcome to SumRuxBookExchange. We at Sumrux identify people in the same pincode and exchange books.' 
        'We help create a community of readers who are physically proximate to each other.'
        'WhAT is your locality',
        reply_markup=ReplyKeyboardRemove())
	return LOCALITY"""

def start(update, context):
    """Send a message when the command /start is issued."""
    localty =update.message.reply_text( 'Hi! Welcome to SumRuxBookExchange. '
    'Thank you for choosing us to help you'
    'This is a free service by Sumrux for academic books for covid-19 recovery .'
    'Let us know the details of the books you are looking for and the books you have.\n'
    'Please let us know your current locality?')

    return CITY

def city(update, context):
	user=update.message.from_user
	locacity=logger.info("locality of%s: %s", user.first_name, update.message.text)
	update.message.reply_text(
        'What is your city?',
        reply_markup=ReplyKeyboardRemove())

	return PINCODE

def pincode(update, context):
	user=update.message.from_user
	city=logger.info("City of %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
		'Thankyou, you have made it easier for us to find you a match'
		'We do need some more information to help you find a suitable bookmatch.'
		'What is your pincode?',
		reply_markup=ReplyKeyboardRemove())

	return REQ

def req(update, context):
	reply_keyboard = [['Need' , 'Have']]

	user=update.message.from_user
	pincode=logger.info("Pincode of %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
    	'Do you need book or have book?',
    	 reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

	return STANDARD

def standard(update, context):
	user=update.message.from_user
	req=logger.info("Requirement of %s: %s", user.first_name, update.message.text)
	standard=update.message.reply_text(
		'Thankyou for trusting us with your information.'
		'We are on our way to connect you with other readers around you.'
		'Which standard books are you looking for/Have?',
		 reply_markup=ReplyKeyboardRemove())

	return BOARD

def board(update, context):
	user=update.message.from_user
	standard=logger.info("Books of standard %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
		'Almost there. Do you have any specific board in mind(CBS/ICSE etc.)?',
		 reply_markup=ReplyKeyboardRemove())

	return MEDIUM

def medium(update, context):
	reply_keyboard = [['English' , 'Hindi']]

	user=update.message.from_user
	board=logger.info("Books of Board %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
    	'Do you want English Medium or Hindi Medium Books?',
    	 reply_markup=ReplyKeyboardMarkup(reply_keyboard, one_time_keyboard=True))

	return SUBJECTS

def subjects(update, context):
	user=update.message.from_user
	medium=logger.info("Books of Medium %s: %s", user.first_name, update.message.text)
	update.message.reply_text(
		 'One last thing. Which subjects are you looking for?',
		 reply_markup=ReplyKeyboardRemove())

	return EMAIL


def email(update, context):
	user=update.message.from_user
	subjects=logger.info("Books of Subject%s: %s", user.first_name, update.message.text)
	update.message.reply_text(
		'We are glad you are trusting us with your information'
		'If you could give us your email ID, it would help us send you the relevant information'
		'What is your email?', 
		reply_markup=ReplyKeyboardRemove())
		

	return DYNAMIC_DATA_ENTRY


def end(update,context):
	user=update.message.from_user
	email=logger.info("Email of%s: %s", user.first_name,update.message.text)
	update.message.reply_text('I hope we are of help to you. Happy reading!',
		                       reply_markup=ReplyKeyboardRemove())

	return ConversationHandler.END


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
    updater = Updater("1099106816:AAEEfUuB0WKPZ7vieQKk7gbiqGymoGPuFO0", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Add conversation handler with the states INFO, LOCATION, BIO, CLASSNAMES
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],

        states={

 		    #LOCALITY: [MessageHandler(Filters.text, locality)],
            CITY: [MessageHandler(Filters.text, city)],
           

            #PHOTO: [MessageHandler(Filters.photo, photo),
             # CommandHandler('skip', skip_photo)],
            PINCODE: [MessageHandler(Filters.text, pincode)],
              REQ: [MessageHandler(Filters.text, req)],

            STANDARD: [MessageHandler(Filters.text, standard)],

            BOARD: [MessageHandler(Filters.text, board)],
          

            MEDIUM:[MessageHandler(Filters.text, medium)],

            SUBJECTS: [MessageHandler(Filters.text, subjects)],

            EMAIL: [MessageHandler(Filters.text, email)],

			DYNAMIC_DATA_ENTRY:[MessageHandler(Filters.text, dynamic_data_entry)],

            END: [MessageHandler(Filters.text,end)]


        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dynamic_data_entry(locality,city,pincode,standard,board,medium,subjects,email,req)
    dp.add_handler(conv_handler)

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    #    press ctrl c for stopping the bot 
    # SIGTERM or SIGABRT. This should be used most of the time
    # start_polling() is non-blocking and will stop the bot.
    updater.idle()

def dynamic_data_entry(locality,city,pincode,standard,board,medium,subjects,email,req):
	conn=sqlite3.connect('details.db')
	c=conn.cursor()
	c.execute(""" CREATE TABLE INFO (
	locality text, city text, pincode integer,standard text, board text, medium text, subjects text,
	email text, req text)   
	""")
	Locality = locality
	City= city
	Pincode= pincode
	Standard= standard
	Board= board
	Medium= medium
	Subjects= subjects
	Email= email
	Req= req
	c.execute("INSERT INTO INFO (locality, city, pincode, standard, board, medium, subjects, email, req) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",(Locality, City, Pincode, Standard, Board, Medium, Subjects, Email, Req))
	conn.commit()
	c.execute("Select * from INFO")
	items=c.fetchall()
	c.close
	conn.close
	return ConversationHandler.END

if __name__ == '__main__':
    main()