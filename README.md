# fitbit-api
FitBit API Project

### api_call.py
The main Python file makes an API call with a user's Fitbit to access its information. 

#### Authorization Code Grant Flow
The **Access** and **Refresh** tokens are user-specific and is obtained from an Authorization code obtained after the user grants
access privileges to the client/application. The purpose of the **Refresh** token is to grant a new **Access** token after it as previously expired, preventing the need for another *authorization code*. In other words, a HTTP POST request updates the Access token.

### Final Output
  * **API_call**: boolean indicating whether API call was successful
  * **API_response**: Response output of request
    * analogous to Fitbit's user profile (**.user_profile_get()** of python-fitbit object)
  * **fitbit_client**: python-fitbit object containing attributes to access the user's Fitbit data

## Drafts
#### read_fitbit.py
Python file uses credentials (client/application credentials + user tokens) to access a user's Fitbit information.

#### tokens.py
Python file uses authorization code to submit a HTTP GET request to obtain the **Access** and **Refresh** tokens. 

**Note**: The user-specific tokens are necessary in addition to the client ID and secret for the client to access the 
user's Fitbit data.

### References
1. https://dev.fitbit.com/docs/oauth2/
2. http://pdwhomeautomation.blogspot.co.uk/2016/01/fitbit-api-access-using-oauth20-and.html
3. https://python-fitbit.readthedocs.io/en/latest/
