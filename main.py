import telebot
import menu
import settings
import random
import time
import sqlite3
import requests
import json
from datetime import datetime


def bot():
    bot = telebot.TeleBot(settings.BotToken, threaded=False)

    @bot.message_handler(commands=['start'])
    def start_handler(message):
        if message.text[7:] == '':
            who_invited = 0
        else:
            who_invited = message.text[7:]
        conn = sqlite3.connect("base.sqlite")
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM info')
        row = cursor.fetchone()

        newuser = 0
        newid = 0

        while row is not None:
            if row[1] == str(message.chat.id):
                newuser = 0
            else:
                newuser = 1
            newid += 1
            row = cursor.fetchone()

        if newuser == 1:
            cursor.execute("INSERT INTO info (id, userid, date, who_invited, his_referral_code) VALUES ('{}','{}','{}','{}','{}')".format(newid, message.chat.id, str(datetime.now()), who_invited, message.chat.id))
            conn.commit()

        cursor.close()
        conn.close()
        bot.send_message(message.chat.id, text='❕Здравствуйте, '+str(message.from_user.first_name)+'\n❕Ваш id - '+str(message.chat.id)+' \n❗️Для продолжения подтвердите свой возраст.\n❗️Нажимая на кнопку « Мне есть 18 », вы подтверждаете наличие 18 лет.', reply_markup=menu.ageChoice)

    @bot.callback_query_handler(func=lambda call: True)
    def callback_inline(call):
        chat_id = call.message.chat.id
        message_id = call.message.message_id

        if call.data == 'Мне есть 18 лет':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='Выберите вашу страну',
                                  reply_markup=menu.countries)

        if call.data == 'Мне нет 18 лет':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='Извините, но вы не достигли возраста совершеннолетия (18 лет).\n'
                                       'Если вы ошиблись с выбором, вы можете вернуться назад, нажав на кнопку « 🔙BACK »''',
                                  reply_markup=menu.back)

        if call.data == '🔙BACK':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='❗️Нажимая на кнопку « Мне есть 18 », вы подтверждаете, что вам уже исполнилось 18 лет.',
                                  reply_markup=menu.ageChoice)

        if call.data in 'cities_ru cities_ua cities_kz':
            country = None
            if call.data == 'cities_ru':
                country = 'Россия'
            if call.data == 'cities_ua':
                country = 'Украина'
            if call.data == 'cities_kz':
                country = 'Казахстан'

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='✅Ваша страна {}\n Выберите город'.format(country),
                                  reply_markup=menu.multi_menu(call.data, type_obj=None))

        if call.data[:2:] in '🇷🇺 🇺🇦 🇰🇿':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='✅Ваша страна {}\n✅Ваш город - {}'.format(call.data[:2:],
                                                                                 call.data[3:]),
                                  reply_markup=menu.menu_num2)

        if call.data == 'back_to_menu':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='Вы вернулись в меню',
                                  reply_markup=menu.menu_num2)

        if call.data == 'referral_system':
            conn = sqlite3.connect("base.sqlite")
            cursor = conn.cursor()
            referred_users = cursor.execute('''SELECT * FROM info WHERE who_invited = {}'''.format(chat_id)).fetchall()
            number_of_purchases = cursor.execute('''SELECT * FROM purchase_information WHERE referral_code = {} AND sum != 0'''.format(chat_id)).fetchall()
            amount_of_income = 0
            cursor.execute('''SELECT * FROM purchase_information WHERE referral_code = {} AND sum != 0'''.format(chat_id))
            row = cursor.fetchall()

            for i in row:
                amount_of_income += int(i[3])

            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=settings.referral_system.format(len(referred_users),
                                                                       len(number_of_purchases),
                                                                       amount_of_income/(settings.percent_referral_system/100),
                                                                       login=settings.login_bot,
                                                                       referral_code=chat_id),
                                  reply_markup=menu.referral_menu)

        if call.data == 'snus_catalog':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='❕ Вы перешил в каталог снюса\n❕ Выберите марку снюса',
                                  reply_markup=menu.multi_menu(call.data, type_obj=None))

        if call.data[:1:] == '💠':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='❕ Каталог {}'.format(call.data[1:]),
                                  reply_markup=menu.multi_menu(call.data[1:], 'type2'))

        if call.data == 'Вернуться к выбору страны и города':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='Выберите вашу страну',
                                  reply_markup=menu.countries)

        if call.data == 'Вернуться к выбору снюса':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='❕ Вы перешли в каталог снюса\n❕ Выберите марку снюса',
                                  reply_markup=menu.multi_menu('snus_catalog', type_obj=None))

        if call.data[:1:] == '💎':
            random_code = random.randint(111111, 999999)
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text=settings.cb.format(call.data[1:],
                                                          random_code,
                                                          call.data[-6:-3]),
                                  reply_markup=menu.check_buy)
            conn = sqlite3.connect("base.sqlite")
            cursor = conn.cursor()
            cursor.execute(f'''INSERT INTO check_payment VALUES("{call.message.chat.id}",
                                                                "{None}",
                                                                "{call.data[-6:-3]}",
                                                                "{random_code}",
                                                                "{None}")''')
            conn.commit()
            cursor.close()
            conn.close()

        if call.data == 'check_payment':
            session = requests.Session()
            session.headers['authorization'] = 'Bearer ' + settings.QIWI_TOKEN
            parameters = {'rows': '3'}
            h = session.get(
                'https://edge.qiwi.com/payment-history/v1/persons/{}/payments'.format(settings.QIWI_ACCOUNT),
                params=parameters)
            req = json.loads(h.text)

            conn = sqlite3.connect('base.sqlite')
            cursor = conn.cursor()
            result = cursor.execute(f'SELECT * FROM check_payment WHERE user_id = {call.message.chat.id}').fetchone()

            for i in range(len(req['data'])):
                if req['data'][i]['comment'] == result[3]:
                    if req['data'][i]['sum']['amount'] == result[2]:
                        bot.send_message(settings.IdAdmin, 'Хозяин вы богаты!!! Прошла оплата {} руб'.format(result[2]))

                        cursor.execute(f'''INSERT INTO purchase_information VALUES("{call.message.chat.id}",
                                                                                    "{datetime.now()}",
                                                                                    "{result[4]}",
                                                                                    "{result[2]}")''')
                        conn.cursor()

                        cursor.execute(f'DELETE FROM check_payment WHERE user_id = {call.message.chat.id}')
                        conn.cursor()

                        bot.send_message(chat_id, '❕ Оплата не найдена\n'
                                                  '❕ Повторите повторную проверку через пару минут\n'
                                                  '❕ Для продолжения нажмите "Подтвердить"',
                                         reply_markup=menu.ch)

            bot.send_message(chat_id, '❕ Оплата не найдена\n'
                                      '❕ Повторите повторную проверку через пару минут\n'
                                      '❕ Для продолжения нажмите "Подтвердить"',
                             reply_markup=menu.ch)
        
        if call.data == 'cancel_payment':
            conn = sqlite3.connect("base.sqlite")
            cursor = conn.cursor()
            cursor.execute("DELETE FROM check_payment WHERE user_id = {}".format(call.message.chat.id))
            conn.commit()
            cursor.close()
            conn.close()
            bot.edit_message_text(
                chat_id=chat_id,
                message_id=message_id,
                text='❕ Вы перешли в каталог снюса\n❕ Выберите марку снюса',
                reply_markup=menu.multi_menu('snus_catalog', type_obj=None)
            )

        if call.data == 'Подтвердить':
            bot.delete_message(chat_id, message_id)

        if call.data == 'exit_admin_menu':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='Вы вышли',
                                  reply_markup=menu.ageChoice)

        if call.data == 'full_info':
            if chat_id == settings.IdAdmin:
                conn = sqlite3.connect('base.sqlite')
                cursor = conn.cursor()
                cursor.execute('SELECT * FROM info')
                row = cursor.fetchone()

                current_time = str(datetime.now())

                amount_user_all = 0
                amount_user_day = 0
                amount_user_hour = 0

                while row is not None:
                    amount_user_all = row[0]
                    if row[2][:-15:] == current_time[:-15:]:
                        amount_user_day += 1
                    if row[2][:-13:] == current_time[:-13:]:
                        amount_user_hour += 1

                    row = cursor.fetchone()

                number_of_purchases = cursor.execute('SELECT * FROM purchase_information').fetchall()

                bot.edit_message_text(chat_id=chat_id,
                                      message_id=message_id,
                                      text='Уникальных пользователей за все время - {}\n'
                                           'Уникальных пользователей за день - {}\n'
                                           'Уникальных пользователей за час - {}\n\n'
                                           'Покупок совершенно - {}'.format(amount_user_all,
                                                                            amount_user_day,
                                                                            amount_user_hour,
                                                                            len(number_of_purchases)),
                                      reply_markup=menu.back_to_admin_menu)

                cursor.close()
                conn.close()

        if call.data == 'user_info':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='Введите id пользователя в виде id:ИД_ПОЛЬЗОВАТЕЛЯ\nПример: id:00000000',
                                  reply_markup=menu.back_to_admin_menu)

        if call.data == 'back_to_admin_menu':
            bot.edit_message_text(chat_id=chat_id,
                                  message_id=message_id,
                                  text='Вы вошли в админское меню',
                                  reply_markup=menu.adminMenu)

        if call.data == 'top_user':
            if chat_id == settings.IdAdmin:
                bot.delete_message(chat_id=chat_id,
                                   message_id=message_id)

                conn = sqlite3.connect("base.sqlite")
                cursor = conn.cursor()

                info = cursor.execute('''SELECT * FROM info WHERE who_invited != 0''').fetchall()
                list_ref = []

                for i in info:
                    list_ref.append(i[3])

                sort_list_ref = list(set(list_ref))

                for i in range(len(sort_list_ref)):
                    if i > 4:
                        break
                    amount = 0
                    if i > 10:
                        break
                    for i2 in list_ref:
                        if i2 == sort_list_ref[i]:
                            amount += 1

                    bot.send_message(chat_id=chat_id,
                                     text='🏅{} место - {} - кол-во приглашенных - {}'.format(i+1,
                                                                                             sort_list_ref[i],
                                                                                             amount))

                bot.send_message(chat_id=chat_id,
                                 text='❕Топ пользователей выведен',
                                 reply_markup=menu.back_to_admin_menu)

    @bot.message_handler(commands=['admin'])
    def send_mes(message):
        if message.chat.id == settings.IdAdmin:
            bot.send_message(message.chat.id, 'Вы вошли в админское меню',
                             reply_markup=menu.adminMenu)

    @bot.message_handler(content_types=['text'])
    def send_message(message):
        if message.chat.id == settings.IdAdmin:
            try:
                if 'id:' in message.text:
                    id_user = None
                    who_invite = None
                    date_of_registration = None
                    number_of_invited_users = None
                    referrals_purchase_amount = 0

                    conn = sqlite3.connect("base.sqlite")
                    cursor = conn.cursor()

                    info = cursor.execute('''SELECT * FROM info WHERE userid = {}'''.format(message.text[3:])).fetchone()
                    id_user = info[1]
                    date_of_registration = info[2]
                    who_invite = info[3]

                    info = cursor.execute('''SELECT * FROM purchase_information WHERE referral_code = {}'''.format(
                        message.text[3:])).fetchall()
                    number_of_invited_users = len(info)

                    info = cursor.execute(
                        '''SELECT * FROM purchase_information WHERE referral_code = {} AND sum != 0'''.format(
                            message.text[3:]))
                    for i in info:
                        referrals_purchase_amount += int(i[3])

                    bot.send_message(chat_id=message.chat.id,
                                     text='❕Информаци о пользователе\n\n'
                                          '❕Ид пользователя - {}\n'
                                          '❕Реферальный код пользователя - {}\n'
                                          '❕Его пригласил - {}\n'
                                          '❕Дата первого входа - {}\n'
                                          '❕Кол-во его рефералов - {}\n'
                                          '❕Количество покупок его рефералов - {}\n'.format(id_user,
                                                                                            id_user,
                                                                                            who_invite,
                                                                                            date_of_registration,
                                                                                            number_of_invited_users,
                                                                                            referrals_purchase_amount),
                                     reply_markup=menu.back_to_admin_menu)
            except:
                bot.send_message(chat_id=message.chat.id,
                                 text='❌Некорректный id пользователя, либо его не существует',
                                 reply_markup=menu.back_to_admin_menu)

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(e)
            time.sleep(15)


bot()
