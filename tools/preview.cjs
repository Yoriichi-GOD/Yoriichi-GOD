/* Local-only GFM review harness. No product application or remote writes. */
const fs=require('node:fs');
const path=require('node:path');
const crypto=require('node:crypto');
const {createRequire}=require('node:module');
const {pathToFileURL}=require('node:url');
const requireFromBundle=createRequire(process.env.ARCHIVE_NODE_MODULES+'/package.json');
const {chromium}=requireFromBundle('playwright');
const sharp=requireFromBundle('sharp');
const ROOT=path.resolve(__dirname,'..');
const review=path.join(ROOT,'.review');

async function main(){
  const {marked}=await import(pathToFileURL(path.join(process.env.ARCHIVE_NODE_MODULES,'marked/lib/marked.esm.js')).href);
  const md=fs.readFileSync(path.join(ROOT,'README.md'),'utf8');
  const headings=[];
  const renderer=new marked.Renderer();
  renderer.heading=function({tokens,depth,text}){
    const name=text.toLowerCase().replace(/&amp;/g,'').replace(/[^\w\s-]/g,'').trim().replace(/\s/g,'-');
    headings.push(name);return `<h${depth} id="${name}">${this.parser.parseInline(tokens)}</h${depth}>`;
  };
  marked.use({gfm:true,renderer});
  let body=marked.parse(md);
  let rendering='marked GFM';
  const metaPath=path.join(review,'github-markup-meta.json');
  if(fs.existsSync(metaPath)){
    const meta=JSON.parse(fs.readFileSync(metaPath));
    if(meta.readme_sha256!==crypto.createHash('sha256').update(Buffer.from(md)).digest('hex'))throw Error('Stale GitHub Markdown render; run check_github_markup.py again.');
    body=fs.readFileSync(path.join(review,'github-rendered.html'),'utf8');
    body=body.replace(/<h([1-6])>(.*?)<\/h\1>/g,(all,depth,label)=>`<h${depth} id="${label.toLowerCase().replace(/&amp;/g,'').replace(/[^\w\s-]/g,'').trim().replace(/\s/g,'-')}">${label}</h${depth}>`);
    rendering='GitHub Markdown API HTML; local heading IDs';
  }
  const css=fs.readFileSync(path.join(review,'github-markdown.css'),'utf8');
  const make=(theme)=>`<!doctype html><html lang="en" data-color-mode="${theme}" data-${theme}-theme="${theme}"><head><meta charset="utf-8"><base href="${pathToFileURL(ROOT+path.sep).href}"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Engineering Archive — local GitHub-style preview</title><style>${css}
  *{box-sizing:border-box}body{margin:0;padding:32px 24px;background:${theme==='dark'?'#0d1117':'#fff'};color:${theme==='dark'?'#f0f6fc':'#1f2328'}}.preview-note{max-width:896px;margin:0 auto 12px;font:12px system-ui;color:${theme==='dark'?'#9198a1':'#59636e'}}article.markdown-body{max-width:896px;margin:auto;padding:24px;border:1px solid ${theme==='dark'?'#3d444d':'#d1d9e0'};border-radius:6px}article.markdown-body img{max-width:100%;height:auto}article.markdown-body img[height]{height:24px;width:24px;vertical-align:middle}article.markdown-body picture{display:block}article.markdown-body table{display:block;max-width:100%;overflow:auto} @media(max-width:600px){body{padding:16px 12px}article.markdown-body{padding:16px}.preview-note{font-size:11px}}
  </style></head><body><div class="preview-note">LOCAL GFM PREVIEW · ${theme.toUpperCase()} · GitHub Markdown CSS · not the live GitHub page</div><article class="markdown-body">${body}</article></body></html>`;
  for(const theme of ['dark','light'])fs.writeFileSync(path.join(review,`preview-${theme}.html`),make(theme));
  const browser=await chromium.launch({executablePath:process.env.ARCHIVE_CHROME,headless:true});
  const report=[];
  try{
    for(const width of [1440,1024,390])for(const theme of ['dark','light']){
      const page=await browser.newPage({viewport:{width,height:1000},deviceScaleFactor:1,colorScheme:theme});
      const errors=[];page.on('pageerror',e=>errors.push(e.message));
      await page.goto(pathToFileURL(path.join(review,`preview-${theme}.html`)).href,{waitUntil:'networkidle'});
      await page.evaluate(()=>Promise.all(Array.from(document.images).map(i=>i.decode().catch(()=>{}))));
      const check=await page.evaluate(()=>({
        documentWidth:document.documentElement.scrollWidth,viewport:innerWidth,
        articleWidth:document.querySelector('article').getBoundingClientRect().width,
        bodyHeight:document.documentElement.scrollHeight,
        images:[...document.images].map(i=>({src:i.getAttribute('src'),current:i.currentSrc.split('/assets/')[1],loaded:i.complete&&i.naturalWidth>0,width:i.getBoundingClientRect().width,height:i.getBoundingClientRect().height,alt:i.alt})),
        overflow:[...document.querySelectorAll('article img,article p,article picture')].filter(i=>i.getBoundingClientRect().right>innerWidth+1).map(i=>i.tagName),
        missingAnchors:[...document.querySelectorAll('a[href^="#"]')].filter(a=>!document.getElementById(decodeURIComponent(a.hash.slice(1)))).map(a=>a.hash),
        selectedText:document.querySelector('article').innerText.slice(0,900)
      }));
      const file=`profile-${width}-${theme}.png`;
      await page.screenshot({path:path.join(review,file),fullPage:true});
      await page.screenshot({path:path.join(review,`top-${width}-${theme}.png`),fullPage:false});
      if(width===390||width===1440){
        const items=page.locator('article picture');
        for(let i=0;i<await items.count();i++)await items.nth(i).screenshot({path:path.join(review,`plate-${width}-${i}.png`)});
      }
      await page.locator('#verified-engineering-evidence').scrollIntoViewIfNeeded();
      await page.screenshot({path:path.join(review,`evidence-${width}-${theme}.png`),fullPage:false});
      report.push({width,theme,...check,errors,screenshot:file});await page.close();
    }
    const glyphBounds=[];
    function walk(dir){return fs.readdirSync(dir,{withFileTypes:true}).flatMap(f=>f.isDirectory()?walk(path.join(dir,f.name)):[path.join(dir,f.name)]);}
    for(const file of walk(path.join(ROOT,'assets')).filter(f=>f.endsWith('.svg'))){
      const page=await browser.newPage();await page.goto(pathToFileURL(file).href);
      const issues=await page.evaluate(()=>{
        const root=document.querySelector('svg'),v=root.viewBox.baseVal;
        return [...root.querySelectorAll('path[aria-label]')].map(p=>({label:p.getAttribute('aria-label'),box:p.getBBox()})).filter(p=>p.box.x<0||p.box.y<0||p.box.x+p.box.width>v.width+1||p.box.y+p.box.height>v.height+1).map(p=>p.label);
      });
      glyphBounds.push({file:path.relative(ROOT,file),outOfBounds:issues});await page.close();
    }
    fs.writeFileSync(path.join(review,'glyph-bounds.json'),JSON.stringify(glyphBounds,null,2));
    const hero=path.join(ROOT,'assets/hero.svg');
    await sharp(hero).png({compressionLevel:9,palette:true,quality:100}).toFile(path.join(ROOT,'assets/hero-fallback.png'));
  }finally{await browser.close();}
  fs.writeFileSync(path.join(review,'render-checks.json'),JSON.stringify({renderer:rendering+' + github-markdown-css; local browser, not live GitHub profile',date:'2026-10-27',report},null,2));
  console.log(JSON.stringify(report.map(r=>({width:r.width,theme:r.theme,articleWidth:r.articleWidth,height:r.bodyHeight,overflow:r.documentWidth>r.viewport||r.overflow.length>0,broken:r.images.filter(i=>!i.loaded).length,missingAnchors:r.missingAnchors,errors:r.errors})),null,2));
}
main().catch(e=>{console.error(e);process.exitCode=1});
