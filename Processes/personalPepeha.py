from glob import glob
from Constants import *


def personalPepeha():
    file = PersonalPepehaText
    # Go to data directory
    data_dir = AudioFiles
    # Change working directory
    os.chdir(data_dir)

    # Iterate all audio files
    audio_files = glob(data_dir + '/*.wav')

    # Goes through the dataset to check for recordings that are either mp4 or m4a
    with open(file) as f:
        contents = f.read().splitlines()

    # Goes through the data and removes the personal pepeha
    for p in contents:
        for file in audio_files:
            wav_filename = os.path.splitext(os.path.basename(file))[0]
            if wav_filename == p:
                print(wav_filename + " Removed")
                os.remove(file)

    print('PersonalPepeha completed!\n' + 'Total files left: ' + str(len(os.listdir(AudioFiles))))
