import os
from dotenv import load_dotenv
import json
import requests
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import uuid
import re

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
        tasks_sort()
      
    else:
      id=str(uuid.uuid1())
      if len(userInput)==1:
        tasks_wo_date[id] = [userInput[0]]

      elif len(userInput)==2:
        if (pattern_n.search(userInput[1]) == None):
          if (pattern_abc.search(userInput[1])== None):
            tasks[id] = [userInput[0],userInput[1]]

          else: 
            print('文法エラーです(Make sure it does not contain [a-z].)')
        else:
          tasks_sc[id] = [userInput[0],userInput[1],0]

      else:
        print("引数が多すぎます")
      #"タスク入れ替え処理"
      tasks_sort()

#tasks入れ替え
def tasks_sort():
  global tasks

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
  
#SocketModeHandler(app,os.environ["SLACK_APP_TOKEN"]).start()
while True:
  main()