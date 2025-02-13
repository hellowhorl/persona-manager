import os
import sys
import requests

from getpass import getuser
from arglite import parser as cliarg

api_url = cliarg.optional.url or "http://localhost"
api_port = cliarg.optional.port or 8000

class Cmd:

    @staticmethod
    def create():
        name = cliarg.optional.name
        prompt = None
        file = None
        if not name:
            print("No name supplied!")
            sys.exit(1)
        try:
            with open(cliarg.optional.prompt) as fh:
                prompt = fh.read()
        except:
            print("Usable prompt file not found at that location")
            sys.exit(1)
        if cliarg.optional.file:
            try:
                file = open(cliarg.optional.file, "rb")
            except:
                print("Error opening binary file to attach.")
                sys.exit(1)
        response = requests.post(
            f"{api_url}:{api_port}/v1/persona/create/{name}",
            data = {
                "persona_creator": getuser(),
                "persona_prompt": prompt,
                "persona_file_name": cliarg.optional.file or ""
            },
            files = {
                "file_binary": file if file else ""
            }
        )
        print(response.json())

    @staticmethod
    def cancel():
        thread_id = cliarg.optional.thread_id
        if not thread_id:
            print("Missing a thread id!")
            sys.exit(1)
        response = requests.get(
            f"{api_url}:{api_port}/v1/persona/cancel/{thread_id}"
        )
        if not response.status_code == 200:
            print("Error stopping thread.")
        return

    @staticmethod
    def delete(self):
        thread_id = cliarg.optional.thread_id
        if not thread_id:
            print("Missing a thread id!")
            sys.exit(1)
        response = requests.delete(
            f"{api_url}:{api_port}/v1/persona/delete/{thread_id}"
        )
        if not response.status_code == 200:
            print("Error deleting thread.")
        return

def main():
    command = sys.argv[1]
    cmd = Cmd()
    if command == "create":
        cmd.create()
    if command == "cancel":
        cmd.cancel()
    if command == "delete":
        cmd.delete()
