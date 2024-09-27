from flask import Flask, request, render_template, redirect, url_for,session
import requests

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Replace with a secure secret key
app.config['SESSION_TYPE'] = 'filesystem'

@app.route('/')
def form():
    return render_template('get_token.html')
    

@app.route('/submit', methods=['POST'])
def submit():
    cssm_on_prem_ip = request.form['cssm_on_prem_ip']
    username = request.form['username']
    password = request.form['password']
    client_id = request.form['client_id']
    client_secret = request.form['client_secret']

    # Extract the host from the provided IP/FQDN
    host = cssm_on_prem_ip.split("//")[-1].split("/")[0]

    # Prepare the API call
    url = f"{cssm_on_prem_ip}/oauth/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': '*/*',
        'Cache-Control': 'no-cache',
        'Host': host,
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive'
    }
    data = {
        'grant_type': 'password',
        'username': username,
        'password': password,
        'client_id': client_id,
        'client_secret': client_secret
    }

    # Make the API call
    response = requests.post(url, headers=headers, data=data, verify=False)  # verify=False to ignore SSL warnings

    # Check the response
    if response.status_code == 200:
        #print(response.text)
        #return "Authorization token received successfully!"
        token = response.json().get('access_token')
        session['auth_token'] = token
        session['cssm_on_prem_ip'] = cssm_on_prem_ip
        return redirect(url_for('deploy_lvas'))
    else:
        return f"Failed to get authorization token. Status code: {response.status_code}, Response: {response.text}"

@app.route('/deploy_lvas', methods=['GET', 'POST'])
def deploy_lvas():
    if request.method == 'POST':
        cssm_on_prem_ip = session.get('cssm_on_prem_ip')
        on_prem_account = request.form['on_prem_account']
        lva_count = int(request.form['lva_count'])
        lva_names = [request.form[f'lva_name_{i}'] for i in range(lva_count)]
        lva_descriptions = [request.form[f'lva_description_{i}'] for i in range(lva_count)]

        # Extract the host from the provided IP/FQDN
        host = cssm_on_prem_ip.split("//")[-1].split("/")[0]

        # Prepare the API call
        url = f"{cssm_on_prem_ip}/api/v1/accounts/{on_prem_account}/virtual-accounts"
        headers = {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f"Bearer {session['auth_token']}",
            'Accept': '*/*',
            'Cache-Control': 'no-cache',
            'Host': host,
            'Accept-Encoding': 'gzip, deflate, br',
            'Connection': 'keep-alive'
        }
         # Deploy each LVA
        for i in range(lva_count):
            data = {
                'name': lva_names[i],
                'description': lva_descriptions[i]
            }

            # Make the API call
            response = requests.post(url, headers=headers, data=data, verify=False)  # verify=False to ignore SSL warnings

            # Check the response
            if response.status_code != 200:
                return f"Failed to deploy LVA {i + 1}. Status code: {response.status_code}, Response: {response.text}"

        return "All LVAs deployed successfully!"

    return render_template('deploy_lvas.html')

    

if __name__ == '__main__':
    app.run(debug=True)