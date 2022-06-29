import pickle
import datetime

with open('users_tasks.pkl', 'rb') as f:
    users = pickle.load(f)
print(users)
users={}
with open("users_tasks.pkl","wb") as f:
    pickle.dump(users, f)