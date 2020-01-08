from telebot import types
import sqlite3


# Меню
def multi_menu(obj, type_obj):
    conn = sqlite3.connect("base.sqlite")
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM {}'.format(obj))
    row = cursor.fetchone()

    if type_obj == 'type2':
        menu = types.InlineKeyboardMarkup(row_width=1)
    else:
        menu = types.InlineKeyboardMarkup(row_width=3)

    buttons = []

    while row is not None:
        buttons.append(types.InlineKeyboardButton(text=row[0], callback_data=row[0]))
        row = cursor.fetchone()

    try:
        for i in range(int(len(buttons))):
            menu.add(buttons[0], buttons[1], buttons[2])

            del buttons[2]
            del buttons[1]
            del buttons[0]
    except IndexError:
        if len(buttons) == 2:
            menu.add(buttons[0], buttons[1])
        if len(buttons) == 1:
            menu.add(buttons[0])

    menu.add(types.InlineKeyboardButton(text='Вернуться к выбору страны и города',
                                        callback_data='Вернуться к выбору страны и города'))

    if type_obj == 'type2':
        menu.add(types.InlineKeyboardButton(text='Вернуться к выбору снюса',
                                            callback_data='Вернуться к выбору снюса'))

    del buttons

    return menu


# Меню после выбора города
menu_num2 = types.InlineKeyboardMarkup(row_width=2)
menu_num2_btn = types.InlineKeyboardButton(text='Каталог', callback_data='snus_catalog')
menu_num2_btn_2 = types.InlineKeyboardButton(text='Реферальная система', callback_data='referral_system')
menu_num2.add(menu_num2_btn, menu_num2_btn_2)

# Реферальное меню
referral_menu = types.InlineKeyboardMarkup(row_width=2)
referral_menu_btn = types.InlineKeyboardButton(text='Назад в меню', callback_data='back_to_menu')
referral_menu.add(referral_menu_btn)

# Проверить оплату & отменить покупку   чекает оплату киви
check_buy = types.InlineKeyboardMarkup(row_width=1)
check_buy_btn = types.InlineKeyboardButton(text='🔄 Проверить оплату', callback_data='check_payment')
check_buy_btn2 = types.InlineKeyboardButton(text='❌ Отменить заказ', callback_data='cancel_payment')
check_buy.add(check_buy_btn, check_buy_btn2)

# Подтвердить
ch = types.InlineKeyboardMarkup()
ch.add(types.InlineKeyboardButton(text='Подтвердить', callback_data='Подтвердить'))

# Перейги к каталогу
go_to_catalog = types.InlineKeyboardMarkup(row_width=1)
go_to_catalog.add(types.InlineKeyboardButton(text='Перейти к каталогу', callback_data='snus_catalog'))
go_to_catalog.add(types.InlineKeyboardButton(text='Вернуться к выбору страны и города',
                                             callback_data='Вернуться к выбору страны и города'))

# Вырор возраста
ageChoice = types.InlineKeyboardMarkup(row_width=2)
ageChoiceBTN = types.InlineKeyboardButton(text='Мне есть 18 лет', callback_data='Мне есть 18 лет')
ageChoiceBTN2 = types.InlineKeyboardButton(text='Мне нет 18 лет', callback_data='Мне нет 18 лет')
ageChoice.add(ageChoiceBTN, ageChoiceBTN2)

# Кнопка назад
back = types.InlineKeyboardMarkup()
back_btn = types.InlineKeyboardButton(text='🔙BACK', callback_data='🔙BACK')
back.add(back_btn)

# Выбор страны
countries = types.InlineKeyboardMarkup(row_width=1)
countriesBTN = types.InlineKeyboardButton(text='🇷🇺 Россия', callback_data='cities_ru')
countriesBTN2 = types.InlineKeyboardButton(text='🇺🇦 Украина', callback_data='cities_ua')
countriesBTN3 = types.InlineKeyboardButton(text='🇰🇿 Казахстан', callback_data='cities_kz')
countries.add(countriesBTN, countriesBTN2, countriesBTN3)

# Админ меню
adminMenu = types.InlineKeyboardMarkup(row_width=1)
adminMenu.add(types.InlineKeyboardButton(text='Полная информация',
                                         callback_data='full_info')),
adminMenu.add(types.InlineKeyboardButton(text='Информация о пользователе',
                                         callback_data='user_info')),
adminMenu.add(types.InlineKeyboardButton(text='Топ 5 пользователей по приглашениям',
                                         callback_data='top_user')),
adminMenu.add(types.InlineKeyboardButton(text='Выйти из админского меню',
                                         callback_data='exit_admin_menu'))

# Обратно в админ меню
back_to_admin_menu = types.InlineKeyboardMarkup(row_width=3)
back_to_admin_menu.add(types.InlineKeyboardButton(text='Обратно в админ меню', callback_data='back_to_admin_menu'))

