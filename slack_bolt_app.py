#!/usr/local/bin/python3
import os
from dotenv import load_dotenv
import pickle
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import uuid
import re
import datetime
from dateutil.relativedelta import relativedelta

load_dotenv()
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))
is_file = os.path.isfile('users_tasks.pkl')
if is_file:
  with open('users_tasks.pkl', 'rb') as f:
      users = pickle.load(f)
else:
    users={}

# users={userid:[tasks, tasks_wo_date, tasks_sc, id_to_uuid],…}

pattern_n = re.compile(r'n')
pattern_abc = re.compile(r'[a-z]')


@app.command("/task")
def todo(ack, respond, command):
    ack()
    userInput = command['text'].split()
    userid = str(command['user_id'])

    if (not (userid in users)):
        users[userid]=[{},{},{},{}]


    # nを用いたタスクの登録処理
    for i in users[userid][2].keys():
        n_regist(i,userid)

    tasks_sort(userid)

    if userInput == []:
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
        respond(prt_txt)

    elif(userInput[0] == "fin"):
        if len(userInput) == 1:
            respond("削除したいタスクの番号を入力してください")
        else:
            tasks_value = users[userid][0].pop(
                users[userid][3][int(userInput[1])], False)
            if(tasks_value == False):
                tasks_value = users[userid][1].pop(
                    users[userid][3][int(userInput[1])], False)
                if(tasks_value == False):
                    respond("削除に失敗しました。")
                else:
                    respond(str(tasks_value[0])+"の削除に成功しました。")
            else:
                respond(str(tasks_value[0])+"の削除に成功しました。")

    elif(userInput[0] == "del"):
        if len(userInput) == 1:
            respond("エラー:削除したいタスクの番号を入力してください")
        else:
            tasks_value = users[userid][0].pop(
                users[userid][3][int(userInput[1])], False)
            tasks_value += users[userid][2].pop(users[userid]
                                                [3][int(userInput[1])], False)
            if(tasks_value == False):
                tasks_value = users[userid][1].pop(
                    users[userid][3][int(userInput[1])], False)
                if(tasks_value == False):
                    respond("削除に失敗しました。")
                else:
                    respond(str(tasks_value[0])+"の削除に成功しました。")
            else:
                respond(str(tasks_value[0])+"の削除に成功しました。")
    elif(userInput[0] == "help"):
        respond("Hi there :wave: このアプリはwalnuts製のToDo管理アプリです！ \n \n 適当に作ったアプリなのでプライバシー的に問題がある可能性があります。知られちゃ困ることは登録しないでね～ \n \n  コマンドの使い方 \n --------------------------------------------------------------------------------------- \n タスクを追加する `/task 名前` \n \n 期限付きのタスクを追加する (hhmmは省略すると00:00になります) `/task 名前 yyyymmddhhmm` \n 例(test, 2003/10/18 10:45): `/task test 200310181045` \n \n 任意の整数nを用いて定期的なタスクを登録できます。y:年、m:月、d:日を用いて繰り返しを定義できます。この場合、時刻を省略することはできません。+のところスペースは入れないでね～ `/task 名前 yyyymmddhhmm+[任意の数字]n[y,m,d]` \n  例(お誕生日 2003/10/18/00:00から毎年繰り返し): `/task walnutsお誕生日 200310180000+1ny` \n \n タスクを一覧表示します。 `/task` \n \nタスクを消します。 `/task` で表示したときの番号で指定します。タスクを追加したり消したりするとこの番号は変わるので注意してください。 `/task fin [タスクの番号]` \n \n 同じくタスクを消しますが、こちらを用いると繰り返しタスクをすべて消すことができます。 `/task del [タスクの番号]` \n \n このヘルプを表示します。 `/task help` \n ---------------------------------------------------------------------------------------")
    else:
        id = str(uuid.uuid1())
        if len(userInput) == 1:
            users[userid][1][id] = [userInput[0]]

        elif len(userInput) == 2:
            if (pattern_n.search(userInput[1]) == None):
                if (pattern_abc.search(userInput[1]) == None):
                    if (len(userInput[1]) == 8):
                        dt = datetime.datetime(int(str(userInput[1])[0:4]), int(
                            str(userInput[1])[4:6]), int(str(userInput[1])[6:8]))
                        users[userid][0][id] = [userInput[0], dt]
                    elif(len(userInput[1]) < 8):
                        respond("日付の形式に誤りがあります。")
                    else:
                        dt = datetime.datetime(int(str(userInput[1])[0:4]), int(str(userInput[1])[4:6]), int(
                            str(userInput[1])[6:8]), int(str(userInput[1])[8:10]), int(str(userInput[1])[10:12]))
                        users[userid][0][id] = [userInput[0], dt]
                else:
                    respond('文法エラーです(Make sure it does not contain [a-z].)')

            # nでの指定がある場合
            else:
                date_wo_n = str(userInput[1])[0:12]
                date_n = str(userInput[1])[13:]
                if(len(date_wo_n) < 12):
                    respond("日付の形式に誤りがあります。")
                else:
                    dt = datetime.datetime(int(str(date_wo_n)[0:4]), int(str(date_wo_n)[4:6]), int(
                        str(date_wo_n)[6:8]), int(str(date_wo_n)[8:10]), int(str(date_wo_n)[10:12]))
                    users[userid][2][id] = [userInput[0], dt, date_n, 0]

        else:
            respond("引数が多すぎます")
        respond("タスクを登録しました。")
    with open("users_tasks.pkl","wb") as f:
        pickle.dump(users, f)

def tasks_sort(userid):
    tasks_list_tmp = sorted(users[userid][0].items(), key=lambda x: x[1][1])
    tasks_tmp = {}

    for i in tasks_list_tmp:
        tasks_tmp[i[0]] = i[1]
    users[userid][0] = tasks_tmp
    uuid_to_id(userid)


def uuid_to_id(userid):
    num = 1
    uuid_tmp = {}
    for i in users[userid][0].keys():
        uuid_tmp[num] = i
        num += 1
    for i in users[userid][1].keys():
        uuid_tmp[num] = i
        num += 1
    users[userid][3] = uuid_tmp


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


def n_regist(given_uuid,userid):
    tasks_sc_tmp = users[userid][2][given_uuid]
    users[userid][2][given_uuid] = [tasks_sc_tmp[0], tasks_sc_tmp[1],
                                    tasks_sc_tmp[2], time_cal(tasks_sc_tmp[1], tasks_sc_tmp[2])[0]]
    users[userid][0][given_uuid] = [tasks_sc_tmp[0],
                                    time_cal(tasks_sc_tmp[1], tasks_sc_tmp[2])[1]]
    return True


SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
