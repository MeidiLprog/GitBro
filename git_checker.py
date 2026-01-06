#this is where the magic operates

import subprocess
import os
import sys
import requests
import re
_PYTHON_ = sys.executable


#checking if git is installed
def check_git():
    print("Checking Git installation \n")

    try:
        subprocess.run(["git","--version"],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Git is not installed or not in PATH\n")
        return False
    print("Git is installed \n")
    return True

def install_git():
    print("Git installation required (Windows)\n")

    print("Please install Git for Windows(I didn't find better sorry buddy):")
    print("https://git-scm.com/download/win\n")

    print("Or via winget on powershell:")
    print("winget install --id Git.Git -e\n")

    return False

#checking the token
def checktokenENV(token : str):
    if not isinstance(token,str) or not re.match("github_pat_",token):
        print("The token must be a string \n")
        return False
    print("Checking GITHUB Token \n")
    token = os.getenv("GIT_TOKEN")
    if not token:
        print("GIT_TOKEN NOT FOUND in the current environnement \n")
        print("Use: export GIT_TOKEN=github_pat_xxxxxx\n")
    print("Token retrieved !\n")
    return True



def test_github_token():
    print("Testing GITHUB token \n")
    _TOKEN_ = os.getenv("GIT_TOKEN")
    if not checktokenENV(_TOKEN_):
        print("An error occured, your token is unacceptable \n")
        return False
    #prepare the core of the request
    headers = {
        "Authorization": f"token {_TOKEN_}",
        "Accept" : "application/vnd.github+json"
    }

    #try out whether the token is received
    try: 
        response = requests.get("https://api.github.com/user",headers=headers)
    #error while reaching out
    except requests.RequestException:
        print("An error occured on the network side while reaching github \n")
        return False
    #token invalid token
    if response.status_code != 200:
        print("Invalid GitHub token\n")
        print("Status:", response.status_code)
        return False
    
    print("GitHub token valid \n")
    print(f"Logged as: {response.json().get("login"),"\n"} ")
    return True

    
