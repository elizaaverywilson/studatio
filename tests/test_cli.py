from importlib.metadata import version
from os import linesep
import datetime

from _pytest.monkeypatch import MonkeyPatch
from cli_test_helpers import shell
from click.testing import CliRunner
from hypothesis import given, reproduce_failure, note, settings, Verbosity
import hypothesis.strategies as st

from studatio.cal_handler import MonthYear
from studatio.main import schedule
# See https://youtrack.jetbrains.com/issue/PY-53913/ModuleNotFoundError-No-module-named-pydevtestspython
from .conftest import st_month_year


def test_entrypoint():
    result = shell('studatio --help')
    assert result.exit_code == 0


def test_version():
    expected_version = version('studatio')
    result = shell('studatio --version')

    assert result.stdout == f'studatio, version {expected_version}{linesep}'
    assert result.exit_code == 0


# Tests whether `studatio schedule` command plugs correct inputs in to `export_schedule`
# Provides --month and --year based on `use_month` or `use_year.
# `studatio schedule` should default to inputting current month/year
# @reproduce_failure('6.58.0', b'AAAAAAAAAAA=')
@given(month_year_input=st_month_year(), use_month=st.booleans(), use_year=st.booleans(), data=st.binary())
@settings(verbosity=Verbosity.verbose, max_examples=1)
def test_schedule(month_year_input, use_month, use_year, data):
    # Arrange
    arguments = []
    inputted_month_years = None
    to_print = None
    today = datetime.datetime.today()

    if use_month:
        expected_input_month = month_year_input.month
        arguments += ['--month', expected_input_month]
    else:
        expected_input_month = today.month
    if use_year:
        expected_input_year = month_year_input.year
        arguments += ['--year', expected_input_year]
    else:
        expected_input_year = today.year
    expected_input = MonthYear(expected_input_month, expected_input_year)

    def mocked_export_schedule(*args) -> [MonthYear]:
        nonlocal inputted_month_years
        inputted_month_years = args[0]
        return data

    def mocked_output(printing):
        nonlocal to_print
        to_print = printing

    with MonkeyPatch().context() as mp:
        mp.setattr('studatio.cal_handler.export_schedule', mocked_export_schedule)
        mp.setattr('studatio.main.output', mocked_output)

        runner = CliRunner()

        # Act
        # noinspection PyTypeChecker
        note(schedule)
        note(arguments)
        results = runner.invoke(schedule, arguments)

    # Assert
    note(results)
    assert results.exit_code == 0
    assert inputted_month_years == [expected_input]
    assert to_print == data
    assert 0 == 1

# See https://github.com/painless-software/python-cli-test-helpers/issues/25
# def test_command(command='schedule'):
# shell_input = 'studatio {} --help'.format(command)
# result = shell(shell_input)
# assert result.exit_code == 0
