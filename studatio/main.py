import datetime

import click
import pyperclip

try:
    from . import cal_handler
    from .user_config import Settings
except ImportError:
    import cal_handler
    from user_config import Settings


@click.group(help="Python tool for private music teachers to manage their studio's data.")
@click.version_option()
def main():
    pass


@main.command(help='prints and copies to clipboard a formatted list of studio events.')
@click.option('-m', '--month', default=str(datetime.date.today().month),
              help='int, or range of ints, representing a month/s of the year to export. Defaults to current month.')
@click.option('-y', '--year', default=datetime.date.today().year,
              help='int representing a year to export. Defaults to current year.')
def schedule(month: str, year: int):
    months_range = []
    month_years = []
    try:
        one_month = int(month)
        months_range += [one_month]
    except ValueError:
        months_range_extremes = month.split('-')
        start_month = int(months_range_extremes[0])
        end_month = int(months_range_extremes[1])
        if validate_months(start_month, end_month) is False:
            raise ValueError

        months_range = range(start_month, end_month + 1)

    for a_month in months_range:
        month_years += [cal_handler.MonthYear(a_month, year)]

    output(cal_handler.export_schedule(month_years, Settings()))


def validate_months(start_month: int, end_month: int) -> bool:
    months_valid = True
    if start_month >= end_month:
        months_valid = False
    for month in [start_month, end_month]:
        if month < 1 or month > 12:
            months_valid = False
    return months_valid


def output(result: str):
    try:
        pyperclip.copy(result)
    except pyperclip.PyperclipException:
        pass

    click.echo(result)


if __name__ == '__main__':
    main()
