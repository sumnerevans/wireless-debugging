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

    /** @private @const {!jQuery} */
    this.metricsTable_ = $('.metrics-table');

    /** @private @const {?WebSocket} */
    this.ws_ = null;

    this.metricGrapher = new MetricGrapher();
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
      apiKey: 'api_key',
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
    }
    if (messageData.messageType === 'deviceMetrics') {
      //this.metricsTable_.append(this.renderMetrics(messageData))
      metricGrapher.setMetrics(messageData);
      metricGrapher.render();
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

  renderMetrics(metrics) {
    return `<tr>
    <td>${metrics.cpuUsage}</td>
    <td>${metrics.timeStamp}</td>
    <td>${metrics.memUsage}</td>
    </tr>`;
  }
}

/** When the document has been loaded, start Widb */
$(document).ready(() => {
  new WirelessDebug().start();
});
