import os
import sys
import types
import base64
import requests
import importlib
import narrator

from dotenv import load_dotenv
from .Instance import Instance

load_dotenv()

class Give:
    """A class to handle giving items to other users in the inventory system.

    This class processes item transfers between users by validating ownership,
    confirming the transfer, and updating the inventory system.

    :ivar item_name: Name of item to transfer
    :type item_name: str
    :ivar item_receiver: Username of recipient
    :type item_receiver: str
    """

    def __init__(self, item_name, item_receiver):
        """Initialize the give process for transferring an item.

        :param item_name: Name of item to transfer
        :type item_name: str
        :param item_receiver: Username of recipient
        :type item_receiver: str
        :raises SystemExit: If item is not found in inventory
        """
        self.item_name = item_name
        self.item_receiver = item_receiver
        item_record = self.__search_inventory()
        if not item_record:
            print(f"You don't seem to have any {self.item_name}!")
            sys.exit(1)
        self.__give_item(item_record)

    def __search_inventory(self) -> dict:
        """Search for an item in the user's inventory.

        :return: Item record if found, empty dict if not found
        :rtype: dict
        :raises requests.exceptions.RequestException: If the API request fails
        """
        item = requests.post(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/search/",
            data = {
                "charname": os.getenv('GITHUB_USER') or getpass.getuser(),
                "item_name": self.item_name
            }
        )
        if item.status_code == 200:
            return item.json()
        return {}

    def __confirm_transfer(self) -> bool:
        """Prompt user to confirm the item transfer.

        :return: True if user confirms, False if declined
        :rtype: bool
        """
        # TODO: Could substitute with YesNoQuestion (from narrator)
        q = narrator.Question({
            "question": f"Give {self.item_name} to {self.item_receiver}?",
            "responses": [
                {"choice": "yes", "outcome": True},
                {"choice": "no", "outcome": False}
            ]
        })
        return q.ask()

    def __give_item(self, item_record) -> None:
        """Transfer an item to another user's inventory.

        :param item_record: Record of item to transfer
        :type item_record: dict
        :return: None
        :rtype: None
        :raises SystemExit: If transfer is cancelled or fails
        :raises requests.exceptions.RequestException: If the API request fails
        """
        response = self.__confirm_transfer()
        if not response:
            print("Transfer cancelled.")
            sys.exit(0)
        result = requests.patch(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/transfer/{self.item_receiver}",
            data = {
                "charname": os.getenv('GITHUB_USER') or getpass.getuser(),
                "item_name": self.item_name
            }
        )
        if result.status_code == 200:
            print("Transfer successful!")
            sys.exit(0)
        print("Transfer not successful")
        sys.exit(1)

def cmd():
    """Command entry point for giving items.
    
    Process command line arguments and initialize item transfer.
    
    :return: None
    :rtype: None
    :raises SystemExit: If required arguments are missing
    """
    Give(*sys.argv[1:3])
