from telegram.ext import Updater
updater = Updater(token="475944334:AAGzxbLNdkxdTh5DKIvv-YOvyu_BUhwvFN0")
dispatcher = updater.dispatcher
import logging
#enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)


def start(bot, update):
    update.message.reply_text('Hi! use /set <second> to set a timer')
from telegram.ext import CommandHandler
start_handler = CommandHandler("start", start)
dispatcher.add_handler(start_handler)
#start the bot
updater.start_polling()

#send an alarm message
def alarm(bot, job):
    bot.send_message(job.context, text='Beep!')

def set_timer(bot, update, args, job_queue, chat_data):
    #add a job to the queue
    chat_id = update.message.chat_id
    try:
        #arg[0] should contain the time for the timer in seconds
        due = int(args[0])
        if due < 0:
            update.message.reply_text('Sorry! we can not go back to future')
            return
        #add job to queue
        job = job_queue.run_once(alarm, due, context=chat_id)
        chat_data['job'] = job

        update.message.reply_text('Timer successfully set!')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /set <second>')
from telegram.ext import CommandHandler
set_timer_handler = CommandHandler("set", set_timer,
                               pass_args=True,
                               pass_job_queue=True,
                               pass_chat_data=True)
dispatcher.add_handler(set_timer_handler)

def unset(bot, update, chat_data):
    #remove the job if user changed the plan
    if 'job' not in chat_data:
        update.message.reply_text('no active timer')
        return

    job = chat_data['job']
    job.schedule_removal()
    del chat_data['job']

    update.message.reply_text('Timer successfully unset!')
from telegram.ext import CommandHandler
unset_handler = CommandHandler("unset", unset, pass_chat_data=True)
dispatcher.add_handler(unset_handler)

def error(bot, update, error):
    #log errors caused by updates
    logger.warning('Update "%s" caused error "%s"', update, error)
dispatcher.add_error_handler(error)
