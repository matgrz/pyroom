import xlrd
from .baseconfig import UniversalConfig
from utils import log


first_data_row = 4
fixed_params_row = 1
log = log.Log()


def parse_config(path):
    """
    Prepares simulation config objects based on xlsx file.
    :param path: path to xlsx file
    :return: list of simulation configs
    """
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)

    fixed_params = parse_fixed_params(sheet)
    configs = []
    for row in range(first_data_row, sheet.nrows):
        current_data_row = sheet.row_values(row)
        log.DBG("parsed data:", current_data_row)
        formatted_data = set_proper_format(current_data_row)
        cfg = UniversalConfig(formatted_data)
        cfg.fill_fixed_params(data=fixed_params)
        configs.append(cfg)

    return configs


def set_proper_format(data):
    """
    Converts parsed data to desirable format.
    :param data: a row parsed from xlsx file
    :return: list of formatted data
    """
    return [float(data[0]), int(data[1]), eval(data[2]), eval(data[3]), int(data[4]), float(data[5]), float(data[6]),
            eval(data[7]), eval(data[8]), data[9]]


def parse_fixed_params(sheet):
    """
    Parses data which is exactly the same for every parsed config object.
    :param sheet: xlrd sheet
    :return: list of formatted data
    """
    fixed_params = sheet.row_values(1)
    log.DBG("parsed fixed params: ", fixed_params)
    return [int(fixed_params[1]), int(fixed_params[2]), float(fixed_params[3]), bool(fixed_params[4]),
            bool(fixed_params[5]), bool(fixed_params[6]), float(fixed_params[7])]
