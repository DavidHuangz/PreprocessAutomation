from glob import glob
from Constants import *
import shutil


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
