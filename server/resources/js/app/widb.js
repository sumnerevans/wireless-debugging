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

    this.dataTable = $('#log-table').DataTable();
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
    // Extract the api key from the cookies on the web page.
    let cookieStrings = document.cookie.replace(/['"]+/g, '').split(';');
    let apiKey = '';
    for(let i = 0; i < cookieStrings.length; i++) {
      let [cookieKey, cookieVal] = cookieStrings[i].trim().split('=');
      if (cookieKey == 'api_key') {
        apiKey = cookieVal;
        break;
      }
    }

    let payload = {
      messageType: 'associateUser',
      apiKey: apiKey || '',
    };

    this.data_table = $('#log-table').DataTable();
    this.ws_.send(JSON.stringify(payload));
  }

  /** Decodes the WebSocket message and adds to table */
  websocketOnMessage(message) {
    let messageData = JSON.parse(message.data);
    if (messageData.messageType === 'logData') {
      //if(this.data_table) {
        this.data_table.destroy();
      //}
      for (let entry of messageData.logEntries) {
        this.logTable_.append(this.renderLog(entry));
      }
      this.data_table = $('#log-table').DataTable();
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
