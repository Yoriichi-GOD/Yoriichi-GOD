"""Anonymous GET audit of README links and SVG/Markdown local references.

No sign-in, provider inference, submissions, mutations or product tests.
"""
from pathlib import Path
import concurrent.futures, hashlib, json, re, urllib.request, urllib.error, xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
README=(ROOT/'README.md').read_text(encoding='utf-8')

def check(url):
    try:
        req=urllib.request.Request(url,headers={'User-Agent':'EngineeringArchive-public-link-review/1.0'})
        with urllib.request.urlopen(req,timeout=25) as r:
            body=r.read(300000).decode('utf-8',errors='replace')
            title=re.search(r'<title[^>]*>(.*?)</title>',body,re.S|re.I)
            return dict(url=url,status=r.status,final=r.url,title=re.sub(r'\s+',' ',title.group(1)).strip() if title else None,bytes_checked=len(body),scope='anonymous HTTP reachability only')
    except urllib.error.HTTPError as e:return dict(url=url,status=e.code,error=str(e))
    except Exception as e:return dict(url=url,status=None,error=str(e))

if __name__=='__main__':
    urls=sorted(set(re.findall(r'\]\((https://[^)]+)\)',README)))
    # Extra candidate product websites are investigated, never silently promoted.
    candidates=['https://warscythe.com','https://warscythe.in','https://peekolitix.in','https://peekolitix.vercel.app','https://api.github.com/repos/Yoriichi-GOD/Yoriichi-GOD']
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:external=list(pool.map(check,urls+candidates))
    local=[]
    for ref in sorted(set(re.findall(r'(?:src|srcset)="([^"]+)"',README)+re.findall(r'\]\((?!https?:|#)([^)]+)\)',README))):
        p=ROOT/ref.split('#')[0];local.append(dict(path=ref,exists=p.is_file()))
    svgs=[]
    for p in sorted((ROOT/'assets').rglob('*.svg')):
        data=p.read_bytes();tree=ET.fromstring(data);bad=[]
        for node in tree.iter():
            tag=node.tag.split('}')[-1]
            if tag in ['script','foreignObject','style','text','animate','set']:bad.append(tag)
            for k,v in node.attrib.items():
                if (k.endswith('href') and not v.startswith(('data:','#'))) or k.startswith('on'):bad.append(k)
        svgs.append(dict(path=str(p.relative_to(ROOT)),bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),unsafe_or_font_dependent=bad))
    result=dict(date='2026-10-27',external=external,local=local,svg=svgs)
    dest=ROOT/'.review/link-checks.json';dest.write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(dict(external=external,missing=[x for x in local if not x['exists']],svg_count=len(svgs),svg_issues=[x for x in svgs if x['unsafe_or_font_dependent']]),indent=2))
