import logging
def SetupLogger(name:str, level:int = logging.INFO) -> logging.Logger:
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    # create console handler with a higher log level
    handler = logging.StreamHandler()
    handler.setLevel(level)
    # create formatter and add it to the handler
    formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    # add the handler to the logger
    logger.addHandler(handler)
    return logger
if __name__ == "__main__":
    logger = SetupLogger("Test", logging.DEBUG)
    logger.debug("Test debug")
    logger.info("Test info")
    logger.warning("Test warning")
    logger.error("Test error")
    logger.critical("Test critical")
