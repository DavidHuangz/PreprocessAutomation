from selenium import webdriver
import time
# Other files
from HelperFunctions import *
from Constants import *


def WebMAUS_process(dataChunks):
    URL = 'https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/WebMAUSGeneral'

    prefs = {"download.default_directory": WebMAUSOutputFile,
             "download.prompt_for_download": False,
             "download.directory_upgrade": True,
             "safebrowsing_for_trusted_sources_enabled": False,
             "safebrowsing.enabled": False}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=s, options=options)
    driver.get(URL)

    print('Starting WebMAUS General automation for thread ' + str(dataChunks))
    checkPageLoad(driver)

    # Accept privacy policy
    clickElement('//*[@id="ngdialog1"]/div[2]/div/button', driver)
    print('Accept privacy policy')

    # Add audio files-driver
    uploadToFile('//*[@id="ngf-dropArea"]', dataChunks, 1, driver)
    print('Upload Enhanced audio file(s)')

    # Add .par files that was outputted by G2P
    uploadToFile('//*[@id="ngf-dropArea"]', dataChunks, 2, driver)
    print('Upload .par text files G2P file(s)')

    # click accept terms
    clickElement('//*[@id="touReadCheckbox"]', driver)
    print('Accept terms conditions')

    # change dropdown language to indent. (samp)
    clickElement("//select[@id='LANGUAGE']/option[@value='sampa']", driver)
    print('Change language')

    # click upload file
    clickElement('/html/body/div[3]/div/div/upload-element-multiple/div/div[1]/div[6]/button[1]', driver)
    print('Accept upload')

    # Wait till downloads
    print('Running service...')
    while True:
        if not downloading(driver):
            time.sleep(2)
            clickElement('/html/body/div[3]/div/div/upload-element-multiple/div/div[3]/div/div[1]/div[2]/div', driver)
            time.sleep(2)  # Extra delay for downloading
            print('Run service complete!')
            break

    # Wait till processing
    print('processing files...')
    while True:
        if not downloading(driver):
            time.sleep(2)  # Extra delay for downloading
            # Wait for other threads to finish downloading to prevent duplicate zip files
            waitForThreadsDownload(dataChunks, WebMAUSOutputFile, driver)
            clickElement('/html/body/div[3]/div/div/upload-element-multiple/div/div[3]/div/div[2]/div[2]', driver)
            print('Click download zips')
            break

    # Wait for download
    isDownloadComplete(WebMAUSOutputFile, driver)

    # Extract the zips files
    unzipFile(WebMAUSOutputFile)

    # close WebMAUS
    driver.close()
    print('WebMAUS closed for thread ' + str(dataChunks))
