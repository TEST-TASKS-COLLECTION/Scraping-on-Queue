FROM python:3.10.7-alpine3.16
WORKDIR /code
COPY requirements.txt /code
RUN pip install -r requirements.txt --no-cache-dir
COPY . /code
CMD ["python", "run.py"]