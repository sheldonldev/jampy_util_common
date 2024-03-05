from datetime import datetime


def format_now(format: str = '%Y%m%d_%H%M%S', utc: bool = True) -> str:
    if utc is True:
        return f'{datetime.utcnow().strftime(format)}_UTC'
    else:
        return f'{datetime.now().strftime(format)}'
