import datetime


def format_now(format: str = '%Y%m%d_%H%M%S', utc: bool = True) -> str:
    if utc is True:
        return f'{datetime.datetime.now(tz=datetime.UTC).strftime(format)}Z'
    else:
        return f'{datetime.datetime.now().strftime(format)}'
