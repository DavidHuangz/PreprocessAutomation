import os
import os.path
from glob import glob
import shutil
from zipfile import ZipFile
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

# Helper functions #
from Constants import *


def emptyFolder(folder):
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.remove(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    if os.path.isdir(folder):
        while os.listdir(folder):
            print(folder + " ... removing content")
        print(folder + " is empty")
    else:
        print(folder + " doesn't exist")

    print(folder + ' contents removed')


def makeTextFile():
    file_in = AudioFiles
    file_out = TextFile

    os.chdir(file_in)

    # Iterate all audio files
    audio_files = glob(file_in + '/*.wav')

    # Goes through the dataset to check for recordings that are either mp4 or m4a
    for file in audio_files:
        wav_filename = os.path.splitext(os.path.basename(file))[0]
        output = "{0}.audioenhance.txt".format(wav_filename)
        audioEnhance = open(output, "a", encoding="utf-8", errors='ignore')
        audioEnhance.write(PepehaPhrase)
        print('Generated text file for ' + wav_filename)
        audioEnhance.close()
        shutil.move(os.path.join(file_in, output), os.path.join(file_out, output))

    # Check all the text files are in the directory
    processedFiles = len(os.listdir(AudioFiles))
    textFileCount = len(os.listdir(file_out))
    while processedFiles > textFileCount:
        processedFiles = len(os.listdir(file_in))
        textFileCount = len(os.listdir(file_out))


def checkPageLoad(driver):
    delay = 1  # seconds
    try:
        # Check if element in the page (terms of usage) has successfully loaded
        WebDriverWait(driver, delay).until(EC.presence_of_element_located(
            (By.XPATH, '/html/body/div[3]/div/div/upload-element-multiple/div/div[3]/div/div[1]/div[1]/label')))
        print("Page successfully loaded!")
    except TimeoutException:
        print("Page still loading...")
        checkPageLoad(driver)


def clickElement(XPATH_element, driver):
    buttonToClick = driver.find_element(By.XPATH, XPATH_element)
    buttonToClick.click()


def fillForm(XPATH_element, Userinput, driver):
    driver.find_element(By.XPATH, XPATH_element).click()
    driver.find_element(By.XPATH, XPATH_element).clear()
    driver.find_element(By.XPATH, XPATH_element).send_keys(Userinput)


def findFile(directory):
    fileName = ''
    for subdir, dirs, files in os.walk(directory):
        for file in files:
            # find file name
            fileName = file
    return os.path.join(directory, fileName)


def downloading(driver):
    try:
        elementCSS = driver.find_element(By.XPATH, '//*[@id="ngProgress-container"]/div[2]')
        if elementCSS.is_displayed():
            print(elementCSS.text)
            return True
    except Exception as e:
        print(e)
        print('complete!')
        return False


def unzipFile(directory):
    extension = ".zip"
    os.chdir(directory)  # change directory from working dir to dir with files

    zip_list = os.listdir(directory)  # dir is your directory path
    print('zip files: ' + str(len(zip_list)))

    try:
        # Extract all the contents of zip file to a directory
        print('extracting files...')
        for item in os.listdir(directory):  # loop through items in dir
            if item.endswith(extension):  # check for ".zip" extension
                file_name = os.path.abspath(item)  # get full path of files
                zip_ref = ZipFile(file_name)  # create zipfile object
                zip_ref.extractall(directory)  # extract file to dir
                print('Complete extraction')
                zip_ref.close()  # close file
                print('Removed zip file')
                os.remove(file_name)  # delete zipped file
    except Exception as e:
        print("Error with zip \n" + str(e))


def isDownloadComplete(directory):
    num_files = 0
    checkFiles = 0
    print('File downloading...')
    while checkFiles < Num_threads:
        for file in os.listdir(directory):
            if file.endswith(".zip"):
                num_files += 1
        checkFiles = num_files
        num_files = 0
    print('file fully downloaded')


def waitForThreadsDownload(dataChunks, directory):
    print('Waiting for thread ' + str(dataChunks - 1) + ' to finish downloading...')
    num_files = 0
    checkFiles = 0

    while checkFiles < dataChunks:
        for file in os.listdir(directory):
            if file.endswith(".zip"):
                num_files += 1
        checkFiles = num_files
        num_files = 0

    print('Downloading file for thread ' + str(dataChunks))


# uploading multiple files concurrently
def uploadToFile(XPATH_element, dataChunks, FileNum, driver):
    if FileNum == 1:
        driver.find_element(By.XPATH, XPATH_element).send_keys(eval('fileX{}'.format(dataChunks)))
    else:
        driver.find_element(By.XPATH, XPATH_element).send_keys(eval('fileY{}'.format(dataChunks)))


# uploading one file
def uploadOneFile(XPATH_element, data, driver):
    driver.find_element(By.XPATH, XPATH_element).send_keys(data)


# For main controller to prepare and separate chunks of data
def dataChunkProcess(directory1, directory2):
    # get full string
    counterThread = 0

    # Create dynamic variables
    for i in range(Num_threads):
        globals()['fileX{0}'.format(i)] = ""  # dynamic variables for upload 1
        if directory2 != '':
            globals()['fileY{0}'.format(i)] = ""  # dynamic variables for upload 2

    print('\n----------Separating files into chunks for each thread(s)----------\n')
    for subdir, dirs, files in os.walk(directory1):
        for file in files:
            # assign dynamic variables to string
            globals()['fileX{0}'.format(counterThread)] += '\n' + os.path.join(subdir, file)

            counterThread += 1
            if counterThread >= Num_threads:
                counterThread = 0

    # Reset counter
    counterThread = 0
    # If there's directory2 for second upload
    if directory2 != '':
        for subdir, dirs, files in os.walk(directory2):
            for file in files:
                # assign dynamic variables to string
                # Second upload used only for WebMaus
                globals()['fileY{0}'.format(counterThread)] += '\n' + os.path.join(subdir, file)

                counterThread += 1
                if counterThread >= Num_threads:
                    counterThread = 0
    print('----------Upload 1----------\n')
    for i in range(Num_threads):
        globals()['fileX{0}'.format(i)] = globals()['fileX{0}'.format(i)][1:]  # get rid of new line at end of string
        print('thread{}: '.format(i) + '\n' + eval('fileX{0}'.format(i)) + '\n')
    # If there's directory2 for second upload
    if directory2 != '':
        print('----------Upload 2----------\n')
        for i in range(Num_threads):
            globals()['fileY{0}'.format(i)] = globals()['fileY{0}'.format(i)][
                                              1:]  # get rid of new line at end of string
            print('thread{}: '.format(i) + '\n' + eval('fileY{0}'.format(i)) + '\n')


def modifyConstant(thread, directory):
    AudioNum = len(os.listdir(directory))
    if thread > AudioNum:
        global Num_threads
        global ThreadsNum
        Num_threads = AudioNum
        ThreadsNum = AudioNum
        print('Changed number of thread(s) to ' + str(Num_threads))
