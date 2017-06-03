/**
 * Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
 *
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
    this.guid_ = $('.guid');

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

    this.ws_.send(JSON.stringify(payload));
    //TO DO: remove, for testing purposes only
    payload = {
        "messageType": "startSession",
        "apiKey": "tikalin",
        "osType": "Android",
        "deviceName": "Google Pixel7",
        "appName": "Google Stuff9"
    }

    this.ws_.send(JSON.stringify(payload));

    let data = {
      'apiKey': payload.apiKey,
    };
    $.ajax({
      type: "POST",
      url: '/deviceList',
      data: JSON.stringify(data, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      cache: false,
      success: function(data){
        var device = document.getElementById('device');
        $(device).append('<option value="None"></option>');
        for (var i in data.devices){
          $(device).append('<option value=\"' + data.devices[i] + '\">' + data.devices[i] + '</option>');
        }
      }
    });

    // TODO: get rid of this, only for testing purposes
    payload = {
      messageType: 'logDump',
      rawLogData: "--------- beginning of /dev/log/system \n05-22 11:44:31.180 7080 7080 I WiDB Example: aX: 3.0262709 aY: 2.0685902 \n05-22 11:44:32.191 7080 7080 W IInputConnectionWrapper: getTextBeforeCursor on inactive InputConnection",
    };

    this.ws_.send(JSON.stringify(payload));

        // TODO: get rid of this, only for testing purposes
    payload = {
      messageType: 'endSession',
    };

    this.ws_.send(JSON.stringify(payload));

  }

  /** Decodes the WebSocket message and adds to table */
  websocketOnMessage(message) {
    let messageData = JSON.parse(message.data);
    if (messageData.messageType === 'logData') {
      this.logTable_.append(messageData.logEntries);
    }
    if (messageData.messageType === 'guid') {
      this.guid_.append(messageData.user);
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
  let A = document.getElementById('device');
  $(A).change(function () {
      let device = document.getElementById('device');
      let data = {
	      'apiKey': document.getElementById('apiKey').innerHTML,
	      'device': device.options[device.selectedIndex].text
      };
      $.ajax({
      type: "POST",
      url: '/appList',
      data: JSON.stringify(data, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      cache: false,
      success: function(data){
        let app = document.getElementById('app');
	let time = document.getElementById('starttime');
	app.length = 0;
	      time.length = 0;
	      $("#historical-log-table tbody tr").remove();
	      $(app).append('<option value="None"></option>');
        for (var i in data.apps){
          $(app).append('<option value=' + data.apps[i] + '>' + data.apps[i] + '</option>');
        }

      },
    });
  });
  let B = document.getElementById('app');
  $(B).change (function () {
      let device = document.getElementById('device');
      let app = document.getElementById('app');
      let data = {
	      'apiKey': document.getElementById('apiKey').innerHTML,
	      'device': device.options[device.selectedIndex].text,
      	      'app': app.options[app.selectedIndex].text,
      };
      $.ajax({
      type: "POST",
      url: '/sessionList',
      data: JSON.stringify(data, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      cache: false,
      success: function(data){
        let time = document.getElementById('starttime');
	time.length = 0;
	$("#historical-log-table tbody tr").remove();
	$(time).append('<option value="None"></option>');
        for (var i in data.starttimes){
          $(time).append('<option value=' + data.starttimes[i] + '>' + data.starttimes[i] + '</option>');
        }
      },
    });
  });

  let C = document.getElementById('starttime');
  $(C).change (function () {
      let device = document.getElementById('device');
      let app = document.getElementById('app');
      let time = document.getElementById('starttime');
      let data = {
	      'apiKey': document.getElementById('apiKey').innerHTML,
	      'device': device.options[device.selectedIndex].text,
      	      'app': app.options[app.selectedIndex].text,
	      'starttime': time.options[time.selectedIndex].text,
      };
      $.ajax({
      type: "POST",
      url: '/logs',
      data: JSON.stringify(data, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      cache: false,
      success: function(data){
	$("#historical-log-table tbody tr").remove();
        let table = document.getElementById('historical-log-table');
	$(table).append(data.logs);
      },
    });
  });

  $("#device-alias").click(function(e) {
    e.preventDefault();
    let data = {
	'apiKey': document.getElementById('apiKey').innerHTML,
	'device': device.options[device.selectedIndex].text,
	'alias' : document.getElementById('dev-alias').value,
    };
    $.ajax({
      type: "POST",
      url: "/aliasDevice",
      data: JSON.stringify(data, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      success: function(data) {
	window.location.reload();
      },
    });
  });

  $("#appname-alias").click(function(e) {
    e.preventDefault();
    let data = {
	'apiKey': document.getElementById('apiKey').innerHTML,
	'device': device.options[device.selectedIndex].text,
	'app'   : app.options[device.selectedIndex].text,
	'alias' : document.getElementById('app-alias').value,
    };
    $.ajax({
      type: "POST",
      url: "/aliasApp",
      data: JSON.stringify(data, null, '\t'),
      contentType: 'application/json;charset=UTF-8',
      success: function(data) {
	window.location.reload();
      },
    });
  });
});
