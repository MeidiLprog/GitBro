#############################
## Lefki Meidi              #
## Quick setup(Windows only)#
## #######################


import subprocess
import os
import socket
import sys

#calling interpreter
_PYTHON_ = sys.executable

CURRENT_PATH = os.getcwd()

#let us check for pip
def pipchecker():
    print("Seeking out pip \n")
    try:
        #simply running the command to check for pip and its version
        subprocess.run([_PYTHON_,"-m","pip","--version"],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:#If there was an error in the process (exit)
        print("An error occured\n")
        return False
    
    print("PIP is installed and op !\n")
    return True 

#upgrading pip
def upgrade_pip():
    print("Updating pip\n")

    try:
        subprocess.run([_PYTHON_, "-m", "pip", "install", "--upgrade", "pip"],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    except subprocess.CalledProcessError:
        print("Pip failed to update \n")
        return False
    print("pip updated \n")
    return True

'''
pip when trying to upgrade is going to connect to pypi to retrieve the dependencies 

'''

def check_pypi():
    print("Updating pip\n")

    try:
        socket.create_connection(("pypi.org",443),timeout=5)
    except OSError:
        print("Pypi is unreachable, check on your side whether a vpn/proxy is blocking\n")
        return False
    
    print("Pypi is accessible \n")
    return True

def install_lib():
    print("installing libs \n")

    if not os.path.isfile("requirements.txt"):
        print("requirements is nowhere to be found \n")
    
    CURRENT_FILE = os.path.join(CURRENT_PATH,"requirements.txt")

    if os.path.getsize(CURRENT_FILE) == 0:
        print("requirements is an empty file !\n")
        return False
    
    try: 
        subprocess.run(["py","-m","pip","install","-r",CURRENT_FILE])
    except subprocess.CalledProcessError:
        print("Couldn't install libs\n")
        return False
    
    return True


