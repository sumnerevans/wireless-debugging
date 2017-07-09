/**
 * @fileoverview Contains code for graphing device metrics using Chart.js.
 */

define(['chart'], Chart => class MetricGrapher {
  /**
   * Initializes the graphs for device metrics using chart.js.
   * @param {string} cpuCanvasId the ID of the CPU Usage Canvas DOM Element
   * @param {string} memoryCanvasId the ID of the Memory Usage Canvas DOM
   *                                Element
   * @param {string} networkCanvasId the ID of the Network Usage Canvas DOM
   *                                 Element
   */
  constructor(cpuCanvasId, memoryCanvasId, networkCanvasId) {
    const timeInterval = 0.2;
    // 30 seconds times sample rate gives number of metrics recorded.
    const recordedTime = 30 * (1 / timeInterval);

    /** @private @const Number */
    this.BYTE_CONVERSION = 1024.0;

    /** @private @const {Array<number>} */
    this.cpuUsageHistory_ = [];
    /** @private @const {Array<number>} */
    this.memoryUsageHistory_ = [];
    /** @private @const {Array<number>} */
    this.networkSentHistory_ = [];
    /** @private @const {Array<number>} */
    this.networkReceiveHistory_ = [];
    /** @private @const {Array<number>} */
    this.xAxisScale_ = [];
    /** @private @const {object} */
    this.metrics = {
      cpuUsage: 0.0,
      memUsage: 0,
      memTotal: 0,
      netSentPerSec: 0,
      netReceivePerSec: 0,
    };

    this.initializeData(recordedTime);

    const cpuGraphCanvas = $(`#${cpuCanvasId}`)[0].getContext('2d');
    const memoryGraphCanvas = $(`#${memoryCanvasId}`)[0].getContext('2d');
    const networkGraphCanvas = $(`#${networkCanvasId}`)[0].getContext('2d');

    /** @public @const {!Chart} */
    this.cpuGraph = new Chart(cpuGraphCanvas, 100, {
      dataset: this.cpuUsageHistory_,
      color: '3cba9f',
    });

    /** @public @const {!Chart} */
    this.memoryGraph = this.createChart(memoryGraphCanvas, {
      dataset: this.memoryUsageHistory_,
      color: '3e95cd',
    });

    /** @public @const {!Chart} */
    this.networkGraph = this.createChart(networkGraphCanvas, 1000, [{
      dataset: this.networkSentHistory_,
      color: '4EE9E4',
    }, {
      dataset: this.networkReceiveHistory_,
      color: '8e5ea2',
    }]);
  }

  /**
   * Creates a Chart object.
   *
   * @param {HTMLElement} canvas the canvas element to create the chart in
   * @param {number} suggestedMax the suggested max to use when creating the
   *                              chart
   * @param {array} datasetConfigs the configurations for the datasets
   * @returns {Chart} the created chart
   */
  createChart(canvas, suggestedMax, datasetConfigs) {
    let datasets = [];
    for (const config of datasetConfigs) {
      datasets = this.generateDataset_(config.dataset, config.color);
    }

    return new Chart(canvas, {
      type: 'line',
      data: {
        labels: this.xAxisScale_,
        datasets: datasets,
      },
      options: this.generateOptions_(suggestedMax),
    });
  }

  /**
   * Sets the private variable this.metrics to the metrics passed in.
   *
   * @param {object} metricsObject the new metrics object
   */
  setMetrics(metricsObject) {
    this.metrics = metricsObject;
  }

  /**
   * Adds null values to arrays that are initially graphed before actual
   * metrics recieved.
   *
   * @param {number} recordedTime the number of initial data points to graph
   */
  initializeData(recordedTime) {
    // Adding null values to data points initially graphed
    for (let i = 0; i < recordedTime; i++) {
      this.cpuUsageHistory_.push(null);
      this.memoryUsageHistory_.push(null);
      this.networkSentHistory_.push(null);
      this.networkReceiveHistory_.push(null);
      // X values generated based on time (previous 30 seconds)
      this.xAxisScale_.push((recordedTime - i) / 5);
    }
    this.xAxisScale_[recordedTime] = 0;
  }

  /**
   * Updates the data that is graphed as the metric information is received.
   */
  render() {
    this.cpuUsageHistory_.push(this.metrics.cpuUsage * 100);
    this.cpuUsageHistory_.shift();

    // Divided by 1024 to convert from KB to MB.
    this.memoryUsageHistory_.push(this.metrics.memUsage /
      this.BYTE_CONVERSION);
    this.memoryUsageHistory_.shift();

    // Divided by 1024 to convert from Bytes to KB.
    this.networkSentHistory_.push(this.metrics.netSentPerSec /
      this.BYTE_CONVERSION);
    this.networkSentHistory_.shift();

    this.networkReceiveHistory_.push(this.metrics.netReceivePerSec /
      this.BYTE_CONVERSION);
    this.networkReceiveHistory_.shift();

    this.cpuGraph.data.datasets[0].data = this.cpuUsageHistory_;
    this.memoryGraph.data.datasets[0].data = this.memoryUsageHistory_;
    this.networkGraph.data.datasets[0].data = this.networkSentHistory_;
    this.networkGraph.data.datasets[1].data = this.networkReceiveHistory_;

    this.cpuGraph.update();
    this.memoryGraph.update();
    this.networkGraph.update();
  }

  /**
   * Generates the style of a graph given the max y value.
   *
   * @param {number} suggestedMax the suggested maximum Y value
   * @return {object} an options object
   */
  generateOptions_(suggestedMax) {
    return {
      legend: {
        display: false,
      },
      scales: {
        xAxes: [{
          display: true,
          ticks: {
            maxTicksLimit: 10.1,
            max: 0,
            min: 30,
          },
        }],
        yAxes: [{
          display: true,
          ticks: {
            suggestedMax: suggestedMax,
            beginAtZero: true,
          },
        }],
      },
      tooltips: {
        enabled: false,
      },
      hover: {
        mode: null,
      },
      animation: {
        duration: 0,
      },
    };
  }

  /**
   * Generates style of the line to be graphed.
   *
   * @param {number} data the data from the dataset
   * @param {string} color the color to use for the dataset
   * @returns {object} a dataset object
   */
  generateDataset_(data, color) {
    return {
      data: data,
      borderColor: `#${color}`,
      borderWidth: 2,
      fill: true,
      pointRadius: 0.01,
    };
  }
});
