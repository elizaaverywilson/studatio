import datetime
from importlib.metadata import version
from os import linesep

import hypothesis.strategies as st
import hypothesis as hyp
from _pytest.monkeypatch import MonkeyPatch
from cli_test_helpers import shell
from click.testing import CliRunner

from studatio.events import MonthYear
import studatio.main as main
# See https://youtrack.jetbrains.com/issue/PY-53913/ModuleNotFoundError-No-module-named-pydevtestspython
from .strategies import st_example_urls, st_hours, st_minutes, st_month_opts, st_year_opts


def test_entrypoint():
    result = shell('studatio --help')
    assert result.exit_code == 0


def test_version():
    expected_version = version('studatio')
    result = shell('studatio --version')

    assert result.stdout == f'studatio, version {expected_version}{linesep}'
    assert result.exit_code == 0


@hyp.settings(max_examples=100)
@hyp.given(month_opt=st_month_opts(), year_opt=st_year_opts(), data=st.binary(), url=st_example_urls())
def test_schedule(month_opt, year_opt, data, url):
    """
    Tests whether `studatio schedule` command plugs correct inputs in to `export_schedule`

    Calls with --month and/or --year arguments

    Tests that `studatio schedule` should default to inputting current month/year
    """
    # Arrange
    arguments = []
    inputted_month_years = None
    to_print = None
    today = datetime.datetime.today()
    expected_input = []

    if year_opt is not None:
        expected_input_year = year_opt[1]
        arguments += [year_opt[0], year_opt[1]]
    else:
        expected_input_year = today.year

    if month_opt is not None:
        arguments.insert(0, month_opt[0])
        arguments.insert(1, month_opt[1])
        if type(month_opt[1]) is int:
            months_range = [month_opt[1]]
        else:
            months_range_extremes = str(month_opt[1]).split('-')
            months_range = range(int(months_range_extremes[0]), int(months_range_extremes[1]) + 1)

        for month in months_range:
            expected_input += [MonthYear(month, expected_input_year)]
    else:
        expected_input = [MonthYear(today.month, expected_input_year)]

    def mocked_export_schedule(*args) -> [MonthYear]:
        nonlocal inputted_month_years
        inputted_month_years = args[0]
        return data

    def mocked_output(printing):
        nonlocal to_print
        to_print = printing

    def example_url(_) -> str:
        return url

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
        assert inputted_month_years == expected_input
        assert to_print == data


@hyp.settings(max_examples=100)
@hyp.given(month_opt=st_month_opts(), year_opt=st_year_opts(), hours=st_hours(),
           minutes=st_minutes(), url=st_example_urls())
def test_elapsed(month_opt, year_opt, hours, minutes, url):
    """
    Tests whether `studatio elapsed` command plugs correct inputs in to `elapsed`

    Calls with --month and/or --year arguments

    Tests that `studatio elapsed` should default to inputting current month/year
    """
    # Arrange
    arguments = []
    inputted_month_years = None
    to_print = ''
    today = datetime.datetime.today()
    expected_input = []

    if year_opt is not None:
        expected_input_year = year_opt[1]
        arguments += [year_opt[0], year_opt[1]]
    else:
        expected_input_year = today.year

    if month_opt is not None:
        arguments.insert(0, month_opt[0])
        arguments.insert(1, month_opt[1])
        if type(month_opt[1]) is int:
            months_range = [month_opt[1]]
        else:
            months_range_extremes = str(month_opt[1]).split('-')
            months_range = range(int(months_range_extremes[0]), int(months_range_extremes[1]) + 1)

        for month in months_range:
            expected_input += [MonthYear(month, expected_input_year)]
    else:
        expected_input = [MonthYear(today.month, expected_input_year)]

    def mocked_output(printing):
        nonlocal to_print
        to_print = printing

    def example_url(_) -> str:
        return url

    def mocked_elapsed(*args) -> [MonthYear]:
        nonlocal inputted_month_years
        inputted_month_years = args[0]
        return datetime.timedelta(hours=hours, minutes=minutes)

    with MonkeyPatch().context() as mp:
        mp.setattr('studatio.cal_handler.elapsed_in_months', mocked_elapsed)
        mp.setattr('click.echo', mocked_output)
        mp.setattr('builtins.input', example_url)

        runner = CliRunner()

        # Act
        # noinspection PyTypeChecker
        results = runner.invoke(main.elapsed, arguments)

    # Assert
    assert results.exit_code == 0
    assert inputted_month_years == expected_input

    # Parse formatted "INT Hours, INT Minutes" string
    split_strings = to_print.split(sep=' Hours, ')
    outputted_hours = int(split_strings[0])
    outputted_minutes = int(split_strings[1].split(' ')[0])
    assert outputted_hours == hours
    assert outputted_minutes == minutes


@st.composite
def st_invalid_month_range_opt(draw):
    if draw(st.booleans()):
        opt_str = '-m'
    else:
        opt_str = '--month'

    first_month = draw(st.integers())
    second_month = draw(st.integers())
    if 1 <= first_month < second_month <= 12:
        hyp.reject()
    value = str(first_month) + '-' + str(second_month)

    return tuple([opt_str, value])


@hyp.given(month_opt=st_invalid_month_range_opt(), year_opt=st_year_opts())
def test_commands_throws_for_invalid_month_range(month_opt, year_opt):
    arguments = [month_opt[0], month_opt[1]]
    if year_opt is not None:
        arguments += [year_opt[0], year_opt[1]]

    runner = CliRunner()
    # noinspection PyTypeChecker
    schedule_results = runner.invoke(main.schedule, arguments)
    # noinspection PyTypeChecker
    elapsed_results = runner.invoke(main.elapsed, arguments)

    assert schedule_results.exit_code != 0
    assert elapsed_results.exit_code != 0


@hyp.settings(suppress_health_check=[hyp.HealthCheck.function_scoped_fixture], max_examples=20)
@hyp.given(output_str=st.text())
def test_output(output_str, capsys):
    main.output(output_str)

    assert capsys.readouterr().out.rstrip('\r\n') == output_str.rstrip('\r\n')

# See https://github.com/painless-software/python-cli-test-helpers/issues/25
# def test_command(command='schedule'):
# shell_input = 'studatio {} --help'.format(command)
# result = shell(shell_input)
# assert result.exit_code == 0
