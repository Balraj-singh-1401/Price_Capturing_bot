#import pandas as pd
from typing import Counter
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
browser = webdriver.Chrome(ChromeDriverManager().install())
import xlwings as xw
import time,pyperclip, pyautogui as p 
from playsound import playsound
from selenium.common.exceptions import NoSuchElementException

#browser = webdriver.Chrome(executable_path='C:\\Users\\Lenovo\\Downloads\\uber_code\\chromedriver.exe')
browser.get('https://auth.uber.com/login/#_')

dest = open('D:\\STUFF\\uber_code\\dest115.txt','r', encoding = 'utf8')
pp = open('D:\\STUFF\\uber_code\\pickup115.txt', 'r', encoding='utf8')
#file=pd.read_excel(r'D:\STUFF\uber_code\test.xlsx')
  
pp_list = pp.readlines()
dest_list = dest.readlines()
desti = []
pps = []


def findAndSetValue(xpath, input_field, value = None):
    time.sleep(3)
    try:
        element = browser.find_element_by_xpath(xpath)
        time.sleep(2)
        element.click()
        if input_field:
            element.send_keys(value)
            return element
    except:
        #findAndSetValue(xpath, input_field, value)
        pass

def getValue(xpath):
    try:    
        time.sleep(5)
        element = browser.find_element_by_xpath(xpath).text
        return element
    except:
        element=None

    

def login(xpath, input_field, value = None):
    try:
        element = browser.find_element_by_xpath(xpath)
        element.click()
        if input_field:
            element.send_keys(value)
    except:
        findAndSetValue(xpath, input_field, value)
        
logins = [
    '//*[@id="useridInput"]',
    '//*[@id="app-body"]/div/div[1]/form/div[2]/button',
    '//*[@id="password"]',
    '//*[@id="app-body"]/div/div[1]/form/div[2]/button',
    'https://m.uber.com/looking?_ga=2.91551898.1074888867.1610477863-92334322.1610477863&uclick_id=4fbeb21f-9daa-4579-8f3b-74a3b382165d'
]

#login(logins[0], True, '8882023736')
#login(logins[1], False)
#login(logins[2], True,"uber@1234")

url=("https://m.uber.com/looking?_ga=2.91551898.1074888867.1610477863-92334322.1610477863&uclick_id=4fbeb21f-9daa-4579-8f3b-74a3b382165d")
#pyperclip.copy('uber@1234')
pyperclip.copy(url)
input("Continue")
#time.sleep(2)


xpath=[
    '//*[@id="booking-experience-container"]/div/div[3]/div[2]/div/input',#pickup_point
    '//*[@id="booking-experience-container"]/div/div[3]/div[4]/div/div[2]/div[1]',#pickup_click
    '//*[@id="booking-experience-container"]/div/div[3]/div[2]/div/input',#des_point
    '//*[@id="booking-experience-container"]/div/div[3]/div[4]/div[1]/div[2]/div[1]',#des_click
    '//*[@id="booking-experience-container"]/div/div[3]/div[3]/div[1]/div[4]/div/div[2]/div[1]/div/span[1]',#premier
    '//*[@id="booking-experience-container"]/div/div[3]/div[3]/div[1]/div[6]/div/div[2]/div[1]/div/span[1]',#ubergo rentals
    '//*[@id="booking-experience-container"]/div[2]/div[1]'#back
]
normal_price='//*[@id="booking-experience-container"]/div/div[3]/div[3]/div[1]/div[1]/div/div[3]/div/span/p'
discount_price='//*[@id="booking-experience-container"]/div/div[3]/div[3]/div[1]/div[1]/div/div[3]/div/span/p[2]'
premiere='//*[@id="booking-experience-container"]/div/div[3]/div[3]/div[1]/div[5]/div/div[2]/div[1]/div/span[1]'
ubergo_rentals='//*[@id="booking-experience-container"]/div/div[3]/div[3]/div[1]/div[6]/div/div[2]/div[1]/div/span[1]'
premier_price='//*[@id="booking-experience-container"]/div[2]/div[2]/div[2]/div[2]/h4'
ubergo_rentalsprice='//*[@id="booking-experience-container"]/div[2]/div[2]/div[2]/div[2]/h4'
pick='//*[@id="booking-experience-container"]/div/div[2]/div/div/div[1]/div[2]/div'
dest='//*[@id="booking-experience-container"]/div/div[2]/div/div[2]/div[2]/div[2]/div'

Sheet_name="Dormant"   
prrice=normal_price

wb = xw.Book (r'D:\STUFF\uber_code\test.xlsx')
s =wb.sheets(Sheet_name)

#updating excel sheet
def pd(i,location,column):
    try:
        el= browser.find_element_by_xpath(location).text
        if el is not None:
            el=el.split("Chevron")[0].split(" ",1)[1]
            s.range(str(column)+str(i+2)).value = el
            return el
        else:
            s.range(str(column)+str(i+2)).value = None

    except NoSuchElementException:
        pass

count=0
for  i in range(11,115):

    print(count,i)
    findAndSetValue(xpath[0], True, pp_list[i])#pickuppoint
    
    findAndSetValue(xpath[1], False)#select_pickup_point
    
    findAndSetValue(xpath[2], True, dest_list[i])#dest_point
    
    findAndSetValue(xpath[3], False)#select_dest_point
    time.sleep(3)
    pd(i,pick,'A')
    pd(i,dest,'B')
    
    price = getValue(prrice)#get price
    if price is None:
        playsound("buzzer.wav")
        s.range("C"+str(i+2)).value=None
        if count > 59:
            print('Waiting...')
            time.sleep(1500)
            count=0
        else:
            time.sleep(15)
    else:
        s.range("C"+str(i+2)).value=price[1:]
    

    count+=1
    browser.back()
    browser.back()


playsound("buzzer.wav")
playsound("buzzer.wav")





