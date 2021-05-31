#!/usr/bin/python3

import requests
import json
import subprocess

from bottle import route, run, template, redirect, response


nginx_conf = """
location ~* ^\/_sensorsnapshot {
  proxy_pass {snapshot_url};
  #proxy_redirect  proxypass / dir / /;
  proxy_set_header Host $host;
  proxy_set_header X-Real-IP $remote_addr;
  proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
}
"""
headers = {
    "Authorization": "Bearer {{ sensor_snapshot_api_token }}",
    "Accept": "application/json",
    "Content-Type": "application/json"
}

url = "https://{{ grafana_url }}/api"

query = {
    'q': """SELECT mean("value") FROM "{{ sensor_snapshot_ds }}"."temp" WHERE ("source" = 'sensor') AND time >= now() - {{ sensor_snapshot_time }} GROUP BY time(30s), "name" fill(none)""",
    'db': "{{ sensor_snapshot_db }}",
    'epoch': "ms"
}

# query for the data to make a snapshot out of
r = requests.get(url + "/datasources/proxy/3/query", params=query, headers=headers)
r.raise_for_status()

series = r.json()['results'][0]['series']

# needs to be conveted to a different format
snapshot_data = list()
for item in series:
    times = [a[0] for a in item['values']]
    values  = [a[1] for a in item['values']]
    val_foo = item['columns'][1]

    d = {'fields': [{'config': {},
                     'name': 'Time',
                     'type': 'time',
                     'values': times },
                    {'config': {},
                     'name': 'Value',
                     'type': 'number',
                     'values': values }],
         'meta': {'executedQueryString': query['q'] },
         'name': item['tags']['name'],
         'refid': 'A' }
    snapshot_data.append(d)

# make the dashaboard model, and include snapshot_data

# copy json from grafana web ui
# >>> j="""........"""
# >>> import json, pprint
# >>> pprint.pprint(json.loads(f))
dashboard ={'annotations': {'list': [{'builtIn': 1,
                           'datasource': '-- Grafana --',
                           'enable': True,
                           'hide': True,
                           'iconColor': 'rgba(0, 211, 255, 1)',
                           'name': 'Annotations & Alerts',
                           'type': 'dashboard'}]},
 'editable': False,
 'hideControls': True,
 'gnetId': None,
 'graphTooltip': 0,
 'id': 23,
 'links': [],
 'panels': [{'aliasColors': {'balcony s21': 'dark-blue',
                             'rain balcony s21': 'dark-blue'},
             'bars': False,
             'dashLength': 10,
             'dashes': False,
             'datasource': 'influxdb-sudoisbot',
             'fieldConfig': {'defaults': {'custom': {}}, 'overrides': []},
             'fill': 1,
             'fillGradient': 1,
             'gridPos': {'h': 37, 'w': 24, 'x': 0, 'y': 0},
             'hiddenSeries': False,
             'id': 2,
             'legend': {'avg': False,
                        'current': False,
                        'max': False,
                        'min': False,
                        'show': True,
                        'total': False,
                        'values': False},
             'lines': True,
             'linewidth': 1,
             'nullPointMode': 'null',
             'options': {'alertThreshold': True},
             'percentage': False,
             'pluginVersion': '7.4.0',
             'pointradius': 2,
             'points': False,
             'renderer': 'flot',
             'seriesOverrides': [{'alias': 'rain balcony s21',
                                  'fill': 0,
                                  'fillGradient': 4,
                                  'linewidth': 0,
                                  'yaxis': 2}],
             'snapshotData': snapshot_data,
             'spaceLength': 10,
             'stack': False,
             'steppedLine': False,
             'targets': [{'alias': '$tag_name',
                          'groupBy': [{'params': ['$__interval'],
                                       'type': 'time'},
                                      {'params': ['name'], 'type': 'tag'},
                                      {'params': ['none'], 'type': 'fill'}],
                          'measurement': 'temp',
                          'orderByTime': 'ASC',
                          'policy': 'sudoisbot-infinite',
                          'refId': 'A',
                          'resultFormat': 'time_series',
                          'select': [[{'params': ['value'], 'type': 'field'},
                                      {'params': [], 'type': 'mean'}]],
                          'tags': [{'key': 'name',
                                    'operator': '!=',
                                    'value': 'inside'},
                                   {'condition': 'AND',
                                    'key': 'name',
                                    'operator': '!=',
                                    'value': 'test'}]},
                         {'alias': 'rain $tag_name $tag_location',
                          'groupBy': [{'params': ['1m'], 'type': 'time'},
                                      {'params': ['location'], 'type': 'tag'},
                                      {'params': ['name'], 'type': 'tag'},
                                      {'params': ['none'], 'type': 'fill'}],
                          'hide': False,
                          'measurement': 'rain',
                          'orderByTime': 'ASC',
                          'policy': 'sudoisbot-infinite',
                          'refId': 'B',
                          'resultFormat': 'time_series',
                          'select': [[{'params': ['value'], 'type': 'field'},
                                      {'params': [], 'type': 'last'}]],
                          'tags': []}],
             'thresholds': [],
             'timeFrom': None,
             'timeRegions': [],
             'timeShift': None,
             'title': 'temps',
             'tooltip': {'shared': True, 'sort': 0, 'value_type': 'individual'},
             'transformations': [],
             'type': 'graph',
             'xaxis': {'buckets': None,
                       'mode': 'time',
                       'name': None,
                       'show': True,
                       'values': []},
             'yaxes': [{'decimals': 1,
                        'format': 'celsius',
                        'label': 'temperature',
                        'logBase': 1,
                        'max': None,
                        'min': None,
                        'show': True},
                       {'decimals': 0,
                        'format': 'none',
                        'label': 'rain detected',
                        'logBase': 1,
                        'max': '1',
                        'min': '0',
                        'show': False}],
             'yaxis': {'align': False, 'alignLevel': None}}],
 'schemaVersion': 27,
 'style': 'dark',
 'tags': [],
 'templating': {'list': []},
 'time': {'from': 'now-24h', 'to': 'now'},
 'timepicker': {},
 'timezone': '',
 'title': 'web-temps',
 'uid': 'KP60kGrMk',
 'version': 3}

snapshot_request = {
    "dashboard": dashboard,
    "expires": {{ sensor_snapshot_expires }},
}

s = requests.post(url + "/snapshots", headers=headers, json=snapshot_request)
s.raise_for_status()
j = s.json()
url = j['url']

#with open('/etc/nginx/conf.d/sensorsnapshot.conf', 'w') as f:
#    conf = nginx_conf.format(snapshot_url=url)
#    f.write(conf + "\n")
#
#subprocess.run(["service", "nginx", "reload"], check=True)
def hahawtfisthis():
    return url

# wget --mirror --convert-links --adjust-extension --page-requisites --no-parent  $url

#  location /s/ {
#    proxy_pass http://localhost:3000/dashboard/snapshot/yevjiGczJzHbfy406Scjn7d8oC80c5n6/;
#    proxy_set_header Host $host;
#    proxy_set_header X-Real-IP $remote_addr;
#    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
#  }

@route('<uri:path>')
def test(uri):
    #response.set_header("Access-Control-Allow-Origin", "*")
    if uri == "/":
        return requests.get(hahawtfisthis()).text

    else:
        full = "https://grafana.sudo.is" + uri
        redirect(full)
        # print(full)
        #return requests.get(full).text



run(host='10.102.47.131', port=8080, debug=True)
