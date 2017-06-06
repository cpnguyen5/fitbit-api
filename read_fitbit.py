import fitbit
import os

#read & record user params (consumer key & secret)
f = open('consumer.txt', 'r')
for line in f.readlines():
    if 'consumer_key' in line.split('=')[0]:
        c_key = line.split('=')[1].strip()
    elif 'consumer_secret' in line.split('=')[0]:
        c_secret = line.split('=')[1].strip()

    f.close()



# read & record authorized users
users_dict = dict()

users_f = open('users.txt', 'r')
for line in users_f.readlines():
    usr, usr_id = line.split('=')
    users_dict[usr.strip()] = {'id': usr_id.strip()}

users_f.close()


# Directory of Users
head_path = os.path.split(os.path.abspath(__file__))[0]
user_path = os.path.join(head_path, 'users')
user_lstdir = os.listdir(user_path)  # list of user directories

for user in user_lstdir:
    user_file = os.path.join(user_path, user)

    user_f = open(user_file, 'r')
    for line in user_f.readlines():
        if 'access_token' in line.split('=')[0]:
            access_t = line.split('=')[1].strip()
        elif 'refresh_token' in line.split('=')[0]:
            refresh_t = line.split('=')[1].strip()

    user_f.close()

    user_label = user.split('.')[0]
    users_dict[user_label]['access_tok']=access_t
    users_dict[user_label]['refresh_tok']=refresh_t

    # client
    client = fitbit.Fitbit(client_id=c_key,
                           client_secret=c_secret,
                           access_token=access_t,
                           refresh_token=refresh_t)
    profile = client.user_profile_get(user_id=users_dict[user_label]['id'])
    print profile['user']['fullName']

