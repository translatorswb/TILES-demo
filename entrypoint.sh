sleep 10
uvicorn app.main:app --reload --port 8080 --host 0.0.0.0  --log-config logging.conf
