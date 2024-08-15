from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pytesseract
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import urllib.request
import re
import io
import csv


options = Options()
options.page_load_strategy = 'normal'

options.add_argument('--headless')
options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

driver = webdriver.Chrome(
    options=options,
)


headers = ["Receipt Number", "Status", "Header", "Paragraph"]
try:
    with open('Data.csv', mode="w", newline='') as jn_file:
        jn_writer = csv.writer(jn_file)
        jn_writer.writerow(headers)
        print("Csv File Created successfully")
except:
    print("Csv file was not created")


# provide the receipt list here from your dynamoDB
receipt_list = [
    "IOE9706621457", "IOE9721097962", "IOE9213569751", "IOE9527174646", "IOE9369471851",
    "IOE9770776946", "IOE9404531659", "IOE9801521365", "IOE9447793314", "IOE9830110852",
    "IOE9345859776", "IOE9062693120", "IOE9731467113", "IOE9761145707", "IOE9824952500",
    "IOE9141132517", "IOE9098234355", "IOE9200345650", "IOE9453399085", "IOE9055384147",
    "IOE9652532336", "IOE9844444970", "IOE9007701810", "IOE9186631982", "IOE9081126929",
    "IOE9648000326", "MSC2490072269", "IOE9195250242", "IOE9680637330", "IOE9125605658",
    "IOE9376977326", "IOE9487011725", "IOE9734028209", "IOE9745956102", "IOE9142295458",
    "IOE9572118749", "IOE9558636904", "IOE9334134755", "IOE9786668121", "IOE9848088178",
    "IOE9791518950", "IOE9777957969", "IOE9204747312", "IOE9230056988", "IOE9277168494",
    "IOE9712790560", "IOE9763080894", "IOE9786719891", "IOE9717113494", "IOE9787879307"
]

# first page
driver.get(f"https://egov.uscis.gov/")
time.sleep(5)


# Captcha Bypass code
while True:

    captcha_image_link = driver.find_element(By.CSS_SELECTOR, "div#captchaImage > img").get_attribute('src')
    image_url = captcha_image_link
    # print(image_url)

    headers = {
        'authority': 'egov.uscis.gov',
        'method': 'GET',
        'path': '/captchas/images/ETt21TOmaNKXTheFkZd5Q-sKv2M.jpg',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,pl;q=0.7',
        'cache-control': 'no-cache',
        'cookie': '_ga=GA1.1.1199737375.1723728189; _ga_PKV493T59N=GS1.1.1723732728.2.1.1723732810.49.0.0; _ga_CSLL4ZEK4L=GS1.1.1723732763.2.1.1723732810.0.0.0; __cf_bm=4OELdJLDWYxtNZC.Qoi3jlEo2JaZro5.aOG5x2vIwbU-1723740218-1.0.1.1-M7WFIJRiROX_DIaFncpvup555UXHIuNfFIQH4rDT6FVPw2THjVg0xmOtu09vdda1N19YykePmcdJsFfr1k.ZWA; __cflb=0H28vwBHwZ9XE3i7HUymRAmi3ch9vZxx9nHh9zWtomw',
        'pragma': 'no-cache',
        'priority': 'u=0, i',
        'sec-ch-ua': '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"macOS"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36',
    }

    req =  urllib.request.Request(image_url, headers=headers)

    try:
        with urllib.request.urlopen(req) as response:

            image_data = response.read()
            image = Image.open(io.BytesIO(image_data))
            new_width = image.width * 10
            new_height = image.height * 10
            resized_image = image.resize((new_width, new_height))
            text = pytesseract.image_to_string(resized_image)
            trimmed_text = text.strip() 
            text = re.sub(r'\s+', '', trimmed_text)
            if text == "":
                text="abcd"
    except urllib.error.HTTPError as e:
        print(f"HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"URL Error: {e.reason}")
    except Exception as e:
        print(f"An error occurred: {e}")

    captcha_val_input = driver.find_element(By.CSS_SELECTOR, 'input.usa-input[name="captchaValue"]')
    captcha_val_input.send_keys(text)

    try:
        error_msg = driver.find_element(By.CSS_SELECTOR, 'div.errorMessage').text
    except:
        error_msg =  None
    
    if error_msg is None:
        print("error message is none")
        print(text)
        break
    else:
        refresh_btn = driver.find_element(By.CSS_SELECTOR, 'button.usa-button[name="refresnImage"][title="Refresh Image"]')
        refresh_btn.click()
        time.sleep(0.2)


print("captcha Cleared")

input =driver.find_element(By.CSS_SELECTOR, 'input')
input.send_keys("IOE9200690819")
time.sleep(5)

check_btn = driver.find_element(By.CSS_SELECTOR, 'button.usa-button[name="initCaseSearch"][title="Check Status"]')
check_btn.click()


#  second page
for receipt_number in receipt_list:
  input =driver.find_element(By.CSS_SELECTOR, 'input')
  input.send_keys(receipt_number)
  time.sleep(2.5)

  check_btn = driver.find_element(By.CSS_SELECTOR, 'button.usa-button[name="initCaseSearch"][title="Check Status"]')
  check_btn.click()

  wait = WebDriverWait(driver, 120)

  try:
     
      status = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.caseStatus-container > h1"))).text
  except:
      status = ""
  
  try:
   
      header = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "h2#landing-page-header"))).text
  except:
      header = ""
  
  try:
     
      para2 = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "div.conditionalLanding > div > p"))).text
  except:
      para2 = ""
  
  with open("Data.csv", mode='a', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    writer.writerow([
        receipt_number, status, header, para2
    ])
    input =driver.find_element(By.CSS_SELECTOR, 'input')
    input.send_keys("")
    

time.sleep(5)
print("List Scraped")
driver.quit()