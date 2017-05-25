"""
LogParser class
"""

import re
from datetime import datetime


class LogParser(object):
    """ Handles parsing of all logs from the Mobile API """

    @staticmethod
    def parse(message):
        """ Parses a log message from the Mobile API

        Args:
            message: the actual decoded message

        Returns:
            dict: the message data to be sent to the web browser
        """
        logEntries = []
        # TODO: determine better way of combining the exception stack traces
        # current_log = ''
        for line in message['rawLogData'].splitlines():
            if re.search('--------- beginning of /dev/log/', line) is not None:
                continue

            logEntries.append(LogParser.parse_raw_log(line))

            # if re.search('\\d{2}-\\d{2} \\d{2}:\\d{2}:\\d{2}.\\d{3}', line) is not None:
            #     if current_log != '':
            #         logEntries.append(LogParser.parse_raw_log(current_log))
            #     current_log = ''

            # current_log += '\n%s' % line

            # if current_log != '':
            #     logEntries.append(LogParser.parse_raw_log(current_log))

        return {
            'messageType': 'logData',
            'osType': 'Android',
            'logEntries': logEntries,
        }

    @staticmethod
    def parse_raw_log(log_data):
        """ Parse a raw log line

        Args:
            log_data: the raw log line

        Returns:
            dict: the log entry from the log line
        """
        parsed_log = re.search(
            '(.*?) (\\d*) (\\d*) (.) (.*?): ((?:.*\\n*)*)', log_data)

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
            'logType': log_types[parsed_log.group(4)],
            'tag': parsed_log.group(5),
            'text': parsed_log.group(6),
        }
