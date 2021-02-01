from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import NoSuchElementException

engine = create_engine("sqlite:///users_db.db")
session = sessionmaker(bind=engine)()

#chrome_options = Options()
#chrome_options.add_argument("--headless")
#chrome_options.add_argument("--disable-gpu")

PATH = r"C:\Users\Owner\Downloads\chromedriver_win32\chromedriver.exe"
#driver = webdriver.Chrome(PATH)
dbdriver = webdriver.Chrome(PATH)

#driver.get("https://www.picktime.com/566fe29b-2e46-4a73-ad85-c16bfc64b34b")

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
Base.metadata.drop_all(bind=engine, tables=[Timeslot.__table__])     
Base.metadata.create_all(bind=engine)

users = session.query(User).all()
user_name = ''
user_email = ''
user_HP = ''
user_pass = ''
timeslots = session.query(Timeslot).all()



def updatedb():
    dbdriver.get("https://www.picktime.com/566fe29b-2e46-4a73-ad85-c16bfc64b34b")
    wait = WebDriverWait(dbdriver,10)
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[6]/div/div/div[1]/button/span')))
    popup = dbdriver.find_element_by_xpath('/html/body/div[2]/div[6]/div/div/div[1]/button/span')
    popup.click()
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[1]/div[2]')))
    weekday = dbdriver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[1]/div[2]')
    wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[2]/div[2]')))
    weekday.click()
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
    weekend.click()
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
    

        
        
def main():
    def book():    
        wait = WebDriverWait(driver,10)
        popup = driver.find_element_by_xpath('/html/body/div[2]/div[6]/div/div/div[1]/button/span')
        popup.click()
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[1]/div[2]')))
        weekday = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[1]/div[2]')
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[2]/div[2]')))
        weekend = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/ul/li[2]/div[2]')
        if day == "weekday":
            weekday.click()
        if day == "weekend":
            weekend.click()

        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/ul/li')))
        month = driver.find_element_by_xpath('//*[@id="booking-content"]/div[2]/div[1]/div/div[1]/div').text
        if d_month not in month:
            next_month = driver.find_element_by_xpath('//*[@id="booking-content"]/div[2]/div[1]/div/div[2]/i')
            next_month.click()
            time.sleep(0.5)
        wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[2]/div[2]/div[2]/div[2]/div/ul/li')))
        slots = driver.find_elements_by_xpath('//*[@id="booking-content"]/div[2]/div[2]/div/ul/li')
        for slot in slots:
            text = slot.text
            line = text.split("\n")
            line.remove("- Boulder World")
            dates = text.split(" (GMT+8:00) Asia/Singapore ")
            timesl = str(dates[0])
            avail = dates[1]
            print(timesl)
            if desiredts == timesl:
                if avail[1] != "0":
                    try:
                        slot.click()
                        name = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[1]/input')
                        email = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[2]/input')
                        hp = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[3]/div/input')
                        sp = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[4]/input')
                        submit = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[1]/div/div[6]/button')
                        name.send_keys(user_name)
                        email.send_keys(user_email)
                        hp.send_keys(user_HP)
                        sp.send_keys(user_pass)
                        break
                    except ElementClickInterceptedException:
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")                         
                else:
                    driver.refresh()
                    book()


    desiredts = "5th Feb 2021, 12:45 PM"
    d_month = desiredts.split()[1]
    day = "weekday"
    for user in users:
        user_name = user.name
        user_email = user.email
        user_HP = user.phone
        user_pass = user.passtype
        book()

updatedb()
session.commit()