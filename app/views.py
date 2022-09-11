from crypt import methods
from app import app
from app import q, r
from app.tasks import count_words

from flask import render_template, request

from time import strftime

from rq.job import Job

from rq import get_current_job

@app.route("/")
def index():
    return "Hello World"

@app.route("/add-task", methods=["GET", "POST"])
def add_task():
    
    jobs = q.jobs # get the job in the queue
    message = None
    
    if request.args:
        
        url = request.args.get("url")
        cookie = request.args.get("cookie")
        
        print(url)
        task = q.enqueue(count_words, url, cookie, job_id=f"{cookie}")
        
        print(f"task is : {task.connection}")
        jobs = q.jobs
        
        job = Job.fetch(f"{cookie}", connection=r)
        if job not in jobs:
            jobs.append(job)
            
        print("TASK STATUS IS:", job.get_status())
        print("TASK RESULT IS:",  job.result)
        q_len = len(q)
        print(f"JOBS IS {job}")
        message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {q_len} jobs queued"
        
    return render_template("add_task.html", message=message, jobs=jobs)

@app.route("/get-task", methods=["GET",])
def get_task():
    job = None
    if request.args.get("cookie"):
        cookie = request.args.get("cookie")
        
        job = Job.fetch(f"{cookie}", connection=r)
            
        print("TASK STATUS IS:", job.get_status())
        print("TASK RESULT IS:",  job.result)
        print(f"JOBS IS {job}")
        
    return render_template("get_task.html", job=job)
