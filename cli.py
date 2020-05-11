#! /usr/bin/env python

import os
from pprint import pprint
import sys
from urllib.parse import urljoin

import click
import requests

BASE = os.getenv("EMBY_API_URL")
KEY = os.getenv("EMBY_API_KEY")


@click.group()
def cli():
    pass


@cli.command("get-user")
@click.argument("username", type=str)
def get_user(username: str):
    users_resp = requests.get(urljoin(BASE, "/Users"), params={"api_key": KEY})
    if users_resp.status_code == 200:
        users = {user["Name"]: user for user in users_resp.json()}

        pprint(users[username])
    else:
        print("Invalid response code received: {users_resp.status_code}")


@cli.command("get-folders")
def get_folders():
    folders_resp = requests.get(
        urljoin(BASE, "/Library/MediaFolders"), params={"api_key": KEY}
    )
    if folders_resp.status_code == 200:
        folders = {
            folder["Name"]: folder["Id"]
            for folder in folders_resp.json()["Items"]
        }

        pprint(folders)
    else:
        print("Invalid response code received: {folders_resp.status_code}")


if __name__ == "__main__":
    sys.exit(cli())
