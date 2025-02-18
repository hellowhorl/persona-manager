import os
import sys
import base64
import pennant
import requests
import getpass

from dotenv import load_dotenv

from rich.table import Table
from rich.console import Console

load_dotenv()

# TODO: Move these to a specific command file (like others) instead of main

def search(item_name: str = "", qty_required: int = 1) -> bool:
    """Search for an item in the user's inventory.

    :param item_name: Name of item to search for
    :type item_name: str, optional
    :param qty_required: Minimum quantity required
    :type qty_required: int, optional
    :return: True if item exists in required quantity, False otherwise
    :rtype: bool
    :raises requests.exceptions.RequestException: If the API request fails
    """
    response = requests.post(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/search/",
        data = {
            "charname": os.getenv("GITHUB_USER") or getpass.getuser(),
            "item_name": item_name
        }
    )
    return response.status_code == 200 and response.json()["item_qty"] >= qty_required

def list():
    """Display a formatted table of the user's inventory contents.
    
    Shows item names, quantities, space occupied, and whether items are consumable.
    Also displays total inventory space used and remaining.

    :return: None - Prints inventory table to console
    :rtype: None
    :raises requests.exceptions.RequestException: If the inventory API request fails
    """
    allowed = ["item_name", "item_qty", "item_bulk", "item_consumable"]

    api_request = requests.get(
        f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/list",
        params = {
            "charname": os.getenv('GITHUB_USER') or getpass.getuser()
        }
    )

    context = api_request.json()

    total_volume = 0
    for item in context:
        total_volume += item['item_bulk']

    table = Table(title=f"""{os.getenv('GITHUB_USER') or getpass.getuser()}'s inventory
({total_volume}/10.0 spaces; {10.0 - total_volume} spaces remain)""")
    table.add_column("Item name")
    table.add_column("Item count")
    table.add_column("Space Occupied")
    table.add_column("Consumable")

    for item in context:
        values = [str(item[field]) for field in item if field in allowed]
        table.add_row(*values)

    Console().print(table)
