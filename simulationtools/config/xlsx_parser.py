import xlrd
from .baseconfig import UniversalConfig
from utils import log


first_data_row = 2
log = log.Log()


def parse_config(path):
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)

    configs = []
    for row in range(2, sheet.nrows):
        current_data_row = sheet.row_values(row)
        log.DBG("parsed data:", current_data_row)
        formatted_data = set_proper_format(current_data_row)
        cfg = UniversalConfig(formatted_data)
        configs.append(cfg)

    return configs


def set_proper_format(data):
    return [float(data[0]), int(data[1]), eval(data[2]), eval(data[3]), int(data[4]), float(data[5]), float(data[6]),
            eval(data[7]), eval(data[8]), data[9]]
