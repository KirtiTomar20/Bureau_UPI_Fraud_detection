import logging
import logging.handlers as handlers


def get_logger():
    logger = logging.getLogger('fraud_detection_app_logger')
    logger.setLevel(logging.DEBUG)

    if not logger.hasHandlers():
        logHandler = handlers.RotatingFileHandler('../Bureau_UPI_Fraud_detection/logs/fraud_detection_app.log', maxBytes=10000000,
                                                  backupCount=1)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        logHandler.setLevel(logging.DEBUG)
        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)

    return logger