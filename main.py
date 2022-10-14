from typing import List
from gtts import gTTS
from mutagen.mp3 import MP3 as mp3
import pygame
import os
import time
import sys


BUFFER_FILE_NAME = '.python-japanese-buffer.mp3'


def speak(string: str):
    tts = gTTS(text=string + ' さん', lang='ja')
    tts.save(BUFFER_FILE_NAME)

    pygame.mixer.init()
    pygame.mixer.music.load(BUFFER_FILE_NAME)

    mp3_length = mp3(BUFFER_FILE_NAME).info.length

    pygame.mixer.music.play(1)
    time.sleep(mp3_length + 0.25)

    pygame.mixer.music.stop()

    os.remove(BUFFER_FILE_NAME)


class Name(object):
    surface: str
    kana: str



def load_csv(filename: str) -> List[Name]:
    namelist: List[Name] = []

    with open(filename, 'r') as f:
        t = f.read()
        for line in t.split('\n'):
            if line.strip() == '':
                continue

            n = Name()
            n.surface, n.kana = map(lambda x: x.strip(), line.split(','))
            namelist.append(n)
    
    return namelist


def main():
    filename = sys.argv[1]
    names = load_csv(filename)
    kesseki_name: List[Name] = []
    pass_name: List[Name] = []

    print("=== 出欠とるとる君 by kekeho ===\n")
    print("操作方法:\n出席している: ENTER, 欠席: n, パス: p, 再度読み上げ: r\n")

    for name in names:
        while True:
            print(f'{name.surface} ({name.kana})')
            speak(name.kana)
            result = input()

            if result == 'r':
                continue

            if result == 'n':
                kesseki_name.append(name)
            
            if result == 'p':
                pass_name.append(name)

            break
    
    print("\n\n==== [欠席者] ====")
    for name in kesseki_name:
        print(name.surface)

    print("\n==== [パス/不明] ====")
    for name in pass_name:
        print(name.surface)



if __name__ == "__main__":
    main()
