from selenium import webdriver
import time
# Other files
from HelperFunctions import *
from Constants import *


def G2P_process(dataChunks):
    URL = 'https://clarin.phonetik.uni-muenchen.de/BASWebServices/interface/Grapheme2Phoneme'

    # Output file directory
    prefs = {"download.default_directory": G2POutputFiles}
    options.add_experimental_option("prefs", prefs)

    driver = webdriver.Chrome(service=s, options=options)
    driver.get(URL)

    print('Starting G2P automation')
    checkPageLoad(driver)

    # Accept privacy policy
    clickElement('//*[@id="ngdialog1"]/div[2]/div/button', driver)
    print('Accept privacy policy')

    # Upload file
    print('Uploading multiple files...')
    uploadToFile("//*[@id='ngf-dropArea']", dataChunks, 1, driver)
    print('Upload complete!')

    # change dropdown format output to bpfs
    clickElement("//select[@id='oform']/option[@value='bpfs']", driver)
    print('Change format to bpfs')

    # change dropdown language to user defined
    clickElement("//select[@id='lng']/option[@value='und']", driver)
    print('Change language')

    # click accept terms
    clickElement("//*[@id='touReadCheckbox']", driver)
    print('Accept terms conditions')

    # click upload file
    clickElement('/html/body/div[3]/div/div/upload-element-multiple/div/div[1]/div[6]/button[1]', driver)
    print('Accept upload')

    # Upload Imap mapping file
    print('uploading files ...')
    while True:
        if not downloading(driver):
            uploadOneFile(
                '/html/body/div[3]/div/div/upload-element-multiple/div/div[2]/div/div/div[1]/div/div[5]/span[2]/input',
                ImapText, driver)
            print('Upload files complete')
            break

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
            # Wait for other threads to finish downloading to prevent duplicate zip files
            waitForThreadsDownload(dataChunks, G2POutputFiles)
            clickElement('/html/body/div[3]/div/div/upload-element-multiple/div/div[3]/div/div[2]/div[2]', driver)
            print('Download zips')
            break

    # Wait for download
    isDownloadComplete(G2POutputFiles)

    # Extract the zips files
    unzipFile(G2POutputFiles)

    # Close G2P
    driver.close()
    print('G2P closed for thread ' + str(dataChunks))
