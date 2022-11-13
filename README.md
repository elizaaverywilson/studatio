# studatio

![PyPI](https://img.shields.io/pypi/v/studatio)

`studatio` is a Python tool for private music teachers to manage their studio's data.

I am primarily developing this for my own use as a violin teacher. However, I hope for the project to become useful to
other teachers. Currently, studatio pulls and formats iCal data about music lessons for use in lesson schedules or
facility reservations. I hope to add support for automated facility reservations, billing, and note-taking.

## Installation

First, install Python if it is not already installed. Use the package manager [pip](https://pip.pypa.io/en/stable/) to
install studatio.

```bash
pip install studatio
```

On first use, studatio will prompt you for a URL containing iCal data of your studio's calendar.

## Usage

```
studatio schedule [OPTIONS]
Options:
  --month INTEGER  int representing a month of the year to export
  --year INTEGER   int representing a year to export
```

Example:

```
% studatio schedule --month 1 --year 2022
Jan 01 2022 Violin Lesson 10:45 AM to 11:45 AM
Jan 07 2022 Violin/Viola Lessons 04:30 PM to 06:15 PM
Jan 08 2022 Violin Lesson 12:30 PM to 01:30 PM
Jan 18 2022 Violin Lesson 06:05 PM to 06:35 PM
Jan 21 2022 Violin Lessons 03:30 PM to 05:30 PM
Jan 28 2022 Viola Lesson 05:30 PM to 06:15 PM
```

## Contributing

To build, you must install poetry and pre-commit. Pull requests are welcome. Documentation and test changes are just as
welcome as changes to source code.

I am an amateur programmer, but I always want to learn, so if there are things that work but are not best practices, I
would be eager to hear them.

## License
[MIT](https://choosealicense.com/licenses/mit/)
