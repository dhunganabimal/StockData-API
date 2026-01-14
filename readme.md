# Stock Data API

## Environment Variables (.env)

```
DB_HOSTNAME=localhost
#DB_PORT=Port
DB_PASSWORD=DatabasePass
DB_NAME=DatabaseName
DB_USERNAME=DatabaseUsername

```

## Start Project

```bash
source ~/.env/bin/activate
pip install -r requirements.txt
uvicorn app.main:app -- --reload
```


