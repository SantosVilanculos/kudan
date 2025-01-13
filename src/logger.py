from logging import DEBUG, INFO, Logger, StreamHandler, basicConfig, getLogger
from logging.handlers import RotatingFileHandler


from custom.contents_path import contents_path

path = contents_path(".log")
# path.mkdir(parents=True, exist_ok=True)

rotating_file_handler = RotatingFileHandler(
    filename=path,
    maxBytes=512,
    backupCount=2,
)
rotating_file_handler.setLevel(INFO)

basicConfig(
    force=True,
    level=DEBUG,
    encoding="UTF-8",
    format="%(asctime)s:%(levelname)s:%(filename)s:%(lineno)d:%(message)s",
    handlers=[StreamHandler(), rotating_file_handler],
)

logger: Logger = getLogger()
