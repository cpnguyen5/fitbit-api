import base64
import urllib2
import urllib
import ssl
import json
import os


#Fitbit URIs
TokenURI = "https://api.fitbit.com/oauth2/token" #Access/Refresh Token Request
AuthURI = "https://www.fitbit.com/oauth2/authorize" # Authorization

#read & record user params (consumer key & secret)
f = open('consumer.txt', 'r')
for line in f.readlines():
    if 'consumer_key' in line.split('=')[0]:
        c_key = line.split('=')[1].strip()
    elif 'consumer_secret' in line.split('=')[0]:
        c_secret = line.split('=')[1].strip()
f.close()

# Directory of Users
head_path = os.path.split(os.path.abspath(__file__))[0]
user_path = os.path.join(head_path, 'users')
user_lstdir = os.listdir(user_path)  # list of user directories

# User1 tokens
usr1_f = open(os.path.join(user_path, 'user1.txt'), 'r')
for line in usr1_f.readlines():
    if 'access_token' in line.split('=')[0]:
        access_t = line.split('=')[1].strip()
    elif 'refresh_token' in line.split('=')[0]:
        refresh_t = line.split('=')[1].strip()
    elif 'auth_code' in line.split('=')[0]:
        auth_code = line.split('=')[1].strip()


# Data payload (query parameters)
BodyText = {'code' : auth_code,
            'redirect_uri' : 'https://www.google.com/',
            'clientId' : c_key,  # OAuth2 client ID
            'grant_type' : 'authorization_code'}


BodyURLEncoded = urllib.urlencode(BodyText) # encode dictionary in form of POST request URIw

# base64str = base64.b64encode('%s:%s' % (c_key, c_secret)).replace('\n', '')

hdr = {'Authorization': 'Basic %s' % 'MjI4SzI5OjQ2MzE4ZDIyMGQ5Y2JmNzczOGQ2ZTk5MTdmYTY2NDI4',
       'Content-Type': 'application/x-www-form-urlencoded'}

#Start the request
request = urllib2.Request(TokenURI,BodyURLEncoded, headers=hdr) # request

#Fire off the request
context =  ssl._create_unverified_context() # development - bypass SSL certs

try:
  response = urllib2.urlopen(request, context=context)

  FullResponse = response.read() # output

  # Convert response object to dictionary/hashable
  json_response = json.loads(FullResponse.decode('utf-8'))
  AccToken = str(json_response['access_token'])
  RefToken = str(json_response['refresh_token'])

except urllib2.URLError as e:
  print e.code
  print e.read()
