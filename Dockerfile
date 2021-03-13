FROM python:3.8-alpine

COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r ${REQUIREMENTS:-requirements.txt}

COPY main.py .

CMD python /app/bot.py
