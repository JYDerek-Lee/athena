from app.http.api import public_api
from app.utils.logger import PotatoLogger, LoggerInitParam


@public_api.route("/v1/pln/write", methods=["POST"])
def pln_write():
    logger = PotatoLogger(LoggerInitParam(is_use_file_logging=True))
    logger.info("[pln_write][Executed] 🌴")


@public_api.route("/", methods=["GET"])
def get_sample():
    logger = PotatoLogger(LoggerInitParam(is_use_file_logging=True))
    logger.info("[get_sample][Executed] 🌴")
    return 'hello world@@@@@@@@@@@@@@@'

