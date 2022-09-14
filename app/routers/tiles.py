from fastapi import Request, Form, APIRouter, File, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json
from dotenv import load_dotenv
from typing import Optional
load_dotenv()

router = APIRouter()
templates = Jinja2Templates(directory="templates/")

AUDIO_EXTS = ['.wav', '.WAV'] #Can be extended

RHASSPY_URL = "http://localhost:12101"
RESPONSE_TSV_PATH = 'data/answers.tsv'

# garden = {"cherry tomato": "X7Hr9X4I1NY", "orchids": "LxkLc3arKHU", "roses": "OYbbldGNbr8", "mint": "Hw3HXrdt20o", "jalapeno": "i6NrodYFNhg",
#           "idea":"LdxltzhYjHE", "ants":"62A2_gKuBaU"}

# keywords = {"idea":["idea", "ideas", "start"], "ants":["ant", "ants"], "roses":["roses", "rose"], 
#             "cherry tomato":["cherry", "tomato", "tomatoes"], "mint":["mint"], "jalapeno":["jalapeno", "pepper"]}

def say(text):
    url = RHASSPY_URL + "api/text-to-speech"
    requests.post(url, text)

def read_response_data(tsv_path):
    import csv

    with open(tsv_path, newline='') as pscfile:
        reader = csv.reader(pscfile, delimiter='\t')
        next(reader)
        results = dict(reader)  # pull in each row as a key-value pair

    return results

response_data = read_response_data(RESPONSE_TSV_PATH)

print(response_data)

@router.get("/tilesrpi", response_class=HTMLResponse)
def get_tiles(request: Request, intent: Optional[str] = None):
    
    return templates.TemplateResponse('tilesrpi.html', context={'request': request})

@router.post("/tilesrpi/intent")
def post_tiles(intentstr: str = Form(...)):
    intentobj = json.loads(intentstr)
    intent = intentobj['intent']['name']
    slots = intentobj['slots']

    response = response_data.get(intent)

    if response:
        say(response)
        return {"found":False, "id": ""}
    else:
        print("ERROR: intent answer not specified")

    # if intent == 'Grow' and slots['plant'] in garden:
    #     plant = slots['plant']
    #     print(intent, plant)

    #     say("Here's a video on how to grow" + plant)

    #     video_id = garden.get(plant)
    #     print('video_id', video_id)
    #     return {"found":True, "id": video_id}
    # elif intent == 'Prevent':
    #     toprevent = slots['toprevent']
    #     print(intent, toprevent)

    #     say("Here's some tips on how to stop" + toprevent)

    #     video_id = garden.get(toprevent)
    #     print('video_id', video_id)
    #     return {"found":True, "id": video_id}
    # elif intent == 'Stop':
    #     print("Stop")
    #     return {"found":False, "id":""}
    # else:
    #     return {"found":False, "id":""}
