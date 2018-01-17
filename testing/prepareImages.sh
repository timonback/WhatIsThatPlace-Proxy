#!/bin/bash

sourceDir="./src"
destDir="./preprocessed"

# The Google Vision API only handles files up to 4MB
IMoptions=" -define jpeg:extent=4000kb "

images="$sourceDir/*"
for image in $images
do
  filename="${image##*/}"
  echo "Prepare $image..."
  preprocessed="$destDir/$filename"
  convert "$image" $IMoptions -strip "$preprocessed"
  
  # resize
  convert "$preprocessed" $IMoptions -resize "1920x" "$preprocessed.1920.jpg"
  convert "$preprocessed" $IMoptions -resize "1024x" "$preprocessed.1024.jpg"
  convert "$preprocessed" $IMoptions -resize "600x" "$preprocessed.600.jpg"
  convert "$preprocessed" $IMoptions -resize "100x" "$preprocessed.100.jpg"
  
  # distort
  # https://www.imagemagick.org/Usage/distorts/#barrel
  convert "$preprocessed" $IMoptions -distort barrel "0.0 0.0 0.2 1.0" -gravity Center -crop 75%\! "$preprocessed.distortout.jpg"
  convert "$preprocessed" $IMoptions -distort barrel "0.0 0.0 -0.2 1.3" -gravity Center -crop 80%\! "$preprocessed.distortin.jpg"
  
  # exposure
  convert "$preprocessed" $IMoptions -level 0%x75 "$preprocessed.exposureOver.jpg"
  convert "$preprocessed" $IMoptions +level 0%x75 "$preprocessed.exposureUnder.jpg"
  
  # cut-out
  convert "$preprocessed" $IMoptions -gravity Center -crop 50%\! "$preprocessed.cutout50.jpg"
  
  # blur
  convert "$preprocessed" $IMoptions -blur "0x8" "$preprocessed.blur0x8.jpg"
  convert "$preprocessed" $IMoptions -blur "2x2" "$preprocessed.blur2x2.jpg"
  
  # sharpen
  convert "$preprocessed" $IMoptions -sharpen "0x1" "$preprocessed.sharpen0x1.jpg"
  convert "$preprocessed" $IMoptions -sharpen "0x3" "$preprocessed.sharpen0x3.jpg"
  
  # grayscale
  convert "$preprocessed" $IMoptions -set colorspace Gray -separate -average "$preprocessed.gray.jpg"
done

echo "Done"
