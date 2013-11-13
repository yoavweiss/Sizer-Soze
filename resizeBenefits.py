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

def getBenefits(results, dir, ignore_invisibles):
    benefits = []
    devnull = open(os.devnull, "wb")
    for result in results:
        (url, width, height) = analyzeResult(result)
        filedir, filename = resourceSlug(url, dir)
        try:
            buffer = open(filename, "rb").read()
        except IOError:
            continue
        ext = magic.from_buffer(buffer).split()[0].lower()
        # If it's not one of the known image formats, return!
        # Sorry WebP
        if (ext != "jpeg") and (ext != "png") and (ext != "gif"):
            continue
        optimized_file_name = filename + "_lslsopt" + ext
        lossy_optimized_file_name = filename + "_lossyopt" + ext
        resized_file_name = filename + "_" + width + "_" + height + ext
        # optimize the original image
        copyfile(filename, optimized_file_name)
        call(["image_optim", optimized_file_name], stdout=devnull, stderr=devnull)

        # Lossy optimize the original image
        call(["convert", optimized_file_name, "-quality", "85", lossy_optimized_file_name])
        #call(["image_optim", lossy_optimized_file_name], stdout=devnull, stderr=devnull)

        # Resize the original image
        call(["convert", optimized_file_name, "-geometry", width+"x"+height, "-quality", "85", resized_file_name])
        #call(["image_optim", resized_file_name], stdout=devnull, stderr=devnull)

        # Get the original image's dimensions
        original_dimensions = check_output("identify -format \"%w,%h\" " + filename + "|sed 's/,/x/'", shell = True).strip()

        original_size = fileSize(filename)
        optimized_size = fileSize(optimized_file_name)
        lossy_optimized_size = fileSize(lossy_optimized_file_name)
        resized_size = fileSize(resized_file_name)

        # If resizing made the image larger, ignore it
        if resized_size > optimized_size:
            resized_size = optimized_size

        # if the image is not displayed, consider all its data as a waste
        if width == "0":
            resized_size = 0
            if ignore_invisibles:
                continue

        benefits.append([   filename,
                            original_size,
                            original_size - optimized_size,
                            original_size - lossy_optimized_size,
                            original_dimensions + "=>" + width + "x" + height,
                            original_size - resized_size])
    devnull.close()
    return benefits



