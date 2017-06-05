import fitbit


#read & record user params (consumer key & secret)
f = open('consumer.txt', 'r')
for line in f.readlines():
    if 'consumer_key' in line.split('=')[0]:
        c_key = line.split('=')[1].strip()
    elif 'consumer_secret' in line.split('=')[0]:
        c_secret = line.split('=')[1].strip()
    elif 'access_token' in line.split('=')[0]:
        access_t = line.split('=')[1].strip()
    elif 'refresh_token' in line.split('=')[0]:
        refresh_t = line.split('=')[1].strip()

f.close()

# read & record authotized users
users_dict = dict()

users_f = open('users.txt', 'r')
for line in users_f.readlines():
    users_dict[line.split('=')[0]] = line.split('=')[1].strip()

users_f.close()

# client
client = fitbit.Fitbit(client_id='c_key',
                              client_secret='c_secret',
                              access_token=access_t,
                              refresh_token=refresh_t)


if __name__ == '__main__':
    print client.user_profile_get(user_id=users_dict['user1'])
