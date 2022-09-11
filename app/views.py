from crypt import methods
from app import app
from app import q
from app.tasks import count_words

from flask import render_template, request

from time import strftime

@app.route("/")
def index():
    return "Hello World"

@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    
    jobs = q.jobs # get the job in the queue
    message = None
    
    if request.args:
        
        url = request.args.get("url")
        
        print(url)
        task = q.enqueue(count_words, url)
        
        print(f"task is : {task.connection}")
        jobs = q.jobs
        
        q_len = len(q)
        print(f"JOBS IS {jobs}")
        message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {q_len} jobs queued"
        
    return render_template("add_task.html", message=message, jobs=jobs)
