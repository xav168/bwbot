import telebot
from telebot import types
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy import text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

bot_token = **************
bot = telebot.TeleBot(token=bot_token)
Base = declarative_base()
PATH = r"C:\Users\Owner\Downloads\chromedriver_win32\chromedriver.exe"

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

class TS():
    def __init__(self,id):
        self.id = id
        self.day = None
        self.time = None
        self.date = None


engine = create_engine("sqlite:///users_db.db", connect_args={'check_same_thread': False}, echo=True)
user_dict = {}
temp = {}



def updatedb():
    session = sessionmaker(bind=engine)()
    dbdriver = webdriver.Chrome(PATH)
    dbdriver.get("https://www.picktime.com/566fe29b-2e46-4a73-ad85-c16bfc64b34b")
    wait = WebDriverWait(dbdriver,10)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[6]/div/div/div[1]/button/span')))
    popup = dbdriver.find_element_by_xpath('/html/body/div[2]/div[6]/div/div/div[1]/button/span')
    attempts = 0
    while attempts < 2:
        try:
            popup.click()
            break
        except StaleElementReferenceException as e:
            attempts+=1
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[1]/div[2]')))
    weekday = dbdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[1]/div[2]')
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[2]/div[2]')))
    attempts = 0
    while attempts < 2:
        try:
            weekday.click()
            break
        except StaleElementReferenceException as e:
            attempts+=1

    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/ul/li')))
    slots = dbdriver.find_elements_by_xpath('//*[@id="booking-content"]/div[2]/div[2]/div/ul/li')
    for slot in slots:
        text = slot.text
        line = text.split('\n')
        line.remove("- Boulder World")
        timesl = text.split(" (GMT+8:00) Asia/Singapore ")[0]
        date = timesl.split(',')[0]
        tme = timesl.split(',')[1]
        
        full_id = slot.get_attribute('data-date')
        id = full_id[0:12]
        timeslot = Timeslot(id)
        timeslot.day = "weekday"
        timeslot.date = date
        timeslot.time = tme
        session.add(timeslot)
    try:
        next = dbdriver.find_element_by_xpath('//*[@id="booking-content"]/div[2]/div[1]/div/div[2]/i')
        next.click()
        time.sleep(0.5)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/ul/li')))
        slots2 = dbdriver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        for slot in slots2:
            text = slot.text
            line = text.split('\n')
            line.remove("- Boulder World")
            timesl = text.split(" (GMT+8:00) Asia/Singapore ")[0]
            date = timesl.split(',')[0]
            tme = timesl.split(',')[1]

            full_id = slot.get_attribute('data-date')
            id = full_id[0:12]
            timeslot = Timeslot(id)
            timeslot.day = "weekday"
            timeslot.date = date
            timeslot.time = tme
            session.add(timeslot)

        back = dbdriver.find_element_by_xpath('//*[@id="booking-content"]/div[2]/ul/li[1]/a/span')
        back.click()
    except NoSuchElementException:
        back = dbdriver.find_element_by_xpath('//*[@id="booking-content"]/div[2]/ul/li[1]/a/span')
        back.click()

    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[2]/div[2]')))
    weekend = dbdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[2]/div[2]')
    attempts = 0
    while attempts < 2:
        try:
            weekend.click()
            break
        except StaleElementReferenceException as e:
            attempts+=1

    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/ul/li')))
    slots = dbdriver.find_elements_by_xpath('//*[@id="booking-content"]/div[2]/div[2]/div/ul/li')
    for slot in slots:
        text = slot.text
        line = text.split('\n')
        line.remove("- Boulder World")
        timesl = text.split(" (GMT+8:00) Asia/Singapore ")[0]
        date = timesl.split(',')[0]
        tme = timesl.split(',')[1]
        
        full_id = slot.get_attribute('data-date')
        id = full_id[0:12]
        timeslot = Timeslot(id)
        timeslot.day = "weekend"
        timeslot.date = date
        timeslot.time = tme
        session.add(timeslot)
    try:
        next = dbdriver.find_element_by_xpath('//*[@id="booking-content"]/div[2]/div[1]/div/div[2]/i')
        next.click()
        time.sleep(0.5)
        wait.until(EC.presence_of_all_elements_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/ul/li')))
        slots2 = dbdriver.find_elements_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/div/ul/li')
        for slot in slots2:
            text = slot.text
            line = text.split('\n')
            line.remove("- Boulder World")
            timesl = text.split(" (GMT+8:00) Asia/Singapore ")[0]
            date = timesl.split(',')[0]
            tme = timesl.split(',')[1]
            
            full_id = slot.get_attribute('data-date')
            id = full_id[0:12]
            timeslot = Timeslot(id)
            timeslot.day = "weekend"
            timeslot.date = date
            timeslot.time = tme
            session.add(timeslot)
        dbdriver.close()             
    except NoSuchElementException:
        dbdriver.close()
    session.commit()

def booksl(day, user_slotid, user_name, user_email, user_HP, user_pass, user_month):
    session = sessionmaker(bind=engine)()
    driver = webdriver.Chrome(PATH)
    driver.get("https://www.picktime.com/566fe29b-2e46-4a73-ad85-c16bfc64b34b")
    wait = WebDriverWait(driver,10)
    popup = driver.find_element_by_xpath('/html/body/div[2]/div[6]/div/div/div[1]/button/span')
    attempts = 0
    while attempts < 2:
        try:
            popup.click()
            break
        except StaleElementReferenceException as e:
            attempts +=1

    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[1]/div[2]')))
    weekday = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[1]/div[2]')
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[2]/div[2]')))
    weekend = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[2]/div[2]')
    if day == "weekday":
        attempts = 0
        while attempts < 2:
            try:
                weekday.click()
                break
            except StaleElementReferenceException as e:
                attempts +=1

    if day == "weekend":
        attempts = 0
        while attempts < 2:
            try:
                weekend.click()
                break
            except StaleElementReferenceException as e:
                attempts +=1

    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/ul/li')))
    month = driver.find_element_by_xpath('//*[@id="booking-content"]/div[2]/div[1]/div/div[1]/div').text
    if user_month not in month:
        next_month = driver.find_element_by_xpath('//*[@id="booking-content"]/div[2]/div[1]/div/div[2]/i')
        next_month.click()
        time.sleep(0.5)
    slots = driver.find_elements_by_xpath('//*[@id="booking-content"]/div[2]/div[2]/div/ul/li')
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/ul/li')))
    for slot in slots:
        text = slot.text
        line = text.split("\n")
        line.remove("- Boulder World")
        dates = text.split(" (GMT+8:00) Asia/Singapore ")
        avail = dates[1]        
        full_id = slot.get_attribute('data-date')
        id = full_id[0:12]            
        if user_slotid == id:
            if avail[1] != "0":
                attempts = 0
                while attempts < 2:
                    try:
                        slot.click()
                        break
                    except StaleElementReferenceException as e:
                        attempts += 1
                    except ElementClickInterceptedException:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        slot.click()
                        break
                name = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[1]/input')
                email = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[2]/input')
                hp = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/input')
                sp = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[4]/input')
                submit = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[6]/button')
                name.send_keys(user_name)
                email.send_keys(user_email)
                hp.send_keys(user_HP)
                sp.send_keys(user_pass)
                submit.click()
                time.sleep(5)
                driver.close()
                session.close()  
                break; 
                                
            else:
                driver.close()
                booksl(day=day, user_slotid=user_slotid, user_name=user_name, user_email=user_email, user_HP=user_HP, user_pass=user_pass, user_month=user_month )
                
@bot.message_handler(commands=['start'])
def handle_start_help(message):
    session = sessionmaker(bind=engine)()
    if message.text =="/cancel":
        msg = bot.reply_to(message, "Do /start to start again ")
        bot.register_next_step_handler(msg, cancel_reg)
    else:
        chat_id = message.chat.id
        users = session.query('chatid').from_statement(text("SELECT * FROM users WHERE chatid=:id")).params(id=chat_id).all()
        if len(users) != 0:
            bot.reply_to(message, "Do /picktime to pick your timeslot")
        else: 
            msg = bot.reply_to(message, "Hello, to start please type in your name, do /cancel to cancel registration")
            bot.register_next_step_handler(msg, process_name)

def process_name(message):
    try:
        if message.text =="/cancel":
            msg = bot.reply_to(message, "Do /start to start again ")
            bot.register_next_step_handler(msg, cancel_reg)
        else:
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
        if message.text =="/cancel":
            msg = bot.reply_to(message, "Do /start to start again ")
            bot.register_next_step_handler(msg, cancel_reg)
        else:
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
        if message.text =="/cancel":
            msg = bot.reply_to(message, "Do /start to start again ")
            bot.register_next_step_handler(msg, cancel_reg)
        else:
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
    if message.text =="/cancel":
        msg = bot.reply_to(message, "Do /start to start again ")
        bot.register_next_step_handler(msg, cancel_reg)
    else:
        chat_id = message.chat.id
        passtype = message.text
        user = user_dict[chat_id]
        user.passtype = passtype
        bot.send_message(chat_id, "You have been registered.Do /picktime to choose a time." )
        session.add(user)
        session.commit()
        session.close()
def cancel_reg(message):
    chat_id = message.chat.id
    user_dict.pop(chat_id)

@bot.message_handler(commands=['picktime'])
def picktime(message):
    try:
        Base.metadata.drop_all(bind=engine, tables=[Timeslot.__table__])     
        Base.metadata.create_all(bind=engine)
        updatedb()
        day = types.ReplyKeyboardMarkup(row_width=1, one_time_keyboard=True)
        day.add('weekday', 'weekend')
        msg = bot.reply_to(message, "Please choose a timeslot " ,reply_markup=day)
        bot.register_next_step_handler(msg, pickslot)
    except Exception as e:
        print(str(e))
        msg = bot.reply_to(message, "Something went wrong. Please try again")
def pickslot(message):
    try:
        session = sessionmaker(bind=engine)()
        chat_id = message.chat.id
        ts_reg = TS(id=chat_id)
        temp[chat_id] = ts_reg
        ts = temp[chat_id]
        day = message.text
        ts.day = day
        timeslots = session.query('date').from_statement(text("SELECT DISTINCT date FROM timeslots where day=:day")).params(day=ts.day).all()
        date = types.ReplyKeyboardMarkup(row_width=5, one_time_keyboard=True)
        for slot in timeslots:
            strslot = str(slot)
            txt = strslot.split("'")[1]
            date.add(txt)
        msg = bot.reply_to(message, "Please chose a date,", reply_markup=date)
        bot.register_next_step_handler(msg, picktme)
        session.close()
    except Exception as e:
        print(str(e))
        chat_id = message.chat.id
        del temp[chat_id]
        msg = bot.reply_to(message, "Something went wrong. Please try again")
        bot.register_next_step_handler(msg, book_error)
def picktme(message):
    try:
        session = sessionmaker(bind=engine)()
        chat_id = message.chat.id
        ts = temp[chat_id]
        ts.date = message.text
        timeslots = session.query("time").from_statement(text("SELECT DISTINCT time FROM timeslots WHERE day=:day AND date=:date")).params(day=ts.day, date=ts.date).all()
        ts_markup = types.ReplyKeyboardMarkup(row_width=2, one_time_keyboard=True)
        for slot in timeslots:
            strslot = str(slot)
            txt = strslot.split("'")[1]
            ts_markup.add(txt)
        msg = bot.reply_to(message, "Please pick a time", reply_markup=ts_markup)
        bot.register_next_step_handler(msg, book)
        session.close()
    except Exception as e:
        print(str(e))
        chat_id = message.chat.id
        del temp[chat_id]
        msg = bot.reply_to(message, "Something went wrong. Please try again")
        bot.register_next_step_handler(msg, book_error)       
def book(message):
    try:
        session = sessionmaker(bind=engine)()
        chat_id = message.chat.id
        ts = temp[chat_id]
        ts.time = message.text
        timeslot = session.query('id').from_statement(text("SELECT id FROM timeslots WHERE day=:day AND date=:date AND time LIKE :time")).params(day=ts.day, date=ts.date, time=('%'+ (ts.time))).first()
        user = session.query(User).get(chat_id)
        user.slotid = str(timeslot).split("'")[1]
        session.commit()
        user_name = user.name
        user_email = user.email
        user_HP = user.phone
        user_pass = user.passtype
        user_slotid = user.slotid
        user_month = ts.date.split()[1]
        day = ts.day

        booksl(day=day, user_slotid=user_slotid, user_name=user_name, user_email=user_email, user_HP=user_HP, user_pass=user_pass, user_month=user_month )
        bot.reply_to(message, "Your slot has been booked.")
        session.commit()
        session.close()
    except Exception as e:
        print(str(e))
        chat_id = message.chat.id
        del temp[chat_id]
        msg = bot.reply_to(message, "Something went wrong. Please try again")
        bot.register_next_step_handler(msg, book_error)
def book_error(message):
    bot.reply_to(message, "something went wrong Do /picktime to pick a slot")

bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()

bot.polling()
