import os
import time

import qrcode
import selenium
from selenium import webdriver
from selenium.webdriver import Keys, ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from undetected_chromedriver import ChromeOptions, Chrome
import qrcode_terminal
import csv

message = ""

phone_nums_list = []
with open("phone_numbers.csv", 'r') as f:
    csv_reader = csv.reader(f)
    for row in csv_reader:
        phone_nums_list.append(row)

clean_phone_nums_list = []
for num in phone_nums_list:
    alpha = False
    for i in range(len(num)):
        if (num[i].isalpha()):
            alpha = True
    if not(alpha):
        clean_phone_nums_list.append(num[0].replace('(', '').replace(')', '').replace('-', '').replace(' ', ''))


def message_phones(phone_nums, message, img = None, driver_executable_path=None):
    # https://web.whatsapp.com/send?phone=+15108707022&text="Hi"

    # Configure undetected Chrome WebDriver options
    options = ChromeOptions()
    options.add_argument("--disable-automation")
    options.add_argument("--headless")
    # Create an instance of Chrome WebDriver with undetected-chromedriver
    driver = Chrome(options=options)
    if not(driver_executable_path == None):
        # Create an instance of Chrome WebDriver with undetected-chromedriver
        driver = Chrome(options=options,
                        driver_executable_path=driver_executable_path)

    driver.get("https://web.whatsapp.com")

    # Wait for the page to load (you can adjust the wait time as needed)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="_19vUU"]')))
    time.sleep(5)


    # Find and print QR codes
    qr_code_elements = driver.find_elements(By.XPATH, '//div[@class="_19vUU"]')
    for qr_code_element in qr_code_elements:
        qr_code_data = qr_code_element.get_attribute("data-ref")
        # print("QR Code Data:", qr_code_data)
        # Generate the QR code

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_code_data)
        qr.make(fit=True)

        # Create a QR code image
        imge = qr.make_image(fill_color="black", back_color="white")

        imge.show()

        time.sleep(30)
    for i in range(len(phone_nums)):
        driver.tab_new(f"https://web.whatsapp.com/send?phone={phone_nums[i]}&text=x")
        driver.get(f"https://web.whatsapp.com/send?phone={phone_nums[i]}&text=x")
        time.sleep(30)
        try:
            driver.save_screenshot('AfterClick.png')
        except:
            time.sleep(5)
            driver.save_screenshot('AfterClick.png')
        time.sleep(2)
        driver.find_element(By.XPATH,
                            ".//p[@class='selectable-text copyable-text iq0m558w g0rxnol2' and @dir='ltr']").send_keys(
            Keys.BACKSPACE)
        time.sleep(0.5)
        driver.find_element(By.XPATH,
                            ".//p[@class='selectable-text copyable-text iq0m558w g0rxnol2' and @dir='ltr']").send_keys(
            message)
        time.sleep(0.5)
        driver.find_element(By.XPATH, ".//p[@class='selectable-text copyable-text iq0m558w g0rxnol2' and @dir='ltr']").send_keys(Keys.ENTER)

        time.sleep(5)
        print(f"Sent {message} to {phone_nums[i]}")
    driver.quit()
message_phones(phone_nums=clean_phone_nums_list, message=message, img=None)
