import logging

from dotenv import load_dotenv

from mserver.mserver import MServer

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)
load_dotenv(dotenv_path="c:\\temp\\.env", override=True)

if __name__ == "__main__":
    server = MServer(server_name="MServer", host="localhost", port=8080)
    server.run()
