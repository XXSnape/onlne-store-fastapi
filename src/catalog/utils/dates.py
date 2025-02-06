from datetime import date


def get_day_and_month(d: date) -> str:
    return d.strftime("%d-%m")
