/**
* @fileoverview Contains code for graphing device metrics using D3
*/

class MetricGrapher {
  /** Initializes the graphs for device metrics using chart.js.
   * @param {string=} cpuCanvasId
   * @param {string=} memoryCanvasId
   * @param {string=} networkCanvasId
   */
  constructor(cpuCanvasId, memoryCanvasId, networkCanvasId) {
    let timeInterval = 0.2;
    // 30 seconds times sample rate gives number of metrics recorded.
    let recordedTime = 30 * (1 / timeInterval);

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
    }

    this.initializeData(recordedTime);

    let cpuGraphCanvas = $(`#${cpuCanvasId}`)[0].getContext('2d');
    let memoryGraphCanvas = $(`#${memoryCanvasId}`)[0].getContext('2d');
    let networkGraphCanvas = $(`#${networkCanvasId}`)[0].getContext('2d');

    /** @public @const {!Chart} */
    this.cpuGraph = new Chart(cpuGraphCanvas, {
      type: 'line',
      data: {
        labels: this.xAxisScale_,
        datasets: [
          this.generateDataset_(this.cpuUsageHistory_ ,"#3cba9f"),
        ]
      },
      options: this.generateOptions_(100)
    });

    /** @public @const {!Chart} */
    this.memoryGraph = new Chart(memoryGraphCanvas, {
      type: 'line',
      data: {
        labels: this.xAxisScale_,
        datasets: [
          this.generateDataset_(this.memoryUsageHistory_ ,"#3e95cd"),
        ]
      },
      options: this.generateOptions_(1024)
    });

    /** @public @const {!Chart} */
    this.networkGraph = new Chart(networkGraphCanvas, {
      type: 'line',
      fullWidth: true,
      data: {
        labels: this.xAxisScale_,
        datasets: [
          this.generateDataset_(this.networkSentHistory_ ,"#4EE9E4"),
          this.generateDataset_(this.networkReceiveHistory_ ,"#8e5ea2")
        ]
      },
      options: this.generateOptions_(1000)
    });
  }

  /**
   * Sets the private variable this.metrics to the metrics passed in.
   * @param {object} metricsObject
   */
  setMetrics(metricsObject) {
    this.metrics = metricsObject;
  }

  /**
   * Adds null values to arrays that are initially graphed before actual
   * metrics recieved.
   * @param {number} recordedTime
   */
  initializeData(recordedTime) {
    //Adding null values to data points initially graphed
    for (let i = 0; i < recordedTime; i++) {
      this.cpuUsageHistory_.push(null);
      this.memoryUsageHistory_.push(null);
      this.networkSentHistory_.push(null);
      this.networkReceiveHistory_.push(null);
      // x values generated based on time (previous 30 seconds)
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
   * @param {number} suggestedMax
   * @return {object}
   */
  generateOptions_(suggestedMax) {
    return {
      legend: {
        display: false
       },
       scales: {
         xAxes: [{
          display: true,
          ticks: {
            maxTicksLimit: 10.1,
            max: 0,
            min: 30,
          }
        }],
        yAxes: [{
        display: true,
        ticks: {
          suggestedMax: suggestedMax,
          beginAtZero: true,
        }
        }]
      },
      tooltips: {
        enabled: false,
      },
      hover: {
        mode: null
      },
      animation: {
        duration: 0,
      },
    }
  }

  /**
   * Generates style of the line to be graphed.
   * @param {number} data
   * @param {Array<number>} color
   */
  generateDataset_(data, color) {
    return {
      data: data,
      borderColor: color,
      borderWidth: 2,
      fill: true,
      pointRadius: 0.01,
    }
  }
}
