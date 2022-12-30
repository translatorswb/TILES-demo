export RESPONSETSV=data/answers_climate_hin.tsv
export RHASSPYURL="http://localhost:12101"
export AUDIODIR="../TILES-audio"
export FALLBACKAUDIOPATH="data/fallback_hin_climate.mp3"
uvicorn app.main:app --reload --port 8080
