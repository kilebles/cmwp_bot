from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

main_menu_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Узнать идеал своего офиса', callback_data='ideal')],
        [InlineKeyboardButton(text='Что сотркудники хотят видеть в офисе', callback_data='staff_wants')],
        [InlineKeyboardButton(text='Узнать стоимость организации офиса', 
                              url='https://www.cmwp.ru/cwiq/reviews/obzory-po-segmentam-rynka/ofisnaya-nedvizhimost/?utm_source=tg&utm_medium=bot_pds&utm_campaign=dvizhenie')],
        [InlineKeyboardButton(text='Чем мы можем быть полезны', callback_data='how_helpful')],
        [InlineKeyboardButton(text='Контакты для связи', callback_data='contacts')]
    ]
)

staff_wants_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Назад ↩', callback_data='back')]
    ]
)

how_helpful_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Обсудить мой проект', callback_data='discuss_project')],
        [InlineKeyboardButton(text='Назад ↩', callback_data='back')]
    ]
)

contacts_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Написать письмо', url='https://mail.google.com/mail/?view=cm&to=tgbot-pds@cmwp.ru')],
        [InlineKeyboardButton(text='Связаться в Telegram', url='https://t.me/yeelisey')],
        [InlineKeyboardButton(text='Назад ↩', callback_data='back')]
    ]
)

get_plan_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text='Получить план', callback_data='get_plan')],
        [InlineKeyboardButton(text='Назад ↩', callback_data='back')]
    ]
)


def make_keyboard(options: list[str], prefix: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=opt, callback_data=f"{prefix}:{opt}")] for opt in options]
        
    )