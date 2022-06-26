import os
from dotenv import load_dotenv
import json
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import uuid
import re
import datetime
from dateutil.relativedelta import relativedelta
#load_dotenv()
#app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

tasks={}
tasks_wo_date={}
tasks_sc={}
pattern_n = re.compile(r'n')
pattern_abc = re.compile(r'[a-z]')
id_to_uuid={}

#@app.command("/task")
#def repeat_text(ack, print, command):
def main():
    #ack()
    #userInput = command['text'].split()
    userInput=str(input("コマンド")).split()
          #"タスク入れ替え処理"

    #nを用いたタスクの登録処理
    for i in tasks_sc.keys():
      n_regist(i)

    tasks_sort()

    if userInput ==[] :
      num=1
      prt_txt=""
      for i in tasks.values():
        prt_txt=prt_txt+"\n"+str(num)+" : "+str(i[0])+" "+str(i[1])
        num+=1
      if (len(tasks_wo_date)!=0):
        prt_txt=prt_txt+"\n"+"期限日が設定されていないタスク"
        for i in tasks_wo_date.values():
          prt_txt=prt_txt+"\n"+str(num)+" : "+str(i[0])
          num+=1
      if (prt_txt==""):
        prt_txt="タスクはありません"
      print(prt_txt)

    elif(userInput[0]=="fin"):
      if len(userInput)==1:
        print("削除したいタスクの番号を入力してください")
      else:
        tasks_value=tasks.pop(id_to_uuid[int(userInput[1])],False)
        if(tasks_value==False):
          tasks_value=tasks_wo_date.pop(id_to_uuid[int(userInput[1])],False)
          if(tasks_value==False):
            print("削除に失敗しました。")
          else:
            print(str(tasks_value[0])+"の削除に成功しました。")
        else:
          print(str(tasks_value[0])+"の削除に成功しました。")


    elif(userInput[0]=="del"):
      if len(userInput)==1:
        print("エラー:削除したいタスクの番号を入力してください")
      else:
        tasks_value=tasks.pop(id_to_uuid[int(userInput[1])],False)
        tasks_value+=tasks_sc.pop(id_to_uuid[int(userInput[1])],False)
        if(tasks_value==False):
          tasks_value=tasks_wo_date.pop(id_to_uuid[int(userInput[1])],False)
          if(tasks_value==False):
            print("削除に失敗しました。")
          else:
            print(str(tasks_value[0])+"の削除に成功しました。")
        else:
          print(str(tasks_value[0])+"の削除に成功しました。")


    else:
      id=str(uuid.uuid1())
      if len(userInput)==1:
        tasks_wo_date[id] = [userInput[0]]

      elif len(userInput)==2:
        if (pattern_n.search(userInput[1]) == None):
          if (pattern_abc.search(userInput[1])== None):
            if (len(userInput[1])==8):
              dt = datetime.datetime(int(str(userInput[1])[0:4]),int(str(userInput[1])[4:6]),int(str(userInput[1])[6:8]))
              tasks[id] = [userInput[0],dt]
            elif(len(userInput[1])<8):
              print("日付の形式に誤りがあります。")
            else :
              dt = datetime.datetime(int(str(userInput[1])[0:4]),int(str(userInput[1])[4:6]),int(str(userInput[1])[6:8]),int(str(userInput[1])[8:10]),int(str(userInput[1])[10:12]))
              tasks[id] = [userInput[0],dt]
          else: 
            print('文法エラーです(Make sure it does not contain [a-z].)')

        # nでの指定がある場合
        else:
          date_wo_n=str(userInput[1])[0:12]
          date_n=str(userInput[1])[13:]
          if(len(date_wo_n)<12):
            print("日付の形式に誤りがあります。")
          else :
            dt = datetime.datetime(int(str(date_wo_n)[0:4]),int(str(date_wo_n)[4:6]),int(str(date_wo_n)[6:8]),int(str(date_wo_n)[8:10]),int(str(date_wo_n)[10:12]))
            tasks_sc[id] = [userInput[0],dt,date_n,0]

      else:
        print("引数が多すぎます")
      print("タスクを登録しました。")
#tasks入れ替え
def tasks_sort():
  global tasks
  print(tasks)
  tasks_list_tmp = sorted(tasks.items(), key=lambda x:x[1][1])
  tasks_tmp={}

  for i in tasks_list_tmp:
    tasks_tmp[i[0]]=i[1]
  tasks=tasks_tmp
  uuid_to_id()

def uuid_to_id():
  global id_to_uuid
  num=1
  uuid_tmp={}
  for i in tasks.keys():
    uuid_tmp[num]=i
    num+=1
  for i in tasks_wo_date.keys():
    uuid_tmp[num]=i
    num+=1
  id_to_uuid=uuid_tmp

def time_cal(given_datetime,given_n):
  num_caldate=0
  return_datetime=""
  if (str(given_n)[-1]=="y"):
    return_datetime = given_datetime  
    while (return_datetime < datetime.datetime.now()):
      return_datetime = given_datetime + relativedelta(years=num_caldate*int(str(given_n)[0:-2]))
      num_caldate+=1
  
  if (str(given_n)[-1]=="m"):
    return_datetime = given_datetime
    while (return_datetime < datetime.datetime.now()):
      return_datetime = given_datetime + relativedelta(months=num_caldate*int(str(given_n)[0:-2]))
      num_caldate+=1
  
  if (str(given_n)[-1]=="d"):
    return_datetime = given_datetime
    while (return_datetime < datetime.datetime.now()):
      return_datetime = given_datetime + relativedelta(days=num_caldate*int(str(given_n)[0:-2]))
      num_caldate+=1
  
  return num_caldate,return_datetime

def n_regist(given_uuid):
  tasks_sc_tmp=tasks_sc[given_uuid]
  tasks_sc[given_uuid]=[tasks_sc_tmp[0],tasks_sc_tmp[1],tasks_sc_tmp[2],time_cal(tasks_sc_tmp[1],tasks_sc_tmp[2])[0]]
  tasks[given_uuid] = [tasks_sc_tmp[0],time_cal(tasks_sc_tmp[1],tasks_sc_tmp[2])[1]]
  return True


#SocketModeHandler(app,os.environ["SLACK_APP_TOKEN"]).start()

while True:
  main()
