"""
iOS Log Parser class
"""

import re
from datetime import datetime

from parsing_lib.log_parser import LogParser


class IosLogParser(LogParser):

    def __init__(self):
        super().__init__()
        self.log_line_regex = re.compile('(.*) (.*)\\[(\\d+):(\\d+)\\] (.*)')
        self.exception_regex = re.compile('(.*?)-{2,} BEGIN UNHANDLED EXCEPTION')
        self.group_nums = {
            'time': 1,
            'tag': 2,
            'processId': 3,
            'threadId': 4,
            'text': 5,
        }

    def _parse_datetime(self, date_string):
        """ Parses a datetime string into a datetime Python object.

        Args:
            date_string: the date string to parse

        Returns:
            datetime: the parsed datetime object
        """
        datetime_formats = [
            '%Y-%m-%d %H:%M:%S.%f',
            '%Y-%m-%d %H:%M:%S.%f%z',
            '%Y-%m-%d %H:%M:%S %z',
        ]

        # Try to parse the datetime using all of the datetime formats.
        for datetime_format in datetime_formats:
            try:
                date_time = datetime.strptime(date_string, datetime_format)\
                    .replace(tzinfo=None)
                return date_time
            except:
                # If we got here, it means that that format didn't work, just
                # allow it to fall through.
                continue

        return None
