import base64
import urllib2
import urllib
import ssl
import json

#read & record user params (consumer key & secret)
f = open('consumer.txt', 'r')
for line in f.readlines():
    if 'consumer_key' in line.split('=')[0]:
        c_key = line.split('=')[1].strip()
    elif 'consumer_secret' in line.split('=')[0]:
        c_secret = line.split('=')[1].strip()
    # elif 'access_token' in line.split('=')[0]:
    #     access_t = line.split('=')[1].strip()
    # elif 'refresh_token' in line.split('=')[0]:
    #     refresh_t = line.split('=')[1].strip()
    elif 'auth_code' in line.split('=')[0]:
        auth_code = line.split('=')[1].strip()

f.close()

#Fitbit URIs
TokenURI = "https://api.fitbit.com/oauth2/token" #Access/Refresh Token Request
AuthURI = "https://www.fitbit.com/oauth2/authorize" # Authorization

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
  print json_response['access_token']

except urllib2.URLError as e:
  print e.code
  print e.read()
