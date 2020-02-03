from selenium import webdriver
from time import sleep
from urllib.request import urlretrieve
from captcha import parse_captcha
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from os import remove
from getpass import getpass
timeout = 5
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract

class Vbot():
    def __init__(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--incognito")
        self.driver = webdriver.Chrome(chrome_options=chrome_options)
    def login(self):
        self.driver.get('http://vtopcc.vit.ac.in:8080/vtop/initialProcess')
        try:
            intvl_bt = self.driver.find_element_by_xpath('//*[@id="closedHTML"]/div/div/div/div[2]/div/div/a') 
            intvl_bt.click()
        except Exception: 
            pass
        login_bt = self.driver.find_element_by_xpath('//*[@id="page-wrapper"]/div/div[1]/div[1]/div[3]/div/button')
        login_bt.click()
        #sleep(1)
        try:
            element_present = EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/section/div/div[2]/form/div[1]/span'))
            WebDriverWait(self.driver, timeout).until(element_present)
        except TimeoutException:
            print("Timed out waiting for page to load")
        usr = self.driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div[2]/form/div[1]/input')
        username = input("Enter Username: ")
        usr.send_keys(username)
        pwd = self.driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div[2]/form/div[2]/input')
        password = getpass()
        pwd.send_keys(password)
        captcha = self.driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div[2]/form/div[3]/div/div/img')
        cap_src = captcha.get_attribute('src')
        urlretrieve(cap_src, "captcha.png")
        captcha_text = parse_captcha('captcha.png')
        captcha_input = self.driver.find_element_by_xpath('/html/body/div[1]/div/section/div/div[2]/form/div[3]/div/div/input')
        captcha_input.send_keys(captcha_text)
        sign_in_btn = self.driver.find_element_by_xpath('html/body/div[1]/div/section/div/div[2]/form/div[4]/div[2]/button')
        sign_in_btn.click()
        remove("captcha.png")
bot = Vbot()
bot.login()
