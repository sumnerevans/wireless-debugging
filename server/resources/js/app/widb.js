/*
 * @fileoverview This contains the main app logic.
 */

class Widb {
  constructor() {
    this.logTable_ = $('.log-table');
  }

  start() {
    let ws = new WebSocket('ws://localhost:8080/ws');
    ws.onopen = () => {
      let payload = {
        messageType: 'associateSession',
      };

      ws.send(JSON.stringify(payload));

      payload = {
        messageType: 'logDump',
      };

      ws.send(JSON.stringify(payload));
    };

    ws.onmessage = (message) => {
      let messageData = JSON.parse(message.data);
      if (messageData.messageType === 'logData') {
        for (let l of messageData.logEntries) {
          this.logTable_.append(this.renderLog(l));
        }
      }
    };
  }

  renderLog(logEntry) {
    return `<tr><td>${logEntry.time} ${logEntry.text}</td></tr>`;
  }
}

$(document).ready(() => {
  new Widb().start();
});
