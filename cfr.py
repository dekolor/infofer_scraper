from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import time
import json
import os

#nr_tren = "2872"
data = "16.01.2022"

trenuri = []

f = open("trenuri.txt", "r")
for x in f:
    tren = x.split(",")[2]
    trenuri.append(tren)
f.close()
print(trenuri)

driver = webdriver.Chrome('./chromedriver')

for y in trenuri:
    driver.get("https://mersultrenurilor.infofer.ro/ro-RO/Tren/" + y + "?Date=" + data)

    # time.sleep(5)
    delay = 5

    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'i.fas.fa-stopwatch')))
        print("am gasit elementul")

        status = driver.find_elements_by_css_selector('p.text-1-1rem')[1].text
        statii = driver.find_elements_by_css_selector('li.list-group-item')

        #variabile
        group_data = []

        for x in statii:
            nume_statie = x.find_elements_by_css_selector('div.div-middle')[2].text
            linie_statie = x.find_elements_by_css_selector('div.col-md-2')[2]
            try:
                ora_sosire = x.find_elements_by_css_selector('div.text-1-3rem')[0].text
                status_sosire = x.find_elements_by_css_selector('div.text-0-8rem')[0].text
            except:
                ora_sosire = ""
                status_sosire = ""
            try:
                ora_plecare = x.find_elements_by_css_selector('div.text-1-3rem.text-right')[0].text
                status_plecare = x.find_elements_by_css_selector('div.text-0-8rem.text-right')[0].text
            except:
                ora_plecare = ""
                status_plecare = ""
            group_data.append({"ora_sosire": ora_sosire, "status_sosire": status_sosire, "ora_plecare": ora_plecare, "status_plecare": status_plecare, "nume_statie": nume_statie, "linie": linie_statie.text})

        print("s-a facut final obj")

        final_obj = {"status": status, "statii": group_data}

        fullpath = os.path.join('data', y + '-' + data + '.json')
        print(fullpath)
        with open(fullpath, 'w', encoding='utf8') as json_file:
            json.dump(final_obj, json_file, ensure_ascii=False)
        
        print("s-a scris fisierul")
    except TimeoutException:
        print("loading took too much time")

driver.close()
