import os
import concurrent.futures
from random import shuffle
from glob import glob
from pydub import AudioSegment
import time
from Constants import ThreadsNum, AudioFiles


def convertToWav():
    rawAudioFiles = len(os.listdir(AudioFiles))
    print('Starting with: ' + str(rawAudioFiles) + ' files')

    # Change working directory
    os.chdir(AudioFiles)
    try:
        extension_list = ('.m4a', '.mp4')
        # Previously needed to change directories, merged this together with the personal pepeha script, no longer
        # needs it
        audio_files = glob(AudioFiles + '/*')
        shuffle(audio_files)  # shuffle files for greater efficiency for multithreading
        # Goes through the dataset to check for recordings that are either mp4 or m4a
        for file in audio_files:
            for extension in extension_list:
                if extension in file:
                    wav_filename = os.path.splitext(os.path.basename(file))[0]
                    AudioSegment.from_file(file).export(wav_filename + '.wav', format='wav')
                    os.remove(file)
                    print(file + ' converted to WAV, removed original.')

    except Exception as e:
        print("Error with conversion \n" + str(e))
        time.sleep(ThreadsNum / 100 + 1)  # scalable delay for threads accessing same file
        convertToWav()  # recursive


def threadingConvertToWav():
    startAudioConversion = time.perf_counter()

    # Multithreading
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(convertToWav) for _ in range(ThreadsNum)]
        for f in concurrent.futures.as_completed(results):
            print(f.result())

    finishAudioConversion = time.perf_counter()

    # get number of files
    listX = os.listdir(AudioFiles)
    listOfFiles = len(listX)
    print('Conversion completed!\n' + 'Total files converted: ' + str(listOfFiles))
    print(
        f'Finished in {round(finishAudioConversion - startAudioConversion, 2)} second(s)' + ' with ' + str(
            ThreadsNum) + ' threads')
