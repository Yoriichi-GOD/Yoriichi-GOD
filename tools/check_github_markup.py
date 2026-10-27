"""Ask GitHub's anonymous Markdown API to render only the finished public-safe
README. This is a stateless rendering request, not a repository write or publish.
"""
import hashlib, json, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
payload=json.dumps({'text':(ROOT/'README.md').read_text(encoding='utf-8'),'mode':'gfm'}).encode()
req=urllib.request.Request('https://api.github.com/markdown',data=payload,headers={'User-Agent':'EngineeringArchive-markup-review','Content-Type':'application/json','Accept':'application/vnd.github+json'},method='POST')
with urllib.request.urlopen(req,timeout=40) as r:
    html=r.read().decode()
    (ROOT/'.review/github-rendered.html').write_text(html,encoding='utf-8')
    (ROOT/'.review/github-markup-meta.json').write_text(json.dumps({'readme_sha256':hashlib.sha256((ROOT/'README.md').read_bytes()).hexdigest(),'status':r.status,'date':'2026-10-27','pictures':html.count('<picture>'),'sources':html.count('<source')}))
    print(json.dumps(dict(status=r.status,bytes=len(html),pictures=html.count('<picture>'),sources=html.count('<source'),has_scripts='<script' in html,scope='GitHub Markdown API only; no repository write')))
