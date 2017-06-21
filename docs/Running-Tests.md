# Running Tests
Make sure you follow the steps in [Development Environment
Setup](Development-Environment-Setup) before proceeding.

## Python
1. `cd` into the `server` directory.
2. Run `pytest`. You can run `pytest -vv` for more verbose output.

## Android
1. `cd` into the `mobile/android/WirelessDebugger` directory.
2. Run `./gradlew build connectedCheck`.

## JavaScript
1. `cd` to the `server` directory.
2. Run `mocha js/test`.
