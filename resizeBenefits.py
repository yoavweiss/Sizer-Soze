from downloadr import resourceSlug
from subprocess import call, check_output
import magic
import os
from shutil import copyfile

def analyzeResult(result):
        arr = result.split()
        url = arr[0]
        width = arr[1]
        height = arr[2]
        return (url, width, height)

def fileSize(name):
    return int(os.stat(name).st_size)

def getBenefits(results, dir):
    benefits = []
    devnull = open(os.devnull, "wb")
    for result in results:
        (url, width, height) = analyzeResult(result)
        filename = resourceSlug(url, dir)
        try:
            buffer = open(filename, "rb").read()
        except IOError:
            continue
        ext = magic.from_buffer(buffer).split()[0].lower()
        # If it's not one of the known image formats, return!
        # Sorry WebP
        if (ext != "jpeg") and (ext != "png") and (ext != "gif"):
            continue
        optimized_file_name = filename + "_opt"
        resized_file_name = filename + "_" + width + "_" + height
        # optimize the original image
        copyfile(filename, optimized_file_name)
        call(["image_optim", optimized_file_name], stdout=devnull, stderr=devnull)

        # Resize the original image
        call(["convert", filename, "-geometry", width+"x"+height, resized_file_name])
        call(["image_optim", resized_file_name], stdout=devnull, stderr=devnull)

        # Get the original image's dimensions
        original_dimensions = check_output("identify -format \"%w,%h\" " + filename + "|sed 's/,/x/'", shell = True).strip()

        original_size = fileSize(filename)
        optimized_size = fileSize(optimized_file_name)
        resized_size = fileSize(resized_file_name)

        # If resizing made the image larger, ignore it
        if resized_size > optimized_size:
            resized_size = optimized_size

        # if the image is not displayed, consider all its data as a waste
        if width == 0:
            resized_size = 0

        benefits.append([   filename, 
                            original_size, 
                            original_size-optimized_size, 
                            original_dimensions+"=>"+width+"x"+height,
                            original_size-resized_size])
    devnull.close()
    return benefits



