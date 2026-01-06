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
def checktokenENV(token: str):
    print("Checking GITHUB Token format\n")

    if not token:
        print("GIT_TOKEN not found in environment\n")
        return False

    if not isinstance(token, str):
        print("Token is not a string\n")
        return False

    if not token.startswith("github_pat_"):
        print("Token does not look like a GitHub PAT\n")
        return False

    print("Token format seems valid\n")
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
    print(f"Logged as: {response.json().get('login')}\n")
    return True

'''
Point of this function(struggled to write it)

verify a token
build an http request -> create the repo
send it
retrieve and interpret the result
return True if obj fullfilled False otherwise


'''
    
def create_git_repo(rep_name : str, private=False):
    print(f"Creating repo: {rep_name}\n")
    token : str = None 
    if checktokenENV(os.getenv("GIT_TOKEN")):
        token = os.getenv("GIT_TOKEN") 
    if not token:
        print("Token missing \n")
        return False
    headers={
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    payload = {
        "name" : rep_name,
        "private": private
    }

    #a timeout added just in case
    try: 
        response = requests.post(
            "https://api.github.com/user/repos",
            headers=headers,
            json=payload,
            timeout=15
        )
    except requests.RequestException:
        print("An error occured while reaching out github \n")
        return False

    if response.status_code == 201:
        print("Repo successfully created ! \n")
        return True
    if response.status_code == 422:
        try:
            data = response.json()
            msg = data.get("message")
        except ValueError:
            msg = response.text
        print(f"Github returned {msg}\n")

    print("Failed to create the repo \n")
    print(f"Error {response.status_code}\n")
    print(response.text, end="\n")
    return False


#### TOKEN CHECKED + REPO CREATED ####

#### NOW THE GIT PIPELINE ####

_GIT_USER = "MeidiLprog"
_GIT_EMAIL_ = "m.lef3105@gmail.com"


def initgetRepo():
    print("Initiliazing repo \n")
    if os.path.isdir(".git"):
        print("Git repo already initialized \n")
        return True
    try:
        #gotta initialize it 
        subprocess.run(["git","init"],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("An error occured while initializinh the repo \n")
        return False
    print("Git repo initialized \n")
    return True


#Global config, basic things just the user and email
def configStuff(name : str, email : str):
    if (not isinstance(name,str)) or (not isinstance(email,str)):
        raise TypeError("Your variables must be of type str\n")
    
    if (len(name) == 0) or (len(email) == 0):
        raise ValueError("Variables cannot be empty \n")
    
    try:
        subprocess.run(["git", "config", "user.name", name],check=True)
        subprocess.run(["git","config","user.email",email])
    except subprocess.CalledProcessError:
        print("Git user couldn't be configured \n")
        return False
    print("Git user configured\n")
    return True


def createFiles(repo_name : str):
    try:
        if not os.path.isfile("README.md"):
            with open("README.md","w",encoding="utf-8") as f:
                f.write(f"{repo_name}\n\nInitial Commit\n")
        if not os.path.isfile(".gitignore"):
            with open(".gitignore","w") as f:
                f.write("__pycache__/\n.env\n*.log\n")
    except OSError:
        print("Failed to create files \n")
        return False
    print("Files created \n")
    return True

def gitaddAll():
    print("Adding files to git index\n")

    try:
        subprocess.run(
            ["git", "add", "."],
            check=True
        )
    except subprocess.CalledProcessError:
        print("Failed to add files\n")
        return False

    print("Files added\n")
    return True

def initialCommit():
    print("The first commit \n")
    try:
        subprocess.run["git","commit","-m","Initial commit"]
    except subprocess.CalledProcessError:
        print("Initial commit failed (maybe already exists)\n")
        return False

    print("Initial commit created\n")
    return True

def setBranch():
    print("This function is particular in regard of issues with git naming Master and not main\n")
    try:
        subprocess.run(["git","branch","-M","main"])
        print("Branch named main \n")
    except subprocess.CalledProcessError:
        print("Failed to set main branch's name \n")
        return False
    print("Main branch set \n")
    return True

def gitsetRemote(repo_name : str, user=_GIT_USER ):
    _REMOTE_URL = f"https://github.com/{_GIT_USER}/{repo_name}.git"

    try:
        subprocess.run([_PYTHON_,"git","remote","remove","origin"],
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        pass
    
    try:
        subprocess.run(["git","remote","add","origin",_REMOTE_URL],check=True)
    except subprocess.CalledProcessError:
        print("Failed to add git remote url \n")
        return False
    print(f"Remote set url {_REMOTE_URL}\n")
    return True

def git_push():
    print("Pushing to GitHub\n")

    try:
        subprocess.run(
            ["git", "push", "-u", "origin", "main"],
            check=True
        )
    except subprocess.CalledProcessError:
        print("Failed to push to GitHub\n")
        return False

    print("Push successful\n")
    return True
