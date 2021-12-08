import concurrent.futures
import os.path

# Other files
from Processes.AudioEnchance import enhance_audio
from Processes.WebMAUS import WebMAUS_process
from Processes.G2P import *
from Processes.ConvertToWav import threadingConvertToWav
from HelperFunctions import *
from Constants import Num_threads


def main():
    t1 = time.perf_counter()

    threadingConvertToWav()  # step 1 - Convert all audio files to wav type
    # If Num_threads > audio files, adjust threads equal to audio files
    modifyConstant(Num_threads, AudioFiles)

    # Concurrent datachunks processing for each thread
    dataChunks = []
    for x in range(Num_threads):
        dataChunks.append(x)

    # Empty all relevant folders used for processing
    emptyFolder(AudioEnhanceOutput)
    time.sleep(0.5)  # Extra delay for deleting
    emptyFolder(TextFile)
    time.sleep(0.5)  # Extra delay for deleting
    emptyFolder(G2POutputFiles)
    time.sleep(0.5)  # Extra delay for deleting
    emptyFolder(WebMAUSOutputFile)

    makeTextFile()  # step 2 - Make all text files for G2P - .Par files

    dataChunkProcess(AudioFiles, '')  # step 3 - Separate audio into chunks for each thread
    # Enhance audio process
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(enhance_audio, dataChunks)  # step 4 - processing raw audio to enhance audio

    dataChunkProcess(TextFile, '')  # step 5 - Separate text files into chunks for each thread
    # Enhance G2P process
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(G2P_process, dataChunks)  # step 6 - processing enhance audio to .par files

    dataChunkProcess(AudioEnhanceOutput, G2POutputFiles)  # step 7 - Two separate chunks for two uploads for WebMAUS
    # Enhance WebMAUS process for generating text grids
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(WebMAUS_process, dataChunks)  # step 8 - processing text grids from .par and enhanced audio files

    t2 = time.perf_counter()

    print(f'Finished in {round(t2 - t1, 2)} second(s)' + ' with ' + str(Num_threads) + ' thread(s)')
    processedFiles = os.listdir(WebMAUSOutputFile)
    print('Processed ' + str(len(processedFiles)) + ' files')


if __name__ == '__main__':
    main()
