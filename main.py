import sys
from pip_checker import *
from git_checker import *

_GIT_USER = "MeidiLprog"
_GIT_EMAIL_ = "m.lef3105@gmail.com"


def main():

    # python + pip
    if not pipchecker():
        return

    if not check_pypi():
        return

    if not upgrade_pip():
        return

    if not install_lib():
        return

    # git
    if not check_git():
        install_git()
        return

    # Github authentication
    if not test_github_token():
        return

    # repo name
    repo_name = input("Repository name: ").strip()
    if not repo_name:
        print("Invalid repository name")
        return

    private = input("Private repo? (y/n): ").lower() == "y"

    # handle remote
    if not create_git_repo(repo_name, private):
        return

    # pipeline git
    if not initgetRepo():
        return

    if not configStuff(_GIT_USER, _GIT_EMAIL_):
        return

    if not createFiles(repo_name):
        return

    if not gitaddAll():
        return

    if not initialCommit():
        return

    if not setBranch():
        return

    if not gitsetRemote(repo_name):
        return

    if not git_push():
        return

    print("\nSETUP COMPLETED SUCCESSFULLY\n")


if __name__ == "__main__":
    main()
