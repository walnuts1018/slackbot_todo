from dotenv import load_dotenv
import os
import requests
import pickle
import datetime
import schedule

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
    global url
    global headers
    data = {
        'channel': "walnuts-memo",
        'text': post_text
    }

    r = requests.post(url, headers=headers, data=data)
    print("return ", r.json())


def send_all_task_text():
    global users
    open_pickle()
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
    global users
    return_id=[]
    for i, j in users[userid][0].items():
        if (remind_time-interval_time-30 < (j[1]-datetime.datetime.now()).seconds < remind_time):
            return_id.append(i)
    return return_id

def reminder_send():
    global users
    open_pickle()
    post_ids=reminder_id()
    for i in post_ids:
        post_message(users[userid][0][i][0]+"の締め切りは"+str(int(remind_time/60))+"分後です!")
    return True

open_pickle()
while True:
    schedule.every(interval_time).seconds.do(reminder_send)
    schedule.every().day.at(Regular_reminder_time).do(send_all_task_text)
