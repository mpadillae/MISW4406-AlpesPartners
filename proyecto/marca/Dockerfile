FROM python:3.12

EXPOSE 8000/tcp

WORKDIR /app

COPY requirements.txt .
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "main.py"]
