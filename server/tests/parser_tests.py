# Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
"""
Tests for the Parsing Library
"""

import json
import parsing_lib

from datetime import datetime


def _test_case_parser(test_case):
    """ Parses test case JSON.

    Corrects some of the default parsing functionality to work better with the
    given test cases

    Args:
        test_case: the test case to parse

    Returns:
        the corrected, parsed test case
    """

    current_year = datetime.now().year

    # Parse test case time
    if 'time' in test_case:
        date_with_year = '%s-%s' % (str(current_year), test_case['time'])
        test_case['time'] = datetime.strptime(date_with_year,
                                              '%Y-%m-%d %H:%M:%S.%f')

    # Parse multiline input into one string
    if 'inputLines' in test_case:
        if isinstance(test_case['inputLines'], list):
            test_case['inputLines'] = '\n'.join(test_case['inputLines'])

    # Parse log entry text into one string
    if 'logEntries' in test_case:
        for log_entry in test_case['logEntries']:
            if 'text' in log_entry and isinstance(log_entry['text'], list):
                log_entry['text'] = '\n'.join(log_entry['text'])

    return test_case


def test_parse():
    """ Tests that the LogParser.parse method works properly. """

    with open('test_parse.json') as test_case_file:
        test_cases = json.load(test_case_file, object_hook=_test_case_parser)

        for test_case in test_cases:
            test_input = {
                'rawLogData': test_case['inputLines'],
            }
            expected_result = test_case['expectedResult']
            assert parsing_lib.LogParser.parse(test_input) == expected_result

        assert parsing_lib.LogParser.parse({}) == {
            'messageType': 'logData',
            'osType': 'Android',
            'logEntries': [],
        }


def test_parse_raw_log():
    """ Tests that the LogParser.parse_raw_log method works properly. """

    with open('test_parse_raw.json') as test_case_file:
        test_cases = json.load(test_case_file, object_hook=_test_case_parser)

        for test_case in test_cases:
            test = test_case['input']
            expected_result = test_case['expectedResult']
            assert parsing_lib.LogParser.parse_raw_log(test) == expected_result


def test_convert_line_to_html():
    """Tests that the LogParser.convert_line_to_html works properly"""
    current_year = datetime.now().year
    tests = [
        {
            'time': datetime(current_year, 5, 22, 11, 44, 31, 180000),
            'processId': '7080',
            'threadId': '7080',
            'logType': 'Info',
            'tag': 'WiDB Example',
            'text': 'aX: 3.0262709 aY: 2.0685902',
        },
        {
            'time': datetime(current_year, 5, 22, 11, 44, 32, 191000),
            'processId': '7080',
            'threadId': '7080',
            'logType': 'Warning',
            'tag': 'IInputConnectionWrapper',
            'text': 'getTextBeforeCursor on inactive InputConnection',
        },
    ]

    expected_results = [

        '<tr class="">' +
        '<td>' + str(datetime(current_year, 5, 22, 11, 44, 31, 180000)) + '</td>' +
        '<td>WiDB Example</td>' +
        '<td>Info</td>' +
        '<td>aX: 3.0262709 aY: 2.0685902</td>' +
        '</tr>',

        '<tr class="warning">' +
        '<td>' + str(datetime(current_year, 5, 22, 11, 44, 32, 191000)) + '</td>' +
        '<td>IInputConnectionWrapper</td>' +
        '<td>Warning</td>' +
        '<td>getTextBeforeCursor on inactive InputConnection</td>' +
        '</tr>',
    ]

    for test, expected_result in zip(tests, expected_results):
        assert parsing_lib.LogParser.convert_line_to_html(
            test) == expected_result


def test_convert_to_html():
    """Tests that LogParser.convert_to_html works properly"""
    current_year = datetime.now().year
    test = [
        {
            'time': datetime(current_year, 5, 22, 11, 44, 31, 180000),
            'logType': 'Info',
            'tag': 'WiDB Example',
            'text': 'aX: 3.0262709 aY: 2.0685902',
        },
        {
            'time': datetime(current_year, 5, 22, 11, 44, 32, 191000),
            'processId': '7080',
            'threadId': '7080',
            'logType': 'Warning',
            'tag': 'IInputConnectionWrapper',
            'text': 'getTextBeforeCursor on inactive InputConnection',
        },
    ]

    expected_result = (
        '<tr class="">' +
        '<td>' + str(datetime(current_year, 5, 22, 11, 44, 31, 180000)) + '</td>' +
        '<td>WiDB Example</td>' +
        '<td>Info</td>' +
        '<td>aX: 3.0262709 aY: 2.0685902</td>' +
        '</tr>' +
        '<tr class="warning">' +
        '<td>' + str(datetime(current_year, 5, 22, 11, 44, 32, 191000)) + '</td>' +
        '<td>IInputConnectionWrapper</td>' +
        '<td>Warning</td>' +
        '<td>getTextBeforeCursor on inactive InputConnection</td>' +
        '</tr>'
    )
    assert parsing_lib.LogParser.convert_to_html(test) == expected_result
