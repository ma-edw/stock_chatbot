FROM python:3.11.9-bookworm

WORKDIR /app

COPY requirements.txt ./
COPY chainlit-class.json ./
COPY ./.chainlit ./
COPY chainlit.md ./
COPY app.py ./

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["chainlit", "run", "-h", "app.py"]

