"""
LogParser class
"""

import re

from datetime import datetime


class LogParser(object):
    """ Handles parsing of all logs from the Mobile API.

    Attributes:
        parser_info: info required by the parser that is specific to each OS
    """
    parser_info = {
        'Android': {
            'logLineRegex': re.compile(
                '(.*)\\s+(\\d*)\\s+(\\d*) ([IWVEDAF]) (.*?): ((?:.*\\n*)*)'),
            'datetimeFormat': ['%Y-%m-%d %H:%M:%S.%f'],
            'filterLineRegex': re.compile('-* beginning of'),
            'groupNums': {
                'time': 1,
                'processId': 2,
                'threadId': 3,
                'logType': 4,
                'tag': 5,
                'text': 6,
            },
            'logTypes': {
                'I': 'Info',
                'W': 'Warning',
                'V': 'Verbose',
                'E': 'Error',
                'D': 'Debug',
                'A': 'WTF',
                'F': 'Fatal',
            },
        },
        'iOS': {
            'logLineRegex': re.compile('(.*) (.*)\\[(\\d+):(\\d+)\\] (.*)'),
            'datetimeFormat': [
                '%Y-%m-%d %H:%M:%S.%f',
                '%Y-%m-%d %H:%M:%S.%f%z',
                '%Y-%m-%d %H:%M:%S %z'
            ],
            'exceptionRegex': re.compile('(.*?)-{2,} BEGIN UNHANDLED EXCEPTION'),
            'groupNums': {
                'time': 1,
                'tag': 2,
                'processId': 3,
                'threadId': 4,
                'text': 5,
            },
        },
    }


    @staticmethod
    def parse(raw_log_lines, os_type):
        """ Parses a log message from the Mobile API. Note, this is a Generator
        function.

        Args:
            raw_log_lines (string): the raw log lines
            os_type (string): the OS type from which the logs came ("iOS" or
                "Android")

        Generates:
            a single log entry dictionary every time the function is called
        """
        # If there are no log lines, don't do anything.
        if not raw_log_lines or raw_log_lines.isspace():
            return []

        # Grab the regexes from the config.
        filter_regex = LogParser.parser_info[os_type]\
            .get('filterLineRegex', None)
        exception_regex = LogParser.parser_info[os_type]\
            .get('exceptionRegex', None)

        current_log = None
        in_unhandled_exception = False
        multiline = False

        for line in raw_log_lines.splitlines():
            # Skip lines that are not log lines. There may be cases when these
            # appear in a log line that is not at the beginning of the raw
            # data.
            if filter_regex and filter_regex.match(line):
                continue

            # Check to see if an iOS unhandled exception is starting.
            if exception_regex:
                exception_groups = exception_regex.match(line)
                if exception_groups:
                    in_unhandled_exception = True
                    multiline = True
                    exception_time_string = exception_groups.group(1)
                    current_log = {
                        'time': LogParser._parse_datetime(exception_time_string,
                            os_type),
                        'logType': 'Error',
                        'tag': '',
                        'text': line,
                    }
                    continue

            # If we are in an unhandled exception, just add the line to the
            # current log.
            if in_unhandled_exception:
                current_log['text'] += '\n%s' % line
                multiline = True
            else:
                # Check if current log has the same time as the previous log
                # parsed.
                new_log = LogParser.parse_raw_log(line, os_type)
                if not current_log or current_log['time'] != new_log['time']:
                    current_log = LogParser.parse_entries(new_log)
                    multiline = False
                else:
                    # If part of the same event, add the log's text to the
                    # previous parsed log.
                    current_log['text'] += '\n%s' % new_log['text']
                    multiline = True

            if not multiline:
                yield current_log

        # Yield any leftover unhandled exception logs.
        if in_unhandled_exception:
            yield current_log

    @staticmethod
    def parse_entries(log_entry):
        """ Returns the elements that the web interface shows of a log.

        Args:
            log_entry: the logEntry to return including processId and threadId

        Returns:
            dict: the message data to be sent to the web browser (no processId
                nor threadId)
        """
        return {
            'time': log_entry['time'],
            'logType': log_entry['logType'],
            'tag': log_entry['tag'],
            'text': log_entry['text'],
        }


    @staticmethod
    def parse_raw_log(log_data, os_type):
        """ Parse a raw log line.

        Args:
            log_data: the raw log line
            os_type (string): the OS type from which the logs came ("iOS" or
                "Android")

        Returns:
            dict: the log entry from the log line
        """
        log_line_regex = LogParser.parser_info[os_type]['logLineRegex']
        parsed_log = log_line_regex.match(log_data)
        group_from_log = LogParser._group_from_log

        # Parse the Time
        time_field = group_from_log(parsed_log, 'time', os_type)
        log_time = LogParser._parse_datetime(time_field, os_type)

        # Determine the log type if the OS supports it.
        log_type = None
        if 'logTypes' in LogParser.parser_info[os_type]:
            type_group = group_from_log(parsed_log, 'logType', os_type)
            log_type = LogParser.parser_info[os_type]['logTypes'][type_group]

        return {
            'time': log_time,
            'processId': group_from_log(parsed_log, 'processId', os_type),
            'threadId': group_from_log(parsed_log, 'threadId', os_type),
            'logType': log_type,
            'tag': group_from_log(parsed_log, 'tag', os_type),
            'text': group_from_log(parsed_log, 'text', os_type),
        }

    @staticmethod
    def convert_line_to_html(log_entry):
        """ Takes a parsed_line and converts it to HTML.

        Args:
            log_entry: the log entry dictionary

        Returns:
            string: formatted HTML
        """
        return '''
        <tr class="%s">
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
            <td>%s</td>
        </tr>''' % (
            log_entry['logType'].lower() if log_entry['logType'] else '',
            str(log_entry['time']),
            log_entry['tag'],
            log_entry.get('logType', ''),
            log_entry['text'],
        )
    @staticmethod
    def convert_to_html(log_entries):
        """ Takes a parsed block and converts it to HTML.

        Args:
            log entries (list): a list of log entries

        Returns:
            string: formatted HTML
        """
        return ''.join(LogParser.convert_line_to_html(line)
                       for line in log_entries)

    @staticmethod
    def _group_from_log(parsed_log, group_name, os_type):
        """ Gets a group from a parsed log.

        Args:
            parsed_log: regex results from parsing the log line
            group_name: the name of the group to get
            os_type (string): the OS type from which the logs came ("iOS" or
                "Android")

        Returns:
            string: the value of the group
        """
        group_nums = LogParser.parser_info[os_type]['groupNums']
        if group_name not in group_nums:
            return None

        return parsed_log.group(group_nums[group_name])

    @staticmethod
    def _parse_datetime(date_string, os_type):
        """ Parses a datetime string into a datetime Python object.

        Args:
            date_string: the date string to parse
            os_type (string): the OS type from which the logs came ("iOS" or
                "Android")

        Returns:
            datetime: the parsed datetime object
        """
        # On Android, we have to add the year to the string so that it parses
        # correctly.
        if os_type == 'Android':
            current_year = datetime.now().year
            date_string = '%s-%s' % (str(current_year), date_string)

        # Try to parse the datetime using all of the formats provided.
        datetime_formats = LogParser.parser_info[os_type]['datetimeFormat']
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
