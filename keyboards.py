from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


LANGUAGE_KEYBOARD = InlineKeyboardMarkup(row_width=1)
LANGUAGE_KEYBOARD.add(
    InlineKeyboardButton('Russian', callback_data='lang-Russian'),
    InlineKeyboardButton('English', callback_data='lang-English'),
    InlineKeyboardButton('French', callback_data='lang-French'),
    InlineKeyboardButton('German', callback_data='lang-German'),
)

VISITED_KEYBOARD = InlineKeyboardMarkup(row_width=2)
VISITED_KEYBOARD.add(
    InlineKeyboardButton('Yes', callback_data='visited-Yes'),
    InlineKeyboardButton('No', callback_data='visited-No'),
)

LANGSKILL_KEYBOARD = InlineKeyboardMarkup(row_width=1)
LANGSKILL_KEYBOARD.add(
    InlineKeyboardButton('Zero', callback_data='langskill-Zero'),
    InlineKeyboardButton('Begging', callback_data='langskill-Begging'),
    InlineKeyboardButton('Average', callback_data='langskill-Average'),
    InlineKeyboardButton('Fluent', callback_data='langskill-Fluent'),
)

MARRIED_KEYBOARD = InlineKeyboardMarkup(row_width=2)
MARRIED_KEYBOARD.add(
    InlineKeyboardButton('Yes', callback_data='married-Yes'),
    InlineKeyboardButton('No', callback_data='married-No'),
)

HASCHILD_KEYBOARD = InlineKeyboardMarkup(row_width=2)
HASCHILD_KEYBOARD.add(
    InlineKeyboardButton('Yes', callback_data='haschild-Yes'),
    InlineKeyboardButton('No', callback_data='haschild-No'),
)

CONFIRM_KEYBOARD = InlineKeyboardMarkup(row_width=2)
CONFIRM_KEYBOARD.add(
    InlineKeyboardButton('Confirm', callback_data='confirm'),
    InlineKeyboardButton('Discard', callback_data='discard'),
)

FINALIZE_KEYBOARD = InlineKeyboardMarkup(row_width=1)
FINALIZE_KEYBOARD.add(
    InlineKeyboardButton('Go to channel', url='https://t.me/immigrationtorussia'),
    InlineKeyboardButton('Chat with manager', url='https://t.me/Z_SergeyShevchenko')
)