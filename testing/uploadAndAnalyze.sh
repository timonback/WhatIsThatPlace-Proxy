#!/bin/bash

sourceDir="./preprocessed"
destDir="./dest"

server="http://vision.timonback.de:8888"
server_image="$server/image"

images="$sourceDir/*"
for image in $images
do
  filename="${image##*/}"
  
  md5=$(md5sum $image | awk '{print $1}')
  echo -ne "About to upload image $filename with id $md5...   "
  
  response=$(curl -X HEAD --silent --write-out %{http_code} --output /dev/null -H "Authorization: 988c4dcf-d7d2-45f1-b4ec-9123a0ab61d1" "$server_image/$md5")
  if [ "$response" != "200" ];
  then
    echo -ne "uploading...   "
    curl -X POST --silent -F "image=@$image" -H "Authorization: 988c4dcf-d7d2-45f1-b4ec-9123a0ab61d1" $server_image
    echo -e "done"
	
	cp $image "$destDir/$filename"
	echo "$md5" > "$destDir/$filename.txt"
  else
    echo -e "using cached version"
  fi
  
  echo -ne "Start to analyze $md5...   "
  response=$(curl -X GET --silent -H "Authorization: 988c4dcf-d7d2-45f1-b4ec-9123a0ab61d1" "$server_image/$md5/landmark")
  echo "$response"
  echo "$response" > "$destDir/$filename.json"
  
done
