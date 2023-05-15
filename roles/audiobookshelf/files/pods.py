#!/usr/bin/env python3

import urllib.parse
import requests
import json
import sys
import os

import dateutil.parser
from loguru import logger

abs = "https://url"
authheaders = {
 "Authorization": "Bearer $token"}

try:
  OUTPUT_DIR = sys.argv[1]
except IndexError:
  OUTPUT_DIR = "/tmp/abs_metadata"

logger.info(f"saving metadata json files to '{OUTPUT_DIR}'")

s = requests.Session()
s.headers.update(authheaders)

# idea: what is /s/? socket? tracks progress?
# check with browser dev tools
# could add nginx conf/proxy to inject auth header
# or something if i get progress tracking for free
# or custom proxy
#
# rss feed needs to be open for /feed/ urls to
# work. rss feed can be opened with api
#
# find if episode has been played
# https://api.audiobookshelf.org/#items-listened-to
#
# check with browser dev tools what happens when
# the button is clicked to mark an episode as played
# ANSWER:
# curl \
#   'https://{url}/api/me/progress/li_eadrvpei17yz1unifv/ep_8zz0zme6qtzq9rio8y' \
#   -X PATCH \
#   -H 'Authorization: Bearer $token' \
#   -H 'Accept: application/json, text/plain, */*' \
#   -H 'Accept-Language: en-US,en;q=0.5' \
#   -H 'Accept-Encoding: gzip, deflate, br' \
#   -H 'Content-Type: application/json' \
#   -H 'Referer: https://{url}/item/li_eadrvpei17yz1unifv' \
#   -H 'Origin: https://{url}' \
#   -H 'DNT: 1' \
#   -H 'Sec-Fetch-Dest: empty' \
#   -H 'Sec-Fetch-Mode: cors' \
#   -H 'Sec-Fetch-Site: same-origin' \
#   -H 'Sec-GPC: 1' \
#   -H 'Connection: keep-alive' \
#   -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' \
#   -H 'TE: trailers' \
#   --data-raw '{"isFinished":true}'
#
# $ curl -sX GET 'https://{url}/api/me/progress/li_eadrvpei17yz1unifv/ep_8zz0zme6qtzq9rio8y' -H 'Authorization: Bearer ${token}' | jq .
# {
#   "duration": 0,
#   "progress": 1,
#   "currentTime": 0,
#   "isFinished": true,
#   "hideFromContinueListening": false,
#   "finishedAt": 1679184864387
# }
# ^ removed less interested fields in the response
#
# listening sessions can be streamed?
#
# use hass to remove from playlist when playback
# is finished?

def playlist():

  playlists = s.get(f"{abs}/api/playlists").json()["playlists"]

  for playlist in playlists:
    for episode in playlist["items"]:
      li_id = episode["libraryItemId"]
      ep_id = episode["episodeId"]
      file_name = episode["episode"]["audioTrack"]["metadata"]["filename"]
      encoded_file_name = urllib.parse.quote_plus(file_name)
      file_url = f"{abs}/feed/{li_id}/item/{ep_id}/{encoded_file_name}"

      print(file_url)

def item_embed_metadata(li_id):

  embed_url = f"{abs}/api/tools/item/{li_id}/embed-metadata"
  logger.info(embed_url)
  try:
    r = s.post(embed_url, data={"forceEmbedChapters": False})
    r.raise_for_status()
    return r.json()
  except requests.exceptions.HTTPError as e:
    logger.error(e)
    logger.error(r.text)
    return None


def metadata_main():
  r = s.get(f"{abs}/api/libraries")
  j = r.json()
  podcasts = [a for a in j['libraries'] if a['mediaType'] == "podcast"]
  logger.info(f"podcast libraries: {len(podcasts)}")
  for item in podcasts:
    metadata_library(podcasts)


def metadata_library(podcasts):
  for item in podcasts:
    r = s.get(f"{abs}/api/libraries/{item['id']}/items")
    j = r.json()
    lib_items = j['results']
    metadata_library_item(lib_items)


def metadata_library_item(lib_items):
  logger.info(f"podcasts: {len(lib_items)}")

  for item in lib_items:
    name = item['relPath']
    li_id = item['id']

    #episodes = item['media']['episodes']
    #for episode in episodes:
    #  episode_id = episode['id']
    #  #lib_item = s.get(f"{abs}/api/items/{episode_id}").json()
    #  #logger.info(f"{name}: {lib_item}")
    #  #metadata = item_embed_metadata(episode_id)

    lib_item = s.get(f"{abs}/api/items/{li_id}").json()

    item_name = lib_item['media']['metadata']['title']
    item_id = lib_item['id']

    media = lib_item['media']
    metadata = lib_item['media']['metadata']
    podcast_path = lib_item['path']
    podcast_rel_path = lib_item['relPath']

    save_dir = f"{OUTPUT_DIR}/{podcast_rel_path}"
    logger.info(f"{name} ({item_id}): {save_dir} ")
    os.makedirs(save_dir, exist_ok=True)

    podcast = {
      'podcast_name': item_name,
      'podcast_metadata': metadata,
      'feed_url': metadata['feedUrl'],
      'itunes_id': metadata['itunesId'],
      'path': podcast_path,
      'rel_path': podcast_rel_path,
      'abs_ids': {
        'library_id': lib_item['libraryId'],
        'item_id': item_id,
        'folder_id': lib_item['folderId'],
      }
    }

    episodes = []
    logger.info(f"latest epsiode: {media['episodes'][0]['title']}")
    for ep in media['episodes']:
      ep_file = ep['audioFile']
      ep_metadata = ep_file['metadata']
      ep_filename = ep_metadata['filename']
      ep_path = ep_metadata['path']
      ep_rel_path = f"{podcast_rel_path}/{ep_filename}"

      published_date = dateutil.parser.parse(ep['pubDate']).isoformat()
      published_date_ts = ep['publishedAt']
      episode = {
        'library_item_id': ep['libraryItemId'],
        'id': ep['id'],
        'path': ep_path,
        'rel_path': ep_rel_path,
        'index': ep.get('index'),
        'title': ep['title'],
        'subtitle': ep.get('subititle'),
        'description': ep.get('description'),
        'published_date': published_date,
        'publised_date_ts': published_date_ts,
        'filename': ep_metadata['filename'],
        'ext': ep_metadata['ext'],
        'mtime_ms': int(ep_metadata['mtimeMs']),
        'ctime_ms': int(ep_metadata['ctimeMs']),
        'birthtime_ms': int(ep_metadata['birthtimeMs']),
        'added_at': int(ep_file['addedAt']),
        'updated_at': int(ep_file['updatedAt']),
        'duration': ep_file['duration'],
      }
      episodes.append(episode)
      with open(f'{save_dir}/{ep_filename}.json', 'w') as f:
        f.write(json.dumps(episode, indent=4))


    with open(f'{save_dir}/metadata_podcast.json', 'w') as f:
      f.write(json.dumps(podcast, indent=4))

    full_metadata = podcast.copy()
    full_metadata['episodes'] = episodes.copy()

    with open(f'{save_dir}/metadata.json', 'w') as f:
      f.write(json.dumps(full_metadata, indent=4))



def metadata_embed(item_id):
  r =  s.post(f"{abs}/api/tools/item/{tem_id}/embed-metadata")
  print(r.text)
  print(r.status_code)

if __name__ == "__main__":
  metadata_main()


