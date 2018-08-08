FROM python:2-alpine

ENV PERMS=0777

VOLUME [ "/data" ]

WORKDIR /usr/src/watchdog

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /data

CMD [ "python", "/usr/src/watchdog/app.py" ]
