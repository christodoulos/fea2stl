FROM pymesh/pymesh

COPY . /app

WORKDIR /app

RUN pip install numpy-stl

CMD ["cd", "/app"]

CMD ["python", "/app/example.py"]
