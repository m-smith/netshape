"use strict";

var svg = d3.select("svg")
var width = document.querySelector("svg").clientWidth,
    height = document.querySelector("svg").clientHeight;
var view = svg.call(
        d3.zoom()
        .scaleExtent([0.1, 10])
        .on("zoom", zoomed)
    ).append("g");
var zoomBar = svg.append("rect")
    .attr("x", 0)
    .attr("y", height - 20).attr("class", "bar")
    .attr("width", width * 0.5)
    .attr("height", 2);

var gradient_legend = svg.append("defs").append("linearGradient")
    .attr("id", "legendGradient").attr("y2", "100%").attr("x2", "0%");

var legend = svg.append("g").attr("class", "legend")

function add_gradient(s){
  legend.selectAll("*").remove();
  var w = 20,
      h = 400,
      y = (height - h) / 2,
      x = 10;
  legend.append("text").text(s[0]).attr("x", x + w + 5).attr("y", y+7)
  legend.append("rect").attr("x", x)
    .attr("y", y).attr("width", w).attr("height", h)
    .style("fill", "url(#legendGradient)");
  legend.append("text").text(s[1]).attr("x", x + w + 5).attr("y", y+h)
}

function add_quantized(){
  legend.selectAll("*").remove();
}



var category_legend = 0

d3.select("#colour").on("change", change_colour_attr);
d3.select("#colourScheme").on("change", change_colour_scheme);
var colour_range = ["brown", "steelblue"]
var colour_scheme = 'continuous',
    colourAttr = '',
    colour_scheme_options = {
      'discrete': d3.scaleOrdinal(d3.schemeCategory20),
      'continuous': d3.scaleLinear().range(colour_range)
    };

var simulation = d3.forceSimulation()
    .force("link", d3.forceLink().id(function(d) { return d.id; }))
    .force("charge", d3.forceManyBody().strength(-10))
    .force("center", d3.forceCenter(width / 2, height / 2));

var div = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

d3.json("./data/{{datapath}}", function(error, graph) {
  if (error) throw error;

  var link = view.append("g")
      .attr("class", "links")
    .selectAll("line")
    .data(graph.links)
    .enter().append("line")
      .attr("stroke-width", function(d) { return 0.4 });

  var node = view.append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(graph.nodes)
    .enter().append("circle")
    .attr("r", 5)
    .call(d3.drag()
        .on("start", dragstarted)
        .on("drag", dragged)
        .on("end", dragended)
    ).on("mouseover", function(d) {
        div.transition()
          .duration(200)
          .style("opacity", .9);
        div.html(d.id)
            .style("left", (d3.event.pageX) + "px")
            .style("top", (d3.event.pageY - 28) + "px");
    })
    .on("mouseout", function(d) {
        div.transition()
            .duration(500)
            .style("opacity", 0);
    });

  simulation
      .nodes(graph.nodes)
      .on("tick", ticked);
  simulation.force("link")
      .links(graph.links);
  function ticked() {
    link
        .attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node
        .attr("cx", function(d) { return d.x; })
        .attr("cy", function(d) { return d.y; });
  }
});

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}

function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}

function zoomed() {
    var transform = d3.event.transform;


    var currentScale = (view.attr('transform') &&
    parseFloat(view.attr('transform').split(" ")[1].replace( /[^\d\.]*/g, '')));
    if ((currentScale != transform.k) || d3.event.sourceEvent.shiftKey){
        view.attr("transform", "translate(" + transform.x + "," + transform.y + ") scale(" + transform.k + ")");
        zoomBar.attr("width", transform.k * width * 0.5);
    }
}

function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0);
  d.fx = null;
  d.fy = null;
}

function change_colour_scheme(){
  colour_scheme = d3.event.srcElement.value
  colourNodes()
}

function change_colour_attr(){
  colourAttr = d3.event.srcElement.value
  colourNodes()
}

function scale_colour(){
  if (colour_scheme == 'discrete'){
    add_quantized()
    return
  }
  var node = view.selectAll("circle")
  var s = d3.extent(node.data(), function(e){
    return e[colourAttr];
  })
  colour_scheme_options['continuous'] = d3.scaleLinear()
    .domain([s[0],s[1]]).range(colour_range)
  var c = colour_scheme_options['continuous']
  gradient_legend.selectAll("stop")
    .data( c.range() )
    .enter().append("stop")
    .attr("offset", function(d,i) { return i/(c.range().length-1); })
    .attr("stop-color", function(d) { return d; });
  add_gradient(s);
}

function colourNodes(){
  scale_colour()
  var node = view.selectAll("circle")
  var c = colour_scheme_options[colour_scheme]
  node.attr("fill", function(d) { return c(parseFloat(d[colourAttr])); })
}

