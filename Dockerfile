FROM python:3.8.5

RUN python -m pip install --upgrade pip
RUN mkdir /app
ADD . /app
WORKDIR /app
RUN pip3 install -r /app/requirements.txt

CMD python /app/main.py