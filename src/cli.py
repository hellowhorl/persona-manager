import os
import sys
import requests

from inventory.Instance import Instance

from getpass import getuser
from arglite import parser as cliarg

from rich.table import Table
from rich.console import Console

api_url = cliarg.optional.url or "http://localhost"
api_port = cliarg.optional.port or 8000

class Cmd:

    @staticmethod
    def create():
        file = None
        prompt = None
        name = cliarg.optional.name
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
    def delete():
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

    @staticmethod
    def inventory():
        name = cliarg.optional.name
        if not name:
            print("Need to supply a persona template name.")
            sys.exit(1)
        add = cliarg.optional.add
        listing = cliarg.optional.listing
        if not listing and not add:
            print("Need a method (--listing or --add).")
            sys.exit(1)
        if listing:
            response = requests.get(
                f"{api_url}:{api_port}/v1/inventory/list?charname={name}"
            )
            Cmd.__make_inventory_table(
                name,
                response.json()
            )
        if add:
            count = cliarg.optional.count or 1
            item = cliarg.optional.item
            if not item:
                print("An item is required!")
            instance = Instance(item)
            instance.transmit['item_owner'] = name
            response = requests.post(
                f"{api_url}:{api_port}/v1/inventory/add/",
                data = instance.transmit,
                files = {"item_binary": instance.binary}
            )
            if response.status_code == 409:
                context = response.json()
                print(content['error'])

    @staticmethod
    def __make_inventory_table(name: str = "", inventory: dict = {}) -> None:
        total_volume = 0
        for item in inventory:
            total_volume += item['item_bulk']

        allowed = ["item_name", "item_qty", "item_bulk", "item_consumable"]

        table = Table(title=f"""{name}'s inventory
({total_volume}/10.0 spaces; {10.0 - total_volume} spaces remain)""")
        table.add_column("Item name")
        table.add_column("Item count")
        table.add_column("Space Occupied")
        table.add_column("Consumable")

        for item in inventory:
            values = [str(item[field]) for field in item if field in allowed]
            table.add_row(*values)

        Console().print(table)

def main():
    command = sys.argv[1]
    cmd = Cmd()
    if command == "create":
        cmd.create()
    if command == "cancel":
        cmd.cancel()
    if command == "delete":
        cmd.delete()
    if command == "inventory":
        sys.path.append(os.path.expanduser(os.getcwd()))
        cmd.inventory()
