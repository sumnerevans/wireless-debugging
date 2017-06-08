/**
* Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
* @fileoverview Contains code for graphing device metrics using D3
*/

class MetricGrapher {

  constructor(){

    this.cpuUsageHistory = [];
    for (let i = 0; i < 150; i++) {
      this.cpuUsageHistory.push(0);
    }
    console.log(this.cpuUsageHistory);
    this.metrics = {
      cpuUsage: 0.0
    }

    var ctx = document.getElementById("cpuUsageGraph").getContext('2d');
    this.myLineChart = new Chart(ctx, {
      type: 'line',
      data: this.cpuUsageHistory,
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
  }

}
