/**
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 * @fileoverview This contains the main app logic
 */

/**
 * Creates a table from log data received through WebSockets
 * @class
 */
class WirelessDebug {
  /** Initialize the app */
  constructor() {
    /** @private @const {!jQuery} */
    this.logTable_ = $('.log-table');


    /** @private @const {?WebSocket} */
    this.ws_ = null;
  }

  /**
   * Opens a WebSocket connection to the server
   */
  start() {
    this.ws_ = new WebSocket(`ws://${location.host}/ws`);
    this.ws_.onopen = () => this.websocketOnOpen();
    this.ws_.onmessage = (message) => this.websocketOnMessage(message);
  }

  /** Handles WebSocket opening */
  websocketOnOpen() {
    let payload = {
      messageType: 'associateUser',
      apiKey: 'tikalin',
    };

    this.ws_.send(JSON.stringify(payload));

    payload = {
      messageType: 'logDump',
      rawLogData: "--------- beginning of /dev/log/system \n05-22 11:44:31.180 7080 7080 I WiDB Example: aX: 3.0262709 aY: 2.0685902 \n05-22 11:44:32.191 7080 7080 W IInputConnectionWrapper: getTextBeforeCursor on inactive InputConnection",
    };

    this.ws_.send(JSON.stringify(payload));
  }

  /** Decodes the WebSocket message and adds to table */
  websocketOnMessage(message) {
    let messageData = JSON.parse(message.data);
    if (messageData.messageType === 'logData') {
      for (let entry of messageData.logEntries) {
        this.logTable_.append(this.renderLog(entry));
      }
      $('#log-table').DataTable();
    }
  }

  /** Formats new table entries from log data */
  renderLog(logEntry) {
    let color = {
      'Warning': 'warning',
      'Error': 'danger',
    };

    return `<tr class="${color[logEntry.logType]}">
    <td>${logEntry.time}</td>
    <td>${logEntry.tag}</td>
    <td>${logEntry.logType}</td>
    <td>${logEntry.text}</td>
    </tr>`;
  }
}

/** When the document has been loaded, start Widb */
$(document).ready(() => {
  new WirelessDebug().start();
});
