#!/usr/bin/env phantomjs
// Get the command line arguments and init everything
var page = require('webpage').create(),
    system = require('system'),
    url,
    viewportWidth,
    viewportHeight;
if(system.args.length < 3){
    console.log('Usage: ' + system.args[0] + ' <URL> <Viewport width in px> <optional viewport height>');
    phantom.exit()
}
url = system.args[1];
viewportWidth = system.args[2];
viewportHeight = viewportWidth;
if(system.args.length > 3){
    viewportHeight = system.args[3];
}

// Set the page's viewport
page.viewportSize = {width: viewportWidth, height: viewportHeight};
page.onError = function (msg, trace) {console.log("ERROR:"+msg);}

// Open the URL
page.open(url, function(status){
    // Return an array of "imgURL width height" strings
    var imageDimensions = page.evaluate(function(){
        var images = document.querySelectorAll('img');
        var ret=[];
        for(var i = 0; i < images.length; i++){
            var img = images[i];
            ret[i] = img.src + " " + img.clientWidth + " " + img.clientHeight;
        }
        return ret;
    });
    // Print the dimensions to the console
    imageDimensions && imageDimensions.forEach(function(val){console.log(val)});

    phantom.exit(0);
});
