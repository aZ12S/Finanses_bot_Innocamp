import telebot
import sqlite3
conn = sqlite3.connect('example.db', check_same_thread=False)
cursor = conn.cursor()
rows = cursor.fetchall()
cursor.execute('''
CREATE TABLE IF NOT EXISTS users(id INTEGER PRIMARY KEY,
tg_id TEXT NOT NULL,
name TEXT NOT NULL,
budget INTEGER NOT NULL,
balance INTEGER NOT NULL,
goal INTEGER NOT NULL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS report(id INTEGER PRIMARY KEY,
report TEXT NOT NULL,
tg_id TEXT NOT NULL)
''')
cursor.execute('SELECT * FROM users')
conn.commit()
bot = telebot.TeleBot("6869572988:AAHjcqc_bkUImZXAANopvCgTNj43ZLTNVJQ")
@bot.message_handler(commands=["start"])
def start(message):
    user_id = message.from_user.id
    user_name =message.from_user.username
    bot.send_photo(message.chat.id, 'https://vvmvd.ru/uploads/posts/2024-06/1717669066_8234723987482472389473298473489234111111111113333333.jpg')
    bot.send_message(message.chat.id, 'Привет это бот для твоих финансов! \n'
                                        'Введи команду /addincome [сумма] для добавления дохода \n'
                                         'Введи команду /addexpense [сумма] для добавления расхода \n'
                                         'Введи команду /balance для просмотра баланса \n'
                                         'Введи команду /setbudget сумма для установки месячного бюджета \n'
                                         'Введи команду /budget для проверки текущего состояния бюджета \n'
                                         'Введи команду /report[период] для получения отчёта об использованных командах  \n'
                                         'Введи комаенду /categories для управления категориями расходов (добавление , '
                                         'удаление, просмотр \n'
                                         'Введи команду /setgoal [сумма] для установки финансовой цели \n'
                                         'Введи команду /goals для просмотра прогресса по финансовым целям \n')

    cursor.execute(f'''
        INSERT INTO users(tg_id,name,balance,budget,goal) VALUES ({user_id}, '{user_name}', 0,0, 0)
''')
    conn.commit()


@bot.message_handler(commands=["addincome"])
def answer(message):

    #plus = message.text.split(maxsplit=1)[1]
    # cursor.execute(f'''
    # SELECT * from users WHERE tg_id = '{message.from_user.id}'
    # ''')
    # conn.commit()
    cursor.execute(f'''
    UPDATE users SET balance = balance + {message.text.split()[1]} WHERE tg_id = '{message.from_user.id}'
    ''')
    conn.commit()
    cursor.execute('''
    SELECT * FROM users''')
    rows = cursor.fetchall()
    bot.send_message(message.chat.id,f'Ваш баланс теперь  : {rows[0][4]}')
    cursor.execute(f'''
    INSERT INTO report(report, tg_id) VALUES ('/addincome' ,'{message.from_user.id}')
    ''')
    conn.commit()
@bot.message_handler(commands=["balance"])
def balance(message):
    cursor.execute(f'''
    SELECT * from users WHERE tg_id = '{message.from_user.id}'
    ''')
    conn.commit()
    rows = cursor.fetchall()
    bot.send_message(message.chat.id,f'Ваш баланс равен:\n {rows[0][4]}')
    cursor.execute(f'''
    INSERT INTO report(report, tg_id) VALUES ('/balance', '{message.from_user.id}')
    ''')
    conn.commit()
@bot.message_handler(commands=["setgoal"])
def setgoal(message):
    cursor.execute(f'''
    UPDATE users SET goal = {message.text.split()[1]} WHERE tg_id = '{message.from_user.id}'
    ''')
    cursor.execute(f'''
    INSERT INTO report(report, tg_id) VALUES ('/setgoal', '{message.from_user.id}')
    ''')
    conn.commit()
    bot.send_message(message.chat.id,'Ваша цель на месяц установлена!')
@bot.message_handler(commands=["setbudget"])
def set_budget(message):
    bot.send_message(message.chat.id,f'Месячный бюджет составляет: {message.text.split()[1]}')
    cursor.execute(f'''
     UPDATE users SET budget = {message.text.split()[1]}  WHERE tg_id = '{message.from_user.id}' ''')
    conn.commit()
    cursor.execute(f'''
    INSERT INTO report(report, tg_id) VALUES ('/setbudget', '{message.from_user.id}')
    ''')
    conn.commit()

@bot.message_handler(commands=["budget"])
def get_budget(message):

    cursor.execute(f'''
    SELECT budget FROM users WHERE tg_id = '{message.from_user.id}' 
    ''')
    a = cursor.fetchall()
    conn.commit()
    bot.send_message(message.chat.id,f'Ваш бюджет состовляет : {a[0][0]}')
    cursor.execute(f'''
    INSERT INTO report(report, tg_id) VALUES ('/budget', '{message.from_user.id}')
    ''')
    conn.commit()
@bot.message_handler(commands=["addexpense"])
def answer(message):
    cursor.execute(f'''
    UPDATE users SET balance = balance - {message.text.split()[1]} WHERE tg_id = '{message.from_user.id}'
    ''')
    conn.commit()
    cursor.execute('''
    SELECT * FROM users''')
    rows = cursor.fetchall()
    bot.send_message(message.chat.id,f'Ваш баланс теперь  : {rows[0][4]}')
    cursor.execute(f'''
    INSERT INTO report(report, tg_id) VALUES ('/addexpense', '{message.from_user.id}')
    ''')
    conn.commit()
@bot.message_handler(commands=["categories"])
def categories(message):
    bot.send_message(message.chat.id,'Вы можете потратить свой баланнс на:\n'
                                     'Медицину\n'
                                     'Развлечения\n'
                                     'Еду\n'
                                     'и т.д.')
    cursor.execute(f'''
    INSERT INTO report(report, tg_id) VALUES ('/categories','{message.from_user.id}')
    ''')
    conn.commit()
@bot.message_handler(commands=["goals"])
def goals(message):
    cursor.execute(f'''
    SELECT balance, goal FROM users WHERE tg_id = '{message.from_user.id}'
    ''')
    conn.commit()
    d = cursor.fetchall()
    print(d)
    bot.send_message(message.chat.id,f'До вашей цели осталось: {d[0][1] - d[0][0]}')
    cursor.execute(f'''
    INSERT INTO report(report, tg_id) VALUES ('/goals', '{message.from_user.id}')
    ''')
    conn.commit()

@bot.message_handler(commands=["report"])
def report(message):
    cursor.execute(f'''
    SELECT * FROM report WHERE tg_id = '{message.from_user.id}' 
''')
    conn.commit()
    s = cursor.fetchall()
    ans = ''
    for i in s:
        ans += i[1] + '\n'
    bot.send_message(message.chat.id,f'Вот ваши действия за всё время : "{ans}"')
    cursor.execute(f'''
    INSERT INTO report(report, tg_id) VALUES ('/report', '{message.from_user.id}')
    ''')
    conn.commit()
bot.polling(non_stop=True)