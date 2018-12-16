import os
import subprocess
import logging
import getpass

from flask import Flask, request, abort
from systemd.journal import JournaldLogHandler


# #########
# Constants
# #########

HOMEDIR = "/home"
STEP_FILE_NAME = ".cuteworks-powerline-steps"


# #######
# Globals
# #######

request_count = 0
endpoint_map = {}

# ################
# Initialize Flask
# ################

app = Flask(__name__)

@app.before_request
def before_request():
    global request_count
    request_count = request_count + 1


@app.route('/')
def splash():
    logger.debug("serving splash endpoint")

    return "Hello world, powerline running as " + getpass.getuser() + " and has served " + str(request_count) +\
           " requests this session"

def route_handler():
    endpoint = request.endpoint
    logger.debug("handling request for route: " + endpoint)
    if endpoint not in endpoint_map:
        logger.debug("endpoint not mapped: " + endpoint)
        abort(500)

    script = endpoint_map[endpoint]

    if not os.access(script, os.X_OK):
        abort(500, "script not executable")

    logger.debug("executing: " + endpoint + " -> " + script)

    subprocess.call([script])
    return "executed as " + getpass.getuser()

# ##############
# Set up logging
# ##############

logger = logging.getLogger("cuteworks-powerline")

journald_handler = JournaldLogHandler()
journald_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

logger.addHandler(journald_handler)
logger.setLevel(logging.DEBUG)


# ###############
# Read step files
# ###############

logger.debug("traversing home directories and parsing step files")

homedirs = [f.path for f in os.scandir(HOMEDIR) if (f.is_dir() and f.name != "lost+found")]

for p in homedirs:
    if not os.path.exists(p + "/" + STEP_FILE_NAME):
        logger.debug("  no step file in " + p)
        continue
    logger.debug("  step file in " + p)

    with open(p + "/" + STEP_FILE_NAME) as f:
        for line in f:
            split = line.rstrip().split(":")

            if len(split) != 2:
                logger.debug("    invalid format, skipping this line: " + line)
                continue

            endpoint = split[0]
            script = split[1]

            if endpoint in endpoint_map:
                logger.debug("    skipping endpoint /" + endpoint + ", already mapped to " + endpoint_map[endpoint])
                continue

            if not os.path.exists(script):
                logger.debug("    script does not exist or is unreadable, skipping this script: " + script)
                continue

            logger.debug("    mapping endpoint: /" + endpoint + " -> " + script)
            endpoint_map[endpoint] = script
            app.add_url_rule("/" + endpoint, endpoint, route_handler, methods=["GET", "POST"])


# ##################
# Launch application
# ##################

logger.debug("ready")
if __name__ == '__main__':
    app.run(port=22026, host="0.0.0.0")
