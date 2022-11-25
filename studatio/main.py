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
@click.option('-m', '--month', default=datetime.date.today().month,
              help='int representing a month of the year to export. Defaults to current month.')
@click.option('-y', '--year', default=datetime.date.today().year,
              help='int representing a year to export. Defaults to current year.')
def schedule(month: int, year: int):
    month_year = cal_handler.MonthYear(month, year)
    output(cal_handler.export_schedule([month_year], Settings()))


def output(result: str):
    try:
        pyperclip.copy(result)
    except pyperclip.PyperclipException:
        pass

    click.echo(result)


if __name__ == '__main__':
    main()
