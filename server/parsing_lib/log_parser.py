"""
LogParser class
"""

import json
import re
from datetime import datetime


class LogParser(object):

    @staticmethod
    def parse(message):
        logEntries = []
        current_log = None
        for line in message['rawLogData'].splitlines():
            line = line.strip()
            if re.search('^\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}.\\d{3}', line) is not None:
                if current_log is not None:
                    logEntries.append(LogParser.parse_raw_log(current_log))
                current_log = ''

            current_log += '\n%s' % line

        logEntries.append(LogParser.parse_raw_log(current_log))

        return {
            'messageType': 'logData',
            'osType': 'Android',
            'logEntries': logEntries,
        }

    @staticmethod
    def parse_raw_log(log_data):
        parsed_log = re.search(
            '(.*?) (\\d*)-(\\d*)\\/(.*?) (.)\\/(.*?): ((?:.*\\n*)*)', log_data)

        # Parse the Year, we have to add the year to the string so that it
        # parses correctly.
        current_year = datetime.now().year
        date_with_year = '%s-%s' % (str(current_year), parsed_log.group(1))
        log_time = datetime.strptime(date_with_year, '%Y-%m-%d %H:%M:%S.%f')

        # Determine the log type
        log_types = {
            'I': 'Info',
            'W': 'Warning',
            'V': 'Verbose',
            'E': 'Error',
            'D': 'Debug',
            'A': 'WTF',
        }

        return {
            'time': log_time,
            'logType': log_types[parsed_log.group(5)],
            'tag': parsed_log.group(6),
            'text': parsed_log.group(7),
        }
