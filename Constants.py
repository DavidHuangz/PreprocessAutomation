# install in terminal
# pip install selenium
# pip install chromedriver-py
# pip install webdriver-manager
# pip install pydub

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

# Configurable settings #
NoBrowser = False
num_threads = 1
ThreadsNum = num_threads

# Pepeha phrases
pepehaPhrase = 'Ko Maungawhau Ko Maungakiekie ngā maunga\nKo Waitematā Ko Manuka ngā whanga\nKo Tūtahi Tonu te ' \
               'Whare\nKo Te Aka Matua o Te Pou Hawaiki te Marae\nKo Niwaru te waka\nKo Tuputupu Whenua te tangata'

# File locations
AudioFiles = r'D:\pepaha\Input\Audio'
AudioEnhanceOutput = r'D:\pepaha\Output\genFiles\AudioEnhanceOutput'
textFile = r'D:\pepaha\Input\Text'
ImapText = r'D:\pepaha\Input\ImapText\TRMg2p.txt'
G2POutputFiles = r'D:\pepaha\Output\genFiles\G2P_output'
WebMAUSOutputFile = r'D:\pepaha\Output\WebMAUS_output'

options = Options()
options.binary = FirefoxBinary(r'C:\Program Files\Mozilla Firefox\firefox.exe')
options.set_preference("browser.download.folderList", 2)
options.set_preference("browser.download.manager.showWhenStarting", False)
options.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/octet-stream,application/vnd.ms-excel")

# # Setting up browser
# options = Options()
# options.headless = NoBrowser
# options.add_argument('--disable-gpu')
# options.add_argument('--lang=en')
# options.add_argument("--disable-notifications")
# options.add_argument('--window-size=1280,720')
# options.add_argument('--no-sandbox')
# options.add_argument('--disable-dev-shm-usage')
# s = Service(ChromeDriverManager().install())
