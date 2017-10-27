from wifi import Cell, Scheme
from re import match

wifi_interface = "eno1"
sonoff_ssid_prefix = "ITEAD-10000"


def scan():
    cells = Cell.where(wifi_interface, lambda x: match(r"" + sonoff_ssid_prefix + ".*", x))
    return cells

scan()