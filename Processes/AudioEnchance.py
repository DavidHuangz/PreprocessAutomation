from selenium import webdriver
import time
# Other files
from HelperFunctions import *
from Constants import *


def enhance_audio(dataChunks):
    URL = 'https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/AudioEnhance'

    # Output file directorys
    prefs = {"download.default_directory": AudioEnhanceOutput,
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "safebrowsing.enabled": True
             }
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=s, options=options)
    driver.get(URL)

    print('Starting enhancing audio automation')
    checkPageLoad(driver)

    # Accept privacy policy
    clickElement('//*[@id="ngdialog1"]/div[2]/div/button', driver)
    print('Accept privacy policy')

    # edit sampling frequency to 16000Hz
    fillForm('/html/body/div[3]/div/div/upload-element-multiple/div/div[2]/div/div/div[1]/div/div[6]/span[2]/input',
             16000, driver)
    print('sampling frequency to 16000Hz')

    # add audio files
    print('Uploading multiple audio files...')
    uploadToFile("//*[@id='ngf-dropArea']", dataChunks, 1, driver)
    print('Upload complete!')

    # click accept terms
    clickElement("//*[@id='touReadCheckbox']", driver)
    print('Accept terms conditions')

    # click upload file
    clickElement('/html/body/div[3]/div/div/upload-element-multiple/div/div[1]/div[6]/button[1]', driver)
    print('Accept upload')

    # click run services
    print('Run services...')
    while True:
        if not downloading(driver):
            time.sleep(2)  # Extra delay for downloading
            clickElement('/html/body/div[3]/div/div/upload-element-multiple/div/div[3]/div/div[1]/div[2]/div', driver)
            print('Run service')
            break

    # click download zips
    print('processing files...')
    while True:
        if not downloading(driver):
            time.sleep(2)  # Extra delay for downloading
            clickElement('/html/body/div[3]/div/div/upload-element-multiple/div/div[3]/div/div[2]/div[2]', driver)
            print('Download zips')
            break

    # Wait for download to complete
    isDownloadComplete(AudioEnhanceOutput)

    # Extract the zips files
    unzipFile(AudioEnhanceOutput)

    # Close AudioEnhance
    driver.close()
    print('AudioEnhance closed')
