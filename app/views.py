from crypt import methods
from app import app
from app import q, r
from app.tasks import count_words

from flask import render_template, request, make_response 


from time import strftime

from rq.exceptions import NoSuchJobError 
from rq.job import Job

import secrets

import json

@app.route("/")
def index():
    return "Hello World"

@app.route("/add-task", methods=["GET", "POST"])
def add_task():

    cookie = request.cookies.get("user", secrets.token_urlsafe())
    jobs = q.jobs # get the job in the queue
    message = None
    
    job_id = secrets.token_hex(10)
    user_jobs = list(r.get(f"{cookie}").decode().split(" "))
    print(f"Present user jobs are: {user_jobs}, type: {type(user_jobs)}")
    
    if request.args:
        
        url = request.args.get("url")
        
        print(url)
        task = q.enqueue(count_words, url, job_id=f"{job_id}")
        
        user_jobs.append(job_id)
        
        print(f"task is : {task.connection}")
        jobs = q.jobs

        q_len = len(q)
        print(f"JOBS IS {jobs}")
        message = f"Task queued at {task.enqueued_at.strftime('%a, %d %b %Y %H:%M:%S')}. {q_len} jobs queued"
    
    res = make_response(render_template("add_task.html", message=message, jobs=jobs))
    res.set_cookie("user", cookie)
    print("setting job id")
    r.set(f"{cookie}", " ".join(user_jobs))
    
    return res

@app.route("/get-task", methods=["GET",])
def get_task():
    cookie = request.cookies.get("user", None)
    if not cookie:
        return "CREATE A TASK FIRST"
    user_jobs = list(r.get(f"{cookie}").decode().split(" "))
    jobs = []
    print("USER JOBS IS: \n",user_jobs)
    print("*"*15)
    for user_job in user_jobs:
        try:
            jobs.append(Job.fetch(f"{user_job}", connection=r))
            
        # print("TASK STATUS IS:", job.get_status())
        # print("TASK RESULT IS:",  job.result)
        # print(f"JOBS IS {job}")
        except NoSuchJobError:
            print("HAHA NO JOB LOL")
    return render_template("get_task.html", jobs=jobs)


@app.route("/cookieCounter")
def cookie_counter():
    
    res = make_response()
    value = int(request.cookies.get("value", 0))
    res.set_cookie("value", f"{value + 1}")
    
    return res
    
    