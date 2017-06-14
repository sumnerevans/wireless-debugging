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
    this.apiKey_ = $('.api-key');

    /** @private @const {!jQuery} */
    this.metricsTable_ = $('.metrics-table');

    /** @private @const {!jQuery} */
    this.logTablePaste_ = $('.log-table-paste');

    /** @private @const {?WebSocket} */
    this.ws_ = null;

    /** @private @const {!MetricGrapher} */
    this.metricGrapher = new MetricGrapher("cpu-usage-graph", "mem-usage-graph", "net-usage-graph");
    this.metricGrapher.render();

    /** @private @const {!DataTable} */
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
      if (cookieKey === 'api_key') {
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

    // Get all the devices for historical sessions.
    let data = {
      'apiKey': payload.apiKey,
    };
    $.ajax({
      url: '/deviceList',
      data: data,
      dataType: 'json',
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
  }

  /** Decodes the WebSocket message and adds to table */
  websocketOnMessage(message) {
    let messageData = JSON.parse(message.data);

    if (messageData.messageType === 'logData') {
      this.data_table.destroy();
      for (let entry of messageData.logEntries) {
        this.logTable_.append(this.renderLog(entry));
      }
      this.data_table = $('#log-table').DataTable();
    }
    if (messageData.messageType === 'apiKey') {
      this.apiKey_.append(messageData.user);
    }

    if (messageData.messageType === 'deviceMetrics') {
      this.metricGrapher.setMetrics(messageData);
      this.metricGrapher.render();
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
  let api_key = $('#api-key');
  let device = $('#device');
  let app = $('#app');
  let time = $('#start-time');
  device.on('change', () => {
    let chosen_device = device.val();
    // Gets rid of old data but keeps table structure.
    let data_table = $('#historical-log-table').DataTable();
    data_table.destroy();
    if (chosen_device !== 'None') {
      $('#hidden-dev-alias').css('display', 'block');
      $('#hidden-app').css('display', 'block');
      $('#hidden-app-alias').css('display', 'none');
      $('#dev-alias').val('');
      $('#hidden-start').css('display', 'none');
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
          $('#historical-log-table tbody tr').remove();
          app.append('<option value="None"></option>');
          for (let i of data.apps) {
            app.append(`<option value="${i}">${i}</option>`);
          }
        },
      });
    } else {
      $('#hidden-dev-alias').css('display', 'none');
      $('#hidden-app').css('display', 'none');
      $('#hidden-start').css('display', 'none');
      $('#historical-log-table tbody tr').remove();
    }
  });
  app.on('change', () => {
    let chosen_app = app.val();
    // Gets rid of old data but keeps table structure.
    data_table = $('#historical-log-table').DataTable();
    data_table.destroy();
    if (chosen_app !== 'None') {
      $('#hidden-app-alias').css('display', 'block');
      $('#hidden-start').css('display', 'block');
      $('#app-alias').val('');
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
          $('#historical-log-table tbody tr').remove();
          time.append('<option value="None"></option>');
          for (let i of data.starttimes) {
            time.append(`<option value="${i}">${i}</option>`);
          }
        },
      });
    } else {
      $('#hidden-app-alias').css('display', 'none');
      $('#hidden-start').css('display', 'none');
      $('#historical-log-table tbody tr').remove();
    }
  });

  time.on('change', () => {
    let chosen_starttime = time.val();
    // Gets rid of old data but keeps table structure.
    data_table = $('#historical-log-table').DataTable();
    data_table.destroy();
    $('#historical-log-table tbody tr').remove();
    if (chosen_starttime !== 'None') {
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
          data_table = $('#historical-log-table').DataTable();
        },
      });
    }
  });

  $('#device-alias').click(function(e) {
    e.preventDefault();
    let data = {
      'apiKey': api_key.html(),
      'device': device.val(),
      'alias': $('#dev-alias').val(),
    };
    $.ajax({
      url: '/aliasDevice',
      data: data,
      success: function(data) {
        if (data.dev_success) {
          window.location.reload();
        } else {
          alert('Device Alias needs to be unique');
        }
      },
    });
  });

  $('#appname-alias').click(function(e) {
    e.preventDefault();
    let data = {
      'apiKey': api_key.html(),
      'device': device.val(),
      'app': app.val(),
      'alias': $('#app-alias').val(),
    };
    $.ajax({
      url: '/aliasApp',
      data: data,
      success: function(data) {
        if (data.app_success) {
          window.location.reload();
        } else {
          alert('App Alias needs to be unique');
        }
      },
    });
  });

  $('#clear-datastore').click(function(e) {
    e.preventDefault();
    $.ajax({
      url: '/clearDatastore',
      success: window.location.reload()
    });
  });
});
