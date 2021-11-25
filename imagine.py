import requests
import random
import string
import time
import sys
import re
import os
from colorama import Fore, Back, Style
from colorama import init
init()
#==================================================
def line():
    print("==================================================")
#==================================================
print(Fore.LIGHTGREEN_EX)
line()
print("  _               _     _ _ _         ")
print(" | |   _   _  ___(_) __| (_) |_ _   _ ")
print(" | |  | | | |/ __| |/ _` | | __| | | |")
print(" | |__| |_| | (__| | (_| | | |_| |_| |")
print(" |_____\__,_|\___|_|\__,_|_|\__|\__, |")
print("                                |___/ ")
line()
print(Style.RESET_ALL)

#==================================================
startTime = time.time()
#================================================== TEMPORARY MAIL-STUFF
API = 'https://www.1secmail.com/api/v1/'
domainList = ['1secmail.com', '1secmail.net', '1secmail.org']
domain = random.choice(domainList)

def generateUserName():
    name = string.ascii_lowercase + string.digits
    username = ''.join(random.choice(name) for i in range(10))
    return username

def extract():
    getUserName = re.search(r'login=(.*)&',newMail).group(1)
    getDomain = re.search(r'domain=(.*)', newMail).group(1)
    return [getUserName, getDomain]

#CHECKS MAILS AND STORES CONTENT IN .TXT FILE
def checkMails():
    reqLink = f'{API}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
    req = requests.get(reqLink).json()
    length = len(req)
    if length == 0:
        print("Mailbox is empty. Hold tight. Mailbox is refreshed automatically every 2 seconds.")
        return False
    else:
        idList = []
        for i in req:
            for k,v in i.items():
                if k == 'id':
                    mailId = v
                    idList.append(mailId)

        x = 'mails' if length > 1 else 'mail'
        print(f"You've received verification mail")

        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'verifMails')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        for i in idList:
            msgRead = f'{API}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={i}'
            req = requests.get(msgRead).json()
            for k,v in req.items():
                if k == 'from':
                    sender = v
                if k == 'subject':
                    subject = v
                if k == 'date':
                    date = v
                if k == 'textBody':
                    content = v

            mail_file_path = os.path.join(final_directory, f'verifMail.txt')

            with open(mail_file_path,'w') as file:
                file.write("Sender: " + sender + '\n' + "To: " + mail + '\n' + "Subject: " + subject + '\n' + "Date: " + date + '\n' + "Content: " + content + '\n')

        return True

newMail = f"{API}?login={generateUserName()}&domain={domain}"
reqMail = requests.get(newMail)
mail = f"{extract()[0]}@{extract()[1]}"
#pyperclip.copy(mail)
print(Fore.LIGHTBLUE_EX)
line()
print("\nYour temporary email is " + mail + "\n")
line()
print(Style.RESET_ALL)

#================================================== REGISTRATION
import time
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

print(Fore.YELLOW)

config_name = 'msedgedriver.exe'

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, config_name)

s = Service(config_path)
driver = webdriver.Edge(service = s) #launch browser
driver.get("https://creator.nightcafe.studio/login?view=password-signup") #goto site

loaded = False
while not loaded:
    try:
        driver.find_element(By.NAME,"email").send_keys(mail)
        break
    except:
        print("Registration page not loaded yet")
    time.sleep(0.2)

password = "12345678"
driver.find_element(By.NAME,"password").send_keys(password)

driver.find_element(By.NAME,"confirmPassword").send_keys("12345678")

while not loaded:
    try:
        driver.find_element(By.CLASS_NAME,"css-4xonwm").click()
        break
    except:
        print("Button Reg-page not found")
    time.sleep(0.2)

while True:
    time.sleep(2)
    if checkMails():
        break

verifFile = open('verifMails/verifMail.txt', 'r')
link = ""
for line in verifFile:
    if "https://" in line:
        print("Verification Link Found.")
        link = line
        break

#================================================== VERIF SITE
driver.get(link)
while not loaded:
    try:
        driver.find_element(By.CLASS_NAME,"firebaseui-id-submit.firebaseui-button.mdl-button.mdl-js-button.mdl-button--raised.mdl-button--colored").click()
        break
    except:
        print("Verif site not loaded")
    time.sleep(0.2)

loaded = False
while not loaded:
    try:
        driver.find_element(By.CLASS_NAME,"css-1tzvq1v").click()
        break
    except:
        print("css-1tzvq1v not found")
    time.sleep(0.2)

loaded = False
while not loaded:
    try:
        driver.find_element(By.CLASS_NAME,"css-tpvdoh").click()
        break
    except:
        print("css-tpvdoh not found")
    time.sleep(0.2)

#================================================== GET FREE CREDIT
time.sleep(2)
driver.get("https://creator.nightcafe.studio/account/edit-profile")

while not loaded:
    try:
        driver.find_element(By.CLASS_NAME,"css-qzr1ap").click()
        break
    except:
        print("Page not loaded")
    time.sleep(0.2)

while not loaded:
    try:
        driver.find_element(By.CLASS_NAME,"css-hvws00").click()
        break
    except:
        print("Image button not responding")
    time.sleep(0.2)

while not loaded:
    try:
        driver.find_element(By.CLASS_NAME,"css-tpvdoh").click()
        break
    except:
        print("Done Button not responding")
    time.sleep(0.2)

while not loaded:
    try:
        driver.find_element(By.NAME,"username").send_keys(mail[0:10])
        break
    except:
        print("Username input not found")
    time.sleep(0.2)
    
driver.find_element(By.NAME,"displayName").send_keys("t")

driver.find_element(By.NAME,"bio").send_keys("t")

driver.find_element(By.CLASS_NAME,"css-17tew97").click()

time.sleep(2)
driver.get("https://creator.nightcafe.studio/recent")
time.sleep(4)

post_num = 1
stuck = 0
notFound = 0

while post_num <= 500:
    try:
        driver.find_element(By.XPATH,f'//div[@class="css-jcvd79"]/button[1][@title="Like"]').click()
        time.sleep(0.2)
        print("Liked: ", post_num)
        if post_num%40 == 0:
            time.sleep(2)
        post_num += 1
        notFound = 0
    except:
        notFound += 1
        print("Found no such element, most likely page loading")
        # /html/body/div/div[2]/div[3]/div[2]/div/div/div[2]/menu/ul/li[2]
        if notFound >= 3:
            if stuck == 1:
                driver.get("https://creator.nightcafe.studio/top")
            elif stuck == 2:
                driver.find_element(By.XPATH,f'/html/body/div/div[2]/div[3]/div[2]/div/div/div[2]/menu/ul/li[2]').click()
            elif stuck == 3:
                driver.find_element(By.XPATH,f'/html/body/div/div[2]/div[3]/div[2]/div/div/div[2]/menu/ul/li[3]').click()
            elif stuck == 4:
                driver.find_element(By.XPATH,f'/html/body/div/div[2]/div[3]/div[2]/div/div/div[2]/menu/ul/li[4]').click()
            stuck += 1
            time.sleep(2)
            notFound = 0
        time.sleep(3)



print(Style.RESET_ALL)
#======================================== COMPLETED
print(Fore.GREEN)
print("============================")
print("Account creation succesfull.")
print("Email:", mail)
print("Password:", password)
print("Time elapsed:", time.time() - startTime, "seconds")
print("============================")
