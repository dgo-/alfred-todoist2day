#! /usr/bin/env python
# coding: utf8

import requests
import json
import datetime
import uuid
from config import URL_BASE, URL_PROJECT, URL_TASKS, ICON
try:
    from myconfig import TOKEN
except ImportError:
    Token=''
try:
    from mylang import LANG
except ImportError:
    LANG='en'

#try:
#    LANG
#except NameError:
#    LANG=en

def request_get(url):
    r = requests.get(url, params={"token": TOKEN})

    code = r.status_code
    reason = str(code) + " - " + r.reason
    if (code == 200): 
        return True, r.json()
    if (code == 204):
        return True, ""
    else:
        return False, reason

def request_post(url, data=None):
    if data is None:
        r = requests.post(url, params={"token": TOKEN})
    else:
        r = requests.post(url, 
                params={"token": TOKEN}, 
                data=json.dumps(data),
                headers={"Content-Type": "application/json", "X-Request-Id": str(uuid.uuid4())}
                )

    code = r.status_code
    reason = str(code) + " - " + r.reason
    if (code == 200): 
        return True, r.json()
    if (code == 204):
        return True, ""
    else:
        return False, reason

def project_get():
    status, content=request_get(URL_PROJECT)
    return status, content

def task_get():
    status, content=request_get(URL_TASKS)
    return status, content

def task_close(id):
    url=URL_TASKS + '/' + str(id) + '/close'
    status, content = request_post(url)
    return status, content

def task_create(content, project_id=None, order=None, label_ids=None, priority=None, due_string=None, due_lang=None):
    task = {}
    task['content'] = content
    if content is not None:
        task['project_id'] = project_id
    if order is not None:
        task['order'] = order
    if label_ids is not None:
        task['label_ids'] = label_ids
    if priority is not None:
        task['priority'] = priority
    if due_string is not None:
        task['due_string'] = due_string
    if due_lang is not None:
        task['due_lang'] = due_lang

    status, content = request_post(URL_TASKS, task)
    return status, content

def project_name2id(name):
    status, projects = project_get()

    if (status):
        for project in projects:
            if project['name'].lower() == name.lower():
                 return project['id']
    return ''

def alfred_list_task_today():
    status, content = task_get() #request_get(URL_TASKS)
    status_projects, projects = project_get() #request_get(URL_PROJECT)

    items = []
    if (status):
        for task in content:
            if 'due' in task:
                if datetime.date.today().strftime('%Y-%m-%d') == task["due"]["date"]:
                    item = {}
                    item['title'] = task['content']
                    if (status_projects):
                        for project in projects:
                            if project['id'] == task['project_id']:
                                item['subtitle'] = project['name']
                    item['arg'] = task['id']
                    item['icon'] = { "path": ICON }
                    items.append(item)
    else:
        item = {}
        item['title'] = content
        items.append(item)

    alfred_output = { 'items' : items }
    print(json.dumps(alfred_output))

def alfred_create_task(string):

    parts = string.split(';')
    size = len(parts)

    content = parts[0]
    content.strip()
    if ( size == 2 ):
        project = parts[1]
        name=project_name2id(project.strip())
        if (name != ''): 
            status, result = task_create(content, project_id=pid)
        else:
            status, result = task_create(content)
    elif ( size == 3 ):
        project = parts[1]
        pid=project_name2id(project.strip())
        date = parts[2]
        date.strip()
        if (pid != ''): 
            status, result = task_create(content, project_id=pid, due_string=date, due_lang=LANG)
        else:
            status, result = task_create(content, due_string=date, due_lang=LANG)
    else:
        status, result = task_create(content)
        
    if (status):
        print('successfully create task')
    else:
        print('failed create task - ' + result )

def alfred_close_task(id):
    status, result = task_close(id)
    if (status):
        print('successfully close task')
    else:
        print('failed close task - ' + result )
