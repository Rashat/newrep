from datetime import datetime
from logging import getLogger

from telegram import Update
from telegram import Bot
from telegram import InlineKeyboardMarkup
from telegram import InlineKeyboardButton
from telegram.ext import Updater
from telegram.ext import MessageHandler
from telegram.ext import CallbackContext
from telegram.ext import CommandHandler
from telegram.ext import CallbackQueryHandler
from telegram.ext import Filters


from Bot_on_server.config import TG_TOKEN
from Bot_on_server.currency_parser import DOLLAR, EURO, PETROL
#from Bot_on_server.utils import logger_factory



logger = getLogger(__name__)

#debug_requests = logger_factory(logger=logger)


def debug_request(f):
    """Декоратор для отладки событий от телеграма"""
    def inner(*args, **kwargs):
        try:
            logger.info(f'Обращение в функцию {f.__name__}')
            return f(*args, **kwargs)
        except Exception:
            logger.exception(f'Ошибка в обработчике {f.__name__}')
            raise
    return inner


CALLBACK_BUTTON1_LEFT = 'callback_button1_left'
CALLBACK_BUTTON2_RIGHT = 'callback_button2_right'
CALLBACK_BUTTON3_MORE = 'callback_button3_more'
CALLBACK_BUTTON4_BACK = 'callback_button4_back'
CALLBACK_BUTTON5_TIME = 'callback_button5_time'
CALLBACK_BUTTON6_PRICE = 'callback_button6_price'
CALLBACK_BUTTON7_PRICE = 'callback_button7_price'
CALLBACK_BUTTON8_PRICE = 'callback_button8_price'
CALLBACK_BUTTON9_CLEAR = 'callback_button9_clear'


TITLES = {
CALLBACK_BUTTON1_LEFT: 'Новое сообщение ✉',
CALLBACK_BUTTON2_RIGHT: 'Отредактировать ✒',
CALLBACK_BUTTON3_MORE:  'Ещё ▶',
CALLBACK_BUTTON4_BACK : 'Назад ◀',
CALLBACK_BUTTON5_TIME: 'Время ⏰',
CALLBACK_BUTTON6_PRICE: 'Курс доллара 💲',
CALLBACK_BUTTON7_PRICE: 'Курс евро 💴',
CALLBACK_BUTTON8_PRICE: 'Курс нефти ⛽',
CALLBACK_BUTTON9_CLEAR: 'Очистить сообщения💨',
}


@debug_request
def get_base_inline_keyboard():
    """Базовая клавиатура"""
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(TITLES[CALLBACK_BUTTON1_LEFT], callback_data=CALLBACK_BUTTON1_LEFT),
                InlineKeyboardButton(TITLES[CALLBACK_BUTTON2_RIGHT], callback_data=CALLBACK_BUTTON2_RIGHT),
            ],
            [
                InlineKeyboardButton(TITLES[CALLBACK_BUTTON3_MORE], callback_data=CALLBACK_BUTTON3_MORE),
                InlineKeyboardButton(TITLES[CALLBACK_BUTTON9_CLEAR], callback_data=CALLBACK_BUTTON9_CLEAR),
            ]
        ],
    )
    return keyboard


@debug_request
def get_keyboard2():
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(TITLES[CALLBACK_BUTTON5_TIME], callback_data=CALLBACK_BUTTON5_TIME),
            ],
            [
                InlineKeyboardButton(TITLES[CALLBACK_BUTTON6_PRICE], callback_data=CALLBACK_BUTTON6_PRICE),
                InlineKeyboardButton(TITLES[CALLBACK_BUTTON7_PRICE], callback_data=CALLBACK_BUTTON7_PRICE),
                InlineKeyboardButton(TITLES[CALLBACK_BUTTON8_PRICE], callback_data=CALLBACK_BUTTON8_PRICE),
            ],
            [
                InlineKeyboardButton(TITLES[CALLBACK_BUTTON4_BACK], callback_data=CALLBACK_BUTTON4_BACK),
            ],
        ],
    )
    return keyboard


@debug_request
def keyboard_callback_handler(update: Update, callback: CallbackContext, chat_data=None, **kwargs):
    """Обработка всех кнопок со всех клавиавтур"""
    query = update.callback_query
    data = query.data
    current_time = datetime.now().strftime('%H:%M:%S')

    current_text = update.effective_message.text
    if data == CALLBACK_BUTTON1_LEFT:
        query.edit_message_text(
            text=current_text,
        )
        query.message.reply_text(
            text=f"Новое сообщение\n\n{current_time}",
            reply_markup=get_base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON2_RIGHT:
        query.edit_message_text(
            text="Успешно отредактировано в {}".format(current_time),
            reply_markup=get_base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON3_MORE:
        query.edit_message_text(
            text=current_text,
            reply_markup=get_keyboard2()
        )
    elif data == CALLBACK_BUTTON4_BACK:
        query.edit_message_text(
            text=current_text,
            reply_markup=get_base_inline_keyboard(),
        )
    elif data == CALLBACK_BUTTON5_TIME:
        query.edit_message_text(
            text='Точное время {}'.format(current_time),
            reply_markup=get_keyboard2(),
        )
    elif data == CALLBACK_BUTTON6_PRICE:
        query.edit_message_text(
            text='Курс доллара на сегодня {}руб'.format(DOLLAR),
            reply_markup=get_keyboard2(),
        )
    elif data == CALLBACK_BUTTON7_PRICE:
        query.edit_message_text(
            text="Курс евро на сегодня {}руб".format(EURO),
            reply_markup=get_keyboard2(),
        )
    elif data == CALLBACK_BUTTON8_PRICE:
        query.edit_message_text(
            text="Курс нефти  {}руб".format(EURO),
            reply_markup=get_keyboard2(),
        )
    elif data == CALLBACK_BUTTON9_CLEAR:
        query.edit_message_text(
            text="Сообщения удалены!",
            reply_markup=get_keyboard2(),
        )


@debug_request
def echo(update: Update, callback: CallbackContext):
    text = update.message.text

    text = f'Приветствую {update.effective_user.first_name} \n\n Ваше сообщение - {text}'
    update.message.reply_text(
        text,
        reply_markup=get_base_inline_keyboard(),
    )


@debug_request
def do_help(update: Update, callback: CallbackContext):
    update.message.reply_text(
        text='Зис из бест хелп эвер!!!(нет)',
    )


@debug_request
def show_time(update: Update, callback: CallbackContext):
    current_time = datetime.now().strftime('%H:%M:%S')
    text = f'Текущее время \n\n {current_time}'
    update.message.reply_text(text,)


@debug_request
def main():
    bot = Bot(
        token=TG_TOKEN,
    )
    updater = Updater(
        bot=bot,
        use_context=True
    )

    updater.dispatcher.add_handler(CommandHandler('help', do_help))
    updater.dispatcher.add_handler(CommandHandler('time', show_time))
    updater.dispatcher.add_handler(MessageHandler(Filters.all, echo))
    updater.dispatcher.add_handler(CallbackQueryHandler(callback=keyboard_callback_handler))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()