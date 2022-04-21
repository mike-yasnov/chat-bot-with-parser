from lib2to3.pytree import type_repr
import tempfile
import telebot
from telebot import types
from telebot import apihelper
from random import randint
from parse import parse_physics

token='5370145350:AAHyNr5kZ0L3Lh-nogb3hFmLO-S6OxphxOA'
bot=telebot.TeleBot(token)

value='' #текущее значение калькулятора
old_value='' #старое значение калькулятора

themes_phys = ["Прямолинейное движение и движение по окружности", 
        "Законы Ньютона, закон всемирного тяготения, закон Гука, сила трения", 
        "Равновесие, закон Паскаля, сила Архимеда, математический и пружинный маятники, механические волны, звук", 
        "Механика", 
        "Изопроцессы, работа в термодинамике, первый закон термодинамики", 
        "МКТ, термодинамика (объяснение явлений; интерпретация результатов опытов)", 
        "Электромагнитная индукция. Оптика"
        ] 

urls_phys = [r"https://examer.ru/ege_po_fizike/teoriya/pryamolinejnoe_dvizhenie_i_dvizhenie_po_okruzhnosti", 
        r"https://examer.ru/ege_po_fizike/teoriya/zakony_nyutona", 
        r"https://examer.ru/ege_po_fizike/teoriya/sila_arhimeda_2017",
        r"https://examer.ru/ege_po_fizike/teoriya/mehanika_nterpretaciya_rezultatov_opytov",
        r"https://examer.ru/ege_po_fizike/teoriya/izoprocessy",
        r"https://examer.ru/ege_po_fizike/teoriya/mkt_termodinamika_izmenenie_fizicheskih",
        r"https://examer.ru/ege_po_fizike/teoriya/elektromagnitnaya_indukciya_optika"
        ]

theme2url_phys = {theme: url for (theme, url) in zip(themes_phys, urls_phys)}
#print(theme2url)

#создадим клавиатуру калькулятора
keyboard =telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton(' ',callback_data='zero'),
             telebot.types.InlineKeyboardButton('с',callback_data='c'),
             telebot.types.InlineKeyboardButton('<=',callback_data='<='),
             telebot.types.InlineKeyboardButton('/',callback_data='/'))

keyboard.row(telebot.types.InlineKeyboardButton('1',callback_data='1'),
             telebot.types.InlineKeyboardButton('2',callback_data='2'),
             telebot.types.InlineKeyboardButton('3',callback_data='3'),
             telebot.types.InlineKeyboardButton('*',callback_data='*'))

keyboard.row(telebot.types.InlineKeyboardButton('4',callback_data='4'),
             telebot.types.InlineKeyboardButton('5',callback_data='5'),
             telebot.types.InlineKeyboardButton('6',callback_data='6'),
             telebot.types.InlineKeyboardButton('-',callback_data='-'))

keyboard.row(telebot.types.InlineKeyboardButton('7',callback_data='7'),
             telebot.types.InlineKeyboardButton('8',callback_data='8'),
             telebot.types.InlineKeyboardButton('9',callback_data='9'),
             telebot.types.InlineKeyboardButton('+',callback_data='+'))

keyboard.row(telebot.types.InlineKeyboardButton(' ',callback_data='zero'),
             telebot.types.InlineKeyboardButton('0',callback_data='0'),
             telebot.types.InlineKeyboardButton('.',callback_data='.'),
             telebot.types.InlineKeyboardButton('=',callback_data='='))


#приветсвуем пользователя
@bot.message_handler(commands=['start'])
def send_start_massage(message):
    bot.send_message(message.chat.id, 'Привет, я SchoolBot. \nЧтобы узнать интересный факт из мира физики или математики, напиши /facts \nЧтобы открыть калькулятор, напиши /calculator')


@bot.message_handler(commands=["calculator"])
def get_calculator(message):
    global value
    if value=='':
        bot.send_message(message.from_user.id,'0',reply_markup=keyboard)
    else:
        bot.send_message(message.from_user.id,value, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call:True)
def callback_func(query):
    global value,old_value
    data=query.data #теперь дата это, то что возваращает кнопка
    if data=='no':
        pass
    elif data=='<=':
        if value!='':
            value=value[:len(value)-1]
    elif data =='c':
        value=''
    elif data == '=':
        try:
            value=str(eval(value))
        except:
            value='error'
    else:
        value+=data
    if value != old_value:
        if value=='':
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text='0', reply_markup=keyboard)
        else:
            bot.edit_message_text(chat_id=query.message.chat.id, message_id=query.message.message_id, text=value,reply_markup=keyboard)
    old_value=value
    if value=='error':
        value=''







@bot.message_handler(commands=["facts"])
def start(message):
        # Добавляем две кнопки
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1=types.KeyboardButton("Факт по физике")
        item2=types.KeyboardButton("Факт по математике")
        markup.add(item1)
        markup.add(item2)
        bot.send_message(message.chat.id, 'Выбери предметную область ',  reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_subject(message):
    if message.text == "Факт по физике":
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        
        buttons = [types.KeyboardButton(theme) for theme in themes_phys]
        for button in buttons:
            markup.add(button)

        bot.send_message(message.chat.id, 'Выбери тему ',  reply_markup=markup)

    if message.text in themes_phys:
        facts = parse_physics(theme2url_phys[str(message.text)])
        for fact in facts:
            bot.send_message(message.chat.id, fact)

'''@bot.message_handler(content_types=['text'])
def get_fact(message):
    print(message)
    if message.text in themes:
        print(type(message.text))
        facts = parse_physics(theme2url[str(message.text)])
        bot.send_message(message.chat.id, facts[randint(0, len(facts) - 1)])'''




# Получение сообщений от пользователя
#@bot.message_handler(content_types=['text'])
#def handle_text(message):
#    # Если юзер прислал 1
#    if message.text.strip() == 'Факт по физике' :
#            answer = random.choice(factsphisics)
#    # Если юзер прислал 2
#    elif message.text.strip() == 'Факт по математике':
#            answer = random.choice(factsalgebra)
#    else :
#        answer='Я не понимаю'
#    # Отсылаем пользователю сообщение в его чат
#    bot.send_message(message.chat.id, answer)

#@bot.message_handler(commands=["/Факт_по_физике"])
#def physic(message):
#    answer1=random.choice(factsphisics)
#    bot.send_message(message.chat.id, answer1)
#
#@bot.message_handler(commands=["/Факт_по_математике"])
#def physic(message):
#    answer2=random.choice(factsalgebra)
#    bot.send_message(message.chat.id, answer2)





bot.polling(none_stop=True,interval=0)


