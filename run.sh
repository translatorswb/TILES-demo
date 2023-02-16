export RESPONSETSV=data/answers_climate_hin.tsv
export RHASSPYURL="http://localhost:12101"
export AUDIODIR="../TILES-audio"
export FALLBACKAUDIOPATH=""
export SKIPAUDIOPLAY=1
export TTSFALLBACK=0
uvicorn app.main:app --reload --port 8080
