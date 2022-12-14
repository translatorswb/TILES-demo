from fastapi import Request, Form, APIRouter, File, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json
import os
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

AUDIO_EXTS = ['.wav', '.WAV'] #Can be extended

RHASSPY_URL = os.environ.get('RHASSPYURL') or "http://localhost:12101"
RESPONSE_TSV_PATH = os.environ.get('RESPONSETSV') or 'data/answers.tsv'

print('Responses path:', RESPONSE_TSV_PATH)

def say(text):
    url = RHASSPY_URL + "/api/text-to-speech"
    requests.post(url, text.encode('utf-8'))

def read_response_data(tsv_path):
    import csv
    row_no = 1
    results = {}
    with open(tsv_path, newline='') as pscfile:
        for line in pscfile.readlines():
            try:
                key, val = line.strip().split('\t')
                results[key] = val
            except:
                print("problem in row", row_no)
                print(line)
            row_no += 1
        
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
        say(response)
        return {"found":False, "id": ""}
    else:
        print("ERROR: intent answer not specified")

