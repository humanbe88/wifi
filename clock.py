import requests
import json

def login(email, password, access_type):
    url = 'https://aapp.fple.com/api/employees/login'
    headers = {
        'Content-Type': 'application/json',
    }
    data = {
        "email": email,
        "password": password,
        "type": access_type,
        "device_uuid": "8eafa1a7d350fb24",
        "address": "EKOCHERAS A-21-01 (HQ)",
        "longtitude": "101.7394237",
        "latitude": "3.0927721",
        "platform": "Android",
        "version": "API 33",
        "cordova": "Xiaomi",
        "model": "2201123G",
        "serial": "unknown",
        "registration_id": "e1Sw9Kg4RguysqWbimQM_m:APA91bHWrtHgGphAYyCVAyKPQN9HDo7q1xs6Viw5js7h7pKWqAO9s0UuaQf71Q_WdFzTN8nCZxoftS0CspWY36GdLIdVehKIswMub6nljFm5rtUy_F_rtmhxHd_yAy7ppck14vmmVNzx",
        "registration_type": "GCM"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def logout(access_token, access_type):
    url = 'https://aapp.fple.com/api/employees/logout'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    data = {
        "type": access_type
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

def clock_in_out(access_token, action):
    url = 'https://aapp.fple.com/api/employees/attendance-clock-in-out'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {access_token}'
    }
    #part data ambil dari db yang takda biarkan kosong
    data = {
        "mac_address": "d8:ec:5e:6f:02:6f",
        "device_uuid": "8eafa1a7d350fb24",
        "action": action,
        "address": "EKOCHERAS A-21-01 (HQ)",
        "longtitude": "101.7394237",
        "latitude": "3.0927721",
        "platform": "Android",
        "version": "API 33",
        "cordova": "Xiaomi",
        "model": "2201123G",
        "serial": "unknown",
        "registration_id": "e1Sw9Kg4RguysqWbimQM_m:APA91bHWrtHgGphAYyCVAyKPQN9HDo7q1xs6Viw5js7h7pKWqAO9s0UuaQf71Q_WdFzTN8nCZxoftS0CspWY36GdLIdVehKIswMub6nljFm5rtUy_F_rtmhxHd_yAy7ppck14vmmVNzx",
        "registration_type": "GCM"
    }
    response = requests.post(url, headers=headers, data=json.dumps(data))
    return response.json()

#save accessSS token to a file
def save_access_token(access_token):
    with open('access_token.txt', 'w') as file:
        file.write(access_token)

# read accesstoken from file
def read_access_token():
    try:
        with open('access_token.txt', 'r') as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

email = "shubki@fple.com"      #user/pass 
password = "xx"
access_type = "mobile"

print("Lai2 Pilih:")
print("1. Login")
print("2. Logout")
print("3. Clock in/out")
option = input("Pilih: ")

if option == "1":
    login_response = login(email, password, access_type)
    if 'data' in login_response:
        access_token = login_response['data']['access_token']
        save_access_token(access_token)
        print("Login successful!")
        print("Access Token:", access_token)
    else:
        print("Login failed Check User/Pass.")
elif option == "2":
    access_token = read_access_token()
    if access_token:
        logout_response = logout(access_token, access_type)
        if 'message' in logout_response and logout_response['message'] == "Logout successful":
            print("Logout success!")
        else:
            print("Logout failed dong")
    else:
        print("access token tak jumpa. Login dulu laaaaaa..")
elif option == "3":
    access_token = read_access_token()
    if access_token:
        action = input("Enter 'in' or 'out' for clock in/out: ")

        clock_response = clock_in_out(access_token, action)
        print("Clock in/out response:", clock_response)
    else:
        print("access token tak jumpa. Login dulu laaaaaa.")
else:
    print("Silap pilih tu")
