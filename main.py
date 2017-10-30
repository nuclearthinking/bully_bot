import logging
import random

from ruamel.yaml.main import YAML
from telegram.bot import Bot
from telegram.ext.commandhandler import CommandHandler
from telegram.ext.filters import Filters
from telegram.ext.messagehandler import MessageHandler
from telegram.ext.updater import Updater
from telegram.update import Update

logger = logging.getLogger(__name__)

TOKEN = YAML().load(open('config.yml').read()).get('token')
messages = [
    'пойди нахуй',
    'умри',
    'опять какую то хуйню несёшь, заебал',
    'когда ты заткнёшься уже?',
    'завали ебало своё, пидор',
    'нахуй иди',
    'ты такой тупой, пиздец просто'
]

ENABLED = False

admins = ['nuclearthinking', 'SoberFest']


def message_from_chat(bot: Bot, update: Update):
    if ENABLED:
        if update.effective_user.username in ['zmbpnd'] and (random.randint(0, 100) < 7):
            bot.send_message(
                chat_id=update.effective_chat.id,
                text=random.choice(messages),
                reply_to_message_id=update.effective_message.message_id
            )


def stop_handler(bot: Bot, update: Update):
    global ENABLED
    ENABLED = False
    bot.send_message(update.effective_chat.id, text='Выключен')


def start_handler(bot: Bot, update: Update):
    global ENABLED
    ENABLED = True
    bot.send_message(update.effective_chat.id, text='Включен')


def status_handler(bot: Bot, update: Update):
    message = 'Сейчас бот включен' if ENABLED else 'Сейчас бот выключен'
    bot.send_message(update.effective_chat.id, message)


def error(bot, update, error):
    logger.error(error)


message_handler = MessageHandler(
    callback=message_from_chat,
    filters=Filters.all
)
start_command = CommandHandler(
    command='start',
    callback=start_handler,
    filters=Filters.chat(username=admins)
)
stop_command = CommandHandler(
    command='stop',
    callback=stop_handler,
    filters=Filters.chat(username=admins)
)
status_command = CommandHandler(
    command='status',
    callback=status_handler,
    filters=Filters.chat(username=admins)
)


def main():
    handlers = [start_command, stop_command, status_command, message_handler]
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    [dp.add_handler(handler) for handler in handlers]
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
