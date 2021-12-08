import concurrent
import os
from random import shuffle
from glob import glob
from pydub import AudioSegment
import time


def convertToWav(threads, directory):
    rawAudioFiles = len(os.listdir(directory))
    print('Starting with: ' + str(rawAudioFiles) + ' files')

    # Change working directory
    os.chdir(directory)
    try:
        extension_list = ('.m4a', '.mp4')
        # Previously needed to change directories, merged this together with the personal pepeha script, no longer
        # needs it
        audio_files = glob(directory + '/*')
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
        time.sleep(threads / 100 + 1)  # scalable delay for threads accessing same file
        convertToWav(threads, directory)  # recursive


def convertWavThread(threads, directory):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        results = [executor.submit(convertToWav, threads, directory) for _ in range(threads)]
        for f in concurrent.futures.as_completed(results):
            print(f.result())
    print('Conversion completed!\n' + 'Total files converted: ' + str(len(os.listdir(directory))))
