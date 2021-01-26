import telebot
import time
from telebot import types
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine("sqlite:///users_db.db")
session = sessionmaker(bind=engine)()
Base = declarative_base()
bot_token = r"1499123388:AAHEYgPe21c5MXUDzBHNuOB6Hxymv0hHWdU"
bot = telebot.TeleBot(token=bot_token)
user_dict = {}

class User(Base):

    __tablename__ = "users"
    chatid = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    passtype = Column(String)

    def __init__(self, name, chat_id):
        self.chatid = chat_id
        self.name = name
        self.email = None
        self.phone = None
        self.passtype = None


@bot.message_handler(commands=['start'])
def handle_start_help(message):
    chat_id = message.chat.id
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
    bot.send_message(chat_id, "USER: %s" %user.name + "\nEMAIL: %s" %user.email + "\nHP: %s" %user.phone + "\nPass: %s" %user.passtype)
    session.add(user)
    session.commit()

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()