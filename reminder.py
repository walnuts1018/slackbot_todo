from dotenv import load_dotenv
import os
import requests
import pickle
import datetime
import schedule
import time
from dateutil.relativedelta import relativedelta

load_dotenv()
TOKEN = str(os.environ.get("SLACK_BOT_TOKEN"))
url = "https://slack.com/api/chat.postMessage"
headers = {"Authorization": "Bearer "+TOKEN}
users={}

# seconds
remind_time = 1*3600
interval_time = 60
Regular_reminder_time="07:00"
userid='U03BH0RKCR0'


def open_pickle():
    global users
    is_file = os.path.isfile('users_tasks.pkl')
    if is_file:
        with open('users_tasks.pkl', 'rb') as f:
            users = pickle.load(f)
    else:
        print("there are no users files.")

def post_message(post_text):
    data = {
        'channel': "walnuts-memo",
        'text': post_text
    }

    r = requests.post(url, headers=headers, data=data)
    print("return ", r.json())


def send_all_task_text():
    open_pickle()
    for i in users[userid][2].keys():
        n_regist(i,userid)
    num = 1
    prt_txt = ""
    for i in users[userid][0].values():
        prt_txt = prt_txt+"\n"+str(num)+" : "+str(i[0])+" "+str(i[1])
        num += 1
    if (len(users[userid][1]) != 0):
        prt_txt = prt_txt+"\n"+"期限日が設定されていないタスク"
        for i in users[userid][1].values():
            prt_txt = prt_txt+"\n"+str(num)+" : "+str(i[0])
            num += 1
    if (prt_txt == ""):
        prt_txt = "タスクはありません"
    post_message(prt_txt)

def reminder_id():
    return_id=[]
    for i, j in users[userid][0].items():
        if (remind_time-interval_time < (j[1]-datetime.datetime.now()).total_seconds() < remind_time):
            return_id.append(i)
    return return_id

def reminder_send():
    open_pickle()
    post_ids=reminder_id()
    for i in post_ids:
        post_message(users[userid][0][i][0]+"の締め切りは"+str(int(remind_time/60))+"分後です!")
    return True

def n_regist(given_uuid,userid):
    tasks_sc_tmp = users[userid][2][given_uuid]
    users[userid][2][given_uuid] = [tasks_sc_tmp[0], tasks_sc_tmp[1],
                                    tasks_sc_tmp[2], time_cal(tasks_sc_tmp[1], tasks_sc_tmp[2])[0]]
    users[userid][0][given_uuid] = [tasks_sc_tmp[0],
                                    time_cal(tasks_sc_tmp[1], tasks_sc_tmp[2])[1]]
    return True

def time_cal(given_datetime, given_n,):
    num_caldate = 0
    return_datetime = ""
    if (str(given_n)[-1] == "y"):
        return_datetime = given_datetime
        while (return_datetime < datetime.datetime.now()):
            return_datetime = given_datetime + \
                relativedelta(years=num_caldate*int(str(given_n)[0:-2]))
            num_caldate += 1

    if (str(given_n)[-1] == "m"):
        return_datetime = given_datetime
        while (return_datetime < datetime.datetime.now()):
            return_datetime = given_datetime + \
                relativedelta(months=num_caldate*int(str(given_n)[0:-2]))
            num_caldate += 1

    if (str(given_n)[-1] == "d"):
        return_datetime = given_datetime
        while (return_datetime < datetime.datetime.now()):
            return_datetime = given_datetime + \
                relativedelta(days=num_caldate*int(str(given_n)[0:-2]))
            num_caldate += 1

    return num_caldate, return_datetime

open_pickle()
reminder_id()
schedule.every().day.at(Regular_reminder_time).do(send_all_task_text)

while True:
    schedule.run_pending()
    reminder_send()
    time.sleep(interval_time)
