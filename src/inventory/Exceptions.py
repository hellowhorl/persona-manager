class InvalidCommandException(Exception):
    """Exception raised when an invalid command is used.

    :param args: Variable length argument list
    :type args: tuple
    """

    def __init__(self, *args):
        """Initialize the exception with the provided arguments.

        :param args: Variable length argument list
        :type args: tuple
        """
        super().__init__(*args)

class InvalidArgumentsException(Exception):
    """Exception raised when invalid arguments are provided to a command.

    :param args: Variable length argument list
    :type args: tuple
    """

    def __init__(self, *args):
        """Initialize the exception with the provided arguments.

        :param args: Variable length argument list
        :type args: tuple
        """
        super().__init__(*args)