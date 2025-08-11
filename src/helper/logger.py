from datetime import datetime
import loguru


def init_sdk_logger(logger_level):
    loguru.logger.add(
        "logs/{name}.log".format(name=datetime.now().strftime("%Y.%m.%d_%H.%M.%S")),
        level=logger_level,
    )
    loguru.logger.info(f"log level: {logger_level}")
