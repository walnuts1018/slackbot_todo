import pickle
with open('users_tasks.pkl', 'rb') as f:
    users = pickle.load(f)
print(users)
