/**
* Licensed under http://www.apache.org/licenses/LICENSE-2.0 <see LICENSE file>
* @fileoverview Contains code for graphing device metrics using D3
*/

class MetricGrapher {

  constructor(){

    this.cpuUsageHistory = [];
    this.cpuXScale = [];
    for (let i = 0; i < 150; i++) {
      this.cpuUsageHistory.push([i / 2, i / 5]);
      //this.cpuXScale.push(i / 5);
    }
    //console.log(this.cpuXScale);
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



    var vis = d3.select(".cpuUsageGraph"),
    WIDTH = 300,
    HEIGHT = 150,
    MARGINS = {
        top: 20,
        right: 20,
        bottom: 20,
        left: 50
    },
    xScale = d3.scaleLinear().range([MARGINS.left, WIDTH - MARGINS.right]).domain([0,30]),
    yScale = d3.scaleLinear().range([HEIGHT - MARGINS.top, MARGINS.bottom]).domain([0,100]),
    xAxis = d3.axisBottom()
    .scale(xScale),
    yAxis = d3.axisLeft()
    .scale(yScale);

    vis.append("svg:g")
    .attr("transform", "translate(0," + (HEIGHT - MARGINS.bottom) + ")")
    .call(xAxis);

    vis.append("svg:g")
    .attr("transform", "translate(" + (MARGINS.left) + ",0)")
    .call(yAxis);

    var lineGen = d3.line()
    .x(function(d) {
      return xScale(d[1]);
    })
    .y(function(d) {
      return yScale(d[0]);
    });

    vis.append('svg:path')
      .attr('d', lineGen(this.cpuUsageHistory))
      .attr('stroke', 'green')
      .attr('stroke-width', 2)
      .attr('fill', 'none');









    /*
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
    */
  }

}
