from flask import Flask
from redis import Redis
from rq import Queue

app = Flask(__name__)

r = Redis(host="redis") # with docker container
# r = Redis()
q = Queue(connection=r)


from app import views