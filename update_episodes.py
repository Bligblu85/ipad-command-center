#!/usr/bin/env python3
"""Fetch the most recent Come And Talk 2 Me YouTube uploads via public RSS."""
import json,urllib.request,xml.etree.ElementTree as ET,datetime,pathlib
CHANNEL='UCIDbIn1BZAQg74rj_IlgwhA'
URL='https://www.youtube.com/feeds/videos.xml?channel_id='+CHANNEL
req=urllib.request.Request(URL,headers={'User-Agent':'Mozilla/5.0 (compatible; CommandCenterFeed/1.0)'})
with urllib.request.urlopen(req,timeout=25) as resp: xml=resp.read()
root=ET.fromstring(xml)
ns={'atom':'http://www.w3.org/2005/Atom','yt':'http://www.youtube.com/xml/schemas/2015'}
items=[]
for e in root.findall('atom:entry',ns):
 video=e.findtext('yt:videoId',namespaces=ns)
 if video and len(video)==11:
  items.append({'id':video,'title':e.findtext('atom:title',default='Episode',namespaces=ns),'published':e.findtext('atom:published',default='',namespaces=ns)})
if not items:raise RuntimeError('YouTube RSS returned no videos; keeping previous episode feed')
out={'updated':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC'),'episodes':items[:15]}
pathlib.Path('episodes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print('Saved',len(out['episodes']),'recent uploads')
