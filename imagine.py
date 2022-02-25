import requests
import random
import string
import time
import sys
import re
import os
import shutil
from colorama import Fore, Back, Style
from colorama import init
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)

clearConsole()
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
try:
    shutil.rmtree("verifMails")
except:
    print("No verifMails folder found, no deletion required.")

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

#Checks what filename for verifMail.txt
mailNumber = 1
try:
    list = os.listdir(r'./verifMails') # dir is your directory path
    number_files = len(list)
    mailNumber = number_files + 1
    print(mailNumber, "scripts running")
except:
    print("1 script running.")

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

        print(f"You've received verification mail")

        current_directory = os.getcwd()
        final_directory = os.path.join(current_directory, r'verifMails')
        if not os.path.exists(final_directory):
            os.makedirs(final_directory)

        for index in idList:
            msgRead = f'{API}?action=readMessage&login={extract()[0]}&domain={extract()[1]}&id={index}'
            req = requests.get(msgRead).json()
            for mailForm,formData in req.items():
                if mailForm == 'from':
                    sender = formData
                if mailForm == 'subject':
                    subject = formData
                if mailForm == 'date':
                    date = formData
                if mailForm == 'textBody':
                    content = formData
            
            mail_file_path = os.path.join(final_directory, f'verifMail{str(mailNumber)}.txt')

            
            file = open(mail_file_path, "x")
            file.write("Sender: " + sender + '\n' + "To: " + mail + '\n' + "Subject: " + subject + '\n' + "Date: " + date + '\n' + "Content: " + content + '\n')
            file.close()
            
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
print(Fore.YELLOW)

config_name = 'chromedriver.exe'

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, config_name)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--log-level=3") #hide errors

s = Service(ChromeDriverManager().install()) #install chrome driver
driver = webdriver.Chrome(service = s, options = chrome_options) #launch browser
driver.get("https://creator.nightcafe.studio/login?view=password-signup") #goto site

while True:
    try:
        driver.find_element(By.NAME,"email").send_keys(mail)
        break
    except:
        print("Registration page not loaded yet")
    time.sleep(0.2)

password = "12345678"
driver.find_element(By.NAME,"password").send_keys(password)

driver.find_element(By.NAME,"confirmPassword").send_keys(password)

while True:
    try:
        driver.find_element(By.XPATH,"//button[@type='submit']").click()
        break
    except:
        print("Button Reg-page not found")
    time.sleep(0.2)

while True:
    time.sleep(2)
    if checkMails():
        break

verifFile = open(f'verifMails/verifMail{str(mailNumber)}.txt', 'r')
link = ""
for line in verifFile:
    if "https://" in line:
        print("Verification Link Found.")
        link = line
        break

#================================================== VERIF SITE
driver.get(link)
while True:
    try:
        driver.find_element(By.CLASS_NAME,"firebaseui-id-submit.firebaseui-button.mdl-button.mdl-js-button.mdl-button--raised.mdl-button--colored").click()
        break
    except:
        print("Verif site not loaded")
    time.sleep(0.2)

while True:
    try:
        driver.find_element(By.CLASS_NAME,"css-1tzvq1v").click()
        break
    except:
        print("css-1tzvq1v not found")
    time.sleep(0.2)

while True:
    try:
        driver.find_element(By.CLASS_NAME,"css-e3l1on").click()
        break
    except:
        print("css-e3l1on not found")
    time.sleep(0.2)

#================================================== GET FREE CREDIT
time.sleep(2)
driver.get("https://creator.nightcafe.studio/account/edit-profile")

while True:
    try:
        driver.find_element(By.NAME,"displayName").click()
        break
    except:
        print("Profile page not loaded")
    time.sleep(0.2)

while True:
    try:
        driver.find_element(By.XPATH,"//span[text()='Choose Photo']/parent::*").click()
        break
    except:
        print("Image button not responding")
    time.sleep(0.2)

while True:
    try:
        driver.find_element(By.XPATH,"//img[@alt='Lion']").click()
        break
    except:
        print("Lion image button not responding")
    time.sleep(0.2)

while True:
    try:
        driver.find_element(By.XPATH,"//span[text()='Done']/parent::*").click()
        break
    except:
        print("Done Button not responding")
    time.sleep(0.2)

while True:
    try:
        driver.find_element(By.NAME,"username").send_keys(mail[0:10])
        break
    except:
        print("Username input not found")
    time.sleep(0.2)

driver.find_element(By.NAME,"displayName").send_keys("t")

driver.find_element(By.NAME,"bio").send_keys("t")

driver.find_element(By.XPATH,"//span[text()='Save']/parent::*").click()

time.sleep(2)
driver.get("https://creator.nightcafe.studio/explore?q=new")
time.sleep(4)

post_num = 0
stuck = 0
notFound = 0

while post_num <= 500:
    try:
        WebDriverWait(driver, 3).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@class='css-jcvd79']/button[1][@title='Like']"))).click()
        time.sleep(0.2)
        print("Liked: ", post_num)
        post_num += 1
        notFound = 0
    except:
        notFound += 1
        print("Found no such element, most likely page loading")
        if notFound >= 3:
            if stuck == 1:
                driver.get("https://creator.nightcafe.studio/explore")
            elif stuck == 2:
                driver.get("https://creator.nightcafe.studio/explore?q=top-day")
            elif stuck == 3:
                driver.get("https://creator.nightcafe.studio/explore?q=top-week")
            elif stuck == 4:
                driver.get("https://creator.nightcafe.studio/explore?q=top-month")
            stuck += 1
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
print("Account saved to accounts.txt")
print("============================")

f = open("accounts.txt", "a")

f.write("\n============================\n")
f.write("Email: "+mail+"\n")
f.write("Password: "+password+"\n")
f.write("============================\n")

f.close()