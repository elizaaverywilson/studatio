import datetime
from importlib.metadata import version
from os import linesep

import hypothesis.strategies as st
from _pytest.monkeypatch import MonkeyPatch
from cli_test_helpers import shell
from click.testing import CliRunner
from hypothesis import given, settings, HealthCheck
import pyperclip

from studatio.cal_handler import MonthYear
import studatio.main as main
# See https://youtrack.jetbrains.com/issue/PY-53913/ModuleNotFoundError-No-module-named-pydevtestspython
from .conftest import st_month_year, st_example_url


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
@given(month_year_input=st_month_year(), use_month=st.booleans(), use_year=st.booleans(), data=st.binary(),
       a_url=st_example_url())
def test_schedule(month_year_input, use_month, use_year, data, a_url):
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

    def example_url(_) -> str:
        return a_url

    with MonkeyPatch().context() as mp:
        mp.setattr('studatio.cal_handler.export_schedule', mocked_export_schedule)
        mp.setattr('studatio.main.output', mocked_output)
        mp.setattr('builtins.input', example_url)

        runner = CliRunner()

        # Act
        # noinspection PyTypeChecker
        results = runner.invoke(main.schedule, arguments)

    # Assert
    assert results.exit_code == 0
    assert inputted_month_years == [expected_input]
    assert to_print == data


@settings(suppress_health_check=[HealthCheck.function_scoped_fixture], max_examples=20)
@given(output_str=st.text())
def test_output(output_str, capsys):
    main.output(output_str)

    assert pyperclip.paste() == output_str
    assert capsys.readouterr().out.rstrip('\r\n') == output_str.rstrip('\r\n')

# See https://github.com/painless-software/python-cli-test-helpers/issues/25
# def test_command(command='schedule'):
# shell_input = 'studatio {} --help'.format(command)
# result = shell(shell_input)
# assert result.exit_code == 0
