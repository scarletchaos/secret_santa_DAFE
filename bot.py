from telebot import types, TeleBot
from enum import Enum
import pandas as pd
import json


class State(Enum):
    nothing = 0
    name = 1
    room_number = 2
    course = 3
    description = 4
    check_correct = 5
    ready = 6
    
clients = pd.DataFrame(columns=["Chat_id", "State", "Is_member", "Ready", "Name", "Room_number", "Course_number", "Description"])
# clients.loc[ len(clients.index) ] = [0, Sta"test", None, None]


API_TOKEN = '7030787887:AAGCfXK8RJ2gFOD7uoTPkhs1Jd1z4AgLmYg'
bot = TeleBot(API_TOKEN, parse_mode=None) # You can set parse_mode by default. HTML or MARKDOWN

welcome_txt = "Привет, я телеграм бот для игры Тайный Санта. Познакомимся?"
notification_txt = "Привет, напоминаем о нашей игре. Ты уже приготовил подарок?"

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    global clients, welcome_txt

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1 = types.KeyboardButton("/registration")
    markup.add(button1)

    bot.reply_to(message, welcome_txt, reply_markup = markup)

    chat_id = message.chat.id
    find = clients["Chat_id"] == chat_id
    if find.any():
        i = clients[ find ].index[0]
        clients.loc[i]["State"] = State.nothing
        return
    clients.loc[ len(clients.index) ] = [chat_id, State.nothing, False, False, None, None, None, None]
        
    
@bot.message_handler(commands=["registration"])
def registration(message):
    global clients

    chat_id = message.chat.id
    find = clients["Chat_id"] == chat_id
    i = clients[ find ].index[0]

    bot.reply_to(message, "Введи свое настоящее ФИО:")
    clients.loc[i, "State"] = State.name
    
@bot.message_handler()
def get_answer(message):
    global clients
    chat_id = message.chat.id
    find = clients["Chat_id"] == chat_id
    if find.any():
        i = clients[ find ].index[0]
        waiting = clients.loc[i, "State"]
    else:
        return
    
    match(waiting):
        case State.name:
            clients.loc[i, "Name"] = message.text

            bot.reply_to(message, "Введи номер своей комнаты:")
            clients.loc[i, "State"] = State.room_number
            return
        
        case State.room_number:
            try:
                ans = message.text
                num = int(ans)
            except:
                bot.reply_to(message, "Некорректный формат данных, попробуй еще")
                return
            clients.loc[i, "Room_number"] = num
            bot.reply_to(message, "Укажи абсолютный номер курса, на котором ты учишься")
            clients.loc[i, "State"] = State.course
            return
        
        case State.course:
            try:
                ans = message.text
                num = int(ans)
            except:
                bot.reply_to(message, "Некорректный формат данных, попробуй еще")
                return
            clients.loc[i, "Course_number"] = num
            bot.reply_to(message, "Введи свои пожелания по поводу подарка.")
            clients.loc[i, "State"] = State.description
        
        case State.description:
            clients.loc[i, "Description"] = message.text
            clients.loc[i, "State"] = State.check_correct

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            button1 = types.KeyboardButton("Да")
            button2 = types.KeyboardButton("Нет")
            markup.add(button1, button2)

            bot.reply_to(
                message,
                f"Проверь, все ли правильно в анкете?\nИмя: {clients['Name'][i]}\nКомната: {clients['Room_number'][i]}\nПожелания: {clients['Description'][i]}\nПодтверждая свою анкету, ты подтверждаешь свое участие в игре.",
                reply_markup = markup
                )
            return
        
        case State.check_correct:
            if message.text == "Да":
                bot.reply_to(message, "Принято! Готовь подарки, а мы вернемся позже с напоминанием.")   
                clients.loc[i, "State"] = State.nothing
                clients.loc[i, "Is_member"] = True
            else:
                bot.reply_to(message, "Давай попробуем заново. Введи свое настоящее имя:")
                clients.loc[i, "State"] = State.name
            return

        case State.ready:
            if message.text == "Да":
                bot.reply_to(message, "Круто! Отключаем уведомления, приятной игры!")
                clients.loc[i, "Ready"] = True
                clients.loc[i, "State"] = State.nothing
                print("srthsrthsrthsrt")
                return
            bot.reply_to(message, "Хорошо, мы напомним позже, но поторопись! Праздник уже близко!")
            clients.loc[i, "State"] = State.nothing

# def send_notification(ids: list[int]):
#     global clients
#     for i in clients[ ["Chat_id"]:
#         bot.send_message(i, )

clients.loc[0] = [1852576017, State.nothing, False, False, "Alex", 134, 1, "Хочу это"]
# clients.loc[0] = [822396067, State.nothing, False, "Сехир", 618, "Может это?"]

def send_notification():
    global clients, notification_txt
    for i in clients[ clients["Ready"] == False ]["Chat_id"]:
        find = clients["Chat_id"] == i
        index = clients[ find ].index[0]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button1 = types.KeyboardButton("Да")
        button2 = types.KeyboardButton("Нет")
        markup.add(button1, button2)

        bot.send_message(i, notification_txt, reply_markup=markup)

        clients.loc[index, "State"] = State.ready

# def send_notification(ids: list[int]):
#     global clients, notification_txt
#     for i in ids:
#         bot.send_message(i, notification_txt)
#         clients.loc[i]["State"] = State.ready


send_notification()
bot.infinity_polling(timeout=15)

print(clients)