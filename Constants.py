# install in terminal
# pip install selenium
# pip install chromedriver-py
# pip install webdriver-manager
# pip install pydub

import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from Processes.ConvertToWav import convertWavThread

# Configurable settings #
NoBrowser = False
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
options.add_argument('--disable-software-rasterizer')
options.add_argument('--verbose')
options.add_argument('--safebrowsing.disable_download_protection')
options.add_argument("safebrowsing-disable-extension-blacklist")
s = Service(ChromeDriverManager().install())

# step 1 - Convert all audio files to wav type concurrently in Constants.py
convertWavThread(ThreadsNum, AudioFiles)
# If Num_threads > audio files, adjust threads equal to audio files
AudioNum = len(os.listdir(AudioFiles))
if Num_threads > AudioNum:
    Num_threads = AudioNum
    print('Changed number of thread(s) to ' + str(AudioNum))
else:
    print('Changed number of thread(s) remained as ' + str(Num_threads))
ThreadsNum = Num_threads
