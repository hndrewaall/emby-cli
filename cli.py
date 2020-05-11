#! /usr/bin/env python

import os
from pprint import pprint
import sys
from typing import Dict
from urllib.parse import urljoin

import click
import requests

BASE = os.getenv("EMBY_API_URL")
KEY = os.getenv("EMBY_API_KEY")


@click.group()
def cli():
    pass


def get_users() -> Dict:
    users_resp = requests.get(urljoin(BASE, "/Users"), params={"api_key": KEY})
    if users_resp.status_code == 200:
        users = {user["Name"]: user for user in users_resp.json()}

        return users
    else:
        raise RuntimeError(
            "Invalid response code received: {users_resp.status_code}"
        )


@cli.command("get-user")
@click.argument("username", type=str)
def get_user_cmd(username: str):
    pprint(get_users()[username])


def get_folders() -> Dict:
    folders_resp = requests.get(
        urljoin(BASE, "/Library/MediaFolders"), params={"api_key": KEY}
    )
    if folders_resp.status_code == 200:
        folders = {
            folder["Name"]: folder["Id"]
            for folder in folders_resp.json()["Items"]
        }

        return folders
    else:
        raise RuntimeError(
            "Invalid response code received: {folders_resp.status_code}"
        )


@cli.command("get-folders")
def get_folders_cmd():
    pprint(get_folders())


@cli.command("enable-folder-globally")
@click.argument("folder", type=str)
def enable_folder_globally(folder: str):
    users = get_users()
    folders = get_folders()
    folder_id = folders[folder]

    for user in users:
        user_id = users[user]["Id"]
        policy = users[user]["Policy"]

        if not policy["EnableAllFolders"]:
            enabled_folders = policy["EnabledFolders"]
            if folder_id not in enabled_folders:
                print(f"Enabling {folder} for {user}")
                enabled_folders.append(folder_id)
                update_resp = requests.post(
                    urljoin(BASE, f"/Users/{user_id}/Policy"),
                    params={"api_key": KEY},
                    json=policy,
                )
                resp_code = update_resp.status_code
                if resp_code == 204:
                    print(f"Updated policy for {user} successfully!")
                else:
                    print(f"Update failed with status {resp_code}")


if __name__ == "__main__":
    sys.exit(cli())
