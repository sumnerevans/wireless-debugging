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

    for (let i = 0; i < recordedTime + 1; i++) {
      this.cpuUsageHistory.push(20);
      this.memoryUsageHistory.push(20);
      this.networkSentHistory.push(20);
      this.networkReceiveHistory.push(20);
      this.xAxisScale.push((recordedTime - i) / 5);
    }
    this.xAxisScale[recordedTime] = 0;
    console.log(this.xAxisScale);
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
          borderWidth: 2,
          pointBackgroundColor: "#3cba9f",
          fill: true,
          cubicInterpolationMode: "default",
          pointRadius: 0.01,
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
          borderWidth: 2,
          fill: true,
          pointRadius: 0.01,
        },
        ]
      },
      options: this.getOptions(1024)
    });

    this.networkGraph = new Chart(networkGraphCanvas, {
      type: 'line',
      fullWidth: true,
      data: {
        labels: this.xAxisScale,
        datasets: [{
          data: this.networkSentHistory,
          label: "Sent",
          borderColor: "#4EE9E4",
          borderWidth: 2,
          fill: true,
          pointRadius: 0.01,
        },
        {
          data: this.networkReceiveHistory,
          label: "Received",
          borderColor: "#8e5ea2",
          borderWidth: 2,
          fill: true,
          pointRadius: 0.01,
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
    console.log(this.cpuUsageHistory);
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


    console.log(this.cpuGraph.data.datasets);
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
    }
  }

}
