import datetime

MONTHS_TH = [
    'มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน',
    'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม',
    'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม',
]
MONTHS_SHORT = [
    'ม.ค.', 'ก.พ.', 'มี.ค.', 'เม.ย.', 'พ.ค.', 'มิ.ย.',
    'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.',
]


def current_year() -> int:
    return datetime.date.today().year


def current_month() -> int:
    return datetime.date.today().month


def month_name(month: int, short: bool = False) -> str:
    idx = max(1, min(12, month)) - 1
    return MONTHS_SHORT[idx] if short else MONTHS_TH[idx]


def months_list() -> list:
    return [{"num": i + 1, "name": MONTHS_TH[i], "short": MONTHS_SHORT[i]} for i in range(12)]


def years_range(start: int = 2020) -> list:
    return list(range(start, current_year() + 2))
