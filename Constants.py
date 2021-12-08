# install in terminal
# pip install selenium
# pip install chromedriver-py
# pip install webdriver-manager
# pip install pydub

import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Configurable settings #
NoBrowser = True
Num_threads = 10
ThreadsNum = Num_threads

# Pepeha phrases
PepehaPhrase = 'Ko Maungawhau Ko Maungakiekie ngā maunga\nKo Waitematā Ko Manuka ngā whanga\nKo Tūtahi Tonu te ' \
               'Whare\nKo Te Aka Matua o Te Pou Hawaiki te Marae\nKo Niwaru te waka\nKo Tuputupu Whenua te tangata'

# File locations
AudioFiles = r'D:\pepaha\Input\Audio'
AudioEnhanceOutput = r'D:\pepaha\Output\genFiles\AudioEnhanceOutput'
TextFile = r'D:\pepaha\Output\genFiles\Text'
ImapText = r'D:\pepaha\Input\ImapText\TRMg2p.txt'
G2POutputFiles = r'D:\pepaha\Output\genFiles\G2P_output'
WebMAUSOutputFile = r'D:\pepaha\Output\WebMAUS_output'

# Setting up browser
options = Options()
options.headless = NoBrowser
options.add_argument('--disable-gpu')
options.add_argument('--lang=en')
options.add_argument("--disable-notifications")
options.add_argument('--window-size=1280,720')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
s = Service(ChromeDriverManager().install())

# If Num_threads > audio files, adjust the threads
xAudioNum = len(os.listdir(AudioFiles))
if Num_threads > xAudioNum:
    Num_threads = xAudioNum
