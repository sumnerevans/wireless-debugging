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

      // TEMP
      payload = {
        messageType: 'logDump',
      };

      ws.send(JSON.stringify(payload));
    };

    ws.onmessage = (message) => {
      let messageData = JSON.parse(message.data);
      if (messageData.messageType === 'logData') {
        for (let l of messageData.logEntries) {
          console.log(l);
          this.logTable_.append(this.renderLog(l));
        }
      }
    };
  }

  renderLog(logEntry) {
    let type = logEntry.logType;
    let color = "";
    if (type === `Warning`) {
      color = "warning";
    }
    return `<tr class="${color}"> 
          <td>${logEntry.time}</td>
          <td>${logEntry.tag}</td>
          <td>${logEntry.logType}</td>
          <td>${logEntry.text}</td>
          </tr>`;
  }
}

// When the document has been loaded, start Widb.
$(document).ready(() => {
  new Widb().start();
});
