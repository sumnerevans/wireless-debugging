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
    const apiKey = Util.getCookie('api_key');

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
            $('#device').append(
              `<option value="${i}">${i}</option>`);
          }
        } else {
          $('#main-page').html('<p>No Datastore and/or No Data</p>');
        }
      }
    });

    if ($('#cpu-usage-graph').length > 0) {
      this.metricGrapher = new MetricGrapher('cpu-usage-graph',
        'mem-usage-graph', 'net-usage-graph');
      this.metricGrapher.render();
    }
  }

  /** Decodes the WebSocket message and adds to table */
  websocketOnMessage(message) {
    let messageData = JSON.parse(message.data);

    if (messageData.messageType === 'logData') {
      this.data_table.destroy();
      this.logTable_.append(messageData.logEntries);
      this.data_table = $('#log-table').DataTable();
    }

    if (messageData.messageType === 'deviceMetrics') {
      this.metricGrapher.setMetrics(messageData);
      this.metricGrapher.render();
    }
  }
});
