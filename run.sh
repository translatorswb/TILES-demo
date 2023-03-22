export RESPONSETSV=data/answers_climate_hin.tsv
export RHASSPYURL="http://localhost:12101"
export AUDIODIR="../TILES-audio"
export FALLBACKAUDIOPATH="data/GV_fallback_hin_climate_v2.mp3"
export COMPLETIONAUDIOPATH="data/GV_completion_hin_climate.mp3"
export SKIPAUDIOPLAY=1
export TTSFALLBACK=0
uvicorn app.main:app --reload --port 8080  --log-config logging.conf
