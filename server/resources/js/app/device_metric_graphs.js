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

    //Adding null values to data points initially graphed
    for (let i = 0; i < recordedTime + 1; i++) {
      this.cpuUsageHistory.push(null);
      this.memoryUsageHistory.push(null);
      this.networkSentHistory.push(null);
      this.networkReceiveHistory.push(null);
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
        datasets: [
          this.getDataset(this.cpuUsageHistory ,"#3cba9f"),
        ]
      },
      options: this.getOptions(100)
    });


    this.memoryGraph = new Chart(memoryGraphCanvas, {
      type: 'line',
      data: {
        labels: this.xAxisScale,
        datasets: [
          this.getDataset(this.memoryUsageHistory ,"#3e95cd"),
        ]
      },
      options: this.getOptions(1024)
    });

    this.networkGraph = new Chart(networkGraphCanvas, {
      type: 'line',
      fullWidth: true,
      data: {
        labels: this.xAxisScale,
        datasets: [
          this.getDataset(this.networkSentHistory ,"#4EE9E4"),
          this.getDataset(this.networkReceiveHistory ,"#8e5ea2")
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

    this.memoryUsageHistory.push(this.metrics.memUsage/1024.0);
    this.memoryUsageHistory.shift();

    this.networkSentHistory.push(this.metrics.netSentPerSec);
    this.networkSentHistory.shift();

    this.networkReceiveHistory.push(this.metrics.netReceivePerSec);
    this.networkReceiveHistory.shift();

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

  getDataset(data, color) {
    return {
      data: data,
      borderColor: color,
      borderWidth: 2,
      fill: true,
      pointRadius: 0.01,
    }
  }

}
