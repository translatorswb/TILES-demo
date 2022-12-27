from fastapi import Request, Form, APIRouter, File, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json
import os
import pygame
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

AUDIO_EXTS = ['.wav', '.WAV'] #Can be extended

RHASSPY_URL = os.environ.get('RHASSPYURL') or "http://rhasspy:12101"
RESPONSE_TSV_PATH = os.environ.get('RESPONSETSV') or 'data/covid_hin.tsv'
ANSWERS_AUDIO_PATH = os.environ.get('AUDIODIR') or 'data/audio'

if os.path.exists(RESPONSE_TSV_PATH):
    print('Responses path:', RESPONSE_TSV_PATH)
else:
    print("Responses file not found", RESPONSE_TSV_PATH)

if os.path.exists(ANSWERS_AUDIO_PATH) and os.path.isdir(ANSWERS_AUDIO_PATH):
    print('Audio responses path:', ANSWERS_AUDIO_PATH)
else:
    print("Audio responses path not found", ANSWERS_AUDIO_PATH)

def say(text):
    url = RHASSPY_URL + "/api/text-to-speech"
    requests.post(url, text.encode('utf-8'))

def play(audio):
    pygame.mixer.init()
    pygame.mixer.music.load(audio)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy() == True:
        continue

def read_response_data(tsv_path):
    import csv
    row_no = 1
    results = {}
    with open(tsv_path, newline='') as pscfile:
        firstline = True
        for line in pscfile.readlines():
            if firstline:
                firstline = False
                continue
            try:
                line_info = line.strip().split('\t')
                if len(line_info) == 2:
                    intent_id, answer = line_info
                    audio_path = None
                elif len(line_info) == 3:
                    intent_id, answer, audio_path = line_info

                results[intent_id] = {'text': answer, 'audio': audio_path}
            except:
                print("problem in row", row_no)
                print(line)
            row_no += 1
        
    print("Successfully read answers sheet. #intents:", len(results))
    return results

response_data = read_response_data(RESPONSE_TSV_PATH)

@router.get("/tilesrpi", response_class=HTMLResponse)
def get_tiles(request: Request, intent: Optional[str] = None):
    
    return templates.TemplateResponse('tilesrpi.html', context={'request': request})

@router.post("/tilesrpi/intent")
def post_tiles(intentstr: str = Form(...)):
    intentobj = json.loads(intentstr)
    intent = intentobj['intent']['name']
    slots = intentobj['slots']
    
    print("intent", intent)

    response = response_data.get(intent)

    if response:
        print("response", response)
        if response['audio']:
            full_audio_path = os.path.abspath(os.path.join(ANSWERS_AUDIO_PATH, response['audio']))
            if os.path.exists(full_audio_path):
                print("play", full_audio_path)
                play(full_audio_path)
            else:
                print(f"Couldn't file audio for intent {intent} in path {full_audio_path}. Using TTS instead")
                say(response['text'])
        else:
            print("say", response['text'])
            say(response['text'])
        return {"found":False, "id": ""}
    else:
        print("Answer not specified for intent", intent)

