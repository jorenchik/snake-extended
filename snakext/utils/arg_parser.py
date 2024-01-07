"""
This module handles argument parsing for configuring multiplayer settings in a 
game. It utilizes argparse to process command-line arguments, specifically for 
setting up socket connections in a multiplayer environment. The module validates
IP addresses and ports for remote servers, sets up local server ports, and 
initializes multiplayer configurations based on the provided arguments.
"""

import argparse
import re

NO_IP_WITH_LOCAL_PORT_MESSAGE = "Cannot use custom ports without specified ip address or socket."
INVALID_IP_MESSAGE = "Provided socket is invalid"
INVALID_PORT_MESSAGE = "Provided port is invalid"

PORT_REGEX = r'(?P<PORT>\d{1,5}$)'
IP_V4_SOCKET_REGEX = r'^(?P<IP>((\d{1,3}\.){3}\d{1,3})|(localhost)):?(?P<PORT>\d{1,5}$)?'

DEFAULT_LOCAL_SERVER_PORT = "54321"
DEFAULT_REMOTE_SERVER_PORT = "54321"

# Configuration variables
MULTIPLAYER = False
LOCAL_SERVER_IP = None
LOCAL_SERVER_PORT = None
REMOTE_SERVER_SOCKET = None
REMOTE_SERVER_IP = None
REMOTE_SERVER_PORT = None
LOCALHOST_IPS = ("127.0.0.1", "localhost")
REMOTE_LISTEN_IP = "0.0.0.0"

parser = argparse.ArgumentParser(
    description="""Snake game with both singleplayer and multiplayer. You need 
    to get as big a snake as possible while not hitting yourself or other 
    snake. Change direction with UDLR or KJHL.""")
parser.add_argument(
    'socket',
    type=str,
    nargs="?",
    default="",
    help="""Sockets or IP address to connect to for multiplayer.
    Usage: <ip>:<socket> or <ip> for default port.""",
)
parser.add_argument(
    '--local-port',
    type=str,
    default=0,
    help="""Custom port for local server if socket is provided for multiplayer.
    Defaults to 54321.""",
)

args: argparse.Namespace | None = None
is_configuration_initialized = False


def parse_arguments() -> None:
    """
    Parses command-line arguments to configure the game's multiplayer settings.

    This function initializes global configuration variables based on the provided command-line arguments. It sets up the local server port and remote server socket, and validates their formats. It also determines if the game is in multiplayer mode based on the presence of a remote server IP address.

    Raises:
        AttributeError: If the local server port or remote server socket is invalid.
    """
    global is_configuration_initialized
    global REMOTE_SERVER_SOCKET, LOCAL_SERVER_PORT, REMOTE_SERVER_IP, REMOTE_SERVER_PORT, MULTIPLAYER, LOCAL_SERVER_IP
    if is_configuration_initialized:
        return
    args = parser.parse_args()
    REMOTE_SERVER_SOCKET = args.socket
    LOCAL_SERVER_PORT = args.local_port if args.local_port else "0"
    if LOCAL_SERVER_PORT != "0" and REMOTE_SERVER_SOCKET == "":
        raise AttributeError(NO_IP_WITH_LOCAL_PORT_MESSAGE)
    if LOCAL_SERVER_PORT == "0":
        LOCAL_SERVER_PORT = DEFAULT_LOCAL_SERVER_PORT
    if not re.match(PORT_REGEX, LOCAL_SERVER_PORT):
        raise AttributeError(INVALID_PORT_MESSAGE)
    REMOTE_SERVER_IP, REMOTE_SERVER_PORT = _parse_socket(REMOTE_SERVER_SOCKET)
    MULTIPLAYER = REMOTE_SERVER_IP != ""
    if REMOTE_SERVER_IP not in LOCALHOST_IPS:
        LOCAL_SERVER_IP = REMOTE_LISTEN_IP
    if REMOTE_SERVER_PORT == "":
        REMOTE_SERVER_PORT = DEFAULT_REMOTE_SERVER_PORT
    is_configuration_initialized = True


def _parse_socket(socket: str) -> tuple[str, str]:
    """
    Parses the socket string to extract the IP address and port.

    Args:
        socket (str): The socket string in the format '<ip>:<port>'.

    Returns:
        tuple[str, str]: A tuple containing the extracted IP address and port.

    Raises:
        AttributeError: If the provided socket string is not in a valid format.
    """
    is_ip_valid = re.match(IP_V4_SOCKET_REGEX, socket)
    if socket != "" and not is_ip_valid:
        raise AttributeError(INVALID_IP_MESSAGE)
    remote_port = re.sub(
        IP_V4_SOCKET_REGEX,
        r'\g<PORT>',
        socket,
    )
    remote_ip = re.sub(
        IP_V4_SOCKET_REGEX,
        r'\g<IP>',
        socket,
    )
    return remote_ip, remote_port
