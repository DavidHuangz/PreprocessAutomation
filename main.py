# install in terminal
# pip install selenium
# pip install chromedriver-py
# pip install webdriver-manager
# pip install pydub

import concurrent.futures
import os.path

# Other files
from AudioEnchance import enhance_audio
from ConvertToWav import threadingConvertToWav
from WebMAUS import WebMAUS_process
from G2P import *
from HelperFunctions import *


def main():
    t1 = time.perf_counter()

    # Concurrent datachunks processing for each thread
    dataChunks = []
    for x in range(num_threads):
        dataChunks.append(x)

    # Empty all relevant folders used for processing
    emptyFolder(AudioEnhanceOutput)
    time.sleep(1)  # Extra delay for deleting
    emptyFolder(textFile)
    time.sleep(1)  # Extra delay for deleting
    emptyFolder(G2POutputFiles)
    time.sleep(1)  # Extra delay for deleting
    emptyFolder(WebMAUSOutputFile)

    threadingConvertToWav()  # step 1 - Convert all audio files to wav type

    makeTextFile()  # step 2 - Make all text files for G2P - .Par files

    dataChunkProcess(AudioFiles, '')  # step 3 - Separate audio into chunks for each thread
    # Enhance audio process
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(enhance_audio, dataChunks)  # step 4 - processing raw audio to enhance audio

    dataChunkProcess(textFile, '')  # step 5 - Separate text files into chunks for each thread
    # Enhance G2P process
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(G2P_process, dataChunks)  # step 6 - processing enhance audio to .par files

    dataChunkProcess(AudioEnhanceOutput, G2POutputFiles)  # step 7 - Two separate chunks for two uploads for WebMaus
    # Enhance WebMAUS process for generating text grids
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(WebMAUS_process, dataChunks)  # step 8 - processing text grids from .par and enhanced audio files

    t2 = time.perf_counter()

    print(f'Finished in {round(t2 - t1, 2)} second(s)' + ' with ' + str(num_threads) + ' thread(s)')
    processedFiles = os.listdir(WebMAUSOutputFile)
    print('Processed ' + str(len(processedFiles)) + ' files')


main()
