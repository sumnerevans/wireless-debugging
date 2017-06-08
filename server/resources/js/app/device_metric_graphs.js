/**
* Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
* @fileoverview Contains code for graphing device metrics using D3
*/

class MetricGrapher {

  constructor(cpuCanvasId, memoryCanvasId, networkCanvasId) {
    let timeInterval = 0.2;
    // 30 seconds times sample rate gives number of metrics recorded
    let recordedTime = 30 * (1 / timeInterval);

    this.cpuUsageHistory = [];
    this.memoryUsageHistory = [];
    this.networkSentHistory = [];
    this.networkReceiveHistory = [];
    this.xAxisScale = [];

    for (let i = 0; i < recordedTime; i++) {
      this.cpuUsageHistory.push(0.0);
      this.memoryUsageHistory.push(0);
      this.networkSentHistory.push(0);
      this.networkReceiveHistory.push(0);
      this.xAxisScale.push((recordedTime - i) / 5);
    }
    this.xAxisScale[recordedTime - 1] = 0;

    this.metrics = {
      cpuUsage: 0.0,
      memUsage: 0,
      memTotal: 0,
      netSentPerSec: 0,
      netReceivePerSec: 0
    }

    let cpuGraphCanvas = document.getElementById(cpuCanvasId).getContext('2d');
    let memoryGraphCanvas = document.getElementById(memoryCanvasId).getContext('2d');
    let networkGraphCanvas = document.getElementById(networkCanvasId).getContext('2d');

    this.cpuGraph = new Chart(cpuGraphCanvas, {
      type: 'line',
      data: {
        labels: this.xAxisScale,
        datasets: [{
          radius: 1.5,
          data: this.cpuUsageHistory,
          label: "CPU Usage",
          borderColor: "#3cba9f",
          pointBackgroundColor: "#3cba9f",
          fill: true,
          cubicInterpolationMode: "default",
          pointRadius: 0.5,
        },
        ]
      },
      options: this.getOptions(100)
    });

    this.memoryGraph = new Chart(memoryGraphCanvas, {
      type: 'line',
      data: {
        labels: this.xAxisScale,
        datasets: [{
          data: this.memoryUsageHistory,
          label: "CPU Usage",
          borderColor: "#3e95cd",
          fill: true,
          pointRadius: 0.5,
        },
        ]
      },
      options: this.getOptions(1024)
    });

    this.networkGraph = new Chart(networkGraphCanvas, {
      type: 'line',
      data: {
        labels: this.xAxisScale,
        datasets: [{
          data: this.networkSentHistory,
          label: "Sent",
          borderColor: "#fcc182",
          fill: true,
          pointRadius: 0.5,
        },
        {
          data: this.networkReceiveHistory,
          label: "Received",
          borderColor: "#8e5ea2",
          fill: true,
          pointRadius: 0.5,
        },
        ]
      },
      options: this.getOptions(1000)
    });
  }

  setMetrics(metricsObject) {
    this.metrics = metricsObject;
  }

  render() {
    this.cpuUsageHistory.push(this.metrics.cpuUsage * 100);
    this.cpuUsageHistory.shift();

    this.memoryUsageHistory.push(this.metrics.memUsage);
    this.memoryUsageHistory.shift();

    this.networkSentHistory.push(this.metrics.netSentPerSec);
    this.networkSentHistory.shift();

    this.networkReceiveHistory.push(this.metrics.netReceivePerSec);
    this.networkReceiveHistory.shift();

    console.log(this.metrics);

    this.cpuGraph.data.datasets[0].data = this.cpuUsageHistory;
    this.memoryGraph.data.datasets[0].data = this.memoryUsageHistory;
    this.networkGraph.data.datasets[0].data = this.networkSentHistory;
    this.networkGraph.data.datasets[1].data = this.networkReceiveHistory;

    this.cpuGraph.update();
    this.memoryGraph.update();
    this.networkGraph.update();
  }

  getOptions(suggestedMax) {
    return {
        legend: {
          display: false
         },
         scales: {
           xAxes: [{
            display: true,
            ticks: {
              autoSkip: true,
              maxTicksLimit: 10,
              beginAtZero: true,
            }
          }],
          yAxes: [{
          display: true,
          ticks: {
            suggestedMax: suggestedMax,
            beginAtZero: true
          }
          }]
        },
        tooltips: {
          enabled: false,
        },
        hover: {
          mode: null
        },
    }
  }

}
