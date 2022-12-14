export RESPONSETSV=data/rhasspy_responses_hin.tsv
export RHASSPYURL="http://localhost:12101"
uvicorn app.main:app --reload --port 8080
