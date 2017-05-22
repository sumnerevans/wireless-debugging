/*
 * @fileoverview This contains the main app logic
 */

/**
 * Creates a table from log data received through websockets
 * @class
 */
class Widb {
  /** Initialize the app */
  constructor() {
    /** @private @const {!jQuery} */
    this.logTable_ = $('.log-table');
    this.ws_ = null;
  }

  /**
   * Opens a websockets connection to the server
   */
  start() {
    this.ws_ = new WebSocket('ws://localhost:8080/ws');
    this.ws_.onopen = () => this.websocketOnOpen();
    this.ws_.onmessage = (message) => this.websocketOnMessage(message);
  }

  /** Handles websocket opening */
  websocketOnOpen() {
    let payload = {
      messageType: 'associateSession',
    };

    this.ws_.send(JSON.stringify(payload));

    // TODO: get rid of this function, only for testing purposes
    payload = {
      messageType: 'logDump',
    };

    this.ws_.send(JSON.stringify(payload));
  }

  /** Decodes the websocket message and adds to table */
  websocketOnMessage(message) {
    let messageData = JSON.parse(message.data);
    if (messageData.messageType === 'logData') {
      for (let l of messageData.logEntries) {
        this.logTable_.append(this.renderLog(l));
      }
    }
  }

  /** Formats new table entries from log data */
  renderLog(logEntry) {
    let type = logEntry.logType;
    let color = '';

    switch (type) {
      case 'Warning':
        color = 'warning';
        break;
      case 'Error':
        color = 'danger';
        break;
    }

    return `<tr class="${color}">
    <td>${logEntry.time}</td>
    <td>${logEntry.tag}</td>
    <td>${logEntry.logType}</td>
    <td>${logEntry.text}</td>
    </tr>`;
  }
}

/** When the document has been loaded, start Widb */
$(document).ready(() => {
  new Widb().start();
});
