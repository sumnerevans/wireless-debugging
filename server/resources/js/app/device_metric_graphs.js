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
    this.networkUsageHistory = [];
    this.xAxisScale = [];

    for (let i = 0; i < recordedTime; i++) {
      this.cpuUsageHistory.push(0);
      this.memoryUsageHistory.push(0);
      this.networkUsageHistory.push(0);
      this.xAxisScale.push((recordedTime - i) / 5);
    }

    this.metrics = {
      cpuUsage: 0.0,
      memUsage: 0.0,
    }

    let cpuGraphCanvas = document.getElementById(cpuCanvasId).getContext('2d');
    let memoryGraphCanvas = document.getElementById(cpuCanvasId).getContext('2d');
    let networkGraphCanvas = document.getElementById(cpuCanvasId).getContext('2d');


    this.lineGraph = new Chart(cpuGraphCanvas, {
      type: 'line',
      data: {
        labels: this.xAxisScale,
        datasets: [{
            data: this.cpuUsageHistory,
            label: "CPU Usage",
            borderColor: "#3e95cd",
            fill: true
          },
        ]
      },
      options: {}
    });



  }

  setMetrics(metricsObject){
    this.metrics = metricsObject;
  }

  render(){
    this.cpuUsageHistory.push(this.metrics.cpuUsage);
    this.cpuUsageHistory.shift();

    console.log(this.metrics.cpuUsage);

    this.lineGraph.data.datasets[0].data = this.cpuUsageHistory;
    this.lineGraph.update();

  }

}
