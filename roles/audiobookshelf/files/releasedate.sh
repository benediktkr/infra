#!/bin/bash

set -e

orig_file="$1"
release_date="$2"

if [[ "$orig_file" == "" ]]; then
    echo "missing parameter"
    exit 1
fi

if [[ "$release_date" == "" ]]; then
    echo "missing parameter"
    exit 1
fi

if [[ "$3" == "" ]]; then
    prefix=""
else
    prefix="${3}-"
fi

orig_name=$(basename "$1")
orig_dir=$(dirname "$1")
cover_path="${orig_dir}/cover.jpg"

ffmpeg_file="ffmpeg-${prefix}${orig_name}"
eyed3_file="eyeD3-${prefix}${orig_name}"
abs_podcast_dir="/deadspace/audiobookshelf/podcasts/00-test-metadata"

rm "${ffmpeg_file}" &> /dev/null || true
rm "no-date-tag-${ffmpeg_file}" &> /dev/null || true
rm "releasedate-${ffmpeg_file}" &> /dev/null || true
rm "release_date-${ffmpeg_file}" &> /dev/null || true
rm "${eyed3_file}" &> /dev/null || true

rm -vf "${abs_podcast_dir}/${ffmpeg_file}"
rm -vf "${abs_podcast_dir}/${eyed3_file}"
rm -vf "${abs_podcast_dir}/metadata.abs"
rm -vf "${abs_podcast_dir}/cover.jpg"
ls -l "${abs_podcast_dir}/"

cp "${orig_file}" "${eyed3_file}"


echo
set -x
eyeD3 --add-image "${cover_path}:FRONT_COVER" --release-date "${release_date}" "${eyed3_file}" > /dev/null

#ffmpeg -i "${orig_file}" -c copy -metadata date="${release_date}" -metadata releasedate="${release_date}" "${ffmpeg_file}" &> /dev/null
ffmpeg -i "${orig_file}" -c copy -metadata date="${release_date}" "${ffmpeg_file}" &> /dev/null
#ffmpeg -i "${orig_file}" -c copy -metadata releasedate="${release_date}" "releasedate-${ffmpeg_file}" &> /dev/null
#ffmpeg -i "${orig_file}" -c copy -metadata release_date="${release_date}" "release_date-${ffmpeg_file}" &> /dev/null
set +x

echo
echo "--------"
echo

echo "file: ${orig_name}"
echo "original as downloaded by abs"

echo
echo "> ffprobe ${orig_file}"
ffprobe "${orig_file}" 2>&1 | grep date
echo
echo "> eyeD3 ${orig_file}"
eyeD3 "${orig_file}" 2>&1 | grep date
echo


echo
echo "--------"
echo

echo "file: ${eyed3_file}"
echo "eyeD3 with '--release-date ${release_date}'"

echo
echo "> ffprobe ${eyed3_file}"
ffprobe "${eyed3_file}" 2>&1 | egrep "image|date|COVER"
echo
echo "> eyeD3 ${eyed3_file}"
eyeD3 "${eyed3_file}" 2>&1 | egrep "image|date|COVER"
echo

echo
echo "--------"
echo

echo "file: ${ffmpeg_file}"
#echo "ffmpeg with ONLY 'date=${release_date}'"
echo "ffmpeg with BOTH 'date=${release_date}' and 'releasedate=${release_date}' set to ISO date strings"

echo
echo "> ffprobe ${ffmpeg_file}"
ffprobe "${ffmpeg_file}" 2>&1 | grep date
echo
echo "> eyeD3 ${ffmpeg_file}"
eyeD3 "${ffmpeg_file}" 2>&1 | grep date
echo

echo
echo "--------"
echo


# echo
# echo "--------"
# echo
# echo "file: releasedate-${ffmpeg_file}"
# echo "ffmpeg with ONLY 'releasedate=${release_date}'"

# echo
# echo "> ffprobe releasedate-${ffmpeg_file}"
# ffprobe "releasedate-${ffmpeg_file}" 2>&1 | grep date
# echo
# echo "> eyeD3 releasedate-${ffmpeg_file}"
# eyeD3 "releasedate-${ffmpeg_file}" 2>&1 | grep date
# echo

# echo
# echo "--------"
# echo

# echo "file: release_date-${ffmpeg_file}"
# echo "ffmpeg with ONLY 'release_date=${release_date}'"

# echo
# echo "> ffprobe release_date-${ffmpeg_file}"
# ffprobe "release_date-${ffmpeg_file}" 2>&1 | grep date
# echo
# echo "> eyeD3 release_date-${ffmpeg_file}"
# eyeD3 "release_date-${ffmpeg_file}" 2>&1 | grep date
# echo



chgrp media "${eyed3_file}"
chgrp media "${ffmpeg_file}"

# chgrp media "releasedate-${ffmpeg_file}"
# chgrp media "release_date-${ffmpeg_file}"



set -x
mv "${eyed3_file}" "${abs_podcast_dir}/"
mv "${ffmpeg_file}" "${abs_podcast_dir}/"

#mv "releasedate-${ffmpeg_file}" "${abs_podcast_dir}/"
#mv "release_date-${ffmpeg_file}" "${abs_podcast_dir}/"
set +x

echo
echo "> ls '${abs_podcast_dir}/'"
ls -1 "${abs_podcast_dir}/"
echo
echo
echo "done"


# curl -si 'https://audio.sudo.is/api/rescan' -X PUT \
#      -H 'Accept: application/json, text/plain, */*' \
#      -H 'Cookie: authelia_session=W^lyficYWGLOKCevu9qzsTsrFF4i!hA0' \
#      -H 'Content-Length: 0' \
#      -H 'TE: trailers' | head -n 1
