import argparse
import re

NO_IP_WITH_LOCAL_PORT_MESSAGE = "Cannot use custom ports without specified ip address"
INVALID_IP_MESSAGE = "Provided socket is invalid"
INVALID_PORT_MESSAGE = "Provided port is invalid"

PORT_REGEX = r'(?P<PORT>\d{1,5}$)'
IP_V4_SOCKET_REGEX = r'^(?P<IP>((\d{1,3}\.){3}\d{1,3})|(localhost)):(?P<PORT>\d{1,5}$)'

DEFAULT_LOCAL_SERVER_PORT = "54321"
# DEFAULT_REMOTE_SERVER_PORT = "54322"

# Configuration variables
MULTIPLAYER = False
LOCAL_SERVER_PORT = None
REMOTE_SERVER_SOCKET = None
REMOTE_SERVER_IP = None
REMOTE_SERVER_PORT = None

parser = argparse.ArgumentParser(description="Configuration CLI")
parser.add_argument(
    'socket',
    type=str,
    nargs="?",
    default="",
    help='Sockets (<ip>:<port>) address to connect to for multiplayer',
)
parser.add_argument(
    '--local-port',
    type=str,
    default=0,
    help='Custom port for local server (default:54321)',
)

args: argparse.Namespace | None = None
is_configuration_initialized = False


def init_configuration() -> None:
    global is_configuration_initialized, DEFAULT_LOCAL_SERVER_PORT
    global REMOTE_SERVER_SOCKET, LOCAL_SERVER_PORT, REMOTE_SERVER_IP, REMOTE_SERVER_PORT, MULTIPLAYER
    if is_configuration_initialized:
        return
    args = parser.parse_args()
    REMOTE_SERVER_SOCKET = args.socket
    LOCAL_SERVER_PORT = args.local_port if args.local_port else DEFAULT_LOCAL_SERVER_PORT
    if not re.match(PORT_REGEX, LOCAL_SERVER_PORT):
        raise AttributeError(INVALID_PORT_MESSAGE)
    if LOCAL_SERVER_PORT == 0 and REMOTE_SERVER_SOCKET == "":
        raise AttributeError(NO_IP_WITH_LOCAL_PORT_MESSAGE)
    REMOTE_SERVER_IP, REMOTE_SERVER_PORT = parse_socket(REMOTE_SERVER_SOCKET)
    MULTIPLAYER = REMOTE_SERVER_IP != ""
    is_configuration_initialized = True


def parse_socket(socket: str) -> tuple[str, str]:
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
