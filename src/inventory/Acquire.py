import os
import sys
import base64
import pennant
import requests

from .Instance import Instance
from .Exceptions import *

from dotenv import load_dotenv

load_dotenv()

class Acquisition:
    """A class to handle acquiring and transmitting new items to the inventory system.

    This class processes item acquisitions by validating files and transmitting them 
    to the inventory API endpoint.

    :ivar sys.argv: Command line arguments containing files to process
    :type sys.argv: list
    """
    def __init__(self):
        """Initialize the acquisition process for multiple files.
        
        Processes all files provided as command line arguments, creating
        Instance objects and transmitting them to the API.
        
        :return: None
        :rtype: None
        :raises FileNotFoundError: If specified files don't exist
        :raises requests.exceptions.RequestException: If API transmission fails
        """
        # Accommodate multiple files; acquire each serially
        for file in sys.argv[1:]:
            instance = Instance(file)
            self.__transmit_to_api(instance)

    def __transmit_to_api(self, instance: dict = {}) -> None:
        """Transmit an item instance to the inventory API.

        :param instance: Instance object containing item data and binary content
        :type instance: Instance
        :return: None
        :rtype: None
        :raises requests.exceptions.RequestException: If the API request fails
        """
        response = requests.post(
            f"{os.getenv('API_URL')}:{os.getenv('API_PORT')}/v1/inventory/add/",
            data = instance.transmit,
            files = {"item_binary": instance.binary}
        )
        if response.status_code == 409:
            context = response.json()
            print(context['error'])

def cmd():
    """Command entry point for the get command.
    
    Validates command usage and initializes item acquisition.

    :raises InvalidCommandException: If not called via the 'get' command
    :raises InvalidArgumentsException: If no item names are provided
    :return: None
    :rtype: None
    """
    # Validate correct use of function
    try:
        if sys.argv[0].split("/")[-1] != "get":
            raise InvalidCommandException(
                "Cannot call Acqusition directly!"
            )
    except InvalidCommandException as e:
        print(e)
        sys.exit(1)
    try:
        if len(sys.argv) < 2:
            raise InvalidArgumentsException(
                "At least one item name required!"
            )
    except InvalidArgumentsException as e:
        print(e)
        sys.exit(1)
    # Failing any issues, add CWD to the path and
    # start Acquisition
    sys.path.append(os.path.expanduser(os.getcwd()))
    Acquisition()
