import os
from dotenv import load_dotenv

load_dotenv()

PAPERTRAIL_HOST: str = os.environ["PAPERTRAIL_HOST"]
PAPERTRAIL_PORT: int = int(os.environ["PAPERTRAIL_PORT"])
PORT = int(os.environ["PORT"])

