# What is the cost of your non-responsive images?

We've been talking about responsive images for years now, but what is
the actual cost of delivering non-responsive images to narrow viewports?
How many bytes are we sending for nothing?

(@grigs)[https://github.com/grigs] wrote a [blog post](http://blog.cloudfour.com/sensible-jumps-in-responsive-image-file-sizes) on responsive images breakpoints and their
relation to a site's performance budget, which got me thinking: "We cannot manage a budget if we cannot measure costs".

So, I wrote this small script that measures a certain site in multiple
viewports and outputs the bytes we can optimize losslessly and the bytes
we can optimize if we'd tailor the images to this specific viewport.

## Usage

`./sizer <URL>`

# Results

Besides the summary results printed to screen, you can see detailed
per-image results in your `/tmp/` directory. Each tested site creates a
directory there, and the original, optimized and resized images are
stored there, as well as result logs per viewport.

## Dependencies

* image_optim
* ImageMagick
* curl
* PhantomJS

## How it works

* `run.sh` simply iterates over 2 other scripts with several viewport
  sizes. Adding more viewports is simple, but it slows down the
running time.
* `getImageDimensions.js` is a phantomjs script that downloads the
  requested URL, and outputs all of its content images as well as their
dimensions.
* `getResizedBenefits.sh` is a bash script that gets the results of
  `getImageDimensions.js`, downloads the original images and resizes
these images to see what their resized size is. It also optimizes the
original images using image_optim, to see how much lossless optimization
can get us.

## Why bash???

I was aiming to minimize dependencies, so I went with bash. 

## What's with the name????

It's Saturday.
