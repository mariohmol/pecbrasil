function infinite_scroll(selection){
  var url = window.location.href,
      refresh = false,
      remove = false,
      offset = 0,
      format_items = function(d){ return d };
  
  // Initialize variables
  var formatDate = d3.time.format("%B %-d, %Y"),
      parseDate = d3.time.format.iso.parse,
      offset = 0,
      fetching;
  
  scroll = function(selection) {
    selection.each(function(data_passed) {
      var container_el = this;
      
      // On first time add
      var inf_loading_div = d3.select(container_el).selectAll(".infinite_loading")

      inf_loading_div.data([container_el])
        .enter().append("div")
        .attr("class", "infinite_loading")
      
      var loading = dataviva.ui.loading(".infinite_loading")
      loading.text("Loading more items").show()
      
      // The item we're going to listen on for scrolling
      d3.select(window)
          .on("scroll", maybe_fetch)
      
      // Check if we need to fetch
      function maybe_fetch() {

        // get the position of the loading div
        var loading_div_y = !d3.select(".infinite_loading").empty() ? d3.select(".infinite_loading").node().getBoundingClientRect().top : NaN;

        // if we're not currently fetching and offset if not NaN and the loader
        // y pos is less than the height of the page then fetch new items
        if(isNaN(offset)){
          offset = 0;
        }
        // console.log(fetching, offset, loading_div_y, innerHeight, refresh)
        if ((!fetching && offset >= 0 && loading_div_y < innerHeight) || refresh) {
          fetch();
        }

      }
      
      // Call the server for more acitivities
      function fetch() {
        fetching = true;
        refresh = false;
  
        // conver url to Location object
        var a = document.createElement('a');
        a.href = url;
        
        // decide whether to use '?' or '&'
        if(a.search.length > 0){
          a.href = a.href + "&offset="+offset
        }
        else {
          a.href = a.href + "?offset="+offset
        }
  
        // Here we set the header X-Requested-With to XMLHttpRequest so the 
        // server knows it's an AJAX call
        d3.json(a.href)
          .header("X-Requested-With", "XMLHttpRequest")
          .get(display);
      }
      
      // The meat and potatoes, this function get called after we've made the 
      // call to the server
      function display(error, new_data) {
        
        activities = new_data.activities || new_data.data || new_data.candidaturas;
  
        // we're obviously no longer fetching
        fetching = false;
  
        // if the server returned an empty list, return and get rid of loading
        // div
        if (!activities.length) {
          if(offset == 0){
            d3.select(container_el).selectAll("p.no_data")
              .data(['No items here'])
              .enter().append("p")
              .attr("class", "no_data")
              .text(String)
            if(remove){
              d3.select(container_el).html('')
            }
          }
          offset = NaN;
          d3.select(".infinite_loading").remove();
          return;
        }
  
        // increment offset by number of items received from server
        offset += activities.length;
  
        // using d3's helpful enter/update/exit paradigm add new items from
        // the server
        format_items(container_el, activities, offset)
        
        // remove no data p
        d3.select(container_el).selectAll("p.no_data").remove()
  
        // maybe the user has a super dooper tall screen (or high resolution)
        // so we need to check if we're already at the bottem, even though we
        // just added new items
        setTimeout(maybe_fetch, 50);
        
      }
      
      // call this on page load
      maybe_fetch();
      
    })
  }
  
  scroll.url = function(value) {
    if(!arguments.length) return url;
    if(value.split("?")[0] != url.split("?")[0]){
      refresh = true;
    }
    url = value;
    return scroll;
  }
  
  scroll.format_items = function(value) {
    if(!arguments.length) return format_items;
    format_items = value;
    return scroll;
  }
  
  scroll.remove = function(value) {
    if(!arguments.length) return remove;
    remove = value;
    return scroll;
  }
  
  scroll.offset = function(value) {
    if(!arguments.length) return offset;
    offset = value;
    return scroll;
  }
  
  return scroll
  
}
