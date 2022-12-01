# studatio

![PyPI](https://img.shields.io/pypi/v/studatio)

`studatio` is a Python tool for private music teachers to manage their studio's data.

I am primarily developing this for my own use as a violin teacher. However, I hope for the project to become useful to
other teachers. Currently, studatio pulls and formats Apple iCal data about music lessons for use in lesson schedules or
facility reservations.

I hope to add support for automated facility reservations, expanded business statistics, billing, and note-taking.

## Installation

First, [install Python](https://www.python.org/downloads/) if it is not already installed. Use the package
manager [pip](https://pip.pypa.io/en/stable/) to
install studatio.

```bash
pip install studatio
```

On first use, studatio will prompt you for a URL containing iCal data of your studio's calendar.

## Usage

```
Usage: studatio schedule [OPTIONS]

  Prints and copies to clipboard a formatted list of
  studio events.

Options:
  -m, --month TEXT    Integer, or range of ints
                      separated by a hyphen,
                      representing a month/s of the
                      year. Defaults to current
                      month.
  -y, --year INTEGER  Defaults to current year.
```

```
Usage: studatio elapsed [OPTIONS]

  Prints the time elapsed of events in the given
  period

Options:
  -m, --month TEXT    Integer, or range of ints
                      separated by a hyphen,
                      representing a month/s of the
                      year. Defaults to current
                      month.
  -y, --year INTEGER  Defaults to current year.
```

Examples:

```
% studatio schedule --month 1 --year 2022
Jan 01 2022 Violin Lesson 10:45 AM to 11:45 AM
Jan 07 2022 Violin/Viola Lessons 04:30 PM to 06:15 PM
Jan 08 2022 Violin Lesson 12:30 PM to 01:30 PM
Jan 18 2022 Violin Lesson 06:05 PM to 06:35 PM
Jan 21 2022 Violin Lessons 03:30 PM to 05:30 PM
Jan 28 2022 Viola Lesson 05:30 PM to 06:15 PM
```

`studatio schedule -m 10-12`

`% studatio elapsed --month 10 --year 2022
22 Hours, 0 Minutes Elapsed`

## Contributing

To build, you must install [poetry](https://python-poetry.org/) and [pre-commit](https://pre-commit.com/). Pull requests
are welcome. Documentation and test changes are just as
welcome as changes to source code.

I am an amateur programmer, but I always want to learn, so if there are things that work but are not best practices, I
would be eager to hear them.

## License
[MIT](https://choosealicense.com/licenses/mit/)
