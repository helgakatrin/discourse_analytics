
  $.ajax({
      url : "/api/post/", // the endpoint
      type : "GET", // http method
      dataType: 'json',
      // handle a successful response
      success : function(json) {
          var defaults = {
          }        
          //$('#post-text').val(''); // remove the value from the input
          console.log(json); // log the returned json to the console
          console.log("success"); // another sanity check
          var visualization = d3plus.viz()            
            .container("#viz")     // container DIV to hold the visualization
            .data(json.result)     // data to use with the visualization            
            .id(["group", "word"]) // nesting keys
            .depth(1)              // 0-based depth            
            .size("frequency")         // key name to size bubbles
            .color("word")        // color by each group
            .config(defaults)
            .draw()                // finally, draw the visualization!
               
      },

      // handle a non-successful response
      error : function(xhr,errmsg,err) {
          console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
  });

  /*
  var sample_data = [
    {"value": 100, "name": "alpha", "group": "group 1"},
    {"value": 70, "name": "beta", "group": "group 2"},
    {"value": 40, "name": "gamma", "group": "group 2"},
    {"value": 15, "name": "delta", "group": "group 2"},
    {"value": 5, "name": "epsilon", "group": "group 1"},
    {"value": 1, "name": "zeta", "group": "group 1"}
  ]
  */
