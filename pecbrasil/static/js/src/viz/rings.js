d3plus.data.rings = "object";
d3plus.vars.rings = [];

d3plus.apps.rings = function(vars) {
      
  var tooltip_width = 300
      
  var width = vars.small ? vars.width : vars.width-tooltip_width
      
  var tree_radius = vars.height > width ? width/2 : vars.height/2,
      node_size = d3.scale.linear().domain([1,2]).range([8,4]),
      ring_width = vars.small ? tree_radius/2.25 : tree_radius/3,
      total_children,
      hover = null;
      
  // container for the visualization
  var viz_enter = vars.parent_enter.append("g").attr("class", "viz")
    .attr("transform", "translate(" + width / 2 + "," + vars.height / 2 + ")");
    
  viz_enter.append("g").attr("class","links")
  viz_enter.append("g").attr("class","nodes")
    
  d3.select("g.viz").transition().duration(d3plus.timing)
    .attr("transform", "translate(" + width / 2 + "," + vars.height / 2 + ")");
  
  //^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  // INIT vars & data munging
  //-------------------------------------------------------------------

  var tree = d3.layout.tree()
      .size([360, tree_radius - ring_width])
      .separation(function(a, b) { return (a.parent == b.parent ? 1 : 2) / a.depth; });

  var diagonal = d3.svg.diagonal.radial()
      .projection(function(d) { return [d.y, d.x / 180 * Math.PI]; });
      
  var line = d3.svg.line()
      .x(function(d) { return d.x; })
      .y(function(d) { return d.y; })
      .interpolate("basis");
      
  if (vars.app_data) {
    var root = get_root()
  }
  else {
    var root = {"links": [], "nodes": []}
  }
      
  //===================================================================
  
  //^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  // LINKS
  //-------------------------------------------------------------------
  
  var link = d3.select(".links").selectAll(".link")
    .data(root.links)
      
  link.enter().append("path")
    .attr("fill", "none")
    .attr("class", "link")
    .attr("opacity",0);
      
  if (!vars.last_highlight || vars.last_highlight != vars.highlight) {
    link.transition().duration(d3plus.timing/2)
      .attr("opacity",0)
      .transition().call(line_styles)
      .transition().duration(d3plus.timing/2)
      .attr("opacity",function(d) {
        if (hover && d3.select(this).attr("stroke") == "#ddd") {
           return 0.25
        } return 0.75;
      })
  }
  else {
    link.call(line_styles)
      .attr("opacity",function(d) {
        if (hover && d3.select(this).attr("stroke") == "#ddd") {
           return 0.25
        } return 0.75;
      })
  }
      
  link.exit().transition().duration(d3plus.timing)
    .attr("opacity",0)
    .remove();

  //===================================================================

  //^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  // NODES
  //-------------------------------------------------------------------
  
  var node = d3.select(".nodes").selectAll("g.node")
    .data(root.nodes,function(d){return d[vars.id]})
      
  var node_enter = node.enter().append("g")
      .attr("class", "node")
      .attr("opacity",0)
      .attr("transform", function(d) {
        if (d.depth == 0) return "none"
        else return "rotate(" + (d.ring_x - 90) + ")translate(" + d.ring_y + ")"; 
      })
      
  node_enter.append("circle")
    .attr("id",function(d) { return "node_"+d[vars.id]; })
    .call(circle_styles)
    .attr("r",0)
    
  node_enter.append("text")
    .attr("font-weight",vars.font_weight)
    .attr("x",0)
    .attr("font-family",vars.font)
    .attr("opacity",0)
    .call(text_styles);
      
  node
    .on(d3plus.evt.over,function(d){
      if (d.depth != 0) {
        d3.select(this).style("cursor","pointer")
        if (!d3plus.ie) {
          d3.select(this).style("cursor","-moz-zoom-in")
          d3.select(this).style("cursor","-webkit-zoom-in")
        }
        hover = d;
        if (!vars.small) {
          link.call(line_styles);
          d3.selectAll(".node circle").call(circle_styles);
          d3.selectAll(".node text").call(text_styles);
        }
      }
    })
    .on(d3plus.evt.out,function(d){
      if (d.depth != 0) {
        hover = null;
        if (!vars.small) {
          link.call(line_styles);
          d3.selectAll(".node circle").call(circle_styles);
          d3.selectAll(".node text").call(text_styles);
        }
      }
    })
    .on(d3plus.evt.click,function(d){
      if (d.depth != 0) vars.parent.call(chart.highlight(d[vars.id]));
    })
      
  node.transition().duration(d3plus.timing)
      .attr("opacity",1)
      .attr("transform", function(d) {
        if (d.depth == 0) return "none"
        else return "rotate(" + (d.ring_x - 90) + ")translate(" + d.ring_y + ")"; 
      })
  
  node.select("circle").transition().duration(d3plus.timing)
    .call(circle_styles)
    
  node.select("text").transition().duration(d3plus.timing)
    .attr("opacity",function(d){
      if (vars.small) return 0
      else return 1
    })
    .call(text_styles)
    .each(function(d) {
      if (d.depth == 0) {
        var s = Math.sqrt((ring_width*ring_width)/2), 
            w = s*1.4, 
            h = s/1.4, 
            resize = true
      }
      else {
        d3.select(this).attr("font-size","10px")
        var w = ring_width-d.radius*2, resize = false
        if (d.depth == 1) var h = (Math.PI*((tree_radius-(ring_width*2))*2))*(d.size/360);
        if (d.depth == 2) var h = (Math.PI*((tree_radius-ring_width)*2))/total_children;
      }

      if (h < 15) h = 15;
      
      d3plus.utils.wordwrap({
        "text": d3plus.utils.variable(vars,d,vars.text),
        "parent": this,
        "width": w,
        "height": h,
        "resize": resize,
        "font_min": 10
      })

      d3.select(this).attr("y",(-d3.select(this).node().getBBox().height/2)+"px")
      
    })
      
  node.exit().transition().duration(d3plus.timing)
      .attr("opacity",0)
      .remove()
      
  //===================================================================
  
  hover = null;
  
  vars.last_highlight = vars.highlight
  
  if (!vars.small && vars.app_data) {

    d3plus.ui.tooltip.remove(vars.type)
    
    make_tooltip = function(html) {
        
      if (typeof html == "string") html = "<br>"+html
    
      var tooltip_appends = "<div class='d3plus_tooltip_data_title'>"
      tooltip_appends += vars.format("Primary Connections")
      tooltip_appends += "</div>"

      vars.connections[vars.highlight].forEach(function(n){
      
        var parent = "d3.select(&quot;#"+vars.parent.node().id+"&quot;)"
      
        tooltip_appends += "<div class='d3plus_network_connection' onclick='"+parent+".call(chart.highlight(&quot;"+n[vars.id]+"&quot;))'>"
        tooltip_appends += "<div class='d3plus_network_connection_node'"
        tooltip_appends += " style='"
        tooltip_appends += "background-color:"+fill_color(n)+";"
        tooltip_appends += "border-color:"+stroke_color(n)+";"
        tooltip_appends += "'"
        tooltip_appends += "></div>"
        tooltip_appends += "<div class='d3plus_network_connection_name'>"
        tooltip_appends += d3plus.utils.variable(vars,n[vars.id],vars.text)
        tooltip_appends += "</div>"
        tooltip_appends += "</div>"
      })
    
      var tooltip_data = d3plus.utils.tooltip(vars,vars.highlight)

      d3plus.ui.tooltip.remove(vars.type)
      d3plus.ui.tooltip.create({
        "title": d3plus.utils.variable(vars,vars.highlight,vars.text),
        "color": d3plus.utils.color(vars,vars.highlight),
        "icon": d3plus.utils.variable(vars,vars.highlight,"icon"),
        "style": vars.icon_style,
        "id": vars.type,
        "html": tooltip_appends+html,
        "footer": vars.footer,
        "data": tooltip_data,
        "x": vars.width-tooltip_width-5,
        "y": vars.margin.top+5,
        "max_height": vars.height-10,
        "fixed": true,
        "width": tooltip_width,
        "mouseevents": true,
        "parent": vars.parent,
        "background": vars.background
      })
      
    }
    
    var html = vars.click_function ? vars.click_function(vars.highlight,root.nodes) : ""
    
    if (typeof html == "string") make_tooltip(html)
    else {
      d3.json(html.url,function(data){
        html = html.callback(data)
        make_tooltip(html)
      })
    }
    
  }
  
  function fill_color(d) {
    if(!vars.active || d3plus.utils.variable(vars,d[vars.id],vars.active)){
      return d[vars.color];
    } 
    else {
      var lighter_col = d3.hsl(d[vars.color]);
      lighter_col.l = 0.95;
      return lighter_col.toString()
    }
  }
  
  function stroke_color(d) {
    if(!vars.active || d3plus.utils.variable(vars,d[vars.id],vars.active)){
      return "#333";
    } else {
      return d3plus.utils.darker_color(d[vars.color])
    }
  }
  
  function line_styles(l) {
    l
      .attr("stroke", function(d) {
        if (hover) {
          if (d.source == hover || d.target == hover || 
          (hover.depth == 2 && (hover.parents.indexOf(d.target) >= 0))) {
            this.parentNode.appendChild(this);
            return vars.highlight_color;
          } else if (hover.depth == 1 && hover.children_total.indexOf(d.target) >= 0) {
            return vars.secondary_color;
          }
          else {
            return "transparent"
          }
        }
        if (d.source[vars.id] == vars.highlight) {
          this.parentNode.appendChild(this)
          return "#888"
        }
        else return "#ccc"
      })
      .attr("stroke-width", function(d){
        if (d.source[vars.id] == vars.highlight) return 2
        else return 1
      })
      .attr("d", function(d) {
        if (d.source[vars.id] == vars.highlight) {
          var x = d.target.ring_y * Math.cos((d.target.ring_x-90)*(Math.PI/180)),
              y = d.target.ring_y * Math.sin((d.target.ring_x-90)*(Math.PI/180))
          return line([{"x":0,"y":0},{"x":x,"y":y}]);
        } else {
          var x1 = d.source.ring_x,
              y1 = d.source.ring_y,
              x2 = d.target.ring_x,
              y2 = d.target.ring_y
          return diagonal({"source":{"x":x1,"y":y1},"target":{"x":x2,"y":y2}});
        }
      })
  }
  
  function circle_styles(c) {
    c
      .attr("fill", function(d){
        var color = fill_color(d)
        
        if (d.depth == 0) return color;
        else if (d.depth == 1 && (!hover || d == hover || d.children_total.indexOf(hover) >= 0)) return color;
        else if (d.depth == 2 && (!hover || d == hover || d.parents.indexOf(hover) >= 0)) return color;
        else return "lightgrey"
      
      })
      .attr("stroke", function(d){
        var color = stroke_color(d)
        
        if (d.depth == 0) return color;
        else if (d.depth == 1 && (!hover || d == hover || d.children_total.indexOf(hover) >= 0)) return color;
        else if (d.depth == 2 && (!hover || d == hover || d.parents.indexOf(hover) >= 0)) return color;
        else return "darkgrey"
      
      })
      .attr("stroke-width", "1")
      .attr("r", function(d){ 
        if (d.depth == 0) return ring_width/2;
        var s = node_size(d.depth); 
        if (d.depth == 1) var limit = (Math.PI*((tree_radius-(ring_width*2))*2))/total_children;
        if (d.depth == 2) var limit = (Math.PI*((tree_radius-ring_width)*2))/total_children;
        if (s > limit/2) s = limit/2;
        if (s < 2) s = 2;
        d.radius = s;
        return d.radius;
      })
  }
  
  function text_styles(t) {
    t
      .attr("fill",function(d){
        if (d.depth == 0) {
          var color = d3plus.utils.text_color(fill_color(d));
        } 
        else {
          var color = d3plus.utils.darker_color(d[vars.color]);
        }

        if (d.depth == 0) return color;
        else if (d.depth == 1 && (!hover || d == hover || d.children_total.indexOf(hover) >= 0)) return color;
        else if (d.depth == 2 && (!hover || d == hover || d.parents.indexOf(hover) >= 0)) return color;
        else return "lightgrey"
      })
      .attr("text-anchor", function(d) { 
        if (d.depth == 0) return "middle"
        else return d.ring_x%360 < 180 ? "start" : "end"; 
      })
      .attr("transform", function(d) { 
        if (d.depth == 0) return "none"
        else {
          var offset = d.radius*2
          return d.ring_x%360 < 180 ? "translate("+offset+")" : "rotate(180)translate(-"+offset+")";
        }
      })
  }
  
  function get_root(){
    
    var links = [], nodes = [], root = {}
      
    root.ring_x = 0;
    root.ring_y = 0;
    root.depth = 0;
    root[vars.text] = d3plus.utils.variable(vars,vars.highlight,vars.text)
    root[vars.id] = vars.highlight
    root.children = []
    root[vars.color] = d3plus.utils.color(vars,vars.highlight)
    root[vars.active] = d3plus.utils.variable(vars,vars.highlight,vars.active)
  
    nodes.push(root);
    
    // populate first level
    var prim_links = vars.connections[vars.highlight]
    if (prim_links) {
      prim_links.forEach(function(child){
  
        // give first level child the properties
        child.ring_x = 0;
        child.ring_y = ring_width;
        child.depth = 1;
        child[vars.text] = d3plus.utils.variable(vars,child[vars.id],vars.text)
        child.children = []
        child.children_total = []
        child[vars.color] = d3plus.utils.color(vars,child[vars.id])
        child[vars.active] = d3plus.utils.variable(vars,child[vars.id],vars.active)
  
        // push first level child into nodes
        nodes.push(child);
        root.children.push(child);
  
        // create link from center to first level child
        links.push({"source": nodes[nodes.indexOf(root)], "target": nodes[nodes.indexOf(child)]})
      
        vars.connections[child[vars.id]].forEach(function(grandchild){ 
          child.children_total.push(grandchild);
        })
      
      })
    
      // populate second level
      var len = nodes.length,
          len2 = nodes.length
        
      while(len--) {

        var sec_links = vars.connections[nodes[len][vars.id]]
        if (sec_links) {
          sec_links.forEach(function(grandchild){
    
            // if grandchild isn't already a first level child or the center node
            if (prim_links.indexOf(grandchild) < 0 && grandchild[vars.id] != vars.highlight) {
          
              grandchild.ring_x = 0;
              grandchild.ring_y = ring_width*2;
              grandchild.depth = 2;
              grandchild[vars.text] = d3plus.utils.variable(vars,grandchild[vars.id],vars.text)
              grandchild[vars.color] = d3plus.utils.color(vars,grandchild[vars.id])
              grandchild[vars.active] = d3plus.utils.variable(vars,grandchild[vars.id],vars.active)
              grandchild.parents = []

              var s = 10000, node_id = 0;
              prim_links.forEach(function(node){
                var temp_links = vars.connections[node[vars.id]]
                temp_links.forEach(function(node2){
                  if (node2[vars.id] == grandchild[vars.id]) {
                    grandchild.parents.push(node);
                    if (temp_links.length < s) {
                      s = temp_links.length
                      node_id = node[vars.id]
                    }
                  }
                })
              })
              var len3 = len2;
              while(len3--) {
                if (nodes[len3][vars.id] == node_id && nodes[len3].children.indexOf(grandchild) < 0) {
                  nodes[len3].children.push(grandchild);
                }
              }
      
              // if grandchild hasn't been added to the nodes list, add it
              if (nodes.indexOf(grandchild) < 0) {
                nodes.push(grandchild);
              }
      
              // create link from child to grandchild
              links.push({"source": nodes[len], "target": nodes[nodes.indexOf(grandchild)]})
      
            }
    
          })
        }
  
      }
    }
    
    var first_offset = 0
    
    total_children = d3.sum(nodes,function(dd){
        if (dd.depth == 1) {
          if (dd.children.length > 0) return dd.children.length;
          else return 1;
        } else return 0;
      })
    

    // sort first level vars.connections by color
    nodes[0].children.sort(function(a, b){
      var a_color = d3.rgb(a[vars.color]).hsl().h
      var b_color = d3.rgb(b[vars.color]).hsl().h
      if (d3.rgb(a[vars.color]).hsl().s == 0) a_color = 361
      if (d3.rgb(b[vars.color]).hsl().s == 0) b_color = 361
      if (a_color < b_color) return -1;
      if (a_color > b_color) return 1;
      return 0;
    })
    
    nodes[0].children.forEach(function(d){
      if (d.children.length > 1) var num = d.children.length;
      else var num = 1;
      d.ring_x = ((first_offset+(num/2))/total_children)*360
      d.size = (num/total_children)*360
      if (d.size > 180) d.size = 180
      
      var positions = (num)/2
      
      // sort children by color
      d.children.sort(function(a, b){
        var a_color = d3.rgb(a[vars.color]).hsl().h
        var b_color = d3.rgb(b[vars.color]).hsl().h
        if (d3.rgb(a[vars.color]).hsl().s == 0) a_color = 361
        if (d3.rgb(b[vars.color]).hsl().s == 0) b_color = 361
        if (a_color < b_color) return -1;
        if (a_color > b_color) return 1;
        return 0;
      })
      
      d.children.forEach(function(c,i){
        if (d.children.length <= 1) c.ring_x = d.ring_x
        else c.ring_x = d.ring_x+(((i+0.5)-positions)/positions)*(d.size/2)
      })
      first_offset += num
    })


    return {"nodes": nodes, "links": links};
  }
};
