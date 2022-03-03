import requests # Otevře stránku a collectne JSON
import simplejson as json # Práce se slovníkem JSON

url = "API_RESPONSE_URL"

# Vezme JSON kód z URL
slovnik = requests.get(url).json()

# Převede JSON do čitelného formátu
randomak = slovnik['observations'] # Převede observations na list
randomak2 = randomak[0] # Převede zpět na dictionary
randomak3 = randomak2["metric"] # Filtruje metric

# Definuje číselné hodnoty pro další práci
teplota_ted_input = randomak3.pop('temp')
teplota_ted_input_str = str(teplota_ted_input) # Převede na string pro pochopení čísla webem a správné zadání do formuláře

tlak_input = randomak3.pop('pressure')
tlak_input_str = str(tlak_input)

vlhkost_input = randomak2.pop('humidity')
vlhkost_input_str = str(vlhkost_input)

srazky_input = randomak3.pop('precipTotal')
srazky_input_str = str(srazky_input)

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# VLOŽENÍ DAT DO FORMULÁŘE

from selenium import webdriver # Webdriver
import datetime # Vloźení aktuálního data do formuláře
import time # Importuje čas, aby mohl skript vyčkat na načtení formuláře
from selenium.webdriver.support.ui import Select # Seznamy a vybrání ze seznamu na webové stránce

driver = webdriver.Chrome("\\chromedriver\\chromedriver.exe") # Umístění webdriveru

driver.get("GLOBE_WEBPAGE") # Počáteční stránka

# Přihlášení do GLOBE systému

email = driver.find_element_by_xpath('//*[@id="_com_liferay_login_web_portlet_LoginPortlet_login"]')
email.send_keys("LOGIN_EMAIL")

password = driver.find_element_by_xpath('//*[@id="_com_liferay_login_web_portlet_LoginPortlet_password"]')
password.send_keys("LOGIN_PASSWORD")

time.sleep(5)

login = driver.find_element_by_xpath('/html/body/div[1]/div[1]/section/div/div/div/div/section/div/div[2]/div/div/form/fieldset/div[3]/button')
login.click()

# Dostání se na zadávací obrazovku
integrated_atmosphere = driver.get('GLOBE_WEBPAGE')

time.sleep(5) # Počká na načtení celého webu

# PŘIPRAVENÍ FORMULÁŘE PRO ZADÁNÍ DAT!

# Zadá aktuální datum
date = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[1]/input')
d = datetime.datetime.now()
date.send_keys(f'{d.strftime("%Y-%m-%d")}')

# Zadá čas 12:00
time_now = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[2]/input')
time_now.send_keys("12:00")

# Nastaví čas na LOCAL
local_time = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[2]/div/div[3]/div[1]/div/div[3]/div[1]/label[2]/input')
local_time.click()

# Rozklikne TEPLOTU
teplota = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div[1]')
teplota.click()

time.sleep(0.5)

# Rozklikne TLAK
tlak = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div[2]')
tlak.click()

time.sleep(0.5)

# Rozklikne VLHKOST
vlhkost = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div[3]')
vlhkost.click()

time.sleep(0.5)

# Rozklikne SRÁŽKY
srazky = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[1]/div[1]/div[4]')
srazky.click()

time.sleep(0.5)

# VKLÁDÁNÍ SAMOTNÝCH DAT

# Vložení TEPLOTY
vlozeni_teplota = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/form/div/div/div[2]/div/fieldset/div/div[5]/div[2]/div[1]/div/div/div/input')
vlozeni_teplota.send_keys(teplota_ted_input_str)

time.sleep(0.5)

# Vložení TLKAU
station_pressure = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/form/div/div/div[3]/div/fieldset/div/div/div[2]/div/div/div/label[3]/input')
station_pressure.click()

time.sleep(1)

pressure = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/form/div/div/div[3]/div/fieldset/div/div/div[3]/div/div/div/div/input')
pressure.send_keys(tlak_input_str)

time.sleep(0.5)

# Vložení VLHKOSTI
digital_hydrometer = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/form/div/div/div[4]/div/fieldset/div/div[1]/div/div[2]/label[3]/input')
digital_hydrometer.click()

ambient_temperatur = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/form/div/div/div[4]/div/fieldset/div/div[2]/div[1]/div[2]/div/div/input')
ambient_temperatur.send_keys(teplota_ted_input_str)

relative_humidity = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/form/div/div/div[4]/div/fieldset/div/div[2]/div[2]/div[2]/div/div/input')
relative_humidity.send_keys(vlhkost_input_str)

time.sleep(0.5)

# Vložení SRÁŽEK

rainfall = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/form/div/div/div[5]/div/fieldset/div/div/div[1]/div[2]/div/div/div/span[1]')
rainfall.click()

# Vybere srázky nasbírané za jeden den
selectrain = Select(driver.find_element_by_id('rainDaysSelect'))
selectrain.select_by_visible_text('1')

# Vybere srážky měřitelné
selectaccum = Select(driver.find_element_by_id('submission-precipitation-precipitation_rain_daily-accumulation_flag'))
selectaccum.select_by_visible_text('Measurable')

time.sleep(1)

rainfall_mm = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/form/div/div/div[5]/div/fieldset/div/div/div[2]/div[2]/div[2]/div/div/div/input')
rainfall_mm.send_keys(srazky_input_str)

time.sleep(0.5)

# ODESLAT DATA
send_data = driver.find_element_by_xpath('/html/body/div/div/div[3]/div[2]/div/div[3]/div[1]/div[2]/form/div/div/div[7]/button[1]')
send_data.click()

time.sleep(10)

# UKONČÍ PROHLÍŽEČ
driver.quit()

# -----------------------------------------------------------------------------------------------------------------------------------------------------
# ULOŽENÍ OBRÁZKU Z WEBKY DO SLOŽKY

import requests
import datetime

# Definuje měsíc jako číslo -> 01 (Leden)
d = datetime.datetime.now()

response = requests.get("WEBCAM_URL")

file = open(f'./images/{d.strftime("%m")}/{d.strftime("%d_%m")}.jpg', "wb")
file.write(response.content)
file.close()
