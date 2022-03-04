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

def printTag(text, tag_type=""):
    tag = f"{Fore.LIGHTGREEN_EX}[INFO] {Fore.RESET}{text}"
    if tag_type == "error":
        tag = f"{Fore.RED}[ERROR] {Fore.LIGHTRED_EX}{text}"
    elif tag_type == "warn":
        tag = f"{Fore.LIGHTYELLOW_EX}[WARN] {Fore.YELLOW}{text}"
    elif tag_type == "mail":
        tag = f"{Fore.CYAN}[MAIL] {Fore.RESET}{text}"
        
    print(tag+Fore.YELLOW)

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
    printTag("No verifMails folder found, no deletion required.")

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
    printTag(mailNumber, "scripts running")
except:
    printTag("1 script running.")

#CHECKS MAILS AND STORES CONTENT IN .TXT FILE
def checkMails():
    reqLink = f'{API}?action=getMessages&login={extract()[0]}&domain={extract()[1]}'
    req = requests.get(reqLink).json()
    length = len(req)
    if length == 0:
        printTag("Mailbox is empty. Hold tight. Mailbox is refreshed automatically every 2 seconds.","mail")
        return False
    else:
        idList = []
        for i in req:
            for k,v in i.items():
                if k == 'id':
                    mailId = v
                    idList.append(mailId)

        printTag("You've received verification mail","mail")

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
print(Fore.YELLOW)

#================================================== LAUNCH

config_name = 'chromedriver.exe'

# determine if application is a script file or frozen exe
if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, config_name)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--log-level=3") #hide errors

s = Service(ChromeDriverManager(log_level=0, print_first_line=False).install()) #install chrome driver plus hide warnings
driver = webdriver.Chrome(service = s, options = chrome_options) #launch browser

#================================================== REGISTRATION
driver.get("https://creator.nightcafe.studio/login?view=password-signup") #goto site

def waitForElement(find_by, value):
    return WebDriverWait(driver, 10).until(expected_conditions.element_to_be_clickable((find_by, value)))

waitForElement(By.NAME,"email").send_keys(mail)
printTag("Registration page loaded")

password = "12345678"
waitForElement(By.NAME,"password").send_keys(password)
waitForElement(By.NAME,"confirmPassword").send_keys(password)
waitForElement(By.XPATH,"//button[@type='submit']").click()
printTag("Checking mail for verif link...")

while True:
    time.sleep(2)
    if checkMails():
        break

verifFile = open(f'verifMails/verifMail{str(mailNumber)}.txt', 'r')
link = ""
for line in verifFile:
    if "https://" in line:
        printTag("Verification Link Found.")
        link = line
        break

#================================================== VERIF SITE
driver.get(link)

waitForElement(By.CLASS_NAME, "firebaseui-id-submit.firebaseui-button.mdl-button.mdl-js-button.mdl-button--raised.mdl-button--colored").click()
printTag("Verif site loaded")

waitForElement(By.CLASS_NAME,"css-1tzvq1v").click()
waitForElement(By.CLASS_NAME,"css-e3l1on").click()
printTag("Finished new account creation for 5 credit(s)")

#================================================== GET FREE CREDIT
time.sleep(2)
driver.get("https://creator.nightcafe.studio/account/edit-profile")

waitForElement(By.NAME,"displayName").click()
printTag("Profile page loaded")

waitForElement(By.XPATH,"//span[text()='Choose Photo']/parent::*").click()
waitForElement(By.XPATH,"//img[@alt='Lion']").click()
waitForElement(By.XPATH, "//span[text()='Done']/parent::*").click()
printTag("Profile picture set")

waitForElement(By.NAME,"username").send_keys(mail[0:10])
waitForElement(By.NAME,"displayName").send_keys("t")
waitForElement(By.NAME,"bio").send_keys("t")
waitForElement(By.XPATH,"//span[text()='Save']/parent::*").click()
printTag("Finished profile setup for 1 credit(s)")

time.sleep(2)
driver.get("https://creator.nightcafe.studio/explore?q=new")
time.sleep(4)

post_num = 0
stuck = 0
notFound = 0

while post_num <= 500:
    try:
        WebDriverWait(driver, 6).until(expected_conditions.element_to_be_clickable((By.XPATH, "//div[@class='css-jcvd79']/button[1][@title='Like']"))).click()
        printTag(f"Liked: {post_num}")
        post_num += 1
        notFound = 0
    except:
        notFound += 1
        printTag("No like elements found, most likely page loading","warn")
        if notFound >= 3:
            stuck += 1
            notFound = 0
            if stuck == 1:
                driver.get("https://creator.nightcafe.studio/explore")
            elif stuck == 2:
                driver.get("https://creator.nightcafe.studio/explore?q=top-day")
            elif stuck == 3:
                driver.get("https://creator.nightcafe.studio/explore?q=top-week")
            elif stuck == 4:
                driver.get("https://creator.nightcafe.studio/explore?q=top-month")
            elif stuck == 5:
                driver.get("https://creator.nightcafe.studio/explore?q=top-all")
            time.sleep(2)
        time.sleep(3)

printTag("Finished liking posts for 18 credit(s)")

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
f.write("Time elapsed:", time.time() - startTime, "seconds")
f.write("Date created:", time.ctime)
f.write("============================\n")

f.close()