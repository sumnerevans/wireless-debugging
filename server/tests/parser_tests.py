"""
Tests for the Parsing Library
"""

import json
from datetime import datetime
import parsing_lib


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
    if isinstance(test_case.get('inputLines', None), list):
        test_case['inputLines'] = '\n'.join(test_case['inputLines'])

    # Parse log entry text into one string
    if isinstance(test_case.get('expectedResult', None), list):
        for log_entry in test_case['expectedResult']:
            if 'text' in log_entry and isinstance(log_entry['text'], list):
                log_entry['text'] = '\n'.join(log_entry['text'])

    return test_case


def test_parse_android():
    """ Tests that the LogParser.parse method works properly for Android. """

    with open('tests/inputs/test_parse_android.json') as test_case_file:
        test_cases = json.load(test_case_file, object_hook=_test_case_parser)

        for test_case in test_cases:
            test_input = test_case['inputLines']
            expected_result = test_case['expectedResult']
            assert list(parsing_lib.LogParser.parse(test_input, 'Android')) == \
                    expected_result

        assert list(parsing_lib.LogParser.parse({}, 'Android')) == []


def test_parse_ios():
    """ Tests that the LogParser.parse method works properly for iOS. """
    with open('tests/inputs/test_parse_ios.json') as test_case_file:
        test_cases = json.load(test_case_file, object_hook=_test_case_parser)

        for test_case in test_cases:
            test_input = test_case['inputLines']
            expected_result = test_case['expectedResult']
            assert list(parsing_lib.LogParser.parse(test_input, 'iOS')) == \
                    expected_result

        assert list(parsing_lib.LogParser.parse({}, 'iOS')) == []


def test_parse_raw_log_android():
    """ Tests that the LogParser.parse_raw_log method works properly for
        Android.
    """

    with open('tests/inputs/test_parse_android_raw.json') as test_case_file:
        test_cases = json.load(test_case_file, object_hook=_test_case_parser)

        for test_case in test_cases:
            test = test_case['input']
            expected_result = test_case['expectedResult']
            result = parsing_lib.LogParser.parse_raw_log(test, 'Android')
            assert result == expected_result


def test_parse_raw_log_ios():
    """ Tests that the LogParser.parse_raw_log method works properly for
        iOS.
    """
    with open('tests/inputs/test_parse_ios_raw.json') as test_case_file:
        test_cases = json.load(test_case_file, object_hook=_test_case_parser)

        for test_case in test_cases:
            test = test_case['input']
            expected_result = test_case['expectedResult']
            result = parsing_lib.LogParser.parse_raw_log(test, 'iOS')
            assert result == expected_result


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

    expected_results = [[
        '<tr class="">',
        '    <td>%s</td>' % datetime(current_year, 5, 22, 11, 44, 31, 180000),
        '    <td>WiDB Example</td>',
        '    <td>Info</td>',
        '    <td>aX: 3.0262709 aY: 2.0685902</td>',
        '</tr>',
    ], [
        '<tr class="warning">',
        '    <td>%s</td>' % datetime(current_year, 5, 22, 11, 44, 32, 191000),
        '    <td>IInputConnectionWrapper</td>',
        '    <td>Warning</td>',
        '    <td>getTextBeforeCursor on inactive InputConnection</td>',
        '</tr>',
    ]]

    for test, expected_result in zip(tests, expected_results):
        html = parsing_lib.LogParser.convert_line_to_html(test)
        html = html.replace(' ', '').replace('\n', '')
        expected_result = ''.join(expected_result)
        expected_result = expected_result.replace(' ', '').replace('\n', '')
        assert html == expected_result


def test_convert_to_html():
    """Tests that LogParser.convert_to_html works properly"""
    current_year = datetime.now().year
    tests = [[{
        'time': datetime(current_year, 5, 22, 11, 44, 31, 180000),
        'logType': 'Info',
        'tag': 'WiDB Example',
        'text': 'aX: 3.0262709 aY: 2.0685902',
    }, {
        'time': datetime(current_year, 5, 22, 11, 44, 32, 191000),
        'processId': '7080',
        'threadId': '7080',
        'logType': 'Warning',
        'tag': 'IInputConnectionWrapper',
        'text': 'getTextBeforeCursor on inactive InputConnection',
    }, {
        'time': datetime(current_year, 5, 24, 12, 12, 49, 247000),
        'logType': 'Error',
        'tag': 'AndroidRuntime',
        'text': ''.join([
            'FATAL EXCEPTION: main',
            'Process: com.google.wireless.debugging, PID: 23930',
            'java.lang.RuntimeException: Forced Crash',
            'at com.google.wireless.debugging.example.MainFragment$2.onClick(MainFragment.java:73)',
            'at android.view.View.performClick(View.java:4445)',
            'at android.view.View$PerformClick.run(View.java:18446)',
            'at android.os.Handler.handleCallback(Handler.java:733)',
            'at android.os.Handler.dispatchMessage(Handler.java:95)',
            'at android.os.Looper.loop(Looper.java:136)',
            'at android.app.ActivityThread.main(ActivityThread.java:5146)',
            'at java.lang.reflect.Method.invokeNative(Native Method)',
            'at java.lang.reflect.Method.invoke(Method.java:515)',
            'at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:796)',
            'at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:612)',
            'at dalvik.system.NativeStart.main(Native Method)'
        ]),
    }]]

    expected_results = [[
        '<tr class="">',
        '    <td>%s</td>' % datetime(current_year, 5, 22, 11, 44, 31, 180000),
        '    <td>WiDB Example</td>',
        '    <td>Info</td>',
        '    <td>aX: 3.0262709 aY: 2.0685902</td>',
        '</tr>',
        '<tr class="warning">',
        '    <td>%s</td>' % datetime(current_year, 5, 22, 11, 44, 32, 191000),
        '    <td>IInputConnectionWrapper</td>',
        '    <td>Warning</td>',
        '    <td>getTextBeforeCursor on inactive InputConnection</td>',
        '</tr>',
        '<tr class="danger">',
        '    <td>%s</td>' % datetime(current_year, 5, 24, 12, 12, 49, 247000),
        '    <td>AndroidRuntime</td>',
        '    <td>Error</td>',
        '    <td>FATAL EXCEPTION: main',
        '        Process: com.google.wireless.debugging, PID: 23930',
        '        java.lang.RuntimeException: Forced Crash',
        '        at com.google.wireless.debugging.example.MainFragment$2.onClick(MainFragment.java:73)',
        '        at android.view.View.performClick(View.java:4445)',
        '        at android.view.View$PerformClick.run(View.java:18446)',
        '        at android.os.Handler.handleCallback(Handler.java:733)',
        '        at android.os.Handler.dispatchMessage(Handler.java:95)',
        '        at android.os.Looper.loop(Looper.java:136)',
        '        at android.app.ActivityThread.main(ActivityThread.java:5146)',
        '        at java.lang.reflect.Method.invokeNative(Native Method)',
        '        at java.lang.reflect.Method.invoke(Method.java:515)',
        '        at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:796)',
        '        at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:612)',
        '        at dalvik.system.NativeStart.main(Native Method)',
        '    </td>',
        '</tr>',
    ]]

    for test, expected_result in zip(tests, expected_results):
        html = parsing_lib.LogParser.convert_to_html(test)
        html = html.replace(' ', '').replace('\n', '')
        expected_result = ''.join(expected_result)
        expected_result = expected_result.replace(' ', '').replace('\n', '')
        assert html == expected_result
