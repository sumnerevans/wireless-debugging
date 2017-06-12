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

    //TODO: remove, for testing purposes only
    payload = {
      "messageType": "startSession",
      "apiKey": "tikalin",
      "osType": "Android",
      "deviceName": "Google Pixel10",
      "appName": "tuff"
    };

    this.ws_.send(JSON.stringify(payload));

    let data = {
      'apiKey': payload.apiKey,
    };
    $.ajax({
      type: "GET",
      url: '/deviceList',
      data: data,
      dataType: "json",
      cache: false,
      success: function(data) {
        if (data.success) {
          $('#device').append('<option value="None"></option>');
          for (let i of data.devices) {
            $('#device').append(`<option value="${i}">${i}</option>`);
          }
        }
        else {
          $('#main-page').html('<p>No Datastore</p>');
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
  let api_key = $('#apiKey');
  let device = $('#device');
  let app = $('#app');
  let time = $('#starttime');
  device.on('change', () => {
    let chosen_device = device.val();
    if (chosen_device !== "None") {
      $('#hidden-dev-alias').css("display", "block");
      $('#hidden-app').css("display", "block");
      $('#hidden-app-alias').css("display", "none");
      $('#dev-alias').val("");
      $('#hidden-start').css("display", "none");
      let data = {
        'apiKey': api_key.html(),
        'device': chosen_device,
      };
      $.ajax({
        url: '/appList',
        data: data,
        cache: false,
        success: function(data) {
          app.empty();
          time.empty();
          $("#historical-log-table tbody tr").remove();
          app.append('<option value="None"></option>');
          for (let i of data.apps) {
            app.append(`<option value="${i}">${i}</option>`);
          }
        },
      });
    } else {
      $('#hidden-dev-alias').css("display", "none");
      $('#hidden-app').css("display", "none");
      $('#hidden-start').css("display", "none");
      $("#historical-log-table tbody tr").remove();
    }
  });
  app.on('change', () => {
    let chosen_app = app.val();
    if (chosen_app !== "None") {
      $('#hidden-app-alias').css("display", "block");
      $('#hidden-start').css("display", "block");
      $('#app-alias').val("");
      let data = {
        'apiKey': api_key.html(),
        'device': device.val(),
        'app': chosen_app,
      };
      $.ajax({
        url: '/sessionList',
        data: data,
        cache: false,
        success: function(data) {
          time.empty();
          $("#historical-log-table tbody tr").remove();
          time.append('<option value="None"></option>');
          for (let i of data.starttimes) {
            time.append(`<option value="${i}">${i}</option>`);
          }
        },
      });
    } else {
      $('#hidden-app-alias').css("display", "none");
      $('#hidden-start').css("display", "none");
      $("#historical-log-table tbody tr").remove();
    }
  });

  time.on('change', () => {
    let chosen_starttime = time.val();
    $("#historical-log-table tbody tr").remove();
    console.log(chosen_starttime);
    if (chosen_starttime !== "None") {
      let data = {
        'apiKey': api_key.html(),
        'device': device.val(),
        'app': app.val(),
        'starttime': chosen_starttime,
      };
      $.ajax({
        url: '/logs',
        data: data,
        cache: false,
        success: function(data) {
          $('#historical-log-table').append(data.logs);
        },
      });
    }
  });

  $("#device-alias").click(function(e) {
    e.preventDefault();
    let data = {
      'apiKey': api_key.html(),
      'device': device.val(),
      'alias': $('#dev-alias').val(),
    };
    $.ajax({
      url: "/aliasDevice",
      data: data,
      success: function(data) {
        if (data.dev_success) {
          window.location.reload();
        } else {
          alert("Device Alias needs to be unique");
        }
      },
    });
  });

  $("#appname-alias").click(function(e) {
    e.preventDefault();
    let data = {
      'apiKey': api_key.html(),
      'device': device.val(),
      'app': app.val(),
      'alias': $('#app-alias').val(),
    };
    $.ajax({
      url: "/aliasApp",
      data: data,
      success: function(data) {
        if (data.app_success) {
          window.location.reload();
        } else {
          alert("App Alias needs to be unique");
        }
      },
    });
  });

  $("#clear-datastore").click(function(e) {
    e.preventDefault();
    $.ajax({
      url: "/clearDatastore",
      success: window.location.reload()
    });
  });
});
