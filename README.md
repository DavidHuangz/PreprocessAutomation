# Preprocessing raw audio files to text grid automation

## Requirements:
## Libraries to install in terminal
pip install selenium <br />
pip install chromedriver-py <br />
pip install webdriver-manager <br />
pip install pydub <br />

## 1. Create these Folders
1. Make these two folders in a directory  <br />
![step1](https://user-images.githubusercontent.com/52488862/145132475-f44ba6cd-b10d-4a09-958e-414c09fe1cc2.PNG)

1.1. Inside the "Input" file, add these folders  <br />
![step2](https://user-images.githubusercontent.com/52488862/145132557-b60ad200-3258-46c4-a388-0f11cc12e011.PNG)

1.2. Inside the "output" file, add these folders  <br />
![step3](https://user-images.githubusercontent.com/52488862/145132662-a9aa067b-9940-4a73-8750-71058c00264b.PNG)

1.2.1. Inside the "genFiles" file, add these folders  <br />
![step4](https://user-images.githubusercontent.com/52488862/145132710-feee7831-3b15-4470-a7e4-af9c981c9573.PNG)

## 2. Add the full directory path to the following variables in the "Constants.py" file
### Examples
AudioFiles = r'D:\Input\Audio' <br />

AudioEnhanceOutput = r'D:\Output\genFiles\AudioEnhanceOutput' <br />

TextFile = r'D:\Input\Text' <br />

ImapText = r'D:\Input\ImapText\TRMg2p.txt' <br />

G2POutputFiles = r'D:\Output\genFiles\G2P_output' <br />

WebMAUSOutputFile = r'D:\Output\WebMAUS_output' <br />

## 3. Add Input files
3.1. Inside the "Input", add your all your raw audio files inside "Audio" folder (e.g "Input\Audio\audio1") <br />
3.2. Inside the "Input", add your "TRMg2p" file inside "ImapText" folder (e.g Input\ImapText\TRMg2p.txt) <br />

## 4. Run code
4.1. Run main.py file <br />
