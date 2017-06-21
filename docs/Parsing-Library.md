# Parsing Library
The parsing library is a Python library which provides functions to parse raw
logs into log entries (as Python `dict`s) and to convert those log entries to
HTML.

The Parsing Library exposes a single class: `LogParser`. This class has two
public static functions:

**`parse (raw_log_data)`**
- **Arguments:**
    - `raw_log_data (string)`: the raw log data from the Mobile API.

- **Returns:**
    - `dict`: A Python list of Log Entry dictionaries, each of which have the
      following fields:
        - `time (datetime)`: the time the log occurred
        - `text (string)`: the text of the log
        - `tag (string)`: The tag on the log. For Android, this allows the user
          to specify an additional annotation to add to their log entry for
          organizational purposes.
        - `logType (string)`: The type of log (Warning, Error, Info, etc.)

**`convert_line_to_html(parsed_line)`**
- **Arguments:**
    - `parsed_line (string)`: Parsed line of a log
- **Returns:**
    - `string`: A string containing an HTML table row which represent the log
      entry.

**`convert_to_html(parsed_log_dict)`**
- **Arguments:**
    - `parsed_log_dict (dict)`: A python list of Log Entry dictionaries, each of
      which have the following fields:
        - `time (datetime)`: the time the log occurred
        - `text (string)`: the text of the log
        - `tag (string)`: The tag on the log. For Android, this allows the user
          to specify an additional annotation to add to their log entry for
          organizational purposes.
        - `logType (string)`: The type of log (Warning, Error, Info, etc.)
- **Returns:**
    - `string`: A string containing the HTML table rows (not the entire table)
      which represent the log entries.
