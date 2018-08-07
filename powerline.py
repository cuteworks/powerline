from flask import Flask
import logging
import getpass

from systemd.journal import JournaldLogHandler


app = Flask(__name__)
logger = logging.getLogger(__name__)

journald_handler = JournaldLogHandler()

journald_handler.setFormatter(logging.Formatter('[%(levelname)s] %(message)s'))

logger.addHandler(journald_handler)
logger.setLevel(logging.DEBUG)

@app.route('/')
def hello_world():
    logger.info("Test logging")

    return 'Hello World! I am ' + getpass.getuser()


if __name__ == '__main__':
    app.run(port=22026, host="0.0.0.0")
