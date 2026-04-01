FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y ffmpeg

COPY . .

RUN pip install -r requirements.txt

CMD ["python", "bot/main.py"]
