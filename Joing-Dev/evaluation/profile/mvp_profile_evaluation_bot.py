import os
import base64
from time import sleep

from dotenv import load_dotenv
from openai import OpenAI

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')

# screenshot -> analyzing
def screenshot_selenium(url, driver):
    channel_name = url.split("/")[-1]
    saved_path  = os.path.join("screenshots/", channel_name+"_channel.png")
    driver.get(url=url)
    
    sleep(2)
    
    driver.execute_script("document.body.style.zoom='80%'")
    driver.save_screenshot(saved_path)
    
    sleep(2)
    
    driver.quit()
    return saved_path

# analyzing -> result
def screenshot_verification(url,driver):
    path_to_screenshot = screenshot_selenium(url=url, driver=driver)
    with open(path_to_screenshot, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    messages=[
    {
      "role": "system",
      "content": "You are an image classification system to find inappropriate youtube channel. Classify whether this is inappropriate for teenagers or not  {'inappropriate': 'True/False'}"
    },
    {
      "role": "user",
      "content": [
        {"type": "text", "text": "Classify whether this youtube channel is appropriate for teenagers or not"},
        {
          "type": "image_url",
          "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
          },
        },
      ],
    }
    ]
    
    client = OpenAI()
    response = client.chat.completions.create(
        model="gpt-4o-2024-08-06",
        messages=messages,
        max_tokens=300,
        )
    return response.choices[0].message.content

# result -> delete
def result_generation(url,driver):
    result  = screenshot_verification(url,driver)
    return result


url = "https://www.youtube.com/@ddoddunam"
# url = "https://www.youtube.com/@parkpdch"
# Driver
driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
channel_name = url.split("/")[-1]
print(result_generation(url=url,driver=driver))