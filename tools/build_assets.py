"""Author the archive's static SVG plates. No font binaries are distributed.

Requires Pillow and fonttools[woff]. Supply OFL-licensed Cormorant Garamond,
Manrope and IBM Plex Mono files with --font-dir; public screen originals with
--sources. Source strings, coordinates and motifs remain editable here.
"""
import argparse, base64, io, math, random
from pathlib import Path
from xml.sax.saxutils import escape
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen

ROOT = Path(__file__).resolve().parents[1]
P = dict(bg='#0C0E13', ink='#121825', ivory='#F1E8D7', gold='#C9A56C', copper='#8C613F', slate='#8692A5', rule='#343944')
FONTS = {}
SOURCES = None

def rect(x,y,w,h,fill,stroke=None,sw=1):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"'+(f' stroke="{stroke}" stroke-width="{sw}"' if stroke else '')+'/>'

def line(x1,y1,x2,y2,color=None,sw=1,opacity=1):
    return f'<path d="M{x1} {y1}H{x2}" stroke="{color or P["gold"]}" stroke-width="{sw}" opacity="{opacity}"/>' if y1==y2 else f'<path d="M{x1} {y1}L{x2} {y2}" fill="none" stroke="{color or P["gold"]}" stroke-width="{sw}" opacity="{opacity}"/>'

def circle(x,y,r,color=None,sw=1,fill='none',opacity=1):
    return f'<circle cx="{x}" cy="{y}" r="{r}" stroke="{color or P["gold"]}" stroke-width="{sw}" fill="{fill}" opacity="{opacity}"/>'

def width(text,size,font='sans',tracking=0):
    f=FONTS[font]; cm=f.getBestCmap(); u=f['head'].unitsPerEm
    return sum(f['hmtx'].metrics.get(cm.get(ord(c),'.notdef'),(u/2,0))[0]*size/u for c in text)+max(0,len(text)-1)*tracking

def text(s,x,y,size=24,font='sans',color=None,tracking=0,opacity=1):
    f=FONTS[font]; gs=f.getGlyphSet(); cm=f.getBestCmap(); sc=size/f['head'].unitsPerEm
    pen=SVGPathPen(gs, ntos=lambda v: f'{v:.2f}'.rstrip('0').rstrip('.')); px=x
    for char in s:
        name=cm.get(ord(char),'.notdef')
        assert name != '.notdef', f'Missing glyph {char!r} in {font}'
        gs[name].draw(TransformPen(pen,(sc,0,0,-sc,px,y)))
        px+=f['hmtx'].metrics[name][0]*sc+tracking
    return f'<path aria-label="{escape(s)}" d="{pen.getCommands()}" fill="{color or P["ivory"]}" opacity="{opacity}"/>'

def lines_text(rows,x,y,size,font='serif',color=None,leading=None):
    return ''.join(text(s,x,y+i*(leading or size*1.05),size,font,color) for i,s in enumerate(rows))

