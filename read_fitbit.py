import fitbit

f = open('consumer.txt', 'r')
for line in f.readlines():
    if 'consumer_key' in line.split('=')[0]:
        c_key = line.split('=')[1]
    elif 'consumer_secret' in line.split('=')[0]:
        c_secret = line.split('=')[1]


#unauthorized client
unauth_client = fitbit.Fitbit(client_id='c_key',
                              client_secret='c_secret')

if __name__ == '__main__':
    print unauth_client
