#!/usr/local/bin/python3
import sys

import pyperclip

import cal_handler

def main():
    if len(sys.argv) == 1:
        export_str = str(cal_handler.export())
    elif len(sys.argv) == 2 or len(sys.argv) == 3:
        month_str = sys.argv[1]
        try:
            int(month_str)
            months = [int(month_str)]
        except ValueError:
            monthBounds = month_str.split('-')
            months = list(range(int(monthBounds[0]), int(monthBounds[1]) + 1))
        export_str = ''
        i = 1
        for month in months:
            if i > 1:
                export_str += '\n'
            if len(sys.argv) == 2:
                export_str += str(cal_handler.export(month))
            else:
                export_str += str(cal_handler.export(month, int(sys.argv[2])))
            i += 1
    else:
        raise AttributeError()
    print(export_str)
    pyperclip.copy(export_str)

if __name__ == "__main__":
    main()
