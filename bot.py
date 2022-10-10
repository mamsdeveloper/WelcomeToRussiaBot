import re

from telebot import TeleBot
from telebot.types import CallbackQuery, Message, Update

import config
from keyboards import CONFIRM_KEYBOARD, FINALIZE_KEYBOARD, HASCHILD_KEYBOARD, LANGSKILL_KEYBOARD, LANGUAGE_KEYBOARD, MARRIED_KEYBOARD, VISITED_KEYBOARD


bot = TeleBot(config.TOKEN, threaded=False)
bot.remove_webhook()
bot.set_webhook(url=config.WEBHOOK_URL)

temp = {}


def webhook_handler(request_content: str):
    """Process new updates

    Args:
        request (Request): encoded content of flask request
    """

    update = Update.de_json(request_content)
    bot.process_new_updates([update])
    return 'ok', 200


def check_retry(message: Message) -> bool:
    """Check if user did not send any answers

    Args:
        message (Message): incoming message

    Returns:
        bool: True, if user data empty
    """

    if not message.chat.id in temp:
        bot.send_message(
            message.chat.id,
            'If you want to change answers, retry with /start command'
        )
        return True

    return False


def get_application_text(message: Message) -> str:
    application_text = f'New offer: {message.chat.username}\n'
    for field, value in temp[message.chat.id].items():
        application_text += f'{field}: {value}\n'
    
    return application_text


@bot.message_handler(commands=['start'])
def start(message: Message):
    temp[message.chat.id] = {}

    bot.send_message(
        message.chat.id,
        'Hello! I`ll ask you some questions to link with manager'
    )
    bot.send_message(
        message.chat.id,
        'For begging, send you full name:'
    )
    bot.register_next_step_handler(message, name_handler)


def name_handler(message: Message):
    temp[message.chat.id]['Name'] = message.text

    bot.send_message(
        message.chat.id,
        # 'Now, choose your country of current residence'
        'Now, send your phone number:'
    )
    bot.register_next_step_handler(message, phone_handler)


def phone_handler(message: Message):
    temp[message.chat.id]['Phone'] = message.text

    bot.send_message(
        message.chat.id,
        # 'Now, choose your country of current residence'
        'And email address:'
    )
    bot.register_next_step_handler(message, email_handler)


def email_handler(message: Message):
    temp[message.chat.id]['Email'] = message.text

    bot.send_message(
        message.chat.id,
        'Now, specify country of your current residence:'
    )
    bot.register_next_step_handler(message, country_handler)


def country_handler(message: Message):
    temp[message.chat.id]['Country'] = message.text

    bot.send_message(
        message.chat.id,
        'Choose language for conversation with manager',
        reply_markup=LANGUAGE_KEYBOARD
    )


@bot.callback_query_handler(lambda call: call.data.startswith('lang-'))
def language_handler(callback: CallbackQuery):
    bot.answer_callback_query(callback.id, cache_time=10)

    if check_retry(callback.message):
        return

    if 'Language' in temp[callback.message.chat.id]:
        return

    _, language = callback.data.split('-')
    temp[callback.message.chat.id]['Language'] = language

    bot.send_message(
        callback.message.chat.id,
        'Have you ever been to Russia?',
        reply_markup=VISITED_KEYBOARD
    )


@bot.callback_query_handler(lambda call: call.data.startswith('visited-'))
def visited_handler(callback: CallbackQuery):
    bot.answer_callback_query(callback.id, cache_time=10)

    if check_retry(callback.message):
        return

    if 'Visited Russia' in temp[callback.message.chat.id]:
        return

    _, visited = callback.data.split('-')
    temp[callback.message.chat.id]['Visited Russia'] = visited

    bot.send_message(
        callback.message.chat.id,
        'Choose your level of Russian language',
        reply_markup=LANGSKILL_KEYBOARD
    )


@bot.callback_query_handler(lambda call: call.data.startswith('langskill-'))
def langskill_handler(callback: CallbackQuery):
    bot.answer_callback_query(callback.id, cache_time=10)

    if check_retry(callback.message):
        return

    if 'Language level' in temp[callback.message.chat.id]:
        return

    _, langskill = callback.data.split('-')
    temp[callback.message.chat.id]['Language level'] = langskill

    bot.send_message(
        callback.message.chat.id,
        'Are you married?',
        reply_markup=MARRIED_KEYBOARD
    )


@bot.callback_query_handler(lambda call: call.data.startswith('married-'))
def married_handler(callback: CallbackQuery):
    bot.answer_callback_query(callback.id, cache_time=10)

    if check_retry(callback.message):
        return

    if 'Married' in temp[callback.message.chat.id]:
        return

    _, married = callback.data.split('-')
    temp[callback.message.chat.id]['Married'] = married

    bot.send_message(
        callback.message.chat.id,
        'Do you have children?',
        reply_markup=HASCHILD_KEYBOARD
    )


@bot.callback_query_handler(lambda call: call.data.startswith('haschild-'))
def haschild_handler(callback: CallbackQuery):
    bot.answer_callback_query(callback.id, cache_time=10)

    if check_retry(callback.message):
        return

    if 'Has children' in temp[callback.message.chat.id]:
        return

    _, haschild = callback.data.split('-')
    temp[callback.message.chat.id]['Has children'] = haschild

    if haschild == 'Yes':
        bot.send_message(
            callback.message.chat.id,
            'Send the age of children splitted by comma (like "10, 4, 3")'
        )
        bot.register_next_step_handler(callback.message, children_handler)
    else:
        confirm(callback.message)


def children_handler(message: Message):
    text = message.text
    temp[message.chat.id]['Children age'] = text
    confirm(message)
    # CHILDREN_PATTERN = r'^(\d+ *,* *)+$'
    # if re.match(CHILDREN_PATTERN, text):
    # else:
    #     bot.send_message(
    #         message.chat.id,
    #         'Illegal format. Age mast be several digits splitted by comma or single digit. Try again'
    #     )
    #     bot.register_next_step_handler(message, children_handler)


def confirm(message: Message):
    bot.send_message(
        message.chat.id,
        'All done. Check your answers'
    )
    bot.send_message(
        message.chat.id,
        get_application_text(message),
        reply_markup=CONFIRM_KEYBOARD
    )


@bot.callback_query_handler(lambda call: call.data == 'confirm')
def confirm_handler(callback: CallbackQuery):
    bot.answer_callback_query(callback.id, cache_time=10)

    if not temp[callback.message.chat.id]:
        return

    finalize(callback.message, get_application_text(callback.message))


@bot.callback_query_handler(lambda call: call.data == 'discard')
def discard_handler(callback: CallbackQuery):
    bot.answer_callback_query(callback.id, cache_time=10)

    if not temp[callback.message.chat.id]:
        return

    bot.send_message(
        callback.message.chat.id,
        'Answers are discarded. Your can try again with /start command'
    )
    temp[callback.message.chat.id] = {}


def finalize(message: Message, application_text: str):
    temp[message.chat.id] = {}
    bot.send_message(
        message.chat.id,
        'All done. You answers sent to manager. Now you can go to our channel or contact with manager',
        reply_markup=FINALIZE_KEYBOARD
    )

    bot.send_message(config.ADMIN_CHAT_ID, application_text)


if __name__ == '__main__':
    bot.polling(non_stop=True)
