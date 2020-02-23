FROM python:3.8-slim-buster

COPY . /app

WORKDIR /app

RUN pip install -r requirements.txt

RUN python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps ucc2stl-chfrag

WORKDIR /app/examples

CMD ["python", "example.py"]
