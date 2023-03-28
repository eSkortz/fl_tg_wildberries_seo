import telebot
from telebot import types
import io
import csv
import Callback_main as wb_main
import Callback_accounts as wb_account
import WBClient as wb_client
import WBPartner as wb_partner
import WBMpstat as wb_mpstat

bot = telebot.TeleBot('')

bot_users = []
wb_accounts = []
users_session = []
admins = [588339594, 377372793]

def init():
    global bot_users
    global wb_accounts
    bot_users = []
    with io.open('bot_users.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            bot_users.append(int(row[0]))
    wb_accounts = []
    with io.open('wb_accounts.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            account = {
                'name': row[0],
                'WBToken': row[1],
                'x_supplier_id': row[2],
                'auth': row[3].split(';')
            }
            for i in range(len(account['auth'])):
                account['auth'][i] = int(account['auth'][i])
            wb_accounts.append(account)
init()

def init_session():
    global users_session
    users_session = []
    with io.open('users_session.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            session = {
                'id' : row[0],
                'name' : row[1]
            }
            users_session.append(session)
init_session()

#Изменение WBToken
def WbbWBT(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            session_name = users_session[i]['name']
    for i in range(len(wb_accounts)):
        if wb_accounts[i]['name'] == session_name:
            account_name = wb_accounts[i]['name']
    newWBToken = message.text
    AddList = []
    with io.open('wb_accounts.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != account_name:
                AddList.append(row)
            else:
                string = []
                string.append(row[0])
                string.append(newWBToken)
                string.append(row[2])
                string.append(row[3])
                AddList.append(string)
    with io.open('wb_accounts.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    init()
    choice(message)
#Изменение x_supplier_id
def WbbXSP(message):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == message.chat.id:
            session_name = users_session[i]['name']
    for i in range(len(wb_accounts)):
        if wb_accounts[i]['name'] == session_name:
            account_name = wb_accounts[i]['name']
    newx_supplier_id = message.text
    AddList = []
    with io.open('wb_accounts.csv', 'r', encoding='utf-8') as csv_file:
        file_reader = csv.reader(csv_file, delimiter="|", quoting=csv.QUOTE_NONE)
        for row in file_reader:
            if row[0] != account_name:
                AddList.append(row)
            else:
                string = []
                string.append(row[0])
                string.append(row[1])
                string.append(newx_supplier_id)
                string.append(row[3])
                AddList.append(string)
    with io.open('wb_accounts.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(AddList)):
            writer.writerow(AddList[i])
    init()
    choice(message)

def change_account(id, name):
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == id:
            users_session[i]['name'] = name
    with io.open('users_session.csv', 'w', encoding='utf-8', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter='|', quoting=csv.QUOTE_NONE)
        for i in range(len(users_session)):
            AddList = []
            AddList.append(users_session[i]['id'])
            AddList.append(users_session[i]['name'])
            writer.writerow(AddList)

create_account = []
def create_account_1(message):
    msg = bot.send_message(message.chat.id, 'Введите имя аккаунта: ')
    bot.register_next_step_handler(msg, create_account_4)
def create_account_4(message):
    global create_account
    create_account.append(message.text)
    msg = bot.send_message(message.chat.id, 'Введите WBToken: ')
    bot.register_next_step_handler(msg, create_account_5)
def create_account_5(message):
    global create_account
    create_account.append(message.text)
    msg = bot.send_message(message.chat.id, 'Введите x-supplier-id: ')
    bot.register_next_step_handler(msg, write_creating_account_to_file)
def write_creating_account_to_file(message):
    name = create_account[0]
    create_account.append(message.text)
    create_account.append(message.chat.id)
    with io.open('wb_accounts.csv', mode= 'a', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = '|', lineterminator="\n")
        file_writer.writerow(create_account)
    init()
    markup_inline = types.InlineKeyboardMarkup()
    four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
    markup_inline.add(four)
    bot.send_message(message.chat.id, f'✅ Аккаунт {name} успешно создан', reply_markup=markup_inline)

def adm_1(message):
    if message.chat.id in admins:
        msg = bot.send_message(message.chat.id, 'Введите нового пользователя: ')
        bot.register_next_step_handler(msg, adm_2)
    else:
        bot.send_message(message.chat.id, f'🤗 Извините, кажется у вас нет доступа к админ панели')
def adm_2(message):
    new_account_id = []
    new_account_id.append(message.text)
    with io.open('bot_users.csv', mode= 'a', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = '|', lineterminator="\n")
        file_writer.writerow(new_account_id)
    init()
    with io.open('users_session.csv', mode= 'a', encoding='utf-8') as w_file:
        file_writer = csv.writer(w_file, delimiter = '|', lineterminator="\n")
        string = []
        string.append(message.text)
        string.append('Не выбран')
        for i in range(0,5):
            string.append(0)
        file_writer.writerow(string)
    markup_inline = types.InlineKeyboardMarkup()
    four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
    markup_inline.add(four)
    bot.send_message(message.chat.id, f'✅ Аккаунт {message.text} успешно создан', reply_markup=markup_inline)

#Поиск рекламных ставок по ключевому слову
def advertising_by_keyword(message):
    keyword = message.text
    jsn = wb_client.GetByKeyword(keyword)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        try:
            CpmList = []
            for i in range(len(jsn['adverts'])):
                CpmList.append(int(jsn['adverts'][i]['cpm']))
            markup_inline = types.InlineKeyboardMarkup()
            markup_list = []
            for i in range(len(CpmList)):
                markup_list.append(types.InlineKeyboardButton(text=f'{i+1} : {CpmList[i]}', callback_data='none'))
            if len(markup_list) >= 10:
                for i in range(0, 10):
                    markup_inline.add(markup_list[i])
            else:
                for i in range(len(markup_list)):
                    markup_inline.add(markup_list[i])
            four = types.InlineKeyboardButton(text='🔙 Вернуться в меню рекламных ставок', callback_data='Advertising rates')
            markup_inline.add(four)
            bot.send_message(message.chat.id, f'🗝 Рекламные ставки по заданному ключевому слову ({keyword})', reply_markup=markup_inline)
        except Exception:
            markup_inline = types.InlineKeyboardMarkup()
            four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
            markup_inline.add(four)
            bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
# Поиск рекламных ставок по ключевому слову
def advertising_by_good(message):
    url = message.text
    jsn = wb_client.GetByGood(url)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        try:
            CpmList = []
            for i in range(len(jsn)):
                CpmList.append(int(jsn[i]['cpm']))
            markup_inline = types.InlineKeyboardMarkup()
            markup_list = []
            for i in range(len(CpmList)):
                markup_list.append(types.InlineKeyboardButton(text=f'{i + 1} : {CpmList[i]}', callback_data='none'))
            if len(markup_list) >= 10:
                for i in range(0, 10):
                    markup_inline.add(markup_list[i])
            else:
                for i in range(len(markup_list)):
                    markup_inline.add(markup_list[i])
            four = types.InlineKeyboardButton(text='🔙 Вернуться в меню рекламных ставок', callback_data='Advertising rates')
            markup_inline.add(four)
            bot.send_message(message.chat.id, f'🧸 Рекламные ставки по заданному товару ({url})', reply_markup=markup_inline)
        except Exception:
            markup_inline = types.InlineKeyboardMarkup()
            four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
            markup_inline.add(four)
            bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
# Поиск рекламных ставок по ключевому слову
def advertising_by_category(message):
    url = message.text
    jsn = wb_client.GetByCategory(url)
    if jsn == 'error':
        markup_inline = types.InlineKeyboardMarkup()
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(four)
        bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)
    else:
        try:
            CpmList = []
            for i in range(len(jsn['adverts'])):
                CpmList.append(int(jsn['adverts'][i]['cpm']))
            markup_inline = types.InlineKeyboardMarkup()
            markup_list = []
            for i in range(len(CpmList)):
                markup_list.append(types.InlineKeyboardButton(text=f'{i + 1} : {CpmList[i]}', callback_data='none'))
            if len(markup_list) >= 10:
                for i in range(0, 10):
                    markup_inline.add(markup_list[i])
            else:
                for i in range(len(markup_list)):
                    markup_inline.add(markup_list[i])
            four = types.InlineKeyboardButton(text='🔙 Вернуться в меню рекламных ставок', callback_data='Advertising rates')
            markup_inline.add(four)
            bot.send_message(message.chat.id, f'🛍 Рекламные ставки по заданной категории ({url})', reply_markup=markup_inline)
        except Exception:
            markup_inline = types.InlineKeyboardMarkup()
            four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
            markup_inline.add(four)
            bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса', reply_markup=markup_inline)


def output_mpstat(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=1)

@bot.message_handler(commands=['recipient'])
def main(message):
    bot.send_message(message.chat.id, f'Ваш recipient-id: {message.chat.id}')

@bot.message_handler(content_types=['text','audio','document','photo'])
@bot.message_handler(commands=['start'])
def choice(message):
    init()
    init_session()
    if message.chat.id in bot_users:
        for i in range(len(users_session)):
            if int(users_session[i]['id']) == message.chat.id:
                session_name = users_session[i]['name']
        for i in range(len(wb_accounts)):
            if wb_accounts[i]['name'] == session_name:
                account_name = wb_accounts[i]['name']
        wb_main.main(message, admins, account_name)
    else:
        bot.send_message(message.chat.id, '🤗 Извините, кажется у вас нет доступа к боту, получите ваш id с помощью /recipient и попросите администратора проекта добавить вас в список пользователей')

@bot.callback_query_handler(func=lambda call: True)
def callback(call):
    init()
    init_session()
    for i in range(len(users_session)):
        if int(users_session[i]['id']) == call.message.chat.id:
            session_name = users_session[i]['name']
    for i in range(len(wb_accounts)):
        if wb_accounts[i]['name'] == session_name:
            account_name = wb_accounts[i]['name']
            WBToken = wb_accounts[i]['WBToken']
            x_supplier_id = wb_accounts[i]['x_supplier_id']

    def output_wbpartner(message):
        jsn = wb_partner.get_tags_by_search(message, WBToken, x_supplier_id)
        if jsn == 'error':
            markup_inline = types.InlineKeyboardMarkup()
            four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
            markup_inline.add(four)
            bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                             reply_markup=markup_inline)
        else:
            markup_inline = types.InlineKeyboardMarkup(row_width=1)
            markup_list = []
            for i in range(len(jsn['data']['list'])):
                markup_list.append(
                    types.InlineKeyboardButton(text=f'{i + 1} : {jsn["data"]["list"][i]["text"]} : {jsn["data"]["list"][i]["requestCount"]}', callback_data='button'))
            for i in range(len(markup_list)):
                markup_inline.add(markup_list[i])
            four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
            markup_inline.add(four)
            bot.send_message(message.chat.id, f'📊 Подбор запросов (WB) по тегу "{message.text}"\nПозиция запроса : Запрос : Частота введения за месяц на Wildberries',
                             reply_markup=markup_inline)

    def output_mpstat(message):
        jsn = wb_mpstat.get_tags_search(message.text)
        if jsn == 'error':
            markup_inline = types.InlineKeyboardMarkup()
            four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
            markup_inline.add(four)
            bot.send_message(message.chat.id, '❌ Кажется произошла ошибка при выполнении запроса',
                             reply_markup=markup_inline)
        else:
            markup_inline = types.InlineKeyboardMarkup(row_width=1)
            markup_list = []
            for i in range(len(jsn['data'])):
                markup_list.append(
                    types.InlineKeyboardButton(text=f'{i + 1} : {jsn["data"][i]["word"]} : {jsn["data"][i]["wb_count"]}',
                                               callback_data='button'))
            for i in range(len(markup_list)):
                markup_inline.add(markup_list[i])
            four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
            markup_inline.add(four)
            bot.send_message(message.chat.id, f'📯 Подбор запросов (MP) по тегу "{message.text}"\nПозиция запроса : Запрос : Частота введения за месяц на Wildberries',
                             reply_markup=markup_inline)

    calling_data = call.data.split('|')

    if calling_data[0] == 'main':
        wb_main.main(call.message, admins, account_name)

    if calling_data[0] == 'Advertising rates':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        one = types.InlineKeyboardButton(text='🗝 Поиск рекламных ставок по ключевому слову', callback_data='Advertising by keyword')
        two = types.InlineKeyboardButton(text='🧸 Поиск рекламных ставок по товару', callback_data='Advertising by good')
        three = types.InlineKeyboardButton(text='🛍 Поиск рекламных ставок по категории', callback_data='Advertising by category')
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(one, two, three, four)
        bot.send_message(call.message.chat.id, f'💸 Это рекламные ставки, здесь вы можете найти рекламные ставки по ключевым словам, товару и категории', reply_markup=markup_inline)
    if calling_data[0] == 'Advertising by keyword':
        msg = bot.send_message(call.message.chat.id, '🗝 Введите ключевое слово: ')
        bot.register_next_step_handler(msg, advertising_by_keyword)
    if calling_data[0] == 'Advertising by good':
        msg = bot.send_message(call.message.chat.id, '🧸 Введите ссылку на товар: ')
        bot.register_next_step_handler(msg, advertising_by_good)
    if calling_data[0] == 'Advertising by category':
        msg = bot.send_message(call.message.chat.id, '🛍 Введите ссылку на категорию: ')
        bot.register_next_step_handler(msg, advertising_by_category)

    if calling_data[0] == 'Tags_wbpartner':
        msg = bot.send_message(call.message.chat.id, 'Введите поисковой запрос: ')
        bot.register_next_step_handler(msg, output_wbpartner)
    if calling_data[0] == 'Tags_mpstat':
        msg = bot.send_message(call.message.chat.id, 'Введите поисковой запрос: ')
        bot.register_next_step_handler(msg, output_mpstat)

    if calling_data[0] == 'Changing account menu':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        five = types.InlineKeyboardButton(text='📕 Изменить WBToken', callback_data='Change WBToken')
        six = types.InlineKeyboardButton(text='📗 Изменить x_supplier_id', callback_data='Change x_supplier_id')
        seven = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(five, six, seven)
        bot.send_message(call.message.chat.id,
                         f'✏ Это изменение аккаунта, здесь вы можете поменять уникальные идентификаторы аккаунта и rec-id менеджера поставок',
                         reply_markup=markup_inline)
    if calling_data[0] == 'Change WBToken':
        wb_account.change_wb_token(call.message, WBToken)
    if calling_data[0] == 'Change WBT':
        msg = bot.send_message(call.message.chat.id, '📕 Введите новый WBToken: ')
        bot.register_next_step_handler(msg, WbbWBT)
    if calling_data[0] == 'Change x_supplier_id':
        wb_account.change_sup_id(call.message, x_supplier_id)
    if calling_data[0] == 'Change x_sup':
        msg = bot.send_message(call.message.chat.id, '📗 Введите новый x_supplier_id: ')
        bot.register_next_step_handler(msg, WbbXSP)

    if calling_data[0] == 'Account menu':
        markup_inline = types.InlineKeyboardMarkup(row_width=1)
        one = types.InlineKeyboardButton(text='♻️ Изменить аккаунт', callback_data='Change account')
        two = types.InlineKeyboardButton(text='✏️ Добавить аккаунт', callback_data='Add account')
        three = types.InlineKeyboardButton(text='🗑 Удалить аккаунт', callback_data='Delete account')
        four = types.InlineKeyboardButton(text='🔙 Вернуться в главное меню', callback_data='main')
        markup_inline.add(one, two, three, four)
        bot.send_message(call.message.chat.id, f'⚙ Это управление аккаунтами, здесь вы можете настроить свои аккаунты wb-partner', reply_markup=markup_inline)
    if calling_data[0] == 'Change account':
        wb_account.change_account(call.message, wb_accounts)
    if calling_data[0] == 'Changing account':
        id = calling_data[1]
        change_account(call.message.chat.id, id)
        wb_account.changing_account(call.message, id)
    if calling_data[0] == 'Add account':
        create_account_1(call.message)
    if calling_data[0] == 'Delete account':
        wb_account.delete_account(call.message, wb_accounts)
    if calling_data[0] == 'Deliting account':
        name = calling_data[1]
        wb_account.deliting_account(call.message, name)
        init()
        init_session()

    if calling_data[0] == 'manual':
        markup_inline = types.InlineKeyboardMarkup()
        one = types.InlineKeyboardButton(text='🔙 Назад в главное меню', callback_data='main')
        markup_inline.add(one)
        bot.send_document(call.message.chat.id, open(r'manual.pdf', 'rb'), reply_markup=markup_inline)

bot.polling(none_stop=True, timeout=0)
