/**
* Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
* @fileoverview Contains code for graphing device metrics using D3
*/

class MetricGrapher {

  constructor(){

    this.cpuUsageHistory = Array.apply(null, new Array(150)).map(Number.prototype.valueOf,0);
    console.log(this.cpuUsageHistory);
    this.metrics = {
      cpuUsage: 0.0
    }

    let barGraph = d3.scaleLinear().domain([0,1.0]).range([0, 1.0]);

    d3.select(".cpuUsageGraph")
      .selectAll("div")
      .data(this.cpuUsageHistory)
      .enter().append("div")
      // d for data selected
      .style("width", function(d) { return (barGraph(d) * 100) + "%"; })
      .text(function(d) { return (d * 100) + "%"; });

    this.cpuGraph = d3.select(".cpuUsageGraph")
      .selectAll("div")
      .data([this.metrics.cpuUsage]);

  }

  setMetrics(metricsObject){
    this.metrics = metricsObject;
  }

  render(){
    this.cpuUsageHistory.push(this.metrics.cpuUsage);
    this.cpuUsageHistory.shift();

    let graph = d3.select(".cpuUsageGraph")
      .selectAll("div")
      .data(this.cpuUsageHistory)
      .style("width", function(d) { return (barGraph(d) * 100) + "%"; })
      .text(function(d) { return (d * 100) + "%"; });

    graph.enter().append("div")
    .data(this.cpuUsageHistory)
    .style("width", function(d) { return (barGraph(d) * 100) + "%"; })
    .text(function(d) { return (d * 100) + "%"; });

    graph.exit().remove();
  }

}
