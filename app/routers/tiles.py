from fastapi import Request, Form, APIRouter, File, UploadFile, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import requests
import json
import os
from typing import Optional
from pydub import AudioSegment
from pydub.playback import play
import logging 

router = APIRouter()
templates = Jinja2Templates(directory="templates/")
logger = logging.getLogger(__name__) 

AUDIO_EXTS = ['.wav', '.WAV'] #Can be extended

RHASSPY_URL = os.environ.get('RHASSPYURL') or "http://rhasspy:12101"
RESPONSE_TSV_PATH = os.environ.get('RESPONSETSV') or 'data/covid_hin.tsv'
ANSWERS_AUDIO_PATH = os.environ.get('AUDIODIR') or './audio'
INTENT_FALLBACK_AUDIO_PATH = os.environ.get('FALLBACKAUDIOPATH') or ''
INTENT_FALLBACK_TEXT = "मुझे वह समझ में नहीं आया। क्या आप फिर से दोहरा सकते हैं? मैं जलवायु परिवर्तन के बारे में आपके सवालों का जवाब दे सकता हूं।"
TTSFALLBACK = os.environ.get('TTSFALLBACK') or 0

last_intentid = None

print("=======TILES-DEMO=======")
#Debug flags
SKIPAUDIOPLAY = os.environ.get('SKIPAUDIOPLAY') or 0
if SKIPAUDIOPLAY == "1":
    msg = f"DEBUG: Skipping audio play"
    print(msg)
    logger.warning(msg)
    SKIPAUDIOPLAY = True
else:
    SKIPAUDIOPLAY = False

if os.path.exists(RESPONSE_TSV_PATH):
    msg = f"Responses path: {RESPONSE_TSV_PATH}"
    print(msg)
    logger.info(msg)
else:
    msg = f"Responses file not found: {RESPONSE_TSV_PATH}"
    print(msg)
    logger.warning(msg)

if os.path.exists(ANSWERS_AUDIO_PATH) and os.path.isdir(ANSWERS_AUDIO_PATH):
    msg = f"Audio responses path: {ANSWERS_AUDIO_PATH}"
    print(msg)
    logger.info(msg)
else:
    msg = f"Audio responses path not found: {ANSWERS_AUDIO_PATH}"
    print(msg)
    logger.warning(msg)
    
if INTENT_FALLBACK_AUDIO_PATH and os.path.exists(INTENT_FALLBACK_AUDIO_PATH):
    msg = f"Fallback audio path: {INTENT_FALLBACK_AUDIO_PATH}"
    print(msg)
    logger.info(msg)
else:
    msg = f"Fallback audio path not found: {INTENT_FALLBACK_AUDIO_PATH}"
    print(msg)
    logger.warning(msg)

if TTSFALLBACK == "1":
    msg = f"Fallback with TTS on"
    print(msg)
    logger.warning(msg)
    TTSFALLBACK = True
else:
    TTSFALLBACK = False
    
def say(text):
    url = RHASSPY_URL + "/api/text-to-speech"
    requests.post(url, text.encode('utf-8'))
    logger.info(f"TTS: {text}")

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
                msg = f"problem in row {row_no}: {line}"
                print(msg)
                logger.error(msg)
            row_no += 1
        
    msg = f"Successfully read answers sheet. #intents: {len(results)}"\
           "\n========================"
    print(msg)
    logger.info(msg)
    
    return results

response_data = read_response_data(RESPONSE_TSV_PATH)

@router.get("/tilesrpi", response_class=HTMLResponse)
def get_tiles(request: Request, intent: Optional[str] = None):
    
    return templates.TemplateResponse('tilesrpi.html', context={'request': request})

@router.post("/tilesrpi/intent")
def check_intent(intentstr: str = Form(...)):
    global last_intentid
    intentobj = json.loads(intentstr)
    intent = intentobj['intent']['name']
    slots = intentobj['slots']
    conf = intentobj['intent']['confidence']
        
    msg = f"QUERY: {intentobj['text']}, INTENT: {intent}, CONF:{conf:.2f}"
    print(msg)
    logger.info(msg)

    response = response_data.get(intent)

    if response:
        last_intentid = intent
        
        return {"found":True, "id": intent, "imageid": "imageid:"+intent}
    else:
        last_intentid = None
        return {"found":False, "id": intent, "imageid": "imageid:"+intent}

@router.post("/tilesrpi/wake")
def wake_request():
    url = RHASSPY_URL + "/api/listen-for-command"
    try:
        requests.post(url)
        logger.info(f"WAKE")
        print("WAKE")
        return {"connection":True}
    except:
        msg = f"ERROR: Couldn't establish connection with rhasspy on {url}"
        logger.info(msg)
        print(msg)
        return {"connection":False} ## CHANGE TO FALSESS


@router.post("/tilesrpi/play")
def audio_play():
    global last_intentid

    if last_intentid:
        if response_data[last_intentid]['audio']:
            full_audio_path = os.path.abspath(os.path.join(ANSWERS_AUDIO_PATH, response_data[last_intentid]['audio']))

            if os.path.exists(full_audio_path):
                msg = f"PLAY: {full_audio_path}\n--------------------------"
                print(msg)
                logger.info(msg)
                # TODO: Plays directly from python. It'd be much better to play from the front-end
                audioseg = AudioSegment.from_mp3(full_audio_path)
                if not SKIPAUDIOPLAY:
                    play(audioseg)
                return {}
            elif TTSFALLBACK:
                msg = f"Couldn't find audio file for intent {intent} in path {full_audio_path}. Using TTS instead"
                print(msg)
                logger.warning(msg)
                say(response_data[last_intentid]['text'])
                return {}
        elif TTSFALLBACK:
            msg = f"No audio file specified for intent {intent}. Using TTS instead"
            print(msg)
            logger.warning(msg)
            
            say(response_data[last_intentid]['text'])
            return {}
    else:
        full_audio_path = INTENT_FALLBACK_AUDIO_PATH
        if full_audio_path:
            msg = f"PLAY: {full_audio_path}\n--------------------------"
            print(msg)
            logger.info(msg)
            # TODO: Plays directly from python. It'd be much better to play from the front-end
            audioseg = AudioSegment.from_mp3(full_audio_path)
            if not SKIPAUDIOPLAY:
                play(audioseg)
            return {}
        elif TTSFALLBACK:
            msg = f"Couldn't find audio file for fallback in path {full_audio_path}. Using TTS instead"
            print(msg)
            logger.warning(msg)
            
            if not SKIPAUDIOPLAY:
                say(INTENT_FALLBACK_TEXT)
            return {}



