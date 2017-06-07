/**
* Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
* @fileoverview Contains code for graphing device metrics using D3
*/

class MetricGrapher {

  constructor(){

  }

  setMetrics(metricsObject){
    this.metrics = metricsObject;
  }

  render(){
    let barGraph = d3.scaleLinear().domain([0,1.0]).range([0, 1.0]);

    d3.select(".cpuUsageGraph")
      .selectAll("div")
      .data(this.metrics.cpuUsage)
      .enter().append("div")
      // d for data selected
      .style("width", function(d) { return (barGraph(d) * 100) + "%"; })
      .text(function(d) { return (d * 100) + "%"; });
  }

}
