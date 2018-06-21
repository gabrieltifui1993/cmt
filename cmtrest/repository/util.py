import arrow
from dateutil.parser import parse

def to_date(date_str):
    return parse(date_str)

def to_local_timezone(date_str):
    return arrow.get(parse(date_str)).to('local').format()