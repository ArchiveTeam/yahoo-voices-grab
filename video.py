'''Get video URLs.

I take in IDs such as ``how-better-housekeeper-12537238``
'''
import json
import re
import sys
import urllib
import urllib2
import string


HTML_PAGE = 'http://voices.yahoo.com/video/{0}.html'
YQL = 'SELECT * FROM yahoo.media.video.streams WHERE id="{video_id}" AND format="mp4,flv,f4m" AND protocol="http" AND rt="flash" AND plrs="Gi_RxaWhgXECOj6ukNwZbO" AND acctid="{user_id}" AND plidl="{context}" AND pspid="{pagespace}" AND offnetwork="false" AND site="" AND lang="en-US" AND region="US" AND override="none" AND plist="" AND hlspre="false" AND ssl="false" AND synd="";'
YQL_URL = 'http://video.query.yahoo.com/v1/public/yql?q={0}&env=prod&format=json'


def main():
    video_id = sys.argv[1]
    response = urllib2.urlopen(HTML_PAGE.format(video_id))

    assert response.geturl() == HTML_PAGE.format(video_id)

    data = response.read()
    match = re.search(r"VideoPlayer\(({.+?})\);", data)
    snippet = match.group(1)
    snippet = snippet.replace('/* REQUIRED CONFIG ITEMS */', '')
    snippet = snippet.replace('/* OPTIONAL CONFIG ITEMS */', '')

    def rep(match):
        name = match.group(1)
        if name not in ('http', 'https') and name[0] in string.ascii_lowercase or name == 'YVAP':
            return '"{0}":'.format(name)
        else:
            return '{0}:'.format(name)

    snippet = re.sub('([a-zA-Z0-9]+) ?:', rep, snippet)

    doc = json.loads(snippet)

    if 'streamUrl' in doc['playlist']['mediaItems'][0]:
        print(doc['playlist']['mediaItems'][0]['streamUrl'])

        return

    video_id = doc['playlist']['mediaItems'][0]['id']
    pagespace = doc['pageSpaceId']
    context = doc['YVAP']['playContext']
    user_id = doc['YVAP']['accountId']

    yql = YQL.format(video_id=video_id, pagespace=pagespace, context=context, user_id=user_id)
    json_url = YQL_URL.format(urllib.quote(yql))

    print(json_url)

    response = urllib2.urlopen(json_url)

    doc = json.loads(response.read())

#     print(json.dumps(doc, indent=2))

    streams = doc['query']['results']['mediaObj'][0]['streams']
    streams = list(sorted(streams, key=lambda x: x['bitrate']))
    stream = streams[-1]
    stream_url = stream['host'] + stream['path']

    print(stream_url)


if __name__ == '__main__':
    main()
