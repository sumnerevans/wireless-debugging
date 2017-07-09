/*
 * @fileoverview This is the entrypoint for the application part of Wireless
 * Debug.
 */

define([
  'jquery',
  'app/device-metric-graphs',
  'app/util',
  'datatables',
], ($, MetricGrapher, Util) => class WirelessDebug {
  /** Initialize the app */
  constructor() {
    /** @private @const {!jQuery} */
    this.logTable_ = $('.log-table');

    /** @private @const {!jQuery} */
    this.metricsTable_ = $('.metrics-table');

    /** @private @const {?WebSocket} */
    this.ws_ = null;

    /** @private @const {?MetricGrapher} */
    this.metricGrapher = null;

    /** @private @const {!Object} */
    this.tableConfig_ = {
      paging: false,
      lengthMenu: [-1],
      scrollY: '75vh',
      scrollCollapse: true,
    };

    /** @private @const {?DataTable} */
    this.dataTable_ = $('#log-table').DataTable(this.tableConfig_); // eslint-disable-line new-cap
  }

  /**
   * Opens a WebSocket connection to the server
   */
  start() {
    this.ws_ = new WebSocket(`ws://${location.host}/ws`);
    this.ws_.onopen = () => this.websocketOnOpen();
    this.ws_.onmessage = message => this.websocketOnMessage(message);

    const apiKey = $('#api-key');
    const device = $('#device');
    const app = $('#app');
    const time = $('#start-time');
    let dataTable = $('#historical-log-table');

    device.on('change', () => {
      const chosenDevice = device.val();
      // Gets rid of old data but keeps table structure.
      dataTable = $('#historical-log-table').DataTable(); // eslint-disable-line new-cap
      dataTable.destroy();
      if (chosenDevice !== 'None') {
        $('#hidden-dev-alias').css('display', 'block');
        $('#hidden-app').css('display', 'block');
        $('#hidden-app-alias').css('display', 'none');
        $('#dev-alias').val('');
        $('#hidden-start').css('display', 'none');
        $.ajax({
          url: '/appList',
          data: {
            apiKey: apiKey.html(),
            device: chosenDevice,
          },
          cache: false,
          success: function(data) {
            app.empty();
            time.empty();
            $('#historical-log-table tbody tr').remove();
            app.append('<option value="None"></option>');
            for (const i of data.apps) {
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
      const chosenApp = app.val();
      // Gets rid of old data but keeps table structure.
      dataTable = $('#historical-log-table').DataTable(); // eslint-disable-line new-cap
      dataTable.destroy();
      if (chosenApp !== 'None') {
        $('#hidden-app-alias').css('display', 'block');
        $('#hidden-start').css('display', 'block');
        $('#app-alias').val('');
        $.ajax({
          url: '/sessionList',
          data: {
            apiKey: apiKey.html(),
            device: device.val(),
            app: chosenApp,
          },
          cache: false,
          success: function(data) {
            time.empty();
            $('#historical-log-table tbody tr').remove();
            time.append('<option value="None"></option>');
            for (const i of data.starttimes) {
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
      const chosenStarttime = time.val();
      // Gets rid of old data but keeps table structure.
      dataTable = $('#historical-log-table').DataTable(); // eslint-disable-line new-cap
      dataTable.destroy();
      $('#historical-log-table tbody tr').remove();
      if (chosenStarttime !== 'None') {
        $.ajax({
          url: '/logs',
          data: {
            apiKey: apiKey.html(),
            device: device.val(),
            app: app.val(),
            starttime: chosenStarttime,
          },
          cache: false,
          success: function(data) {
            $('#historical-log-table tbody').append(data.logs);
            dataTable = $('#historical-log-table').DataTable(); // eslint-disable-line new-cap
          },
        });
      }
    });

    $('#device-alias').click(e => {
      e.preventDefault();
      $.ajax({
        url: '/aliasDevice',
        data: {
          apiKey: apiKey.html(),
          device: device.val(),
          alias: $('#dev-alias').val(),
        },
        success: function(data) {
          if (data.dev_success) {
            window.location.reload();
          } else {
            alert('Device Alias needs to be unique');
          }
        },
      });
    });

    $('#appname-alias').click(e => {
      e.preventDefault();
      $.ajax({
        url: '/aliasApp',
        data: {
          apiKey: apiKey.html(),
          device: device.val(),
          app: app.val(),
          alias: $('#app-alias').val(),
        },
        success: function(data) {
          if (data.app_success) {
            window.location.reload();
          } else {
            alert('App Alias needs to be unique');
          }
        },
      });
    });

    $('#clear-datastore').click(e => {
      e.preventDefault();
      $.ajax({
        url: '/clearDatastore',
        success: window.location.reload(),
      });
    });
  }

  /** Handles WebSocket opening */
  websocketOnOpen() {
    const apiKey = Util.getCookie('api_key');

    const payload = {
      messageType: 'associateUser',
      apiKey: apiKey || '',
    };

    this.ws_.send(JSON.stringify(payload));

    // Get all the devices for historical sessions.
    $.ajax({
      url: '/deviceList',
      data: {
        apiKey: payload.apiKey,
      },
      dataType: 'json',
      cache: false,
      success: function(data) {
        if (data.success) {
          $('#device').append('<option value="None"></option>');
          for (const i of data.devices) {
            $('#device').append(`<option value="${i}">${i}</option>`);
          }
        } else {
          $('#main-page').html('<p>No Datastore and/or No Data</p>');
        }
      },
    });

    if ($('#cpu-usage-graph').length > 0) {
      this.metricGrapher = new MetricGrapher('cpu-usage-graph',
        'mem-usage-graph', 'net-usage-graph');
      this.metricGrapher.render();
    }
  }

  /**
   * Decodes the WebSocket message and adds to table
   *
   * @param {MessageEvent} message the message from the WebSocket connection
   */
  websocketOnMessage(message) {
    const messageData = JSON.parse(message.data);

    if (messageData.messageType === 'logData') {
      // If we get more log data, append the log data to the table and scroll to
      // the bottom of the table.
      for (const logEntry of messageData.logEntries) {
        this.dataTable_.row.add($(logEntry)).draw();
        const scrollBody = $('.dataTables_scrollBody');
        scrollBody.scrollTop(scrollBody[0].scrollHeight);
      }
    }

    if (messageData.messageType === 'deviceMetrics') {
      this.metricGrapher.setMetrics(messageData);
      this.metricGrapher.render();
    }
  }
});
