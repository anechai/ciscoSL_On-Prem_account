# ciscoSL_On-Prem_account
This set of scripts is for the automation of CSSM On-Prem LVA accounts.
1. Clone the repo.
2. Install the Python environment v3.8 and higher.
3. Install Flask micro framework: $ pip install Flask.
Full documentation is here: https://flask.palletsprojects.com/en/3.0.x/
4. Run the Get_token_app_test.py script.
5. The Flask service should start and will be available on the local host by default (http://127.0.0.1:5000/).
Navigate to http://127.0.0.1:5000/ in your browser and provide the following to obtain an access token:
FQDN/IP of your CSSM On-Prem server
- Login
- Password
- Client_ID
- Client_secret

Get the token.
Once the token is obtained successfully, you will be redirected to the LVA modification page.
6. Provide the name of the registered On-Prem account and proceed with LVA deployment.
Note!
1. CSSM On-Prem can be downloaded from downloads.cisco.com along with all necessary documentation, including the API guide.
2. In this repository, there is no CSS available. But you can use your own instead.
