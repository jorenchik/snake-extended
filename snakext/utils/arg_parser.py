import argparse

parser = argparse.ArgumentParser(description="Configuration CLI")
parser.add_argument(
    'role',
    type=str,
    help='Choose the role: host or guest',
)
parser.add_argument(
    '--local_port',
    type=int,
    default=54321,
    help='Local port (local server)',
)

parser.add_argument(
    '--remote_port',
    type=int,
    default=54322,
    help='Remote port (remote server)',
)

args = parser.parse_args()
IS_HOST = args.role == "host"
IS_GUEST = args.role == "guest"
LOCAL_PORT = args.local_port
REMOTE_PORT = args.remote_port
