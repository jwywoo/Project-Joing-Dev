import os
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

url = "https://www.youtube.com/@ddoddunam"
# url = "https://www.youtube.com/@parkpdch"
# Driver
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

driver.get(url = url)

driver.execute_script("document.body.style.zoom='80%'")
sleep(3)
driver.save_screenshot("screen_shots/"+url.split("/")[-1]+"_channel.png")
sleep(3)
driver.quit()