FROM python:3.12

COPY src/notificaciones/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY ../../ /app
WORKDIR /app

CMD [ "python", "./src/notificaciones/main.py" ]