def svg(w,h,title,body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-labelledby="title desc"><title id="title">{escape(title)}</title><desc id="desc">Original Engineering Archive composition. Static outlined typography, explicit charcoal background. Authorized UI specimens and any crops are identified in the content provenance; ornamental diagrams are schematic.</desc>{rect(0,0,w,h,P["bg"])}{body}</svg>'

def write(path,w,h,title,body):
    dest=ROOT/'assets'/path; dest.parent.mkdir(parents=True,exist_ok=True)
    dest.write_text(svg(w,h,title,body),encoding='utf-8')

def frame(w,h,pad=24):
    s=rect(pad,pad,w-pad*2,h-pad*2,'none',P['rule'])
    for x,y,sx,sy in [(pad,pad,1,1),(w-pad,pad,-1,1),(pad,h-pad,1,-1),(w-pad,h-pad,-1,-1)]:
        s+=f'<path d="M{x} {y+18*sy}V{y}H{x+18*sx}" fill="none" stroke="{P["gold"]}" stroke-width="2"/>'
    return s

def instrument(cx,cy,r,opacity=1):
    s=f'<g opacity="{opacity}">'
    # Graduated limbus, broken rings, inclined armillary orbits and meridians.
    for rr in [r,r*.945,r*.72]:s+=circle(cx,cy,rr,sw=1.2,opacity=.65)
    for i in range(120):
        a=i*math.tau/120; rr=r*(.905 if i%10==0 else .926)
        s+=line(round(cx+rr*math.sin(a),2),round(cy-rr*math.cos(a),2),round(cx+r*.945*math.sin(a),2),round(cy-r*.945*math.cos(a),2),sw=1.6 if i%10==0 else .7,opacity=.8)
    for scale in [.23,.48,.75]:
        s+=f'<ellipse cx="{cx}" cy="{cy}" rx="{r*.72*scale}" ry="{r*.72}" fill="none" stroke="{P["slate"]}" stroke-width="1" opacity=".45"/>'
        s+=f'<ellipse cx="{cx}" cy="{cy}" rx="{r*.72}" ry="{r*.72*scale}" fill="none" stroke="{P["slate"]}" stroke-width="1" opacity=".45"/>'
    for angle in [-33,38]:
        s+=f'<ellipse cx="{cx}" cy="{cy}" rx="{r*1.18}" ry="{r*.35}" transform="rotate({angle} {cx} {cy})" fill="none" stroke="{P["gold"]}" stroke-width="1.7" opacity=".85"/>'
    s+=line(cx-r*1.28,cy,cx+r*1.28,cy,P['slate'],.8,.5)+line(cx,cy-r*1.25,cx,cy+r*1.25,P['slate'],.8,.5)
    s+=circle(cx,cy,6,fill=P['ivory'])+circle(cx+r*.73,cy-r*.34,5,fill=P['gold'])
    s+=f'<path d="M{cx-r*.58} {cy+r*.58}L{cx+r*.58} {cy-r*.58}" stroke="{P["copper"]}" stroke-width="3"/>'
    return s+'</g>'

def contours(x,y,w,h,seed=14):
    rng=random.Random(seed);s='<g fill="none" stroke="#253044" stroke-width="1" opacity=".5">'
    for k in range(17):
        pts=[]
        for i in range(45):
            xx=x+i*w/44
            yy=y+k*h/18+math.sin(i*.16+k*.25)*22+math.sin(i*.4+k*.28)*8
            pts.append(f'{xx:.1f},{yy:.1f}')
        s+=f'<polyline points="{" ".join(pts)}"/>'
    return s+'</g>'

def hero(mobile=False):
    w,h=(800,940) if mobile else (1600,500)
    if mobile:
        s=contours(290,300,490,470)+instrument(575,650,173,.72)+frame(w,h)
        s+=text('THE ENGINEERING',54,80,24,'mono',P['gold'],2)+text('ARCHIVE',54,116,24,'mono',P['gold'],2)
        s+=line(54,153,746,153,P['rule'])
        s+=text('SAISHREEK',50,276,103,'serif')+text('SINGH',50,382,103,'serif')
        s+=text('YORIICHI-GOD',56,439,30,'mono',P['gold'],3)
        s+=line(56,475,190,475,P['gold'],2)
        s+=lines_text(['Founder. Engineer.','Builder of difficult things.'],56,529,30,'sans',leading=45)
        s+=text('INTELLIGENCE / VISION / SYSTEMS',54,871,22,'mono',P['slate'])
        s+=text('PERSONAL RECORD  /  VOL. 01',54,906,19,'mono',P['gold'])
    else:
        s=contours(950,35,620,425)+instrument(1272,253,175,.87)+frame(w,h)
        s+=text('THE ENGINEERING ARCHIVE',65,77,21,'mono',P['gold'],3)
        s+=text('PERSONAL RECORD / VOL. 01',1150,64,13,'mono',P['slate'],1)
        s+=text('SAISHREEK',60,238,142,'serif')+text('SINGH',60,371,142,'serif')
        s+=line(526,341,584,341,P['gold'],1.7)
        s+=text('YORIICHI-GOD',611,350,26,'mono',P['gold'],2)
        s+=line(65,407,944,407,P['rule'])
        s+=text('Founder. Engineer. Builder of difficult things.',65,449,27,'sans')
        s+=text('INTELLIGENCE / VISION / SYSTEMS',1120,449,14,'mono',P['slate'],1)
    write('hero-mobile.svg' if mobile else 'hero.svg',w,h,'Saishreek Singh / Yoriichi-GOD — The Engineering Archive. Founder. Engineer. Builder of difficult things.',s)

def image_data(name,crop=None,maxsize=(900,600)):
    source=ROOT/name[6:] if name.startswith('asset:') else SOURCES/name
    if name.startswith('asset:') and source.suffix.lower()=='.webp' and crop is None:
        with Image.open(source) as im:size=im.size
        return base64.b64encode(source.read_bytes()).decode(),size
    im=Image.open(source).convert('RGB')
    if crop:im=im.crop(crop)
    im.thumbnail(maxsize,Image.Resampling.LANCZOS)
    out=io.BytesIO();im.save(out,format='WEBP',quality=86,method=6)
    return base64.b64encode(out.getvalue()).decode(),im.size

def screen(name,x,y,w,h,crop=None,fill=False):
    data,sz=image_data(name,crop,(round(w*1.3),round(h*1.3)))
    mode='slice' if fill else 'meet'
    return rect(x-1,y-1,w+2,h+2,'none','#4F4B45')+f'<svg x="{x}" y="{y}" width="{w}" height="{h}" overflow="hidden"><image width="{w}" height="{h}" preserveAspectRatio="xMidYMid {mode}" href="data:image/webp;base64,{data}"/></svg>'

def doc_diagram(x,y,w,h):
    s=contours(x,y,w,h)
    for i in range(3):
        xx=x+35+i*32;yy=y+25-i*8
        s+=rect(xx,yy,w*.44,h*.70,P['ink'],P['copper'])
    dx=x+99;dy=y+9
    for j in range(7): s+=line(dx+24,dy+40+j*23,dx+w*.33,dy+40+j*23,P['slate'],1,.8)
    s+=rect(dx+18,dy+90,w*.31,29,'#453728',P['gold'])
    s+=line(dx+w*.35,dy+105,x+w*.8,y+h*.4,P['gold'],2)
    s+=circle(x+w*.82,y+h*.4,38,sw=2,fill=P['bg'])
    s+=f'<path d="m{x+w*.82-14} {y+h*.4} 10 10 19-23" stroke="{P["gold"]}" stroke-width="2" fill="none"/>'
    s+=text('SOURCE',dx+20,y+h*.89,19,'mono',P['gold'],2)
    s+=text('REVIEW',x+w*.67,y+h*.89,19,'mono',P['gold'],2)
    return s

def lineage(x,y,w,h):
    s='';coords=[(.12,.62),(.34,.25),(.53,.63),(.78,.30),(.91,.70)]
    for a,b in [(0,1),(1,2),(2,3),(2,4)]:
        ax,ay=coords[a];bx,by=coords[b]
        s+=line(x+ax*w,y+ay*h,x+bx*w,y+by*h,'#81758F',2)
    for i,(xx,yy) in enumerate(coords):
        s+=circle(x+xx*w,y+yy*h,24 if i==2 else 15,'#A098AF',1.5,fill=P['bg'])
        s+=circle(x+xx*w,y+yy*h,4,P['gold'],fill=P['gold'])
    return s

PROJECTS=[
 dict(slug='satquery',num='01',title=['SATQUERY AI'],category='EARTH OBSERVATION',line=['Ask about Earth.','Inspect the answer.'],accent='#748AAE',file='satquery.png',crop=None,caption='PREDICTED WATER / ACTUAL OUTPUT',status='LOCAL RESEARCH PROTOTYPE',full_ui=True),
 dict(slug='warscythe',num='02',title=['WARSCYTHE'],category='PRODUCT ENGINEERING',line=['Make execution','a world worth entering.'],accent='#A27E64',file='asset:assets/projects/warscythe-ui.webp',crop=None,caption='USER-SELECTED UI / COMPLETE VIEWPORT',status='PERSISTENT PROGRESSION',full_ui=True),
 dict(slug='regulens',num='03',title=['REGULENS'],category='DOCUMENT INTELLIGENCE',line=['A finding should','lead back to its source.'],accent='#C9A56C',file='asset:assets/projects/regulens-ui.webp',crop=None,caption='ACTUAL UI / SYNTHETIC DEMONSTRATION',status='PRIVATE / SIH26261 PROTOTYPE',full_ui=True),
 dict(slug='reflex',num='04',title=['REFLEX'],category='COMPUTER VISION',line=['Find the unusual.','Keep the evidence.'],accent='#CB8A61',file='asset:assets/projects/reflex-ui.webp',crop=None,caption='USER-SELECTED UI / COMPLETE VIEWPORT',status='HOSTED V1 / V2 HELD LOCAL',full_ui=True),
 dict(slug='ghosttrace',num='05',title=['GHOSTTRACE'],category='PRIVACY ENGINEERING',line=['Follow what','deletion left behind.'],accent='#9D91AB',file='ghosttrace.png',crop=None,caption='ACTUAL UI / AUTHORED SYNTHETIC CASE',status='READ-ONLY INVESTIGATION',full_ui=True),
 dict(slug='flood-lab',num='06',title=['SATQUERY','FLOOD LAB'],category='GEOSPATIAL EVIDENCE',line=['Observe the change.','Interrogate the impact.'],accent='#7EA09C',file='asset:assets/projects/flood-lab-ui.webp',crop=None,caption='OPTICAL PREVIEW / ACTUAL WORKSPACE',status='LOCAL RESEARCH PROTOTYPE',full_ui=True),
]

def full_ui_plate(p,mobile=False):
    """Preserve the complete viewport in a large, proportional image frame."""
    source=ROOT/p['file'][6:] if p['file'].startswith('asset:') else SOURCES/p['file']
    im=Image.open(source)
    w=800 if mobile else 1600
    ix=44 if mobile else 64
    iw=w-2*ix
    ih=round(iw*im.height/im.width)
    if mobile:
        by=296 if len(p['title'])>1 else 224
        iy=by+84
    else:iy=210
    h=iy+ih+(85 if mobile else 90)
    s=frame(w,h,16)+rect(16,16,5,h-32,p['accent'])
    s+=text(f'{p["num"]} / {p["category"]}',ix,66 if mobile else 65,21 if mobile else 18,'mono',p['accent'],1)
    if mobile:
        s+=lines_text(p['title'],40,162,65 if len(p['title'])>1 else 76,leading=68)
        s+=lines_text(p['line'],44,by,27,'sans',leading=38)
    else:
        s+=text(' '.join(p['title']),61,158,78 if len(p['title'])>1 else 82,'serif')
        s+=lines_text(p['line'],1000,114,26,'sans',leading=38)
        s+=line(64,185,1536,185,P['rule'])
    s+=screen(p['file'],ix,iy,iw,ih,crop=None,fill=False)
    if mobile:s+=text(p['status'],44,h-38,18,'mono',P['slate'],.2)
    else:
        s+=text(p['status'],64,h-36,16,'mono',P['slate'],.7)
        label_width=width(p['caption'],13,'mono',.7)
        s+=text(p['caption'],1536-label_width,h-36,13,'mono',P['slate'],.7)
    write(f'projects/{p["slug"]}{"-mobile" if mobile else ""}.svg',w,h,' / '.join(p['title'])+' — complete captured UI viewport',s)

def desktop_plate(p):
    """Alternate equal image/text halves; fit the row to the screenshot ratio."""
    source=ROOT/p['file'][6:] if p['file'].startswith('asset:') else SOURCES/p['file']
    with Image.open(source) as im:source_width,source_height=im.size
    w=1600
    image_width=784
    image_height=round(image_width*source_height/source_width,3)
    h=round(image_height+32,3)
    image_on_left=int(p['num'])%2==0
    ix=16 if image_on_left else 800
    tx=864 if image_on_left else 64
    s=screen(p['file'],ix,16,image_width,image_height,crop=None,fill=False)
    s+=frame(w,h,16)+line(800,16,800,h-16,P['rule'])
    s+=rect(1579 if image_on_left else 16,16,5,h-32,p['accent'])
    s+=text(f'{p["num"]} / {p["category"]}',tx,65,18,'mono',p['accent'],1.7)
    title_count=len(p['title'])
    first_baseline=round(16+(image_height-((title_count-1)*73+145))/2+55,2)
    size=75 if p['slug']=='ghosttrace' else 82
    s+=lines_text(p['title'],tx-3,first_baseline,size,leading=73)
    tagline_baseline=first_baseline+(title_count-1)*73+50
    s+=lines_text(p['line'],tx,tagline_baseline,28,'sans',leading=40)
    s+=line(tx,h-88,tx+656,h-88,P['rule'])
    s+=text(p['status'],tx,h-55,16,'mono',P['slate'],.7)
    s+=text(p['caption'],tx,h-30,13,'mono',P['slate'],.5)
    write(f'projects/{p["slug"]}.svg',w,h,' / '.join(p['title'])+' — alternating equal-width text and complete UI panels',s)

def plate(p,mobile=False):
    if not mobile:
        desktop_plate(p)
        return
    if p.get('full_ui'):
        full_ui_plate(p,mobile)
        return
    w,h=(800,690 if len(p['title'])>1 else 600) if mobile else (1600,450)
    swap=p['slug'] in ['warscythe','reflex','flood-lab'] and not mobile
    s=frame(w,h,16)
    s+=rect(16,16,5,h-32,p['accent'])
    if mobile:
        s+=text(f'{p["num"]} / {p["category"]}',44,66,21,'mono',p['accent'],1)
        size=76 if len(p['title'])==1 else 65
        s+=lines_text(p['title'],40,162,size,leading=68)
        by=224 if len(p['title'])==1 else 296
        s+=lines_text(p['line'],44,by,27,'sans',leading=38)
        ix,iy,iw,ih=44,by+70,712,220
        if p['file'] and p['slug']!='ghosttrace':
            crop=(940,220,1300,355) if p['slug']=='warscythe' else p['crop']
            s+=screen(p['file'],ix,iy,iw,ih,crop,fill=True)
        elif p['slug']=='regulens':s+=doc_diagram(ix,iy,iw,ih)
        else:s+=lineage(ix,iy,iw,ih)
        s+=text(p['status'],44,h-45,19,'mono',P['slate'],.5)
    else:
        tx=885 if swap else 66
        ix=66 if swap else 868
        s+=text(f'{p["num"]} / {p["category"]}',tx,71,18,'mono',p['accent'],1.7)
        size=82 if p['slug']!='ghosttrace' else 75
        s+=lines_text(p['title'],tx-3,182,size,leading=73)
        by=238 if len(p['title'])==1 else 303
        s+=lines_text(p['line'],tx,by,28,'sans',leading=40)
        s+=text(p['status'],tx,403,16,'mono',P['slate'],1)
        s+=line(tx,353 if len(p['title'])==1 else 366,tx+555,353 if len(p['title'])==1 else 366,P['rule'])
        if p['file']:
            # Desktop specimens preserve public UI composition. Mobile crops isolate visual output.
            crop=p['crop'] if p['slug'] in ['reflex','flood-lab'] else None
            s+=screen(p['file'],ix,61,666,304,crop)
        else:s+=doc_diagram(ix,61,666,304)
        s+=text(p['caption'],ix,403,13,'mono',P['slate'],.9)
    write(f'projects/{p["slug"]}{"-mobile" if mobile else ""}.svg',w,h,' / '.join(p['title'])+' — '+' '.join(p['line']),s)

ICONS={
'intelligent-systems':'M14 18 28 8 42 18V36L28 46 14 36ZM14 18 28 28 42 18M28 28V46M5 28H14M42 28H51M28 1V8M28 46V53',
'computer-vision':'M5 18V7H18M38 7H51V20M51 36V49H38M18 49H5V36M12 28Q28 9 44 28Q28 47 12 28ZM33 28A5 5 0 1 0 23 28A5 5 0 1 0 33 28',
'geospatial-intelligence':'M9 39Q20 5 45 15M8 33Q23 3 47 22M10 45Q31 7 46 29M17 49Q31 19 47 36M28 49Q37 34 47 43M5 5H16M5 5V16M51 51H40M51 51V40',
'product-engineering':'M5 6H51V42H5ZM5 15H51M19 50H37M28 42V50M20 23 14 28 20 33M36 23 42 28 36 33',
'verification-evaluation':'M14 5H42V51H14ZM20 16 24 20 33 11M20 31H36M20 38H36M20 45H30M7 12H14M42 43H49'
}

def identities():
    for slug,path in ICONS.items():
        write(f'identity/{slug}.svg',64,64,slug.replace('-',' ').title(),f'<path d="{path}" transform="translate(4 4)" stroke="{P["gold"]}" stroke-width="1.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
    for mobile in [False,True]:
        w,h=(800,560) if mobile else (1600,330)
        s=frame(w,h,16)
        s+=text('WORKING PRINCIPLE / NOT A FINISHING TOUCH',45,65,17 if not mobile else 19,'mono',P['gold'],1.1)
        size=65 if mobile else 70
        y=164 if mobile else 159
        if mobile:s+=lines_text(['Build the system.','Test the claim.','Preserve the evidence.'],42,y,size,leading=86)
        else:
            for i,t in enumerate(['Build the system.','Test the claim.','Preserve the evidence.']):
                xx=46+[0,475,935][i]
                s+=text(t,xx,y,52 if i==2 else 57,'serif')
                s+=line(xx,207,xx+(410 if i<2 else 585),207,P['rule'])
                s+=text(['01 / MAKE IT WORK','02 / MEASURE IT','03 / KEEP THE RECORD'][i],xx,255,17,'mono',P['slate'],.9)
        if mobile:
            s+=line(46,445,754,445,P['rule'])
            s+=text('TRACEABILITY IS PART OF THE PRODUCT.',46,493,21,'mono',P['slate'])
        write('identity/method'+('-mobile' if mobile else '')+'.svg',w,h,'Build the system. Test the claim. Preserve the evidence. A proposed working principle.',s)
    s=line(0,24,1600,24,P['rule'])+rect(0,21,110,6,P['gold'])+text('THE RECORD CONTINUES',1180,14,14,'mono',P['slate'],1)
    write('dividers/archive-rule.svg',1600,34,'The record continues',s)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--font-dir',type=Path,required=True);ap.add_argument('--sources',type=Path,required=True)
    args=ap.parse_args();SOURCES=args.sources
    for key,name in [('serif','cormorant-garamond-latin-600-normal.woff2'),('sans','manrope-latin-400-normal.woff2'),('mono','ibm-plex-mono-latin-400-normal.woff2')]:
        FONTS[key]=TTFont(args.font_dir/name)
    hero();hero(True)
    for p in PROJECTS:plate(p);plate(p,True)
    identities()
    print('Authored 22 self-contained SVG assets. All display glyphs are outlines.')
