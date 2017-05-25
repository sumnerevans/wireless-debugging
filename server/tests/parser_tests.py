"""
Tests for the Parsing Library
"""

from datetime import datetime
import parsing_lib


def test_parse():
    current_year = datetime.now().year
    tests = [
        {
            'rawLogData': '''--------- beginning of /dev/log/system
        05-22 11:44:31.180 7080 7080 I WiDB Example: aX: 3.0262709 aY: 2.0685902
        05-22 11:44:32.191 7080 7080 W IInputConnectionWrapper: getTextBeforeCursor on inactive InputConnection'''
        },
        {
            'rawLogData':'''05-24 12:12:49.247 23930 23930 E AndroidRuntime: FATAL EXCEPTION: main
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: Process: com.google.wireless.debugging, PID: 23930
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: java.lang.RuntimeException: Forced Crash
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at com.google.wireless.debugging.example.MainFragment$2.onClick(MainFragment.java:73)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.view.View.performClick(View.java:4445)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.view.View$PerformClick.run(View.java:18446)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.os.Handler.handleCallback(Handler.java:733)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.os.Handler.dispatchMessage(Handler.java:95)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.os.Looper.loop(Looper.java:136)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.app.ActivityThread.main(ActivityThread.java:5146)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at java.lang.reflect.Method.invokeNative(Native Method)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at java.lang.reflect.Method.invoke(Method.java:515)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:796)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:612)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at dalvik.system.NativeStart.main(Native Method)'''
        },
        {
            'rawLogData': '''--------- beginning of /dev/log/system
        05-22 11:44:31.180 7080 7080 I WiDB Example: aX: 3.0262709 aY: 2.0685902
        05-22 11:44:32.191 7080 7080 W IInputConnectionWrapper: getTextBeforeCursor on inactive InputConnection
        --------- beginning of /dev/log/system
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: FATAL EXCEPTION: main
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: Process: com.google.wireless.debugging, PID: 23930
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: java.lang.RuntimeException: Forced Crash
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at com.google.wireless.debugging.example.MainFragment$2.onClick(MainFragment.java:73)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.view.View.performClick(View.java:4445)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.view.View$PerformClick.run(View.java:18446)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.os.Handler.handleCallback(Handler.java:733)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.os.Handler.dispatchMessage(Handler.java:95)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.os.Looper.loop(Looper.java:136)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at android.app.ActivityThread.main(ActivityThread.java:5146)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at java.lang.reflect.Method.invokeNative(Native Method)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at java.lang.reflect.Method.invoke(Method.java:515)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:796)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:612)
        05-24 12:12:49.247 23930 23930 E AndroidRuntime: 	at dalvik.system.NativeStart.main(Native Method)'''
        },
	
    ]
    expected_results = [
        {
            'messageType': 'logData',
            'osType': 'Android',
            'logEntries': [
                {
                    'time': datetime(current_year, 5, 22, 11, 44, 31, 180000),
                    'logType': 'Info',
                    'tag': 'WiDB Example',
                    'text': 'aX: 3.0262709 aY: 2.0685902',
                },
                {
                    'time': datetime(current_year, 5, 22, 11, 44, 32, 191000),
                    'logType': 'Warning',
                    'tag': 'IInputConnectionWrapper',
                    'text': 'getTextBeforeCursor on inactive InputConnection',
                },
            ],
        },
        {
            'messageType': 'logData',
            'osType': 'Android',
            'logEntries': [
                {
                    'time': datetime(current_year, 5, 24, 12, 12, 49, 247000),
                    'logType': 'Error',
                    'tag': 'AndroidRuntime',
                    'text':
                    '''FATAL EXCEPTION: main
 Process: com.google.wireless.debugging, PID: 23930
 java.lang.RuntimeException: Forced Crash
 	at com.google.wireless.debugging.example.MainFragment$2.onClick(MainFragment.java:73)
 	at android.view.View.performClick(View.java:4445)
 	at android.view.View$PerformClick.run(View.java:18446)
 	at android.os.Handler.handleCallback(Handler.java:733)
 	at android.os.Handler.dispatchMessage(Handler.java:95)
 	at android.os.Looper.loop(Looper.java:136)
 	at android.app.ActivityThread.main(ActivityThread.java:5146)
 	at java.lang.reflect.Method.invokeNative(Native Method)
 	at java.lang.reflect.Method.invoke(Method.java:515)
 	at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:796)
 	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:612)
 	at dalvik.system.NativeStart.main(Native Method)'''
                },
            ],
        },
        {
            'messageType': 'logData',
            'osType': 'Android',
            'logEntries': [
                {
                    'time': datetime(current_year, 5, 22, 11, 44, 31, 180000),
                    'logType': 'Info',
                    'tag': 'WiDB Example',
                    'text': 'aX: 3.0262709 aY: 2.0685902',
                },
                {
                    'time': datetime(current_year, 5, 22, 11, 44, 32, 191000),
                    'logType': 'Warning',
                    'tag': 'IInputConnectionWrapper',
                    'text': 'getTextBeforeCursor on inactive InputConnection',
                },
                {
                    'time': datetime(current_year, 5, 24, 12, 12, 49, 247000),
                    'logType': 'Error',
                    'tag': 'AndroidRuntime',
                    'text':
                    '''FATAL EXCEPTION: main
 Process: com.google.wireless.debugging, PID: 23930
 java.lang.RuntimeException: Forced Crash
 	at com.google.wireless.debugging.example.MainFragment$2.onClick(MainFragment.java:73)
 	at android.view.View.performClick(View.java:4445)
 	at android.view.View$PerformClick.run(View.java:18446)
 	at android.os.Handler.handleCallback(Handler.java:733)
 	at android.os.Handler.dispatchMessage(Handler.java:95)
 	at android.os.Looper.loop(Looper.java:136)
 	at android.app.ActivityThread.main(ActivityThread.java:5146)
 	at java.lang.reflect.Method.invokeNative(Native Method)
 	at java.lang.reflect.Method.invoke(Method.java:515)
 	at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:796)
 	at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:612)
 	at dalvik.system.NativeStart.main(Native Method)'''
                },
                
            ],
        },
    ]

    for test, expected_result in zip(tests, expected_results):
        assert parsing_lib.LogParser.parse(test) == expected_result


def test_parse_raw_log():
    current_year = datetime.now().year
    tests = {
        '05-22 11:44:31.180 7080 7080 I WiDB Example: aX: 3.0262709 aY: 2.0685902':
        {
            'time': datetime(current_year, 5, 22, 11, 44, 31, 180000),
            'processId': '7080',
            'threadId': '7080',
            'logType': 'Info',
            'tag': 'WiDB Example',
            'text': 'aX: 3.0262709 aY: 2.0685902',
        },
        '05-22 11:44:32.191 7080 7080 W IInputConnectionWrapper: getTextBeforeCursor on inactive InputConnection':
        {
            'time': datetime(current_year, 5, 22, 11, 44, 32, 191000),
            'processId': '7080',
            'threadId': '7080',
            'logType': 'Warning',
            'tag': 'IInputConnectionWrapper',
            'text': 'getTextBeforeCursor on inactive InputConnection',
        },
    }

    for test, expected_result in tests.items():
        assert parsing_lib.LogParser.parse_raw_log(test) == expected_result
