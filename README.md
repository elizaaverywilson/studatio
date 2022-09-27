# studatio

studatio is a Python tool for private music teachers to manage their studio's data.

I am a violin teacher, and am primarily developing this for my own use, but I hope for the project to become useful to more teachers as it grows. Currently, studatio is meant to pull iCal data about music lessons and format in a way that can be useful for lesson schedules or facility reservations. I want to add support for automated facility reservations, billing, and note-taking.

Currently, studatio has only been tested on macOS. It likely runs out of the box on other Unix systems as well, and I would guess it can run on Windows with a few alterations to the file paths.

## Installation

First, install Python if it is not already installed. Use the package manager [pip](https://pip.pypa.io/en/stable/) to install studatio.

```bash
pip install studatio
```

On first use, studatio will prompt you for a URL containing iCal data of your studio's calendar. This is stored in ```.config/studatio/config.toml```

## Usage

```studatio``` prints and copies to clipboard a formatted list of studio events.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change or add. Documentation and test coverage additions are just as welcome as changes to source code. I am an amateur programmer, but I always want to learn, so if there are things that work but are not best practices, I would be eager to hear them.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)
