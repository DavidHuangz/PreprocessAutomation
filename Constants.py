# install in terminal
# pip install selenium
# pip install chromedriver-py
# pip install webdriver-manager
# pip install pydub

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

# Configurable settings
NoBrowser = True
num_threads = 5
ThreadsNum = num_threads

AudioFiles = r'D:\pepaha\Input\Audio'
AudioEnhanceOutput = r'D:\pepaha\Output\genFiles\AudioEnhanceOutput'
textFile = r'D:\pepaha\Input\Text'
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
options.add_argument("--safebrowsing-disable-download-protection");
options.add_argument("safebrowsing-disable-extension-blacklist");
s = Service(ChromeDriverManager().install())
