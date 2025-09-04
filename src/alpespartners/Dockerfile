FROM python:3.12

EXPOSE 5000/tcp

COPY src/alpespartners/requirements.txt ./
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY ../../ /app
WORKDIR /app

CMD [ "flask", "--app", "./src/alpespartners/api", "run", "--host=0.0.0.0"]
