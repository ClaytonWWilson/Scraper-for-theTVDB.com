import json
import os.path
from checks import *
from actions import *
import datetime
import dateutil.parser

def login():
    if os.path.exists("login.json") == False:
        obj = open("login.json", "w")
        obj.write("")
        obj.close()

    if os.stat("login.json").st_size == 0:# Will only ask for credentials if the login file is empty
        login = {
        "API_KEY": "",
        "USER_KEY": "",
        "USER_NAME": "",
        "TOKEN": "",
        "TIMESTAMP": ""
        }

        tmp_api_key = ""
        tmp_user_key = ""
        tmp_user_name = ""

        print("You can find your user key & request an API key while logged in at:\nhttps://www.thetvdb.com/?tab=userinfo")

        while tmp_api_key is "":
            tmp_api_key = input("Enter your api key: ")
        while tmp_user_key is "":
            tmp_user_key = input("Enter your user key: ")
        while tmp_user_name is "":
            tmp_user_name = input("Enter your username: ")

        LOGIN_DATA = {
            "apikey": tmp_api_key,
            "userkey": tmp_user_key,
            "username": tmp_user_name
        }

        tmp_token = getToken(LOGIN_DATA)

        if tmp_token is "":
            print("\nAuthentication failed. Please try again.")
        else:
            login["API_KEY"] = tmp_api_key
            login["USER_KEY"] = tmp_user_key
            login["USER_NAME"] = tmp_user_name
            login["TOKEN"] = tmp_token
            login["TIMESTAMP"] = str(datetime.datetime.now().replace(tzinfo=None))
            obj = open("login.json", "w")
            obj.write(json.dumps(login))
            obj.close()
            print("\nLogin successful!")
    else:# if login.json already exists
        with open("login.json") as json_data:# TODO add a check for a login that is damaged/modified
            login = json.load(json_data)
            json_data.close()
        saveTime = dateutil.parser.parse(login["TIMESTAMP"])
        curTime = datetime.datetime.now().replace(tzinfo=None)# TODO use UTC time?

        if checkTimestamp(saveTime, curTime):# token does not need refreshed
            print("token is good")
        else:
            refreshToken()
# TODO try to get token, if token fails, ask for login info again, if it passes save login details to login.py and save token with timestamp.
# TODO at startup, check token for validity and remove it if it is expired
