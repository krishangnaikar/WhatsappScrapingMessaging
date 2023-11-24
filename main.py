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
import pywhatkit

wanted_title = ""
wanted_titles = []
message = ''

# Configure undetected Chrome WebDriver options
options = ChromeOptions()
options.add_argument("--disable-automation")
options.add_argument("--headless")


# Create an instance of Chrome WebDriver with undetected-chromedriver
driver = Chrome(options=options, driver_executable_path="executable/path/driver.exe")

# Navigate to the website
website_url = "https://web.whatsapp.com"  # Replace with the URL of the website
driver.get(website_url)


# Wait for the page to load (you can adjust the wait time as needed)
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.XPATH, '//div[@class="_19vUU"]')))
time.sleep(5)



driver.save_screenshot('nowsecure.png')

# Find and print QR codes
qr_code_elements = driver.find_elements(By.XPATH, '//div[@class="_19vUU"]')
for qr_code_element in qr_code_elements:
    qr_code_data = qr_code_element.get_attribute("data-ref")
    #print("QR Code Data:", qr_code_data)
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
    img = qr.make_image(fill_color="black", back_color="white")

    img.show()


    time.sleep(60)

    '''

    chats = driver.find_elements(By.XPATH, '//*[@id="pane-side"]/div[1]/div/div')
    #print(chats)


    chats = chats[0].find_elements(By.XPATH, ".//div[@role='listitem']")

    #print(len(chats))
    #chat = chats[6]
    #i = 0
    titles = []
    phone_nums = ""
    
    titles_element = driver.find_elements(By.XPATH,
                                          ".//span[@class='ggj6brxn gfz4du6o r7fjleex g0rxnol2 lhj4utae le5p0ye3 l7jjieqr _11JPr' and @dir='auto']")
    for i in range(0, len(titles_element), 2):
        titles.append(titles_element[i].text)
    print(titles)
    
    found = False

    for chat in chats:

        time.sleep(10)
        driver.save_screenshot('BeforeFind.png')
        #title = chat.find_element(By.TAG_NAME, 'div').find_element(By.XPATH, ".//div[@role='row']").find_element(By.TAG_NAME, 'div').find_element(By.XPATH, ".//div[@class='_8nE1Y']").find_element(By.XPATH, ".//div[@role='gridcell']").find_element(By.XPATH, ".//div[@class='_21S-L']").get_attribute('title')
        #print(title)
    '''


    textbox = driver.find_element(By.XPATH, ".//div[@role='textbox' and @title='Search input textbox']")

    if (len(wanted_titles) == 0):

        textbox.send_keys(wanted_title)
        time.sleep(2)
        textbox.send_keys(Keys.ENTER)
        time.sleep(2)


        driver.save_screenshot('AfterClick.png')
        stuffs = driver.find_elements(By.XPATH, ".//span[@class='ggj6brxn gfz4du6o r7fjleex lhj4utae le5p0ye3 _11JPr selectable-text copyable-text']")
        for stuff in stuffs:
            if ('You' in stuff.get_attribute('title')):
                phone_nums = stuff.get_attribute('title')


        #driver.save_screenshot(f'whatsup{i}.png')
        #i += 1
        phone_nums_list = []
        for num in phone_nums.split(','):
            phone_nums_list.append([num])


        data_list = []


        with open("phone_numbers.csv", 'r') as f:


            csv_reader = csv.reader(f)
            for row in csv_reader:
                data_list.append(row)

        for num in phone_nums_list:
            data_list.append(num)

        with open("phone_numbers.csv", 'w') as f:
            fc = csv.writer(f, lineterminator='\n')
            fc.writerows(list(set(tuple(sublist) for sublist in data_list)))


        '''
        clean_phone_nums_list = []
        for num in phone_nums_list:
            alpha = False
            for i in range(len(num)):
                if (num[i].isalpha()):
                    alpha = True
            if not (alpha):
                clean_phone_nums_list.append(num[0].replace('(', '').replace(')', '').replace('-', '').replace(' ', ''))
    
        for i in range(len(clean_phone_nums_list)):
            pywhatkit.sendwhatmsg_instantly(clean_phone_nums_list[i], message, tab_close=True)
        '''
    elif (len(wanted_titles) > 0):
        for j in range(len(wanted_titles)):
            textbox.send_keys(wanted_titles[j])
            time.sleep(2)
            textbox.send_keys(Keys.ENTER)
            time.sleep(2)

            driver.save_screenshot('AfterClick.png')
            stuffs = driver.find_elements(By.XPATH,
                                          ".//span[@class='ggj6brxn gfz4du6o r7fjleex lhj4utae le5p0ye3 _11JPr selectable-text copyable-text']")
            for stuff in stuffs:
                if ('You' in stuff.get_attribute('title')):
                    phone_nums = stuff.get_attribute('title')

            # driver.save_screenshot(f'whatsup{i}.png')
            # i += 1
            phone_nums_list = []
            for num in phone_nums.split(','):
                phone_nums_list.append([num])

            data_list = []

            with open("phone_numbers.csv", 'r') as f:

                csv_reader = csv.reader(f)
                for row in csv_reader:
                    data_list.append(row)

            for num in phone_nums_list:
                data_list.append(num)

            with open("phone_numbers.csv", 'w') as f:
                fc = csv.writer(f, lineterminator='\n')
                fc.writerows(list(set(tuple(sublist) for sublist in data_list)))

            '''
            clean_phone_nums_list = []
            for num in phone_nums_list:
                alpha = False
                for i in range(len(num)):
                    if (num[i].isalpha()):
                        alpha = True
                if not (alpha):
                    clean_phone_nums_list.append(num[0].replace('(', '').replace(')', '').replace('-', '').replace(' ', ''))

            for i in range(len(clean_phone_nums_list)):
                pywhatkit.sendwhatmsg_instantly(clean_phone_nums_list[i], message, tab_close=True)
            '''
            actions = ActionChains(driver)
            textbox.click()
            actions.key_down(Keys.LEFT_CONTROL).key_down("a")
            time.sleep(0.5)
            actions.key_up(Keys.LEFT_CONTROL).key_up("a")
            textbox.send_keys(Keys.DELETE)
            time.sleep(0.5)

# Close the WebDriver when done
driver.quit()


