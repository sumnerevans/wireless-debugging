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
            'logLineRegex': 
                '(.*)\\s+(\\d*)\\s+(\\d*) ([IWVEDAF]) (.*?): ((?:.*\\n*)*)',
            'datetimeFormat': '%Y-%m-%d %H:%M:%S.%f',
            'filterLineRegex': '-* beginning of',
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
            'logLineRegex': '(.*) (.*)\\[(\\d+):(\\d+)\\] (.*)',
            'datetimeFormat': '%Y-%m-%d %H:%M:%S.%f',
            'groupNums': {
                'time': 1,
                'tag': 2,
                'processId': 3,
                'threadId': 4,
                'text': 5,
            }
        }
    }


    @staticmethod
    def parse(raw_log_lines, os_type):
        """ Parses a log message from the Mobile API.

        Args:
            raw_log_lines (string): the raw log lines
            os_type (string): the OS type from which the logs came ("iOS" or
                "Android")

        Returns:
            list: a list of log entry dictionaries
        """
        # If there are no log lines, don't do anything.
        if not raw_log_lines or raw_log_lines.isspace():
            return []

        filter_regex = LogParser.parser_info[os_type].get('filterLineRegex', None)
        raw_data = raw_log_lines.splitlines()
        log_entries = []

        # Filter out any lines that are not log lines.
        while filter_regex and re.search(filter_regex, raw_data[0]) is not None:
            raw_data = raw_data[1:]

        # Parse the first log line to have context for futher log lines if an
        # event was split across multiple lines.
        old_log = LogParser.parse_raw_log(raw_data[0], os_type)
        log_entries.append(LogParser.parse_entries(old_log))
        current_log = None

        # Since we've already parsed the first line, start at index 1.
        for line in raw_data[1:]:
            # Skip lines that are not log lines. There may be cases when these
            # appear in a log line that is not at the beginning of the raw
            # data.
            if filter_regex and re.search(filter_regex, line) is not None:
                continue

            # Check if current log is like the previous log parsed
            current_log = LogParser.parse_raw_log(line, os_type)
            if current_log['time'] != old_log['time']:
                log_entries.append(LogParser.parse_entries(current_log))
            else:
                # If part of the same event, add the log's text to the previous
                # parsed log
                log_entries[-1]['text'] += ('\n%s' % current_log['text'])
            old_log = current_log

        return log_entries


    @staticmethod
    def parse_entries(log_entry):
        """ Returns the elements that the web interface shows of a log.

        Args:
            log_entry: the logEntry to return including processId and threadId
            os_type (string): the OS type from which the logs came ("iOS" or
                "Android")

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

        Returns:
            dict: the log entry from the log line
        """
        log_line_regex = LogParser.parser_info[os_type]['logLineRegex']
        parsed_log = re.search(log_line_regex, log_data)
        group_from_log = LogParser._group_from_log

        # Parse the Time
        time_field = group_from_log(parsed_log, 'time', os_type)

        # On Android, we have to add the year to the string so that it parses
        # correctly.
        if os_type == 'Android':
            current_year = datetime.now().year
            time_field = '%s-%s' % (str(current_year), time_field)

        datetime_format = LogParser.parser_info[os_type]['datetimeFormat']
        log_time = datetime.strptime(time_field, datetime_format)

        # Determine the log type if the OS supports that.
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
            log_entry: the log entry

        Returns:
            string: formatted HTML
        """
        return '''
        <tr class=\"%s\">
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

        Returns:
            string: the value of the group
        """
        group_nums = LogParser.parser_info[os_type]['groupNums']
        if group_name not in group_nums:
            return None

        return parsed_log.group(group_nums[group_name])
