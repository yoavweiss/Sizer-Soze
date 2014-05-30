# How much image-data are you sending your users for nothing?

We've been talking about responsive images for years now, but what is
the actual cost of delivering non-responsive images to narrow viewports?
How many bytes are wasted on the wire(less)?

This tool evaluates the savings by resizing images to various viewports,
with the goal of fitting images into a "performance budget".

## Usage

`./sizer.py <URL>`
`./bulkSizer <Text file with URLs>`

# Results

Besides the summary results printed to screen, you can see detailed
per-image results in your `/tmp/` directory. A directory will be created 
there for each site. The original, optimized, and resized images are
stored there - as well as result logs per viewport.

## Dependencies

* [Python](http://www.python.org/)
* [PhantomJS](http://phantomjs.org/)
* [image_optim](https://github.com/toy/image_optim) (A CLI version of
  [ImageOptim](https://github.com/pornel/ImageOptim))
* [ImageMagick](http://www.imagemagick.org/script/index.php)
* [python-slugify](https://github.com/un33k/python-slugify)
* [python-magic](https://github.com/ahupp/python-magic)

## How to install

* Ubuntu/Debian run `ubuntu_install.sh`. 
* OSX run `osx_install.sh`.
* Other-linux install the dependencies projects and you should be good to go.
* If you're on Windows, Install Ubuntu :P

## How it works

* `getImageDimensions.js` is a phantomjs script that downloads the
  requested URL, and outputs all of its content images as well as their
dimensions.
* `downloadr.py` downloads the image resources.
* `resizeBenefits.py` gets the results of
  `getImageDimensions.js`, and resizes
the images to see what their resized size is. It also optimizes the
original images using image_optim, to see how much lossless optimization
can get us.
* `sizer.py` iterates over the other scripts with several viewport
  sizes. Adding more viewports is simple, but it slows down the
running time.

## What's with the name????

It's Saturday.
