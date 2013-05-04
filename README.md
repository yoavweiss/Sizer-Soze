# What is the cost of your non-responsive images?

We've been talking about responsive images for years now, but what is
the actual cost of delivering non-responsive images to narrow viewports?
How many bytes are we sending for nothing?

@grigs wrote a blog post on responsive images breakpoints and their
relation to a site's performance budget, which got me thinking: "We cannot manage a budget if we cannot measure costs".

So, I wrote this small script that measures a certain site in multiple
viewports and output the bytes we can optimize losslessly and the bytes
we can optimize if we'd tailor the images to this specific viewport.

## Usage

`./run.sh <URL>`

## Dependencies

* image_optim
* ImageMagick
* curl
* PhantomJS

## How it works

* `run.sh` simply iterates over 2 other scripts with several viewport
  sizes. Feel free to add more viewports, but it'll slow down the
running time
* `getImageDimensions.js` is a phantomjs script that downloads the
  requested URL, and outputs all of its content images as well as their
dimensions.
* `getResizedBenefits.sh` is a bash script that gets the results of
  `getImageDimensions.js`, downloads the original images and resizes
these images to see what their resized size is. It also optimizes the
original images using image_optim, to see how much lossless optimization
can get us.
