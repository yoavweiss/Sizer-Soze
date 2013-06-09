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

var getImageDimensions = function(){
    return page.evaluate(function(){
        var images = document.querySelectorAll('img');
        var ret={};
        for(var i = 0; i < images.length; i++){
            var img = images[i];
            ret[img.src] = [img.clientWidth , img.clientHeight];
        }
        return ret;
    });
};
// Open the URL
page.open(url, function(status){
    var counter = 0;
    var finalDimensions={};
    setInterval(function(){
        // Return an array of "imgURL width height" strings
        var imageDimensions = getImageDimensions();
        var noneSet = true;
        Object.keys(imageDimensions).forEach(function(key){
            if(!finalDimensions[key] || finalDimensions[key][0] == 0){
                finalDimensions[key] = imageDimensions[key];
                noneSet = false;
            }
        });
        counter++;
        if(counter >= 50 || noneSet){
            // Print the dimensions to the console
            Object.keys(finalDimensions).forEach(function(val){console.log(val + " " + finalDimensions[val][0] + " " + finalDimensions[val][1])});
            phantom.exit(0);
        }
    }, 500);
});
