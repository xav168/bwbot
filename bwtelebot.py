import telebot
import time
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import text

Base = declarative_base()
class User(Base):

    __tablename__ = "users"
    chatid = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    passtype = Column(String)
    slotid = Column(String)

    def __init__(self, name, chat_id):
        self.chatid = chat_id
        self.name = name
        self.email = None
        self.phone = None
        self.passtype = None
        self.slotid = None
class Timeslot(Base):
    __tablename__ = "timeslots"
    id = Column(String, primary_key=True)
    day = Column(String)
    date = Column(String)
    time = Column(String)

    def __init__(self, id):
        self.id = id
        self.day = None
        self.time = None
        self.date = None

engine = create_engine("sqlite:///users_db.db", connect_args={'check_same_thread': False}, echo=True)
session = sessionmaker(bind=engine)()
Base = declarative_base()
bot_token = r"1499123388:AAHEYgPe21c5MXUDzBHNuOB6Hxymv0hHWdU"
bot = telebot.TeleBot(token=bot_token)
user_dict = {}
temp = []

Base.metadata.create_all(bind=engine)
users = session.query(User).all()
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    chat_id = message.chat.id
    if chat_id in users:
        bot.reply_to(message, "Do /picktime to pick your timeslot")
    else: 
        msg = bot.reply_to(message, "Hello, to start please type in your name")
        bot.register_next_step_handler(msg, process_name)

def process_name(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = User(name, chat_id)
        user_dict[chat_id] = user
        msg = bot.reply_to(message, "Please enter your email")
        bot.register_next_step_handler(msg, process_email)
    except Exception as e:
        bot.reply_to(message, 'oops something went wrong')

def process_email(message):
    try:
        chat_id = message.chat.id
        email = message.text
        if '@' and '.com' not in email:
            msg = bot.reply_to(message, "Please enter a valid email")
            bot.register_next_step_handler(msg, process_email)
            return
        user = user_dict[chat_id]
        user.email = email
        msg = bot.reply_to(message, "Please enter your mobile number")
        bot.register_next_step_handler(msg, process_hp)
    except Exception as e:
        bot.reply_to(message, "oops something went wrong")
    
def process_hp(message):
    try:
        chat_id = message.chat.id
        phone = message.text
        if not phone.isdigit():
            msg = bot.reply_to(message, "Please enter a valid mobile number")
            bot.register_next_step_handler(msg, process_hp)
            return
        user = user_dict[chat_id]
        user.phone = phone
        markup = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        markup.add('SP' , 'MP')
        msg = bot.reply_to(message, "Please choose your type of pass", reply_markup=markup)
        bot.register_next_step_handler(msg, process_passtype)
    except Exception as e:
        bot.reply_to(message, "oops something went wrong")

def process_passtype(message):
    chat_id = message.chat.id
    passtype = message.text
    user = user_dict[chat_id]
    user.passtype = passtype
    bot.send_message(chat_id, "You have been registered.Do /picktime to choose a time." )
    session.add(user)
    session.commit()

@bot.message_handler(commands=['picktime'])
def picktime(message):
    chat_id = message.chat.id
    day = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
    day.add('weekday', 'weekend')
    msg = bot.reply_to(message, "Please choose a timeslot " ,reply_markup=day)
    bot.register_next_step_handler(msg, pickslot)
def pickslot(message):
    temp.append(message.text)
    timeslots = session.query('date').from_statement(text("SELECT DISTINCT date FROM timeslots where day=:day")).params(day=temp[0]).all()
    date = types.ReplyKeyboardMarkup(row_width=5, one_time_keyboard=True)
    for slot in timeslots:
        strslot = str(slot)
        txt = strslot.split("'")[1]
        date.add(txt)
    msg = bot.reply_to(message, "Please chose a date,", reply_markup=date)
    bot.register_next_step_handler(msg, picktme)
def picktme(message):
    temp.append(message.text)
    timeslots = session.query("time").from_statement(text("SELECT DISTINCT time FROM timeslots WHERE day=:day AND date=:date")).params(day=temp[0], date=temp[1]).all()
    ts_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
    for slot in timeslots:
        strslot = str(slot)
        txt = strslot.split("'")[1]
        ts_markup.add(txt)
    msg = bot.reply_to(message, "Please pick a time", reply_markup=ts_markup)
    bot.register_next_step_handler(msg, book)
def book(message):
    chat_id = message.chat.id
    temp.append(message.text)
    timeslot = session.query('id').from_statement(text("SELECT id FROM timeslots WHERE day=:day AND date=:date AND time LIKE :time")).params(day=temp[0], date=temp[1], time=('%'+ temp[2])).first()
    user = session.query(User).get(chat_id)
    user.slotid = str(timeslot).split("'")[1]
    session.commit()
    bot.reply_to(message, "Your slot has been booked.")

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()