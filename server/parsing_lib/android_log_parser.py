"""
AndroidLogParser class
"""

import re
from datetime import datetime

from parsing_lib.log_parser import LogParser


class AndroidLogParser(LogParser):

    def __init__(self):
        super().__init__()
        self.log_line_regex = re.compile(
            '(.+?)\\s+(\\d+)\\s+(\\d+) ([IWVEDAF]) (.*?): ((?:.*\\n*)*)')
        self.filter_line_regex = re.compile('-* beginning of')
        self.group_nums = {
            'time': 1,
            'processId': 2,
            'threadId': 3,
            'logType': 4,
            'tag': 5,
            'text': 6,
        }
        self.log_types = {
            'I': 'Info',
            'W': 'Warning',
            'V': 'Verbose',
            'E': 'Error',
            'D': 'Debug',
            'A': 'WTF',
            'F': 'Fatal',
        }

    def _parse_datetime(self, date_string):
        """ Parses a datetime string into a datetime Python object.

        Args:
            date_string: the date string to parse

        Returns:
            datetime: the parsed datetime object
        """
        # On Android, we have to add the year to the string so that it parses
        # correctly.
        current_year = datetime.now().year
        date_string = '%s-%s' % (str(current_year), date_string)

        # Try to parse the datetime using all of the formats provided.
        try:
            date_time = datetime.strptime(date_string, '%Y-%m-%d %H:%M:%S.%f')\
                .replace(tzinfo=None)
            return date_time
        except ValueError:
            # If we got here, it means that that string parse didn't work, just
            # return None.
            return None
