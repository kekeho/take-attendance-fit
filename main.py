from typing import List, Optional
from enum import Enum
from gtts import gTTS
from mutagen.mp3 import MP3 as mp3
import pygame
import os
import time
import sys
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


DEBUG = False


BUFFER_FILE_NAME = '.python-japanese-buffer.mp3'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
GOOGLE_CREDS = None

# The file token.json stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.json'):
    GOOGLE_CREDS = Credentials.from_authorized_user_file('token.json', SCOPES)
# If there are no (valid) credentials available, let the user log in.
if not GOOGLE_CREDS or not GOOGLE_CREDS.valid:
    if GOOGLE_CREDS and GOOGLE_CREDS.expired and GOOGLE_CREDS.refresh_token:
        GOOGLE_CREDS.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        GOOGLE_CREDS = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.json', 'w') as token:
        token.write(GOOGLE_CREDS.to_json())


class State(Enum):
    ATTEND = 1
    NOT_ATTEND = 2
    OTHER = 3



class Name(object):
    id: int  # zero origin
    surface: str
    kana: str  # かな
    status: Optional[State]

    def __init__(self, surface: str, kana: str):
        self.surface = surface
        self.kana = kana
        self.status = None


def get_namelist() -> List[Name]:
    try:
        spreadsheet = '1VgaJB7TZybm2Fgwub8tGVOpCXXRIPQE3mZ7dwUOwn5M'
        service = build('sheets', 'v4', credentials=GOOGLE_CREDS)
        sheet = service.spreadsheets()
        names_range = sheet.values().get(spreadsheetId=spreadsheet,
                                    range='出席課題集計!A3:B32').execute()
        
        # 行ごと取ってくる
        values = names_range.get('values', [])
        result = []
        for v in values:
            result.append(Name(v[0], v[1]))
        
        return result
    except HttpError as err:
        print(err)


def set_state(n: int, attendees: List[Name]):
    try:
        col = chr(ord('C') + n)
        spreadsheet = '1VgaJB7TZybm2Fgwub8tGVOpCXXRIPQE3mZ7dwUOwn5M'
        service = build('sheets', 'v4', credentials=GOOGLE_CREDS)
        sheet = service.spreadsheets()
        
        state_list = []
        for name in attendees:
            if name.status == State.ATTEND:
                state_list.append(['○',])
            else:
                state_list.append(['',])

        sheet.values().update(
            spreadsheetId=spreadsheet,
            range=f'出席課題集計!{col}3:{col}32',
            valueInputOption='RAW',
            body={'values': state_list}
        ).execute()

    except HttpError as err:
        print(err)




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



def main():
    names = get_namelist()
    result_names: List[Name] = []

    print("=== 出欠とるとる君 by kekeho ===\n")

    print("何回目の授業ですか?")
    n = int(input())

    print("操作方法:\n出席している: ENTER, 欠席: n, パス: p, 再度読み上げ: 任意のキー\n")

    if DEBUG == False:
        for name in names:
            while True:
                print(f'{name.surface} ({name.kana})')
                speak(name.kana)
                result = input()

                if result == 'n':
                    name.status = State.NOT_ATTEND
                
                elif result == 'p':
                    name.status = State.OTHER
                
                elif result == '':
                    name.status = State.ATTEND
                else:
                    continue

                result_names.append(name)
                break
    else:
        # Debug
        for name in names:
            name.status = State.ATTEND
            result_names.append(name)
    
    set_state(n, result_names)

    

if __name__ == "__main__":
    main()
