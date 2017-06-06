import os, sys
import base64
import urllib
import urllib2
import json
import ssl
import fitbit



def GetClient():
    """
    Obtain client ID and secret key.
    :return: client ID, client secret
    """
    # read & record user params (consumer key & secret)
    f = open('consumer.txt', 'r')
    for line in f.readlines():
        if 'consumer_key' in line.split('=')[0]:
            c_key = line.split('=')[1].strip()
        elif 'consumer_secret' in line.split('=')[0]:
            c_secret = line.split('=')[1].strip()
    return c_key, c_secret


def GetConfig(user_path):
    """
    Obtain configuration (Access and Refresh tokens)
    :return: Access token, Refresh token
    """
    tokens_f = open(user_path,'r') # user txt file
    for line in tokens_f.readlines():
        if 'access_token' in line.split('=')[0]:
            AccToken = line.split('=')[1].strip()
        elif 'refresh_token' in line.split('=')[0]:
            RefToken = line.split('=')[1].strip()
    tokens_f.close()

    # strip newline
    if (AccToken.find("\n") != -1):
        AccToken = AccToken.replace('\n', '')
    if (RefToken.find("\n") != -1):
        RefToken = RefToken.replace('\n', '')
    return AccToken, RefToken


def WriteConfig(user_path, AccToken,RefToken):
    """
    Override configuration file with new Access and Refresh tokens
    :param AccToken: Access token
    :param RefToken: Refresh tokens
    :return: None
    """
    #Read old config file
    oldTokens_f = open(user_path,'r')
    for line in oldTokens_f.readlines():
        if 'access_token' in line.split('=')[0]:
            AccToken = line.split('=')[1].strip()
        elif 'refresh_token' in line.split('=')[0]:
            RefToken = line.split('=')[1].strip()

    #Delete the old config file
    os.remove(user_path)

    #Open and write to the file
    newTokens_f = open(user_path,'w')
    newTokens_f.write('access_token %s' + '\n' % (AccToken))
    newTokens_f.write('refresh_token %s' + '\n' % (RefToken))
    newTokens_f.close()


def GetNewAccessToken(TokenURI, RefToken):
    """
    HTTP POST method to obtain/update new Access token using Refresh token.

    :param TokenURI: token URI
    :param RefToken: Refresh token
    :return: None
    """
    BodyText = {'grant_type' : 'refresh_token',
              'refresh_token' : RefToken}
    BodyURLEncoded = urllib.urlencode(BodyText)

    #Start the request
    token_request = urllib2.Request(TokenURI,BodyURLEncoded)

    token_request.add_header('Authorization', 'Basic %s' % ('MjI4SzI5OjQ2MzE4ZDIyMGQ5Y2JmNzczOGQ2ZTk5MTdmYTY2NDI4'))
                             # base64.b64encode(OAuthTwoClientID + ":" + ClientOrConsumerSecret))
    token_request.add_header('Content-Type', 'application/x-www-form-urlencoded')

    #Fire off the request
    try:

        token_response = urllib2.urlopen(token_request)
        FullResponse = token_response.read()
        json_response = json.loads(FullResponse)

        #Read the access token as a string
        new_AccessToken = str(json_response['access_token'])
        new_RefreshToken = str(json_response['refresh_token'])
        #Write the new access token
        WriteConfig(user_path, new_AccessToken,new_RefreshToken)

    except urllib2.URLError as e:
        print e.code
        print e.read()


def MakeAPICall(user_path, URL, TokenURI, AccToken,RefToken):
    #Start the request
    request = urllib2.Request(URL) # relies on Access token for ID
    # request = urllib2.Request(URL.replace('-','5RW7TT'))

    #Add the access token in the header
    request.add_header('Authorization', 'Bearer ' + AccToken)

    #Fire off the request
    context = ssl._create_unverified_context()  # development - bypass SSL certs

    try:
        response = urllib2.urlopen(request, context=context)
        FullResponse = response.read()

        json_response = json.loads(FullResponse)

        client_key, client_secret = GetClient()
        client = fitbit.Fitbit(client_id=client_key,
                               client_secret=client_secret,
                               access_token=AccToken,
                               refresh_token=RefToken)
        return (True, json_response, client)
    #Catch errors (e.g. A 401 error that signifies the need for a new access token)
    except urllib2.URLError as e:
        print "HTTP error: ", str(e.code)
        print "HTTP Error Message: ", e.read()

    if (e.code == 401) and (e.read().find("Access token invalid or expired") != -1):
        GetNewAccessToken(TokenURI, RefToken) # use Refresh token to obtain new Access token
        return False, "Refreshed"
    return False, "Error"


if __name__ == '__main__':

    # Directory of Users
    head_path = os.path.split(os.path.abspath(__file__))[0]
    user_path = os.path.join(head_path, 'users')
    user_lstdir = os.listdir(user_path) # list of user directories

    for user in user_lstdir:
        user_file = os.path.join(user_path, user)
        # Fitbit URIs
        FitbitURI = "https://api.fitbit.com/1/user/-/profile.json"  # URL for API call (API endpoint)
        TokenURI = "https://api.fitbit.com/oauth2/token"  # URL to refresh access token

        #Get the config (tokens)
        AccessToken, RefreshToken = GetConfig(user_file)

        #API call
        API_call, API_response, fitbit_client = MakeAPICall(user_file, FitbitURI, TokenURI, AccessToken, RefreshToken)

        if API_call == True:
          print API_response
          # profile = fitbit_client.user_profile_get() # equivalent to API response
          # print profile
        else:
            if (API_response == "Refreshed"):
                print "Refreshed the access token."
                API_call, APIResponse, fitbit_client = MakeAPICall(user_file, FitbitURI, TokenURI, AccessToken, RefreshToken)

                if API_call == True:
                    print API_response
            else:
                print "Error in API handling"
