FROM python:3.7.2-alpine

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN pip install --no-cache-dir -r requirements.txt

COPY src/ /usr/src/app

# CMD ["flask", "run", "-h", "0.0.0.0"]
# CMD ["gunicorn", "-w", "5", "-b", "unix:/tmp/gunicorn.sock", "main:app"]
