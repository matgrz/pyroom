import logging
import sys

class Log:
    def __init__(self):
        self.logger = logging.getLogger("project_logger")
        if not self.logger.handlers:
            hdlr = logging.FileHandler('logs/main.log')
            formatter = logging.Formatter('%(levelname)s %(message)s')
            console = logging.StreamHandler(sys.stdout)
            console.setFormatter(formatter)
            console.setLevel(logging.INFO)
            hdlr.setFormatter(formatter)
            self.logger.setLevel(logging.DEBUG)
            self.logger.addHandler(hdlr)
            self.logger.addHandler(console)

        if self.instance == 0:
            logging.basicConfig(level=logging.DEBUG,
                                format='%(levelname)-8s %(message)s',
                                filename='logs/main.log',
                                filemode='w')
            open('logs/main.log', 'w').close()

        self.instance += 1

    instance = 0

    def DBG(self, msg, arg=""):
        self.logger.debug(msg + "%s", arg)

    def INFO(self, msg, arg=""):
        self.logger.info(msg + "%s", arg)

    def WRN(self, msg, arg=""):
        self.logger.warning(msg + "%s", arg)

    def ERR(self, msg, arg=""):
        self.logger.error(msg + "%s", arg)
